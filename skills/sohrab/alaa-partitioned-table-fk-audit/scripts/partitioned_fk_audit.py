#!/usr/bin/env python3
"""Audit source trees for foreign keys that reference a partitioned parent through an incomplete key.

PostgreSQL requires a foreign key's referenced column list to match a full unique or primary
key on the referenced table. A partitioned parent's key must contain every partition-key
column, so it is composite, so an `id`-only reference into it fails with SQLSTATE 42830
("there is no unique constraint matching given keys for referenced table"). This script finds
those references from source text alone; it never opens a database connection.

Usage
  partitioned_fk_audit.py ROOT [ROOT ...] [options]
  partitioned_fk_audit.py --self-test
  partitioned_fk_audit.py --install DEST

ROOT is any directory or file to scan. Pass every tree that can hold schema source:
migrations, raw .sql, schema dumps, docs that show DDL, and vendor-published migrations.
No path is built into this script; a root you do not pass is not audited.

Options
  --ext .sql,.php,.go,.md   file extensions to read (default: .sql,.php,.go,.md,.py,.rb,.ts)
  --exclude NAME            directory name to skip, repeatable
                            (default: .git, node_modules, __pycache__, .idea, dist, build)
  --require-parents         exit 4 when no partitioned parent is discovered
  --json                    emit the full finding set as JSON on stdout
  --quiet                   print only the RESULT line and any finding lines
  --self-test               run the built-in fixture suite and exit
  --install DEST            copy this script to DEST unchanged, then exit

Exit codes, and what a non-zero code obliges the calling agent to do
  0  No incomplete-key reference into a partitioned parent was found. Read the RESULT line
     anyway: "parents=0" means the guard is in place and nothing was proven about a schema
     that does not exist yet.
  1  Usage error: a root does not exist, or no root was given. Fix the invocation and rerun;
     never report an audit result from a run that exited 1.
  2  A partitioned-table key defect was found, in one of two kinds. `incomplete-key-reference`
     means a foreign key supplies fewer columns than the parent's key holds: fix the
     referencing side so its column list equals one of the parent's full keys, under the lock
     obligation in this skill's references/20-lock-safety-and-the-fix.md, and never drop the
     constraint to silence the finding. `parent-key-omits-partition-column` means the parent's
     own declared PRIMARY KEY or UNIQUE omits a partition-key column, which PostgreSQL refuses
     outright, so that migration cannot run at all: fix the parent's key before auditing any
     reference into it.
  3  A partitioned parent was discovered whose key shape could not be read from the roots
     given. Widen the roots to include the file that declares that parent's PRIMARY KEY or
     UNIQUE constraint and rerun; report the audit as inconclusive until it exits 0 or 2.
  4  --require-parents was given and no partitioned parent was discovered. Confirm the roots
     cover this repository's schema sources before concluding the repository has none.
  5  --self-test failed, so this script's own logic is untrusted. Do not use its findings;
     repair the script or report it as broken.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_INCOMPLETE_KEY = 2
EXIT_UNKNOWN_KEY = 3
EXIT_NO_PARENTS = 4
EXIT_SELFTEST = 5

DEFAULT_EXTS = (".sql", ".php", ".go", ".md", ".py", ".rb", ".ts")
DEFAULT_EXCLUDES = (".git", "node_modules", "__pycache__", ".idea", "dist", "build")

IDENT = r'(?:"[^"]+"|[A-Za-z_][A-Za-z0-9_$]*)'
QNAME = rf"(?:{IDENT}\.)*{IDENT}"


# --------------------------------------------------------------------------- text handling

def strip_comments(text: str) -> str:
    """Blank out SQL/PHP/Go comments, preserving every byte offset so line numbers stay true."""
    out = list(text)
    i, n = 0, len(text)
    while i < n:
        two = text[i:i + 2]
        if two == "/*":
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
        elif two == "--" or two == "//":
            j = text.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = " "
            i = j
        else:
            i += 1
    return "".join(out)


def match_paren(text: str, open_idx: int) -> int:
    """Index just past the parenthesis matching the one at open_idx, or len(text) if unbalanced."""
    depth, i, n = 0, open_idx, len(text)
    while i < n:
        c = text[i]
        if c in "'\"":
            quote, i = c, i + 1
            while i < n:
                if text[i] == quote:
                    if i + 1 < n and text[i + 1] == quote:
                        i += 2
                        continue
                    break
                i += 1
            i += 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


WINDOW_OPENERS = re.compile(r"\bOVER\s*\(|\bWINDOW\s+" + IDENT + r"\s+AS\s*\(", re.IGNORECASE)


def mask_window_functions(text: str) -> str:
    """Blank the body of every OVER (...) and WINDOW x AS (...) clause, offsets preserved.

    `PARTITION BY` inside a window clause is query grammar, never a partitioned table, so a
    detector that does not mask these reports the whole reporting layer as schema DDL.
    """
    out = list(text)
    for m in WINDOW_OPENERS.finditer(text):
        open_idx = text.index("(", m.start())
        end = match_paren(text, open_idx)
        for k in range(open_idx, end):
            if out[k] != "\n":
                out[k] = " "
    return "".join(out)


def split_top_level(body: str) -> list[str]:
    parts, depth, cur = [], 0, []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur))
    return parts


def norm_name(raw: str) -> str:
    """Bare, lower-cased table name: schema prefix and quoting removed."""
    last = raw.strip().split(".")[-1].strip()
    return last.strip('"').lower()


NOISE = re.compile(r"\b(asc|desc|nulls\s+first|nulls\s+last)\b", re.IGNORECASE)


def norm_cols(raw: str) -> tuple[str, ...]:
    cols = []
    for part in split_top_level(raw):
        c = NOISE.sub("", part).strip()
        c = c.split("(")[0].strip()
        c = c.strip('"').strip("'").strip()
        c = c.split()[0] if c.split() else ""
        if c:
            cols.append(c.lower())
    return tuple(cols)


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


# --------------------------------------------------------------------------- parent discovery

CREATE_TABLE = re.compile(
    rf"\bCREATE\s+(?:(?:GLOBAL|LOCAL)\s+)?(?:(?:TEMP|TEMPORARY|UNLOGGED)\s+)?TABLE\s+"
    rf"(?:IF\s+NOT\s+EXISTS\s+)?({QNAME})\s*\(",
    re.IGNORECASE,
)
PARTITION_BY = re.compile(r"\bPARTITION\s+BY\s+(\w+)\s*\(([^)]*)\)", re.IGNORECASE)
INHERITS = re.compile(r"\bINHERITS\s*\(([^)]*)\)", re.IGNORECASE)
ATTACH_PARTITION = re.compile(
    rf"\bALTER\s+TABLE\s+(?:ONLY\s+)?({QNAME})\s+ATTACH\s+PARTITION\b", re.IGNORECASE)
PARTITION_OF = re.compile(
    rf"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?{QNAME}\s+PARTITION\s+OF\s+({QNAME})",
    re.IGNORECASE)
ALTER_PARTITION_BY = re.compile(
    rf"\bALTER\s+TABLE\s+(?:ONLY\s+)?({QNAME})\s+PARTITION\s+BY\s+\w+\s*\(([^)]*)\)",
    re.IGNORECASE)


class Parent:
    def __init__(self, name: str):
        self.name = name
        self.evidence: list[str] = []          # "kind file:line"
        self.keys: list[tuple[str, ...]] = []  # candidate keys PostgreSQL would accept
        self.rejected_keys: list[tuple[str, ...]] = []  # declared keys Postgres would reject
        self.partition_cols: tuple[str, ...] | None = None  # None when unknown or an expression
        self.legacy_support: list[str] = []    # CHECK / trigger corroboration for INHERITS

    def add_evidence(self, kind: str, where: str) -> None:
        tag = f"{kind} {where}"
        if tag not in self.evidence:
            self.evidence.append(tag)

    def add_key(self, cols: tuple[str, ...]) -> None:
        if cols and cols not in self.keys:
            self.keys.append(cols)

    def apply_partition_rule(self) -> None:
        """Drop candidate keys that omit a partition-key column.

        PostgreSQL refuses such a constraint outright ("unique constraint on partitioned table
        must include all partitioning columns"), so treating one as a usable key would make a
        reference into it look satisfied when the parent's own DDL cannot even be created.
        """
        if not self.partition_cols:
            return
        keep, drop = [], []
        for k in self.keys:
            (keep if set(self.partition_cols).issubset(set(k)) else drop).append(k)
        self.keys, self.rejected_keys = keep, drop


IDENT_ONLY = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")


def discover_parents(docs: list[tuple[str, str]]) -> dict[str, Parent]:
    """docs is [(path, masked_text)]. Returns confirmed partitioned parents by bare name."""
    parents: dict[str, Parent] = {}
    inherits_children: dict[str, list[tuple[str, str, str]]] = {}  # parent -> (child, body, where)
    body_keys: dict[str, list[tuple[str, ...]]] = {}

    def get(name: str) -> Parent:
        return parents.setdefault(name, Parent(name))

    for path, text in docs:
        for m in CREATE_TABLE.finditer(text):
            name = norm_name(m.group(1))
            open_idx = m.end() - 1
            end = match_paren(text, open_idx)
            body = text[open_idx + 1:end - 1]
            tail = text[end:end + 400].split(";")[0]
            where = f"{path}:{line_of(text, m.start())}"
            for cols in table_keys_from_body(body):
                body_keys.setdefault(name, []).append(cols)
            pm = PARTITION_BY.search(tail)
            if pm:
                p = get(name)
                p.add_evidence("create-table-partition-by", where)
                cols = norm_cols(pm.group(2))
                if cols and all(IDENT_ONLY.match(c) for c in cols):
                    p.partition_cols = cols
            im = INHERITS.search(tail)
            if im:
                for raw in split_top_level(im.group(1)):
                    parent_name = norm_name(raw)
                    inherits_children.setdefault(parent_name, []).append((name, body, where))

        for m in PARTITION_OF.finditer(text):
            get(norm_name(m.group(1))).add_evidence(
                "create-table-partition-of", f"{path}:{line_of(text, m.start())}")
        for m in ATTACH_PARTITION.finditer(text):
            get(norm_name(m.group(1))).add_evidence(
                "alter-table-attach-partition", f"{path}:{line_of(text, m.start())}")
        for m in ALTER_PARTITION_BY.finditer(text):
            get(norm_name(m.group(1))).add_evidence(
                "alter-table-partition-by-INVALID-SYNTAX", f"{path}:{line_of(text, m.start())}")

    # Legacy inheritance partitioning: a parent with INHERITS children counts only when a
    # child carries a CHECK constraint or the tree routes inserts to it, because plain
    # inheritance without either is ordinary table inheritance, not partitioning.
    for parent_name, children in inherits_children.items():
        support = []
        for child, body, where in children:
            if re.search(r"\bCHECK\s*\(", body, re.IGNORECASE):
                support.append(f"check-on-{child} {where}")
        for path, text in docs:
            for m in re.finditer(
                    rf"\bCREATE\s+(?:OR\s+REPLACE\s+)?(?:TRIGGER|RULE)\b[^;]{{0,400}}?\b"
                    rf"(?:ON|TO)\s+(?:ONLY\s+)?{QNAME}", text, re.IGNORECASE):
                if re.search(rf"\b{re.escape(parent_name)}\b", m.group(0), re.IGNORECASE):
                    support.append(f"insert-routing {path}:{line_of(text, m.start())}")
        if support:
            p = get(parent_name)
            p.add_evidence("inherits-legacy-partitioning", support[0].split(" ", 1)[1])
            p.legacy_support = support

    for name, p in parents.items():
        for cols in body_keys.get(name, []):
            p.add_key(cols)
    return parents


PK_TABLE = re.compile(
    rf"(?:CONSTRAINT\s+{QNAME}\s+)?\bPRIMARY\s+KEY\s*\(([^)]*)\)", re.IGNORECASE)
UNIQUE_TABLE = re.compile(
    rf"(?:CONSTRAINT\s+{QNAME}\s+)?\bUNIQUE\s*(?:NULLS\s+(?:NOT\s+)?DISTINCT\s*)?\(([^)]*)\)",
    re.IGNORECASE)


def table_keys_from_body(body: str) -> list[tuple[str, ...]]:
    keys: list[tuple[str, ...]] = []
    for part in split_top_level(body):
        stripped = part.strip()
        if not stripped:
            continue
        head = stripped.split()[0].upper().strip('"')
        is_constraint = head in {"PRIMARY", "UNIQUE", "CONSTRAINT", "FOREIGN", "CHECK", "EXCLUDE"}
        if is_constraint:
            for rx in (PK_TABLE, UNIQUE_TABLE):
                for m in rx.finditer(stripped):
                    cols = norm_cols(m.group(1))
                    if cols and cols not in keys:
                        keys.append(cols)
        else:
            if re.search(r"\bPRIMARY\s+KEY\b", stripped, re.IGNORECASE) or re.search(
                    r"\bUNIQUE\b", stripped, re.IGNORECASE):
                col = (norm_name(stripped.split()[0]),)
                if col not in keys:
                    keys.append(col)
    return keys


ALTER_ADD_KEY = re.compile(
    rf"\bALTER\s+TABLE\s+(?:ONLY\s+)?({QNAME})\s+ADD\s+(?:CONSTRAINT\s+{QNAME}\s+)?"
    rf"(PRIMARY\s+KEY|UNIQUE)\s*\(([^)]*)\)", re.IGNORECASE)
CREATE_UNIQUE_INDEX = re.compile(
    rf"\bCREATE\s+UNIQUE\s+INDEX\s+(?:CONCURRENTLY\s+)?(?:IF\s+NOT\s+EXISTS\s+)?"
    rf"(?:{QNAME}\s+)?ON\s+(?:ONLY\s+)?({QNAME})\s*\(([^)]*)\)", re.IGNORECASE)
SCHEMA_CREATE = re.compile(
    r"Schema::(?:create|table)\s*\(\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
BP_PRIMARY = re.compile(r"->\s*primary\s*\(\s*(\[[^\]]*\]|['\"][^'\"]*['\"])", re.IGNORECASE)
BP_UNIQUE = re.compile(r"->\s*unique\s*\(\s*(\[[^\]]*\]|['\"][^'\"]*['\"])", re.IGNORECASE)
BP_ID = re.compile(r"->\s*(?:id|ulid|uuid)\s*\(\s*(?:['\"]([^'\"]+)['\"])?\s*\)", re.IGNORECASE)


def php_list(raw: str) -> tuple[str, ...]:
    return tuple(s.lower() for s in re.findall(r"['\"]([^'\"]+)['\"]", raw))


def enrich_keys(parents: dict[str, Parent], docs: list[tuple[str, str]]) -> None:
    """Add key shapes declared away from the CREATE TABLE that made the parent partitioned."""
    for path, text in docs:
        for m in ALTER_ADD_KEY.finditer(text):
            p = parents.get(norm_name(m.group(1)))
            if p:
                p.add_key(norm_cols(m.group(3)))
        for m in CREATE_UNIQUE_INDEX.finditer(text):
            p = parents.get(norm_name(m.group(1)))
            if p:
                p.add_key(norm_cols(m.group(2)))
        for m in SCHEMA_CREATE.finditer(text):
            p = parents.get(norm_name(m.group(1)))
            if not p:
                continue
            open_idx = text.find("{", m.end())
            if open_idx < 0:
                continue
            depth, i, n = 0, open_idx, len(text)
            while i < n:
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            block = text[open_idx:i]
            for rx in (BP_PRIMARY, BP_UNIQUE):
                for bm in rx.finditer(block):
                    p.add_key(php_list(bm.group(1)))
            for bm in BP_ID.finditer(block):
                p.add_key(((bm.group(1) or "id").lower(),))


# --------------------------------------------------------------------------- references

FK_TABLE_LEVEL = re.compile(
    rf"\bFOREIGN\s+KEY\s*\(([^)]*)\)\s*REFERENCES\s+({QNAME})\s*(?:\(([^)]*)\))?",
    re.IGNORECASE)
REFERENCES_ANY = re.compile(
    rf"\bREFERENCES\s+({QNAME})\s*(?:\(([^)]*)\))?", re.IGNORECASE)

PHP_STMT = re.compile(r"\$\w+\s*->\s*(?:foreignId|foreignIdFor|foreignUlid|foreignUuid|foreign)\s*\(")
CONSTRAINED = re.compile(
    r"->\s*constrained\s*\(\s*(?:table\s*:\s*)?(?:['\"]([^'\"]+)['\"])?"
    r"(?:\s*,\s*(?:column\s*:\s*)?['\"]([^'\"]+)['\"])?", re.IGNORECASE)
REFS_CALL = re.compile(r"->\s*references\s*\(\s*(\[[^\]]*\]|['\"][^'\"]*['\"])", re.IGNORECASE)
ON_CALL = re.compile(r"->\s*on\s*\(\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
LOCAL_COL = re.compile(
    r"->\s*(foreignId|foreignUlid|foreignUuid|foreign)\s*\(\s*(\[[^\]]*\]|['\"][^'\"]*['\"])",
    re.IGNORECASE)
FOR_MODEL = re.compile(
    r"->\s*foreignIdFor\s*\(\s*([A-Za-z0-9_\\]+)::class\s*(?:,\s*['\"]([^'\"]+)['\"])?",
    re.IGNORECASE)


def pluralize(word: str) -> list[str]:
    w = word.lower()
    out = [w]
    if w.endswith("y") and len(w) > 1 and w[-2] not in "aeiou":
        out.append(w[:-1] + "ies")
    elif re.search(r"(s|x|z|ch|sh)$", w):
        out.append(w + "es")
    else:
        out.append(w + "s")
    return out


def snake(name: str) -> str:
    base = name.split("\\")[-1]
    return re.sub(r"(?<!^)(?=[A-Z])", "_", base).lower()


def candidate_tables(column: str) -> list[str]:
    base = re.sub(r"_(id|ulid|uuid)$", "", column.lower())
    return pluralize(base)


class Ref:
    def __init__(self, target: str, cols: tuple[str, ...], where: str, form: str,
                 local_cols: tuple[str, ...] = ()):
        self.target = target
        self.cols = cols          # referenced columns; () means "omitted, defaults to the PK"
        self.where = where
        self.form = form
        self.local_cols = local_cols


def collect_sql_refs(path: str, text: str) -> list[Ref]:
    refs: list[Ref] = []
    consumed: list[tuple[int, int]] = []
    for m in FK_TABLE_LEVEL.finditer(text):
        refs.append(Ref(norm_name(m.group(2)), norm_cols(m.group(3) or ""),
                        f"{path}:{line_of(text, m.start())}", "sql-foreign-key",
                        norm_cols(m.group(1))))
        consumed.append((m.start(), m.end()))
    for m in REFERENCES_ANY.finditer(text):
        if any(s <= m.start() < e for s, e in consumed):
            continue
        refs.append(Ref(norm_name(m.group(1)), norm_cols(m.group(2) or ""),
                        f"{path}:{line_of(text, m.start())}", "sql-references-inline",
                        ("<single column>",)))
    return refs


def collect_php_refs(path: str, text: str) -> list[Ref]:
    refs: list[Ref] = []
    for m in PHP_STMT.finditer(text):
        end = text.find(";", m.start())
        stmt = text[m.start():end if end > 0 else m.start() + 400]
        has_constrained = CONSTRAINED.search(stmt)
        has_refs = REFS_CALL.search(stmt)
        if not has_constrained and not has_refs:
            continue  # foreignId() alone declares a column and creates no constraint
        local = ()
        lm = LOCAL_COL.search(stmt)
        model = FOR_MODEL.search(stmt)
        if lm:
            local = php_list(lm.group(2))
        elif model:
            local = (model.group(2).lower() if model.group(2)
                     else snake(model.group(1)) + "_id",)
        if has_refs:
            cols = php_list(has_refs.group(1))
        elif has_constrained and has_constrained.group(2):
            cols = (has_constrained.group(2).lower(),)
        else:
            cols = ("id",)
        targets: list[str] = []
        on = ON_CALL.search(stmt)
        if on:
            targets = [norm_name(on.group(1))]
        elif has_constrained and has_constrained.group(1):
            targets = [norm_name(has_constrained.group(1))]
        elif model:
            targets = pluralize(snake(model.group(1)))
        elif local:
            targets = candidate_tables(local[0])
        form = "laravel-constrained" if has_constrained else "laravel-references-on"
        for t in targets:
            refs.append(Ref(t, cols, f"{path}:{line_of(text, m.start())}", form, local))
    return refs


# --------------------------------------------------------------------------- audit

def audit(roots: list[Path], exts: tuple[str, ...], excludes: tuple[str, ...]) -> dict:
    docs: list[tuple[str, str]] = []
    for root in roots:
        files = [root] if root.is_file() else sorted(root.rglob("*"))
        for f in files:
            if not f.is_file() or f.suffix.lower() not in exts:
                continue
            if any(part in excludes for part in f.parts):
                continue
            try:
                raw = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            docs.append((str(f), mask_window_functions(strip_comments(raw))))

    parents = discover_parents(docs)
    enrich_keys(parents, docs)
    for p in parents.values():
        p.apply_partition_rule()

    findings, unknown = [], []
    for name, p in sorted(parents.items()):
        for bad in p.rejected_keys:
            findings.append({
                "kind": "parent-key-omits-partition-column",
                "parent": name,
                "parent_keys": ["(" + ", ".join(k) + ")" for k in p.keys] or ["(none valid)"],
                "supplied": "(" + ", ".join(bad) + ")",
                "form": f"declared key omits partition column(s) "
                        f"({', '.join(p.partition_cols or ())})",
                "where": p.evidence[0].split(" ", 1)[1] if p.evidence else "?",
                "parent_evidence": p.evidence,
            })
        if not p.keys:
            unknown.append({"parent": name, "evidence": p.evidence})
    for path, text in docs:
        for r in collect_sql_refs(path, text) + collect_php_refs(path, text):
            p = parents.get(r.target)
            if p is None or not p.keys:
                continue
            supplied = r.cols
            if not supplied:
                # Omitted column list defaults to the parent's primary key; it is incomplete
                # only when the referencing side names fewer columns than that key holds.
                if r.local_cols and r.local_cols != ("<single column>",):
                    supplied = tuple(f"<col{i}>" for i in range(len(r.local_cols)))
                else:
                    supplied = ("<col0>",)
                matched = any(len(supplied) == len(k) for k in p.keys)
            else:
                matched = any(set(supplied) == set(k) for k in p.keys)
            if not matched:
                findings.append({
                    "kind": "incomplete-key-reference",
                    "parent": name_of(p),
                    "parent_keys": ["(" + ", ".join(k) + ")" for k in p.keys],
                    "supplied": "(" + ", ".join(supplied) + ")",
                    "form": r.form,
                    "where": r.where,
                    "parent_evidence": p.evidence,
                })
    return {"parents": {n: {"evidence": p.evidence,
                            "partition_columns": list(p.partition_cols or ()),
                            "keys": ["(" + ", ".join(k) + ")" for k in p.keys],
                            "rejected_keys": ["(" + ", ".join(k) + ")"
                                              for k in p.rejected_keys]}
                        for n, p in sorted(parents.items())},
            "findings": findings, "unknown_key_parents": unknown}


def name_of(p: Parent) -> str:
    return p.name


def report(result: dict, quiet: bool, as_json: bool, require_parents: bool) -> int:
    if as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    parents, findings = result["parents"], result["findings"]
    unknown = result["unknown_key_parents"]
    if not as_json and not quiet:
        print("Partitioned parents discovered:")
        if not parents:
            print("  (none)")
        for name, info in parents.items():
            keys = ", ".join(info["keys"]) if info["keys"] else "UNKNOWN"
            print(f"  {name}  key={keys}")
            for e in info["evidence"]:
                print(f"      evidence: {e}")
        print()
    if not as_json:
        for f in findings:
            print(f"FINDING [{f['kind']}] {f['where']}  {f['form']}  -> {f['parent']}"
                  f"  supplies {f['supplied']}  parent key {', '.join(f['parent_keys'])}")
        for u in unknown:
            print(f"UNKNOWN-KEY {u['parent']}  partitioned by evidence {u['evidence']}"
                  f"  but no PRIMARY KEY or UNIQUE clause was found in the roots given")

    if findings:
        print(f"RESULT: parents={len(parents)} incomplete_key_references={len(findings)}"
              f" — fix each referencing side to supply the parent's full key.")
        return EXIT_INCOMPLETE_KEY
    if unknown:
        print(f"RESULT: parents={len(parents)} key_shape_unknown={len(unknown)}"
              f" — audit inconclusive; widen the roots to the file declaring that key.")
        return EXIT_UNKNOWN_KEY
    if not parents:
        msg = ("RESULT: parents=0 no_partitioned_tables_found — this is not a clean bill of "
               "health; it means the guard now exists before the schema does.")
        print(msg)
        return EXIT_NO_PARENTS if require_parents else EXIT_OK
    print(f"RESULT: parents={len(parents)} incomplete_key_references=0"
          f" — every reference into a partitioned parent supplies that parent's full key.")
    return EXIT_OK


# --------------------------------------------------------------------------- self-test

SELF_TESTS: list[tuple[str, dict[str, str], int, list[str]]] = []


def _t(name, files, expected, must_contain=()):
    SELF_TESTS.append((name, files, expected, list(must_contain)))


_t("composite parent + id-only SQL reference is the bug",
   {"a.sql": """
CREATE TABLE events (
  id bigint, tenant_id bigint NOT NULL, created_at timestamptz NOT NULL,
  PRIMARY KEY (tenant_id, id, created_at)
) PARTITION BY RANGE (created_at);
CREATE TABLE clicks (id bigint PRIMARY KEY, event_id bigint REFERENCES events(id));
"""}, EXIT_INCOMPLETE_KEY, ["FINDING", "events"])

_t("composite parent + matching composite reference passes",
   {"a.sql": """
CREATE TABLE events (
  id bigint, tenant_id bigint, created_at timestamptz,
  PRIMARY KEY (tenant_id, id, created_at)
) PARTITION BY RANGE (created_at);
CREATE TABLE clicks (
  id bigint PRIMARY KEY, tenant_id bigint, event_id bigint, event_at timestamptz,
  FOREIGN KEY (tenant_id, event_id, event_at) REFERENCES events (tenant_id, id, created_at)
);
"""}, EXIT_OK)

_t("ordinary table with an id-only FK is not this bug",
   {"a.sql": """
CREATE TABLE users (id bigint PRIMARY KEY);
CREATE TABLE posts (id bigint PRIMARY KEY, user_id bigint REFERENCES users(id));
"""}, EXIT_NO_PARENTS)

_t("window-function PARTITION BY is not a partitioned table",
   {"q.sql": """
SELECT *, ROW_NUMBER() OVER (PARTITION BY tenant_id ORDER BY created_at DESC) AS rn FROM events;
CREATE TABLE users (id bigint PRIMARY KEY);
CREATE TABLE posts (id bigint PRIMARY KEY, user_id bigint REFERENCES users(id));
"""}, EXIT_NO_PARENTS)

_t("legacy INHERITS partitioning with an incomplete reference is the bug",
   {"legacy.sql": """
CREATE TABLE measurement (
  city_id int NOT NULL, logdate date NOT NULL, peaktemp int,
  PRIMARY KEY (city_id, logdate)
);
CREATE TABLE measurement_y2026m01 (
  CHECK (logdate >= DATE '2026-01-01' AND logdate < DATE '2026-02-01')
) INHERITS (measurement);
CREATE TRIGGER insert_measurement_trigger BEFORE INSERT ON measurement
  FOR EACH ROW EXECUTE FUNCTION measurement_insert_trigger();
CREATE TABLE readings (id bigint PRIMARY KEY, m_id int REFERENCES measurement(city_id));
"""}, EXIT_INCOMPLETE_KEY, ["measurement"])

_t("laravel constrained() into a partitioned parent is the bug",
   {"m.php": """
Schema::create('events', function (Blueprint $table) { $table->id(); });
DB::statement("CREATE TABLE events (id bigint, tenant_id bigint, created_at timestamptz,
  PRIMARY KEY (tenant_id, id, created_at)) PARTITION BY RANGE (created_at)");
Schema::create('clicks', function (Blueprint $table) {
    $table->id();
    $table->foreignId('event_id')->constrained();
});
"""}, EXIT_INCOMPLETE_KEY, ["laravel-constrained"])

_t("laravel foreignId() without constrained() creates no constraint and is not flagged",
   {"m.php": """
DB::statement("CREATE TABLE events (id bigint, tenant_id bigint, created_at timestamptz,
  PRIMARY KEY (tenant_id, id, created_at)) PARTITION BY RANGE (created_at)");
Schema::create('clicks', function (Blueprint $table) {
    $table->id();
    $table->foreignId('event_id');
});
"""}, EXIT_OK)

_t("foreignIdFor and foreign()->references()->on() both resolve their target",
   {"m.php": """
DB::statement("CREATE TABLE events (id bigint, tenant_id bigint, created_at timestamptz,
  PRIMARY KEY (tenant_id, id, created_at)) PARTITION BY RANGE (created_at)");
Schema::create('a', function (Blueprint $table) { $table->foreignIdFor(Event::class)->constrained(); });
Schema::create('b', function (Blueprint $table) {
    $table->foreign('event_id')->references('id')->on('events');
});
Schema::create('c', function (Blueprint $table) { $table->foreignUlid('event_id')->constrained(); });
"""}, EXIT_INCOMPLETE_KEY, ["laravel-references-on", "laravel-constrained"])

_t("parent whose key lives in a file outside the roots is inconclusive, not clean",
   {"a.sql": "CREATE TABLE events (id bigint, created_at timestamptz) PARTITION BY RANGE (created_at);\n"},
   EXIT_UNKNOWN_KEY, ["UNKNOWN-KEY"])

_t("ATTACH PARTITION alone proves the parent is partitioned",
   {"a.sql": """
CREATE TABLE events (id bigint, created_at timestamptz, PRIMARY KEY (id, created_at));
ALTER TABLE events ATTACH PARTITION events_2026_01 FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE clicks (id bigint PRIMARY KEY, event_id bigint REFERENCES events(id));
"""}, EXIT_INCOMPLETE_KEY, ["alter-table-attach-partition"])

_t("commented-out DDL is not schema",
   {"a.sql": """
-- CREATE TABLE events (id bigint) PARTITION BY RANGE (created_at);
/* CREATE TABLE other (id bigint) PARTITION BY LIST (x); */
CREATE TABLE users (id bigint PRIMARY KEY);
"""}, EXIT_NO_PARENTS)


def run_self_test(verbose: bool = True) -> int:
    import io
    import tempfile
    from contextlib import redirect_stdout

    failed = 0
    for name, files, expected, must_contain in SELF_TESTS:
        with tempfile.TemporaryDirectory() as tmp:
            for fname, content in files.items():
                (Path(tmp) / fname).write_text(content, encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                res = audit([Path(tmp)], DEFAULT_EXTS, DEFAULT_EXCLUDES)
                code = report(res, quiet=False, as_json=False, require_parents=True)
            out = buf.getvalue()
        ok = code == expected and all(s in out for s in must_contain)
        if not ok:
            failed += 1
        if verbose:
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] {name} (expected exit {expected}, got {code})")
            if not ok:
                print("        output:\n" + "\n".join("        " + l for l in out.splitlines()))
    total = len(SELF_TESTS)
    print(f"self-test: {total - failed}/{total} passed")
    return EXIT_OK if failed == 0 else EXIT_SELFTEST


# --------------------------------------------------------------------------- entry point

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="partitioned_fk_audit.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    ap.add_argument("roots", nargs="*", help="directories or files to scan")
    ap.add_argument("--ext", default=",".join(DEFAULT_EXTS))
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--require-parents", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--install", metavar="DEST")
    args = ap.parse_args(argv)

    if args.install:
        dest = Path(args.install)
        if dest.is_dir():
            dest = dest / Path(__file__).name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(__file__, dest)
        os.chmod(dest, 0o755)
        print(f"installed: {dest}")
        return EXIT_OK

    if args.self_test:
        return run_self_test()

    if not args.roots:
        print("usage error: give at least one root to scan, or --self-test", file=sys.stderr)
        return EXIT_USAGE
    roots = [Path(r) for r in args.roots]
    for r in roots:
        if not r.exists():
            print(f"usage error: root does not exist: {r}", file=sys.stderr)
            return EXIT_USAGE

    exts = tuple(e if e.startswith(".") else "." + e for e in args.ext.split(",") if e)
    excludes = tuple(DEFAULT_EXCLUDES) + tuple(args.exclude)
    result = audit(roots, exts, excludes)
    return report(result, args.quiet, args.json, args.require_parents)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Read-only checks over a file-vault memory store (markdown notes in a directory).

Subcommands:
  staleness  Recorded source paths resolve, freshness stamp is present and recent,
             source-derived notes carry the required fields.
  linkcheck  Every wiki link resolves to a note filename, title, alias or permalink;
             with --strict-hygiene, every note also has an incoming link and a
             "## Relations" section.

Vault root: --vault-path, else ALAA_MEMORY_VAULT. An invalid selected root is never
replaced by another one.

Exit codes:
  0  ran to completion, no findings
  1  ran to completion, findings to report
  2  could not run (vault or source root unresolved, no notes, unreadable input,
     bad arguments)

Complexity: one pass over N notes, plus one existence test per recorded path (P) for
staleness, or one dictionary lookup per link (L) for linkcheck. O(N + P) and O(N + L).

Examples:
  python3 alaa_memory_vault_check.py staleness --vault-path "$ALAA_MEMORY_VAULT"
  python3 alaa_memory_vault_check.py linkcheck --strict-hygiene
"""
import argparse
import fnmatch
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

EXIT_FINDINGS = 1
EXIT_BLOCKED = 2

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.S)
KEY_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
LIST_ITEM = re.compile(r"^\s+-\s*(.+?)\s*$")
WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
ISO_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:[T ].*)?$")
HYGIENE_EXCLUDES = ("00-control/templates/*", "00-control/schemas/*", "projects/_template/*")
SKIPPED_DIRS = {".obsidian", "archive"}


class Blocked(Exception):
    """The check could not run; maps to exit 2, never to a pass."""


def resolve_vault(arg):
    selected = arg or os.environ.get("ALAA_MEMORY_VAULT", "")
    if not selected.strip():
        raise Blocked("No vault path given. Pass --vault-path or set ALAA_MEMORY_VAULT.")
    root = Path(selected)
    if not root.is_dir():
        raise Blocked("Selected vault path does not resolve to a directory. Correct the selected path before retrying.")
    return root.resolve()


def list_notes(root):
    try:
        notes = sorted(
            p for p in root.rglob("*.md")
            if p.is_file() and not SKIPPED_DIRS.intersection(p.relative_to(root).parts[:-1])
        )
    except OSError:
        raise Blocked("vault enumeration is incomplete or unreadable.")
    if not notes:
        raise Blocked("no markdown notes found under %s" % root)
    return notes


def read_note(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        raise Blocked("a vault note could not be read.")


def frontmatter(raw):
    """Top-level scalar keys and simple list values; None without a frontmatter block.

    Deliberately small. It is not a YAML parser.
    """
    match = FRONTMATTER.match(raw)
    if not match:
        return None
    out, key = {}, None
    for line in match.group(1).splitlines():
        head = KEY_LINE.match(line)
        if head:
            key = head.group(1)
            value = head.group(2).strip().strip("\"'")
            out[key] = value if value else []
            continue
        item = LIST_ITEM.match(line)
        if item and key is not None:
            if not isinstance(out[key], list):
                out[key] = []
            out[key].append(item.group(1).strip().strip("\"'"))
    return out


def rel(path, root):
    return path.relative_to(root).as_posix()


def emit(lines, out_file):
    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if out_file:
        try:
            Path(out_file).write_text(text, encoding="utf-8")
        except OSError:
            raise Blocked("report file could not be written.")
        print("Report saved: %s" % out_file)


def section(title, entries):
    return ["", "## %s (%d)" % (title, len(entries)), ""] + (entries or ["- none"])


def staleness(args):
    root = resolve_vault(args.vault_path)
    source_root = Path(args.source_root or os.environ.get("ALAA_SOURCE_ROOT", "") or root)
    if not source_root.is_dir():
        raise Blocked("source root is not a directory: %s" % source_root)
    if args.max_age_days < 0:
        raise Blocked("--max-age-days must be zero or greater, got %d" % args.max_age_days)
    notes = list_notes(root)
    cutoff = date.today() - timedelta(days=args.max_age_days)
    derived = set(args.source_derived_types)
    dead, stale, missing, bad = [], [], [], []

    for path in notes:
        raw = read_note(path)
        fm = frontmatter(raw) if raw else None
        if fm is None:
            continue
        name = rel(path, root)
        note_type = fm.get("type") if isinstance(fm.get("type"), str) else ""
        recorded = fm.get("canonical_source_paths", [])
        if isinstance(recorded, str):
            recorded = [] if recorded == "[]" else [recorded]

        if note_type in derived and not recorded:
            missing.append("- `%s` (type: %s) has no `canonical_source_paths`" % (name, note_type))
        for item in recorded:
            if not item.strip():
                continue
            candidate = Path(item) if os.path.isabs(item) else source_root / item
            if not candidate.exists():
                dead.append("- `%s` -> `%s`" % (name, item))

        # last_curated stands in for last_verified on curated lessons.
        key = next((k for k in ("last_verified", "last_curated")
                    if isinstance(fm.get(k), str) and fm[k].strip()), "")
        if not key:
            if note_type in derived:
                missing.append("- `%s` (type: %s) has no `last_verified`" % (name, note_type))
            continue
        stamp = ISO_DATE.match(fm[key])
        try:
            parsed = date.fromisoformat(stamp.group(1)) if stamp else None
        except ValueError:
            parsed = None
        if parsed is None:
            bad.append("- `%s` %s=`%s` is not an ISO date" % (name, key, fm[key]))
        elif parsed < cutoff:
            age = (date.today() - parsed).days
            stale.append((age, "- `%s` %s=%s, %d day(s) old" % (name, key, parsed.isoformat(), age)))

    stale = [line for _, line in sorted(stale, key=lambda t: -t[0])]
    lines = ["# Memory Staleness Report", "",
             "- Vault: %s" % root,
             "- Source root: %s" % source_root,
             "- Date: %s" % date.today().isoformat(),
             "- Notes scanned: %d" % len(notes),
             "- Freshness threshold: %d day(s), so anything verified before %s is stale"
             % (args.max_age_days, cutoff.isoformat())]
    lines += section("Recorded source paths that no longer exist", sorted(dead))
    lines += section("Notes past the freshness threshold", stale)
    lines += section("Source-derived notes missing a required field", sorted(missing))
    lines += section("Unparseable date values", sorted(bad))
    emit(lines, args.out_file)
    total = len(dead) + len(stale) + len(missing) + len(bad)
    print("staleness: %s" % ("%d finding(s)" % total if total else "clean"))
    return EXIT_FINDINGS if total else 0


def linkcheck(args):
    root = resolve_vault(args.vault_path)
    notes = list_notes(root)
    raws = {path: read_note(path) for path in notes}

    # One pass builds the index from every link-target form to the notes it addresses,
    # so a link written as a title or alias credits the note it names.
    index = {}

    def add_target(key, path):
        key = key.strip().lower()
        if key and path not in index.setdefault(key, []):
            index[key].append(path)

    for path, raw in raws.items():
        add_target(path.stem, path)
        fm = frontmatter(raw) if raw else None
        if fm:
            for field in ("title", "permalink"):
                if isinstance(fm.get(field), str):
                    add_target(fm[field], path)
            if isinstance(fm.get("aliases"), list):
                for alias in fm["aliases"]:
                    add_target(alias, path)

    incoming = dict.fromkeys(notes, 0)
    broken = []
    for path, raw in raws.items():
        for match in WIKI_LINK.finditer(raw):
            target = match.group(1).strip()
            # Template placeholders such as [[<Project> Index]] are not links.
            if re.match(r"^<.*>$", target) or re.search(r"<[A-Za-z]", target):
                continue
            credited = index.get(target.lower())
            if credited:
                for note in credited:
                    incoming[note] += 1
            else:
                broken.append("- `%s` -> [[%s]] not found" % (rel(path, root), target))

    orphans, no_relations = [], []
    for path in notes:
        name = rel(path, root)
        if any(fnmatch.fnmatchcase(name.lower(), glob) for glob in HYGIENE_EXCLUDES):
            continue
        if incoming[path] == 0:
            orphans.append("- `%s`" % name)
        if not re.search(r"^##\s+Relations", raws[path], re.M):
            no_relations.append("- `%s`" % name)

    hygiene = len(orphans) + len(no_relations)
    lines = ["# Wiki Link Check Report", "",
             "- Vault: %s" % root,
             "- Date: %s" % date.today().isoformat(),
             "- Notes scanned: %d" % len(notes),
             "- Hygiene findings affect the exit code: %s" % args.strict_hygiene]
    lines += section("Broken wiki links", sorted(broken))
    lines += section("Orphan notes, no incoming wiki link", sorted(orphans))
    lines += section("Notes without a Relations section", sorted(no_relations))
    emit(lines, args.out_file)
    findings = len(broken) + (hygiene if args.strict_hygiene else 0)
    if findings:
        print("linkcheck: %d broken link(s), %d hygiene finding(s)" % (len(broken), hygiene))
        return EXIT_FINDINGS
    print("linkcheck: clean (%d hygiene finding(s) not counted)" % hygiene)
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Exit codes: 0 clean, 1 findings, 2 could not run. A 2 is a failed gate, never a pass.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    for name, handler, summary in (("staleness", staleness, "freshness and source-path check"),
                                   ("linkcheck", linkcheck, "wiki-link health check")):
        p = sub.add_parser(name, help=summary, description=summary)
        p.add_argument("--vault-path", default="", help="vault root; default from ALAA_MEMORY_VAULT")
        p.add_argument("--out-file", default="", help="also write the report to this file")
        p.set_defaults(handler=handler)
        if name == "staleness":
            p.add_argument("--source-root", default="",
                           help="base for relative canonical_source_paths; default ALAA_SOURCE_ROOT, then the vault")
            p.add_argument("--max-age-days", type=int, default=90, help="freshness threshold in days (default 90)")
            p.add_argument("--source-derived-types", nargs="+",
                           default=["architecture", "contract", "service_ownership", "operations"],
                           help="note types that must carry source paths and a freshness stamp")
        else:
            p.add_argument("--strict-hygiene", action="store_true",
                           help="count orphan notes and missing Relations sections as findings")
    return parser


def main():
    args = build_parser().parse_args()
    try:
        return args.handler(args)
    except Blocked as err:
        print("BLOCKED: %s" % err)
        return EXIT_BLOCKED


if __name__ == "__main__":
    sys.exit(main())

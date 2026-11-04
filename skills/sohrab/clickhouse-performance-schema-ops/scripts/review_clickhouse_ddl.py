#!/usr/bin/env python3
"""Review ClickHouse DDL and aggregate writer/read evidence without executing SQL."""

import argparse
import os
import re
import sys

VERSION = "1.1.0"

DEFAULT_TENANT_COLUMNS = (
    "project_id",
    "tenant_id",
    "org_id",
    "organization_id",
    "account_id",
    "workspace_id",
    "customer_id",
)

# Partition expressions that keep the distinct-partition count inside the range
# the official partitioning guidance calls usually optimal (fewer than 100-1,000).
COARSE_PARTITION_FUNCTIONS = (
    "toyyyymm",
    "tostartofmonth",
    "tostartofquarter",
    "tostartofyear",
    "toyear",
    "toquarter",
    "tomonday",
    "tostartofweek",
)

# Partition expressions finer than monthly. Legal, but the distinct count has to
# be computed against the retention window before it is accepted.
FINE_PARTITION_FUNCTIONS = (
    "toyyyymmdd",
    "todate",
    "tostartofday",
    "tostartofhour",
    "tostartofminute",
    "todatetime",
)

IDENTIFIER_TAIL = re.compile(r"(^|_)(id|uuid|ulid|guid|key|hash|token)$", re.I)

CLAUSE_KEYWORDS = (
    "ENGINE",
    "PARTITION BY",
    "PRIMARY KEY",
    "ORDER BY",
    "SAMPLE BY",
    "TTL",
    "SETTINGS",
    "AS SELECT",
    "COMMENT",
)


NAME = r'(?:[A-Za-z_][A-Za-z_0-9]*|"[A-Za-z_][A-Za-z_0-9]*"|`[A-Za-z_][A-Za-z_0-9]*`)'
SQL_TOKEN = re.compile(
    r"""(?P<space>\s+)|(?P<line>--[^\n]*|\#[^\n]*)|(?P<block>/\*.*?\*/)|
    (?P<string>'(?:\\.|''|[^'\\])*')|(?P<quoted>"(?:\\.|""|[^"\\])*"|`(?:\\.|``|[^`\\])*`)|
    (?P<number>[0-9]+(?:\.[0-9]+)?)|[A-Za-z_][A-Za-z_0-9]*|<=|>=|!=|<>|==|
    (?P<invalid>/\*|['"`]|\$)|[^\s]""",
    re.S | re.X,
)
AGGREGATE_ENGINES = {"aggregatingmergetree", "replicatedaggregatingmergetree"}
OPEN_GROUP = {"(": ")", "[": "]", "{": "}"}
CLOSE_GROUP = set(OPEN_GROUP.values())


class ProofError(ValueError):
    pass


def lex(sql):
    for match in SQL_TOKEN.finditer(sql):
        if match.lastgroup not in {"space", "line", "block"}:
            yield match


def top_level(tokens):
    """Yield the positions outside groups, including each opening delimiter."""
    stack = []
    for index, token in enumerate(tokens):
        if not stack:
            yield index
        if token in OPEN_GROUP:
            stack.append(OPEN_GROUP[token])
        elif token in CLOSE_GROUP:
            if not stack or stack.pop() != token:
                raise ProofError("unbalanced SQL delimiters")
    if stack:
        raise ProofError("unbalanced SQL delimiters")


def split_tokens(tokens, separator):
    start = 0
    parts = []
    for index in top_level(tokens):
        if tokens[index].upper() == separator:
            parts.append(tokens[start:index])
            start = index + 1
    return parts + [tokens[start:]]


def token_name(token):
    return token.strip('`"') if re.fullmatch(NAME, token) else None


def qualified_name(tokens, index):
    if index >= len(tokens) or not token_name(tokens[index]):
        raise ProofError("expected a table name")
    name = token_name(tokens[index])
    index += 1
    if index < len(tokens) and tokens[index] == ".":
        if index + 1 >= len(tokens) or not token_name(tokens[index + 1]):
            raise ProofError("expected a qualified table name")
        name += "." + token_name(tokens[index + 1])
        index += 2
    return name, index


def sql_statements(sql):
    """Keep completed statements even if a later one cannot be analyzed."""
    tokens = []
    start = 0
    for match in lex(sql):
        token = match.group()
        if match.lastgroup == "invalid":
            yield start, match.start(), tokens, "unsupported or unterminated SQL token"
            return
        if token == ";":
            if tokens:
                yield start, match.start(), tokens, None
            tokens = []
        else:
            if not tokens:
                start = match.start()
            tokens.append(token)
    if tokens:
        yield start, len(sql), tokens, None


class Finding(object):
    def __init__(self, code, path, line, table, summary, obligation):
        self.code = code
        self.path = path
        self.line = line
        self.table = table
        self.summary = summary
        self.obligation = obligation

    def render(self):
        return "{0}:{1}: {2} [{3}] {4}\n    -> {5}".format(
            self.path, self.line, self.code, self.table, self.summary, self.obligation
        )


# --------------------------------------------------------------------------
# Lexical scrubbing and offset helpers
# --------------------------------------------------------------------------


def scrub(sql):
    """Blank SQL comments and string contents without moving source offsets."""
    out = list(sql)
    for match in SQL_TOKEN.finditer(sql):
        start, end = match.span()
        if match.lastgroup == "string":
            start += 1
            end -= 1
        elif match.lastgroup not in {"line", "block"}:
            continue
        out[start:end] = (ch if ch == "\n" else " " for ch in sql[start:end])
    return "".join(out)


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def match_paren(text, open_index):
    """Return the index just past the parenthesis that closes text[open_index]."""
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    return -1


def split_top_level(text):
    """Split on commas that are not inside parentheses."""
    matches = list(lex(text))
    tokens = [match.group() for match in matches]
    start = 0
    parts = []
    for index in top_level(tokens):
        if tokens[index] == ",":
            parts.append(text[start:matches[index].start()].strip())
            start = matches[index].end()
    return parts + [text[start:].strip()]


def identifiers_in(expression):
    """Bare identifiers in an expression, excluding function names."""
    names = []
    for match in re.finditer(r"[A-Za-z_][A-Za-z_0-9]*", expression):
        end = match.end()
        rest = expression[end:]
        if rest.lstrip().startswith("("):
            continue
        names.append(match.group(0))
    return names


# --------------------------------------------------------------------------
# Statement parsing
# --------------------------------------------------------------------------


class Table(object):
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset
        self.columns = []          # list of (name, type_text, offset)
        self.engine = ""
        self.engine_offset = offset
        self.partition_by = ""
        self.partition_offset = offset
        self.order_by = []         # list of expression strings
        self.order_offset = offset
        self.ambiguous_key = False
        self.inline_primary = False
        self.nonstored_columns = set()
        self.primary_key = []
        self.primary_offset = offset

    def column_names(self):
        return [c[0] for c in self.columns]


CREATE_TABLE = re.compile(
    r"\bCREATE\s+(?:OR\s+REPLACE\s+)?(?:TEMPORARY\s+)?TABLE\s+"
    r"(?:IF\s+NOT\s+EXISTS\s+)?([`\"]?[A-Za-z_][A-Za-z_0-9]*[`\"]?"
    r"(?:\s*\.\s*[`\"]?[A-Za-z_][A-Za-z_0-9]*[`\"]?)?)",
    re.I,
)


def parse_tables(scrubbed):
    tables = []
    for match in CREATE_TABLE.finditer(scrubbed):
        name = re.sub(r"[`\"\s]", "", match.group(1))
        table = Table(name, match.start())
        body_start = re.match(rf"\s*(?:ON\s+CLUSTER\s+(?:{NAME}|' *')\s*)?\(",
                              scrubbed[match.end():], re.I)
        if not body_start:
            continue
        open_index = match.end() + body_start.end() - 1
        close_index = match_paren(scrubbed, open_index)
        if close_index == -1:
            continue
        body = scrubbed[open_index + 1:close_index - 1]
        base = open_index + 1
        cursor = 0
        for item in split_top_level(body):
            item_at = body.find(item, cursor)
            cursor = item_at + len(item) if item_at >= 0 else cursor
            head = item.strip()
            if clause_positions([m.group() for m in lex(head)], [("PRIMARY", "KEY")]):
                table.inline_primary = True
            if re.match(r"^(INDEX|PROJECTION|CONSTRAINT|PRIMARY\s+KEY)\b", head, re.I):
                continue
            column = re.match(r"^[`\"]?([A-Za-z_][A-Za-z_0-9]*)[`\"]?\s+(.*)$", head, re.S)
            if not column:
                continue
            column_name, type_text = column.groups()
            table.columns.append((column_name, type_text.strip(), base + max(item_at, 0)))
            if clause_positions([m.group() for m in lex(type_text)], [("ALIAS",), ("EPHEMERAL",)]):
                table.nonstored_columns.add(column_name)
        tail_end = scrubbed.find(";", close_index)
        tail_end = len(scrubbed) if tail_end == -1 else tail_end
        tail = scrubbed[close_index:tail_end]
        parse_clauses(table, tail, close_index)
        tables.append(table)
    return tables


def clause_text(tail, keyword):
    """Text of one trailing clause, and its offset within tail."""
    matches = list(lex(tail))
    clauses = clause_positions([m.group() for m in matches],
                               [tuple(name.split()) for name in CLAUSE_KEYWORDS])
    for index, (at, label) in enumerate(clauses):
        if " ".join(label) != keyword:
            continue
        end = matches[clauses[index + 1][0]].start() if index + 1 < len(clauses) else len(tail)
        return tail[matches[at + len(label) - 1].end():end].strip(), matches[at].start()
    return None, -1


def tuple_elements(text):
    text = text.strip()
    if text.startswith("("):
        close = match_paren(text, 0)
        if close == len(text):
            return split_top_level(text[1:close - 1])
    return [text] if text else []


def parse_clauses(table, tail, tail_base):
    engine, at = clause_text(tail, "ENGINE")
    if engine is not None:
        table.engine = engine.lstrip("=").strip()
        table.engine_offset = tail_base + at
    partition, at = clause_text(tail, "PARTITION BY")
    if partition is not None:
        table.partition_by = partition
        table.partition_offset = tail_base + at
    order, at = clause_text(tail, "ORDER BY")
    if order is not None:
        table.order_by = tuple_elements(order)
        table.order_offset = tail_base + at
    primary, at = clause_text(tail, "PRIMARY KEY")
    key_clauses = clause_positions([m.group() for m in lex(tail)],
                                   [("ORDER", "BY"), ("PRIMARY", "KEY")])
    table.ambiguous_key = (
        len(key_clauses) != len({label for _, label in key_clauses})
        or primary == ""
        or bool(clause_positions([m.group() for m in lex(tail)], [("AS",)]))
    )
    if primary is not None:
        table.primary_key = tuple_elements(primary)
        table.primary_offset = tail_base + at


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------


def justification_comment(original, offset):
    """True when the column's own line, or the line above it, records a reason.

    The rule in references/20-table-design.md is that a Nullable column names the
    query that needs the null. The checker clears the finding only when the text
    'nullable:' appears in a comment on that line or the line before it, because
    a reason that is not written down cannot be reviewed.
    """
    line_index = original.count("\n", 0, offset)
    lines = original.split("\n")
    window = lines[max(0, line_index - 1):line_index + 1]
    return any("nullable:" in line.lower() for line in window)


def is_nullable(type_text):
    return re.match(r"^\s*Nullable\s*\(", type_text, re.I) is not None


def nullable_inner(type_text):
    match = re.match(r"^\s*Nullable\s*\(\s*([A-Za-z_][A-Za-z_0-9]*)", type_text, re.I)
    return match.group(1) if match else "T"


def replacement_for(inner):
    lowered = inner.lower()
    if lowered == "string":
        return "LowCardinality(String) DEFAULT '' for a repeated dimension, or String DEFAULT ''"
    if lowered.startswith("float") or lowered.startswith("decimal"):
        return "{0} DEFAULT 0".format(inner)
    if lowered.startswith("uint") or lowered.startswith("int"):
        return "{0} DEFAULT 0".format(inner)
    if lowered.startswith("date") or lowered.startswith("datetime"):
        return "{0} with an explicit sentinel the readers agree on".format(inner)
    return "{0} DEFAULT <the empty value>".format(inner)


def check_table(statement, original, table, tenant_columns, single_tenant):
    path = statement.path

    def table_line(offset):
        return statement.line + line_of(original, offset) - 1

    findings = []
    is_aggregate = aggregate_engine(table)
    declared = set(table.column_names())
    if not is_aggregate:
        declared = {name.lower() for name in declared}
    order_names = [identifiers_in(e) for e in table.order_by]
    order_first = [names[0].lower() if names else "" for names in order_names]

    # CH001 / CH002 -- tenancy
    present = [c for c in table.column_names() if c.lower() in tenant_columns]
    if present:
        if not table.order_by:
            findings.append(Finding(
                "CH001", path, table_line(table.offset), table.name,
                "table has tenant column '{0}' but no ORDER BY".format(present[0]),
                "Give the table an ORDER BY whose first element is the tenant column, "
                "or every tenant query reads every tenant's rows."))
        elif order_first[0] not in tenant_columns:
            findings.append(Finding(
                "CH001", path, table_line(table.order_offset), table.name,
                "ORDER BY starts with '{0}', not the tenant column '{1}'".format(
                    table.order_by[0], present[0]),
                "Move '{0}' to the first position in ORDER BY, because the sparse index "
                "prunes on a prefix and a query filtered only by tenant prunes nothing "
                "today.".format(present[0])))
    elif not single_tenant:
        findings.append(Finding(
            "CH002", path, table_line(table.offset), table.name,
            "no tenant column found (looked for: {0})".format(", ".join(sorted(tenant_columns))),
            "Add the tenant column and put it first in ORDER BY. If this table really "
            "holds one tenant's rows only, re-run with --single-tenant so the assertion "
            "is recorded in the command line rather than assumed."))

    # CH003 / CH004 -- partition key cardinality
    if table.partition_by:
        expression = table.partition_by.strip()
        functions = [f.lower() for f in re.findall(r"([A-Za-z_][A-Za-z_0-9]*)\s*\(", expression)]
        bare = not functions and expression.lower() not in ("tuple()", "")
        if bare or any(
            f not in COARSE_PARTITION_FUNCTIONS and f not in FINE_PARTITION_FUNCTIONS
            for f in functions
        ):
            findings.append(Finding(
                "CH003", path, table_line(table.partition_offset), table.name,
                "PARTITION BY {0} has no bounded distinct count".format(expression),
                "Partition on a coarse time bucket such as toYYYYMM(<date column>) and let "
                "ORDER BY do the pruning. Parts are never merged across partitions, so an "
                "unbounded key accumulates unmergeable parts until inserts fail."))
        elif any(f in FINE_PARTITION_FUNCTIONS for f in functions):
            findings.append(Finding(
                "CH004", path, table_line(table.partition_offset), table.name,
                "PARTITION BY {0} is finer than monthly".format(expression),
                "State the retention window and show that window divided by this "
                "granularity stays under 1,000 partitions, or move to toYYYYMM."))

    # CH005 -- Nullable columns with no recorded reason
    for name, type_text, offset in table.columns:
        if is_nullable(type_text) and not justification_comment(original, offset):
            inner = nullable_inner(type_text)
            findings.append(Finding(
                "CH005", path, table_line(offset), table.name,
                "column '{0}' is Nullable({1}) with no recorded reason".format(name, inner),
                "Replace with {0}, or write a comment on that line starting 'nullable:' "
                "naming the query that must tell an absent value from an empty one. A "
                "Nullable column carries a separate UInt8 column processed on every "
                "access.".format(replacement_for(inner))))

    # CH006/CH007 -- raw sort key or the aggregate's effective sparse index.
    index_key = table.primary_key if is_aggregate and table.primary_key else table.order_by
    index_offset = table.primary_offset if is_aggregate and table.primary_key else table.order_offset
    label = "effective PRIMARY KEY" if is_aggregate else "ORDER BY"
    index_names = [identifiers_in(expr) for expr in index_key] if is_aggregate else order_names
    if len(index_key) > 5:
        findings.append(Finding(
            "CH006", path, table_line(index_offset), table.name,
            "{0} has {1} elements".format(label, len(index_key)),
            ("Keep the aggregate merge dimensions in ORDER BY. " if is_aggregate else "") +
            "Cut to five or fewer, or name for each element past the fifth a real query "
            "that filters on it and on every element before it. Official guidance is that "
            "4-5 keys are typically sufficient."))

    # CH007 -- high-cardinality tail
    tail = []
    for position, names in enumerate(index_names[2:], start=3):
        head = names[0] if names else ""
        if head and IDENTIFIER_TAIL.search(head):
            tail.append((position, head))
    if tail:
        listed = ", ".join("{0} (position {1})".format(n, p) for p, n in tail)
        findings.append(Finding(
            "CH007", path, table_line(index_offset), table.name,
            "identifier-like columns in the {0} tail: {1}".format(label, listed),
            ("Keep the aggregate merge dimensions in ORDER BY. " if is_aggregate else "") +
            "Each one prunes only for a query that already constrains every element to "
            "its left; otherwise it is write cost and index memory. Drop it, or serve "
            "the identifier-first access path with a projection or a rollup."))

    # CH008 -- keys referencing undeclared columns
    for label, expressions, offset in (
        ("ORDER BY", table.order_by, table.order_offset),
        ("PARTITION BY", [table.partition_by] if table.partition_by else [], table.partition_offset),
        ("PRIMARY KEY", table.primary_key, table.primary_offset),
    ):
        for expression in expressions:
            for name in identifiers_in(expression):
                if (name if is_aggregate else name.lower()) in declared:
                    continue
                if re.match(r"^\d", name) or name.lower() in ("tuple",):
                    continue
                findings.append(Finding(
                    "CH008", path, table_line(offset), table.name,
                    "{0} references '{1}', which the table does not declare".format(label, name),
                    "Declare the column or correct the name. ClickHouse rejects this at "
                    "CREATE time, so the DDL cannot be applied as written."))

    # CH009 -- PRIMARY KEY must be a prefix of ORDER BY
    if table.primary_key and table.order_by:
        normal_pk = [re.sub(r"\s+", "", e).lower() for e in table.primary_key]
        normal_ob = [re.sub(r"\s+", "", e).lower() for e in table.order_by]
        if is_aggregate and None not in aggregate_key(table.primary_key + table.order_by):
            normal_pk = aggregate_key(table.primary_key)
            normal_ob = aggregate_key(table.order_by)
        if normal_ob[:len(normal_pk)] != normal_pk:
            findings.append(Finding(
                "CH009", path, table_line(table.primary_offset), table.name,
                "PRIMARY KEY is not a prefix of ORDER BY",
                "Make PRIMARY KEY a leading prefix of ORDER BY, or drop it and let it "
                "default to ORDER BY. ClickHouse rejects a non-prefix primary key."))

    return findings


class Statement:
    def __init__(self, path, sql, offset, tokens):
        self.path = path
        self.line = line_of(sql, offset)
        self.tokens = tokens

    def location(self):
        return "{0}:{1}".format(self.path, self.line)


def aggregate_engine(table):
    engine = re.match(r"[A-Za-z_][A-Za-z_0-9]*", table.engine)
    return engine is not None and engine.group().lower() in AGGREGATE_ENGINES


def select_shape(tokens):
    """Locate one top-level SELECT over a named source."""
    upper = [token.upper() for token in tokens]
    if upper[:1] != ["SELECT"] or upper.count("SELECT") != 1:
        raise ProofError("expected a single SELECT without nested queries")
    top = list(top_level(tokens))
    if any(upper[i] in {"WITH", "UNION", "EXCEPT", "INTERSECT", "JOIN", "ARRAY",
                        "SETTINGS", "INTO", "FORMAT"}
           for i in top):
        raise ProofError("unsupported SELECT clause")
    sources = [i for i in top if upper[i] == "FROM"]
    if len(sources) != 1:
        raise ProofError("expected one FROM source")
    source, end = qualified_name(tokens, sources[0] + 1)
    projection = split_tokens(tokens[1:sources[0]], ",")
    return projection, source, tokens[end:]


def projections(items, allow_star=False):
    outputs = {}
    for item in items:
        parts = split_tokens(item, "AS")
        if len(parts) == 2 and parts[0] and len(parts[1]) == 1:
            name = token_name(parts[1][0])
        elif len(item) == 1:
            if allow_star and item == ["*"]:
                continue
            name = token_name(item[0])
        else:
            name = None
        if not name or name in outputs:
            raise ProofError("unsupported or duplicate SELECT output name")
        outputs[name] = parts[0]
    return outputs


def clause_positions(tokens, keywords):
    upper = [token.upper() for token in tokens]
    return [(i, keyword) for i in top_level(tokens) for keyword in keywords
            if upper[i:i + len(keyword)] == list(keyword)]


def writer_dimensions(tokens, table, sources):
    items, source, tail = select_shape(tokens)
    outputs = projections(items)
    clauses = clause_positions(tail, [("WHERE",), ("GROUP", "BY"), ("HAVING",),
                                      ("ORDER", "BY"), ("LIMIT",), ("SETTINGS",)])
    # Admitted writers end at GROUP BY. Rollup/cube/totals/ordinals and other
    # trailing syntax cannot be mistaken for a list of stored dimensions.
    labels = [label for _, label in clauses]
    if labels not in [[("GROUP", "BY")], [("WHERE",), ("GROUP", "BY")]] or clauses[0][0] != 0:
        raise ProofError("expected optional WHERE followed by a final GROUP BY")
    group_at = clauses[-1][0]
    if group_at == 1:
        raise ProofError("empty WHERE clause")
    columns = set(table.column_names()) - table.nonstored_columns
    source_columns = sources.get(source)
    seen = set()
    dimensions = set()
    errors = []
    for item in split_tokens(tail[group_at + 2:], ","):
        name = token_name(item[0]) if len(item) == 1 else None
        if not name or item[0].upper() in {"ALL", "ROLLUP", "CUBE", "TOTALS"} or name in seen:
            errors.append("GROUP BY must list distinct bare column names or SELECT AS aliases")
            continue
        seen.add(name)
        if name not in outputs or name not in columns:
            errors.append("GROUP BY output '{0}' is unresolved in the target".format(name))
            continue
        expression = outputs[name]
        if expression != [name] and not (
            len(expression) == 1 and token_name(expression[0]) == name
        ) and (source_columns is None or name in source_columns or any(
            token_name(token) == name for other, value in outputs.items()
            if other != name for token in value
        )):
            errors.append("GROUP BY alias '{0}' has unresolved source binding".format(name))
            continue
        dimensions.add(name)
    return dimensions, errors


def predicate_operand(tokens):
    if len(tokens) == 1:
        match = SQL_TOKEN.fullmatch(tokens[0])
        return match is not None and match.lastgroup in {"string", "number"}
    if len(tokens) == 2 and tokens[0] == "-":
        return bool(re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", tokens[1]))
    # Native ClickHouse typed scalar query parameters, e.g. {tenant:String}.
    return (len(tokens) == 5 and tokens[0] == "{" and tokens[2] == ":"
            and tokens[4] == "}" and bool(token_name(tokens[1]))
            and token_name(tokens[3]) == tokens[3] and tokens[3].upper() != "IDENTIFIER")


def read_predicates(statement, tables):
    items, target, tail = select_shape(statement.tokens)
    if target not in tables:
        raise ProofError("read target '{0}' is unresolved".format(target))
    if tail[:1] and tail[0].upper() == "FINAL":
        tail = tail[1:]
    labels = [("PREWHERE",), ("WHERE",), ("GROUP", "BY"), ("HAVING",),
              ("ORDER", "BY"), ("LIMIT",)]
    clauses = clause_positions(tail, labels)
    ranks = [labels.index(label) for _, label in clauses]
    if (not clauses or clauses[0][0] != 0 or sorted(set(ranks)) != ranks
            or not any(rank in (0, 1) for rank in ranks)):
        raise ProofError("expected PREWHERE or WHERE on the named read target")

    columns = tables[target]
    for name, expression in projections(items, allow_star=True).items():
        if name in columns and not (len(expression) == 1 and token_name(expression[0]) == name):
            raise ProofError("read projection shadows target column '{0}'".format(name))

    equality = set()
    constrained = set()
    for index, (at, label) in enumerate(clauses):
        end = clauses[index + 1][0] if index + 1 < len(clauses) else len(tail)
        body = tail[at + len(label):end]
        if not body:
            raise ProofError("empty read clause")
        if label not in {("PREWHERE",), ("WHERE",)}:
            continue
        for term in split_tokens(body, "AND"):
            name = token_name(term[0]) if term else None
            if (name not in columns or len(term) < 3
                    or term[1] not in {"=", "==", "<", "<=", ">", ">="}
                    or not predicate_operand(term[2:])):
                raise ProofError("expected AND-connected target column comparisons to literals or parameters")
            constrained.add(name)
            if term[1] in {"=", "=="}:
                equality.add(name)
    return target, equality, constrained


MV_START = re.compile(r"^CREATE(?: OR REPLACE)? MATERIALIZED VIEW(?: IF NOT EXISTS)?\b")
WRITE_START = re.compile(r"^(?:INSERT INTO(?: TABLE)?|ALTER TABLE|ATTACH TABLE|"
                         r"REPLACE TABLE|CREATE OR REPLACE TABLE|UPDATE|DELETE FROM|"
                         r"TRUNCATE TABLE|DROP TABLE(?: IF EXISTS)?)\b")


def collect_writers(statements, aggregates, tables, problems):
    writers = {name: [] for name in aggregates}
    for statement in statements:
        tokens = statement.tokens
        # Only the head can identify a statement; quoted tokens cannot match
        # these unquoted keywords. Limit joining to the longest supported head.
        head = " ".join(token.upper() for token in tokens[:9])
        mv = MV_START.match(head)
        write = WRITE_START.match(head)
        try:
            if mv:
                _, end = qualified_name(tokens, len(mv.group().split()))
                clauses = clause_positions(tokens[end:], [("TO",), ("AS", "SELECT")])
                if not clauses or clauses[0][1] != ("TO",):
                    if any(token.lower() in AGGREGATE_ENGINES for token in tokens[end:]):
                        raise ProofError("unsupported aggregate materialized view without TO target")
                    continue
                target, _ = qualified_name(tokens, end + clauses[0][0] + 1)
                if target not in tables:
                    raise ProofError("materialized view target '{0}' is unresolved".format(target))
                if target in aggregates:
                    selects = [end + at + 1 for at, label in clauses if label == ("AS", "SELECT")]
                    if len(selects) != 1:
                        raise ProofError("materialized view for '{0}' has no single AS SELECT".format(target))
                    writers[target].append((statement, tokens[selects[0]:]))
            elif write and aggregates:
                target, _ = qualified_name(tokens, len(write.group().split()))
                if target in aggregates or (
                    "." not in target and any(name.endswith("." + target) for name in aggregates)
                ):
                    raise ProofError("unsupported direct write or alteration of '{0}'".format(target))
            elif aggregates and (
                tokens[0].upper() in {"USE", "SET", "RENAME", "EXCHANGE"}
                or head.startswith("ATTACH MATERIALIZED VIEW ")
            ):
                raise ProofError("unsupported schema or session change in aggregate bundle")
        except ProofError as exc:
            problems.append((statement, str(exc)))
    return writers


def aggregate_key(expressions):
    return [token_name(tokens[0]) if len(tokens) == 1 else None
            for tokens in ([match.group() for match in lex(expr)] for expr in expressions)]


def check_aggregate(statement, table, writers, queries, tables, problems):
    findings = []
    order = aggregate_key(table.order_by)
    primary = aggregate_key(table.primary_key)
    if (not order or None in order or None in primary or table.inline_primary
            or table.ambiguous_key or len(set(order)) != len(order)
            or table.nonstored_columns.intersection(order + primary)):
        problems.append((statement, "{0}: expected bare ORDER BY and PRIMARY KEY column lists"
                         .format(table.name)))
    if not writers:
        problems.append((statement, "{0}: no analyzable materialized view writer".format(table.name)))
    for writer, query in writers:
        try:
            dimensions, errors = writer_dimensions(query, table, tables)
        except ProofError as exc:
            problems.append((writer, "{0}: {1}".format(table.name, exc)))
            continue
        for error in errors:
            problems.append((writer, "{0}: {1}".format(table.name, error)))
        missing = dimensions.difference(order)
        if missing:
            findings.append(Finding(
                "CH010", writer.path, writer.line, table.name,
                "ORDER BY omits writer GROUP BY dimension(s): {0}".format(", ".join(sorted(missing))),
                "Preserve every independent stored dimension in the merge key. A shorter sparse "
                "PRIMARY KEY does not change merge identity."))
    if primary and len(primary) < len(order) and primary == order[:len(primary)] and None not in primary:
        for query, equal, constrained in queries:
            if set(primary[:-1]) <= equal and primary[-1] in constrained:
                print("{0}: sparse PRIMARY KEY predicate evidence for [{1}] at {2}".format(
                    statement.location(), table.name, query.location()))
                break
        else:
            problems.append((statement, "{0}: short PRIMARY KEY has no qualifying --read-query"
                             .format(table.name)))
    return findings


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

CANNOT_CHECK = """\
not checked by this tool, and still your responsibility:
  - whether supplied writers and read queries cover production paths
  - actual pruning, index memory and merge behavior on the target version
  - whether a LowCardinality column really holds under ~10,000 distinct values
  - whether the retention window times the partition granularity stays bounded
  - whether the engine's deduplication model matches what readers assume
  - whether the tenant predicate is present in every query against this table
  - whether the deployed table still matches this file (compare system.columns)
"""

EPILOG = """\
exit codes:
  0  no finding. The DDL clears the mechanical rules; the unchecked list below
     is still open and must be answered in the change request.
  1  at least one finding. Fix every finding or record the justification the
     finding names, then run this checker again; do not apply the DDL while any
     finding stands.
  2  invalid arguments, unreadable input, or unavailable/unsupported proof.
     Resolve the reported gap and rerun. Structural findings still apply.

checks:
  CH001  a tenant column exists but does not lead ORDER BY
  CH002  no tenant column found, and --single-tenant was not given
  CH003  PARTITION BY has no bounded distinct count
  CH004  PARTITION BY is finer than monthly
  CH005  a Nullable column with no 'nullable:' comment naming the query that
         needs the null
  CH006  more than five elements in ORDER BY or the aggregate sparse index
  CH007  identifier-like columns in the corresponding key tail
  CH008  ORDER BY, PARTITION BY, or PRIMARY KEY names an undeclared column
  CH009  PRIMARY KEY is not a prefix of ORDER BY
  CH010  ORDER BY omits a stored GROUP BY dimension from an aggregate writer
  CH011  required input or proof is invalid, unsupported or unavailable

CH002 and CH005 are cleared by recording an assertion, not by deleting the
check: CH002 by passing --single-tenant, CH005 by writing the reason on the
column's line. Both leave the claim where a reviewer can read it.
"""


def main(argv):
    parser = argparse.ArgumentParser(
        prog="review_clickhouse_ddl.py",
        description="Review a complete ClickHouse DDL and writer SQL bundle.",
        epilog=EPILOG + "\n" + CANNOT_CHECK,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*", help="SQL files defining tables and all writers")
    parser.add_argument(
        "--read-query", action="append", default=[], metavar="FILE",
        help="actual target SELECT SQL for a short aggregate PRIMARY KEY (repeatable)",
    )
    parser.add_argument(
        "--tenant-column",
        action="append",
        default=[],
        metavar="NAME",
        help="treat NAME as a tenant column (repeatable; adds to the built-in list)",
    )
    parser.add_argument(
        "--single-tenant",
        action="store_true",
        help="assert these tables hold one tenant's rows only, which clears CH002",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)

    if not args.paths:
        parser.print_usage(sys.stderr)
        sys.stderr.write("error: give at least one SQL file\n")
        return 2

    tenant_columns = set(DEFAULT_TENANT_COLUMNS)
    tenant_columns.update(name.lower() for name in args.tenant_column)

    all_findings = []
    problems = []
    tables = {}
    table_entries = []
    statements = []
    read_statements = []
    for paths, collection in ((args.paths, statements), (args.read_query, read_statements)):
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    sql = handle.read()
            except (OSError, UnicodeError) as exc:
                problems.append((Statement(path, "", 0, []), str(exc)))
                continue
            has_statement = False
            for start, end, tokens, error in sql_statements(sql):
                has_statement = True
                statement = Statement(path, sql, start, tokens)
                if error:
                    problems.append((statement, error))
                    continue
                collection.append(statement)
                if collection is read_statements:
                    continue
                sql_part = sql[start:end]
                cleaned = scrub(sql_part)
                create_head = " ".join(token.upper() for token in tokens[:5])
                if not re.match(r"^CREATE(?: OR REPLACE)?(?: TEMPORARY)? TABLE\b", create_head):
                    continue
                try:
                    parsed = parse_tables(cleaned)
                    if len(parsed) != 1:
                        raise ProofError("unsupported CREATE TABLE declaration")
                except ProofError as exc:
                    problems.append((statement, str(exc)))
                    continue
                table = parsed[0]
                table_entries.append((statement, table, sql_part))
                if table.name in tables:
                    problems.append((statement, "duplicate table declaration '{0}'".format(table.name)))
                tables[table.name] = set(table.column_names())
            if collection is read_statements and not has_statement:
                problems.append((Statement(path, sql, 0, []), "no read query found"))

    aggregates = {table.name for _, table, _ in table_entries if aggregate_engine(table)}
    writers = collect_writers(statements, aggregates, tables, problems)
    queries = {name: [] for name in aggregates}
    for statement in read_statements:
        try:
            target, equal, constrained = read_predicates(statement, tables)
            if target in aggregates:
                queries[target].append((statement, equal, constrained))
        except ProofError as exc:
            problems.append((statement, str(exc)))

    for statement, table, sql_part in table_entries:
        all_findings.extend(check_table(statement, sql_part, table, tenant_columns, args.single_tenant))
        if aggregate_engine(table):
            all_findings.extend(check_aggregate(statement, table, writers[table.name],
                                                queries[table.name], tables, problems))

    for statement, message in problems:
        print("{0}: CH011 {1}".format(statement.location(), message), file=sys.stderr)

    for finding in all_findings:
        print(finding.render())

    print("")
    print("{0} file(s), {1} table(s) checked, {2} finding(s)".format(
        len(args.paths), len(table_entries), len(all_findings)))
    print("")
    sys.stdout.write(CANNOT_CHECK)
    if problems:
        return 2
    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

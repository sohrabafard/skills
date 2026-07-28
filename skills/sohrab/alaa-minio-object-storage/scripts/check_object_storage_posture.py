#!/usr/bin/env python3
"""Static posture checker for an object-storage consumer repository.

Eight checks, each of which corresponds to a constraint in this skill's SKILL.md
and each of which is decidable from the repository text alone:

  ROOT_CREDENTIAL_SHARED    the application's access or secret key is drawn from
                            the same variable as the store's root credential
  PLAINTEXT_ENDPOINT        an object-storage endpoint uses http:// against a
                            host that is not a loopback address, or TLS is
                            explicitly disabled in a file that names such an
                            endpoint
  CREDENTIAL_LITERAL        a storage credential key is assigned a literal value
                            rather than a variable reference
  LIFECYCLE_RULE_ABSENT     no lifecycle declaration appears anywhere in the
                            scanned files, so nothing aborts incomplete
                            multipart uploads
  MC_CREDENTIAL_ON_COMMAND_LINE
                            an `mc` invocation passes an access key or a secret
                            key as a positional argument, so the plaintext
                            credential lands in that process's argv
  VERSIONING_WITHOUT_NONCURRENT_RULE
                            the repository declares bucket versioning and
                            declares no noncurrent-version expiration rule, so
                            superseded versions accumulate without bound
  PROVIDER_PROFILE_WITHOUT_PINNED_VALUES
                            the repository names a provider profile and does not
                            pin one of the four values no profile supplies -
                            endpoint, bucket, access key, secret key - so the
                            profile is read as covering more than it does
  ADDRESSING_STYLE_CONTRADICTS_ENDPOINT
                            the declared addressing style contradicts the shape
                            the endpoint or the bucket name will produce: path
                            style against an endpoint whose host already carries
                            the bucket, or virtual-hosted style with a dotted
                            bucket name that no wildcard certificate matches

The checker is lexical. It parses `KEY: value` and `KEY=value` assignments at the
start of a line and never evaluates YAML, never expands a variable against a real
environment, and never contacts an object store. A clean run proves what the
repository declares; it proves nothing about how the running bucket is actually
configured.

Three deliberate scope limits, each stated so a clean run is not read as more
than it is:

  - Files matched by a literal, wildcard-free entry in the repository root's
    .gitignore are skipped, because a value in an untracked local file is not a
    repository leak. A file that .gitignore names but git still tracks is missed
    by this rule; a secret scanner over the tracked tree is the control for that.
  - Test files and testdata directories are skipped for CREDENTIAL_LITERAL,
    because a fixture credential is a fake by construction and flagging it trains
    the reader to ignore the rule. A real credential in a test file is a secret
    scanner's finding, not this checker's.
  - The TLS check considers only keys naming object storage, so a disabled TLS
    flag belonging to another dependency is that dependency's finding.
  - MC_CREDENTIAL_ON_COMMAND_LINE recognises three `mc` command families only:
    `mc alias set`, the older `mc config host add`, and `mc admin user add`. A
    credential passed on the command line of any other program is out of scope
    and a clean run says nothing about it.
  - MC_CREDENTIAL_ON_COMMAND_LINE is not skipped in test files, because the
    defect is the shape of the invocation rather than the secrecy of the value,
    and a shape copied out of a smoke script into a provisioner is how it
    spreads.
  - PROVIDER_PROFILE_WITHOUT_PINNED_VALUES and
    ADDRESSING_STYLE_CONTRADICTS_ENDPOINT read the same uppercase `KEY: value`
    and `KEY=value` assignments as every other check, so a lowercase YAML or
    JSON spelling of the same setting is missed. A repository that configures
    addressing style only inside code, without an environment key, is out of
    scope and a clean run says nothing about it.
  - ADDRESSING_STYLE_CONTRADICTS_ENDPOINT compares literals only. A bucket name
    or an endpoint that stays a variable reference is skipped rather than
    guessed, because the value is decided outside the repository.
  - VERSIONING_WITHOUT_NONCURRENT_RULE matches the API and CLI spellings that
    *enable* versioning, so a repository that only reads versioning state does
    not fire it. A repository that enables versioning through a spelling not in
    the list is missed; the list is in VERSIONING_ENABLED_TOKENS and extending
    it is the fix.
"""

import argparse
import os
import re
import shutil
import sys
import tempfile

VERSION = "1.1.0"

ROOT_CREDENTIAL_KEYS = {
    "MINIO_ROOT_USER",
    "MINIO_ROOT_PASSWORD",
    "MINIO_ADMIN_USER",
    "MINIO_ADMIN_PASSWORD",
}

APPLICATION_CREDENTIAL_KEYS = {
    "STORAGE_ACCESS_KEY",
    "STORAGE_SECRET_KEY",
    "S3_ACCESS_KEY",
    "S3_SECRET_KEY",
    "S3_ACCESS_KEY_ID",
    "S3_SECRET_ACCESS_KEY",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
}

CREDENTIAL_KEYS = ROOT_CREDENTIAL_KEYS | APPLICATION_CREDENTIAL_KEYS

ENDPOINT_KEYS = {
    "STORAGE_ENDPOINT",
    "S3_ENDPOINT",
    "MINIO_ENDPOINT",
    "AWS_ENDPOINT_URL",
    "AWS_ENDPOINT_URL_S3",
    "OBJECT_STORAGE_ENDPOINT",
}

TLS_KEY_TOKENS = ("TLS_ENABLED", "USE_SSL", "SSL_ENABLED", "USE_TLS")

# A provider profile supplies defaults and nothing else, so the four values no
# profile can supply have to be pinned wherever a profile is named.
PROVIDER_PROFILE_KEYS = ("STORAGE_PROVIDER_PROFILE", "STORAGE_PROVIDER")
PROFILE_UNCOVERED_KEYS = (
    "STORAGE_ENDPOINT",
    "STORAGE_BUCKET",
    "STORAGE_ACCESS_KEY",
    "STORAGE_SECRET_KEY",
)

BUCKET_KEYS = {"STORAGE_BUCKET", "S3_BUCKET", "MINIO_BUCKET", "OBJECT_STORAGE_BUCKET"}

PATH_STYLE_KEY_TOKENS = ("PATH_STYLE", "PATHSTYLE")

# A TLS flag is this checker's business only when its key names object storage.
STORAGE_KEY_TOKENS = ("STORAGE", "S3", "MINIO", "OBJECT")

FALSE_VALUES = {"false", "0", "no", "off", "disabled", "none"}

TRUE_VALUES = {"true", "1", "yes", "on", "enabled"}

LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]", "0.0.0.0"}

LIFECYCLE_TOKENS = (
    "AbortIncompleteMultipartUpload",
    "abort_incomplete_multipart_upload",
    "abort-incomplete-multipart-upload",
    "PutBucketLifecycleConfiguration",
    "put-bucket-lifecycle-configuration",
    "put_bucket_lifecycle_configuration",
    "LifecycleConfiguration",
    "DaysAfterInitiation",
    "days_after_initiation",
    "mc ilm",
    "aws s3api put-bucket-lifecycle",
)

VERSIONING_ENABLED_TOKENS = (
    "PutBucketVersioning",
    "put-bucket-versioning",
    "put_bucket_versioning",
    "VersioningConfiguration",
    "aws_s3_bucket_versioning",
    "SetBucketVersioning",
    "EnableVersioning",
    "mc version enable",
)

NONCURRENT_RULE_TOKENS = (
    "NoncurrentVersionExpiration",
    "noncurrent_version_expiration",
    "noncurrent-version-expiration",
    "NoncurrentVersionTransition",
    "NoncurrentDays",
    "noncurrent_days",
    "noncurrent-days",
    "noncurrent-expire-days",
)

# Positional-argument counts at which each family is carrying a credential:
# `mc alias set <alias> <endpoint> <access> <secret>` and
# `mc admin user add <alias> <access> <secret>`.
MC_CREDENTIAL_COMMANDS = (
    (re.compile(r"\bmc\s+alias\s+set\s+(.*)$"), "mc alias set", 4),
    (re.compile(r"\bmc\s+config\s+host\s+add\s+(.*)$"), "mc config host add", 4),
    (re.compile(r"\bmc\s+admin\s+user\s+add\s+(.*)$"), "mc admin user add", 3),
)

# A token that ends the positional run: a flag, a redirection, a pipeline or
# list operator, a comment, or a shell keyword closing the command.
MC_STOP_PREFIXES = ("-", "<", ">", "|", "&", ";", "#", "1>", "2>")
MC_STOP_WORDS = {"then", "fi", "do", "done", "else", "elif"}

SCANNED_SUFFIXES = {
    ".yml", ".yaml", ".env", ".sh", ".bash", ".tf", ".tfvars", ".json",
    ".tpl", ".conf", ".ini", ".properties", ".go", ".py", ".php", ".ts",
    ".js", ".rb", ".java", ".kt", ".cs", ".toml", ".hcl",
}

SCANNED_NAMES = {"Makefile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml"}

SKIPPED_DIRECTORIES = {
    ".git", ".hg", ".svn", "vendor", "node_modules", "__pycache__",
    ".gocache", ".gomodcache", ".venv", "venv", "dist", "build", ".idea",
    ".terraform", "target",
}

MAX_FILE_BYTES = 2 * 1024 * 1024

ASSIGNMENT_RE = re.compile(
    r"""^\s*(?:-\s*)?(?:export\s+)?["']?([A-Z][A-Z0-9_]{2,})["']?\s*(?::|=)\s*(.*?)\s*$"""
)
VARIABLE_RE = re.compile(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)")
DEFAULT_EXPANSION_RE = re.compile(r"^\$\{[^}:]*:[-=](.*)\}$")

OBLIGATIONS = {
    "ROOT_CREDENTIAL_SHARED":
        "Create a scoped storage identity, give the application its own access "
        "and secret key, and set the store's root credential to a value no "
        "application holds. See references/30-identity-credentials-and-access.md.",
    "PLAINTEXT_ENDPOINT":
        "Terminate TLS on the object store and set the endpoint scheme to https, "
        "or move the store onto the loopback interface of the calling process. "
        "See references/40-encryption-tls-and-durability.md.",
    "CREDENTIAL_LITERAL":
        "Replace the literal with a variable reference resolved from the "
        "orchestrator's secret store, and rotate the credential that was "
        "committed. See references/30-identity-credentials-and-access.md.",
    "LIFECYCLE_RULE_ABSENT":
        "Add a bucket lifecycle configuration containing an "
        "AbortIncompleteMultipartUpload rule with a stated maximum age, applied "
        "by the same mechanism that creates the bucket. See "
        "references/20-lifecycle-and-retention.md.",
    "MC_CREDENTIAL_ON_COMMAND_LINE":
        "Remove the access key and secret key from the mc command line and pass "
        "them in the environment, or write the alias configuration file with "
        "mode 0600 from the process that already holds the secret. Rotate any "
        "credential that reached a shell history or a published process list. "
        "See references/75-mc-command-line-client.md.",
    "PROVIDER_PROFILE_WITHOUT_PINNED_VALUES":
        "Set the endpoint, the bucket and both credentials explicitly in every "
        "environment that names a provider profile. A profile supplies defaults "
        "for the values that differ between providers and supplies none of "
        "these four, so a profile read as covering them points the service at "
        "whatever the process invented. See "
        "references/05-environment-contract.md.",
    "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT":
        "Set STORAGE_USE_PATH_STYLE to the style the endpoint and the bucket "
        "name can actually carry: virtual-hosted needs a bucket name that is a "
        "valid DNS label with no dot in it, and path style needs an endpoint "
        "host that does not already carry the bucket. See "
        "references/70-client-libraries.md under The addressing style.",
    "VERSIONING_WITHOUT_NONCURRENT_RULE":
        "Add a NoncurrentVersionExpiration rule, with a retention window stated "
        "against a recovery need, to the same lifecycle configuration in the "
        "same change that enables versioning. See "
        "references/20-lifecycle-and-retention.md.",
}


class Finding:
    def __init__(self, rule, path, line, detail):
        self.rule = rule
        self.path = path
        self.line = line
        self.detail = detail

    def render(self, root):
        try:
            shown = os.path.relpath(self.path, root) if self.path else "<repository>"
        except ValueError:
            shown = self.path
        location = f"{shown}:{self.line}" if self.line else shown
        return f"{self.rule} {location}: {self.detail}"


TEST_PATH_TOKENS = ("testdata", "fixtures", "__tests__")
TEST_NAME_RE = re.compile(r"(^test_|_test\.|\.test\.|Test\.[a-z]+$|_spec\.|\.spec\.)")


def is_test_path(path):
    """True for a path a repository uses only for tests.

    A fixture credential is a fake by construction, so reporting it as a leak
    trains the reader to ignore the rule that catches a real one.
    """
    parts = path.replace("\\", "/").split("/")
    if any(part in ("tests", "test") or part in TEST_PATH_TOKENS for part in parts):
        return True
    return bool(TEST_NAME_RE.search(parts[-1]))


def load_ignored(root):
    """Return literal, wildcard-free entries from the root .gitignore.

    A value sitting in an untracked local file is not a repository leak, and
    reporting it as one buries the findings that are. An entry containing a
    wildcard is skipped rather than approximated, because a wrong glob would
    silently suppress a real finding.
    """
    path = os.path.join(root, ".gitignore")
    entries = set()
    text = read_text(path)
    if text is None:
        return entries
    for line in text.splitlines():
        entry = line.strip()
        if not entry or entry.startswith("#") or entry.startswith("!"):
            continue
        if any(char in entry for char in "*?[]"):
            continue
        entries.add(entry.strip("/"))
    return entries


def is_scanned(path):
    name = os.path.basename(path)
    if name in SCANNED_NAMES:
        return True
    if name.startswith(".env"):
        return True
    return os.path.splitext(name)[1] in SCANNED_SUFFIXES


def collect_files(root, ignored=frozenset()):
    collected = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames if d not in SKIPPED_DIRECTORIES and d not in ignored
        )
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            relative = os.path.relpath(full, root).replace("\\", "/")
            if name in ignored or relative in ignored:
                continue
            if not is_scanned(full):
                continue
            try:
                if os.path.getsize(full) > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            collected.append(full)
    return collected


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return None


def strip_comment(value):
    """Remove a trailing shell or YAML comment from an unquoted value."""
    if value.startswith(("'", '"')):
        return value
    marker = value.find(" #")
    return value[:marker].strip() if marker >= 0 else value


def clean_value(raw):
    value = strip_comment(raw.strip())
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def effective_value(value):
    """Return the literal a value collapses to, or None when it stays a reference.

    `${A:-http://host}` collapses to its default; `${A}` and `${A:-${B}}` do not
    collapse to a literal and return None, because the real value is decided
    outside the file.
    """
    seen = 0
    current = value
    while current.startswith("$") and seen < 8:
        match = DEFAULT_EXPANSION_RE.match(current)
        if not match:
            return None
        current = match.group(1).strip()
        seen += 1
    return None if current.startswith("$") else current


def variable_names(value):
    return set(VARIABLE_RE.findall(value))


def assignments(text):
    for number, line in enumerate(text.splitlines(), start=1):
        match = ASSIGNMENT_RE.match(line)
        if match:
            yield number, match.group(1), clean_value(match.group(2))


def mc_positional_count(remainder):
    """Count the positional arguments an mc command carries before its flags.

    The run ends at the first flag, redirection, operator or shell keyword,
    because everything after that belongs to the shell rather than to mc.
    """
    count = 0
    for token in remainder.split():
        if token in MC_STOP_WORDS:
            break
        if token.startswith(MC_STOP_PREFIXES):
            break
        count += 1
    return count


def check_mc_command_lines(path, text):
    """Report every mc invocation carrying a credential in its argv.

    The shell expands the variable before mc starts, so a value passed
    positionally is readable in the process list and recorded in shell history
    whatever the script does with mc's output.
    """
    findings = []
    for number, line in enumerate(text.splitlines(), start=1):
        for pattern, label, threshold in MC_CREDENTIAL_COMMANDS:
            match = pattern.search(line)
            if not match:
                continue
            count = mc_positional_count(match.group(1))
            if count >= threshold:
                findings.append(Finding(
                    "MC_CREDENTIAL_ON_COMMAND_LINE", path, number,
                    f"{label} passes {count} positional arguments, so the "
                    "credential is in this process's argv",
                ))
    return findings


def endpoint_host(literal):
    match = re.match(r"^(https?)://([^/\s]+)", literal)
    if not match:
        return None, None
    scheme = match.group(1)
    host = match.group(2)
    if host.startswith("["):
        closing = host.find("]")
        host = host[: closing + 1] if closing >= 0 else host
    else:
        host = host.split(":")[0]
    return scheme, host


def collect_configuration(path, text, facts):
    """Record the repository-level facts the last two checks decide from.

    Both checks compare values written in different files, so neither can be
    decided while reading one file. Only literals are recorded; a value that
    stays a variable reference is skipped rather than guessed, because the value
    is chosen outside the repository.
    """
    for number, key, value in assignments(text):
        if key in PROVIDER_PROFILE_KEYS and facts["profile"] is None:
            facts["profile"] = (path, number, key, effective_value(value))
        if key in PROFILE_UNCOVERED_KEYS:
            facts["pinned"].add(key)
        if key in BUCKET_KEYS or key.endswith("_BUCKET") or key.endswith("_BUCKET_NAME"):
            literal = effective_value(value)
            if literal and not any(c in literal for c in "/${} "):
                facts["buckets"].append((path, number, literal))
        if any(token in key for token in PATH_STYLE_KEY_TOKENS):
            literal = effective_value(value)
            if literal is not None and literal.lower() in TRUE_VALUES | FALSE_VALUES:
                facts["path_style"].append(
                    (path, number, key, literal.lower() in TRUE_VALUES)
                )
        if key in ENDPOINT_KEYS or key.endswith("_ENDPOINT_URL"):
            literal = effective_value(value)
            if literal:
                _, host = endpoint_host(literal)
                if host:
                    facts["hosts"].append((path, number, key, host))


def check_provider_profile(facts):
    """Report a named profile whose uncovered values are pinned nowhere.

    A profile supplies a default for each value that differs between providers
    and supplies none of the endpoint, the bucket or the two credentials, so a
    repository that names a profile and pins none of those four is reading the
    profile as covering more than it does.
    """
    if facts["profile"] is None:
        return []
    path, number, key, value = facts["profile"]
    missing = [name for name in PROFILE_UNCOVERED_KEYS if name not in facts["pinned"]]
    if not missing:
        return []
    named = value if value else "a profile"
    return [Finding(
        "PROVIDER_PROFILE_WITHOUT_PINNED_VALUES", path, number,
        f"{key} names {named} and the repository pins "
        + ", ".join(missing)
        + " nowhere; a provider profile supplies no endpoint, bucket or credential",
    )]


def check_addressing_style(facts):
    """Report a declared addressing style the endpoint or the bucket cannot carry.

    Two forms are decidable from literals alone. Path style against an endpoint
    whose host already begins with the bucket name addresses the bucket twice,
    once in the host and once in the path, and the store answers not-found.
    Virtual-hosted style with a dotted bucket name puts one label too many in
    front of the wildcard certificate, so TLS fails for that bucket alone.
    """
    findings = []
    for path, number, key, uses_path_style in facts["path_style"]:
        if uses_path_style:
            for _, _, bucket in facts["buckets"]:
                for _, _, endpoint_key, host in facts["hosts"]:
                    if host.lower().startswith(bucket.lower() + "."):
                        findings.append(Finding(
                            "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", path, number,
                            f"{key} selects path style while {endpoint_key} host "
                            f"'{host}' already carries bucket '{bucket}', so the "
                            "bucket is addressed twice",
                        ))
                        break
                else:
                    continue
                break
        else:
            for _, _, bucket in facts["buckets"]:
                if "." in bucket:
                    findings.append(Finding(
                        "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", path, number,
                        f"{key} selects virtual-hosted style while bucket "
                        f"'{bucket}' contains a dot, so no wildcard certificate "
                        "matches the host it becomes",
                    ))
                    break
    return findings


def check_file(path, text):
    findings = check_mc_command_lines(path, text)
    root_variables = set()
    application_variables = set()
    root_literals = {}
    application_literals = {}
    first_root_line = None
    plaintext_endpoint_line = None

    parsed = list(assignments(text))

    for number, key, value in parsed:
        if key in ROOT_CREDENTIAL_KEYS:
            root_variables |= variable_names(value)
            first_root_line = first_root_line or number
            literal = effective_value(value)
            if literal:
                root_literals[literal] = number
        if key in APPLICATION_CREDENTIAL_KEYS:
            application_variables |= variable_names(value)
            literal = effective_value(value)
            if literal:
                application_literals[literal] = number

        if key in CREDENTIAL_KEYS and not is_test_path(path):
            literal = effective_value(value)
            if literal:
                findings.append(Finding(
                    "CREDENTIAL_LITERAL", path, number,
                    f"{key} is assigned a literal value instead of a variable reference",
                ))

        if key in ENDPOINT_KEYS or key.endswith("_ENDPOINT_URL"):
            literal = effective_value(value)
            if literal:
                scheme, host = endpoint_host(literal)
                if scheme == "http" and host and host not in LOOPBACK_HOSTS:
                    plaintext_endpoint_line = plaintext_endpoint_line or number
                    findings.append(Finding(
                        "PLAINTEXT_ENDPOINT", path, number,
                        f"{key} addresses non-loopback host '{host}' over http",
                    ))

    if plaintext_endpoint_line:
        for number, key, value in parsed:
            if not any(token in key for token in STORAGE_KEY_TOKENS):
                continue
            if any(token in key for token in TLS_KEY_TOKENS):
                literal = effective_value(value)
                if literal is not None and literal.lower() in FALSE_VALUES:
                    findings.append(Finding(
                        "PLAINTEXT_ENDPOINT", path, number,
                        f"{key} is disabled in a file that names a non-loopback endpoint",
                    ))

    shared_variables = root_variables & application_variables
    shared_literals = set(root_literals) & set(application_literals)
    if shared_variables:
        findings.append(Finding(
            "ROOT_CREDENTIAL_SHARED", path, first_root_line,
            "root and application credentials are drawn from the same variable(s): "
            + ", ".join(sorted(shared_variables)),
        ))
    elif shared_literals:
        findings.append(Finding(
            "ROOT_CREDENTIAL_SHARED", path, first_root_line,
            "root and application credentials resolve to the same literal value",
        ))

    return findings


def run(root):
    findings = []
    lifecycle_seen = False
    versioning_seen = False
    noncurrent_seen = False
    facts = {"profile": None, "pinned": set(), "buckets": [], "path_style": [], "hosts": []}
    for path in collect_files(root, load_ignored(root)):
        text = read_text(path)
        if text is None:
            continue
        if not lifecycle_seen and any(token in text for token in LIFECYCLE_TOKENS):
            lifecycle_seen = True
        if not versioning_seen and any(token in text for token in VERSIONING_ENABLED_TOKENS):
            versioning_seen = True
        if not noncurrent_seen and any(token in text for token in NONCURRENT_RULE_TOKENS):
            noncurrent_seen = True
        collect_configuration(path, text, facts)
        findings.extend(check_file(path, text))
    findings.extend(check_provider_profile(facts))
    findings.extend(check_addressing_style(facts))
    if not lifecycle_seen:
        findings.append(Finding(
            "LIFECYCLE_RULE_ABSENT", "", 0,
            "no lifecycle declaration appears in any scanned file, so nothing "
            "aborts incomplete multipart uploads",
        ))
    if versioning_seen and not noncurrent_seen:
        findings.append(Finding(
            "VERSIONING_WITHOUT_NONCURRENT_RULE", "", 0,
            "bucket versioning is declared and no noncurrent-version expiration "
            "rule is, so every superseded version stays billable forever",
        ))
    findings.sort(key=lambda f: (f.rule, f.path, f.line or 0))
    return findings


COMPOSE_BAD = """\
services:
  minio:
    image: minio/minio:RELEASE.2025-09-07T16-13-09Z-cpuv1
    environment:
      MINIO_ROOT_USER: ${STORAGE_ACCESS_KEY:-${MINIO_ROOT_USER}}
      MINIO_ROOT_PASSWORD: ${STORAGE_SECRET_KEY:-${MINIO_ROOT_PASSWORD}}
  app:
    environment:
      STORAGE_PROVIDER_PROFILE: arvancloud
      STORAGE_ENDPOINT: ${STORAGE_ENDPOINT:-http://svc-minio:9000}
      STORAGE_ACCESS_KEY: ${STORAGE_ACCESS_KEY:-${MINIO_ROOT_USER}}
      STORAGE_SECRET_KEY: ${STORAGE_SECRET_KEY:-${MINIO_ROOT_PASSWORD}}
"""

ENV_BAD = """\
STORAGE_ENDPOINT=http://svc-minio:9000
STORAGE_TLS_ENABLED=false
STORAGE_ACCESS_KEY=minioadmin
STORAGE_SECRET_KEY=
"""

COMPOSE_GOOD = """\
services:
  minio:
    image: minio/minio:RELEASE.2025-09-07T16-13-09Z-cpuv1
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
  app:
    environment:
      STORAGE_PROVIDER_PROFILE: minio
      STORAGE_ENDPOINT: ${STORAGE_ENDPOINT:-https://svc-minio:9000}
      STORAGE_BUCKET: ${STORAGE_BUCKET:-media-assets}
      STORAGE_USE_PATH_STYLE: ${STORAGE_USE_PATH_STYLE:-true}
      STORAGE_ACCESS_KEY: ${STORAGE_APP_ACCESS_KEY}
      STORAGE_SECRET_KEY: ${STORAGE_APP_SECRET_KEY}
"""

PROVISION_GOOD = """\
#!/bin/sh
set -eu
# The credential reaches mc in the environment, never in argv.
export MC_HOST_local="https://${STORAGE_APP_ACCESS_KEY}:${STORAGE_APP_SECRET_KEY}@${STORAGE_HOST}"
mc alias set local "${STORAGE_ENDPOINT}" --api S3v4 --json
mc mb -p --json "local/${STORAGE_BUCKET}"
mc version enable --json "local/${STORAGE_BUCKET}"
mc ilm import --json "local/${STORAGE_BUCKET}" < lifecycle.json
"""

LIFECYCLE_GOOD = """\
{
  "Rules": [
    {
      "ID": "abort-incomplete-multipart",
      "Status": "Enabled",
      "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 }
    },
    {
      "ID": "expire-noncurrent-versions",
      "Status": "Enabled",
      "NoncurrentVersionExpiration": { "NoncurrentDays": 30 }
    }
  ]
}
"""

PROVISION_BAD = """\
#!/bin/sh
mc alias set local "$STORAGE_ENDPOINT" "$STORAGE_ACCESS_KEY" "$STORAGE_SECRET_KEY" --api S3v4 >/dev/null 2>&1
mc mb -p "local/$STORAGE_BUCKET"
mc admin user add local "$SCOPED_ACCESS_KEY" "$SCOPED_SECRET_KEY"
mc version enable "local/$STORAGE_BUCKET"
"""

ENV_LOCAL_OK = """\
STORAGE_ENDPOINT=http://127.0.0.1:9000
STORAGE_TLS_ENABLED=false
RABBITMQ_TLS_ENABLED=false
STORAGE_ACCESS_KEY=${STORAGE_APP_ACCESS_KEY}
"""

GITIGNORE = """\
# Local env files
.env
"""

ENV_UNTRACKED = """\
STORAGE_ACCESS_KEY=a-real-looking-secret
STORAGE_SECRET_KEY=another-real-looking-secret
"""

ENV_DOTTED_BUCKET = """\
STORAGE_PROVIDER_PROFILE=arvancloud
STORAGE_ENDPOINT=https://s3.ir-thr-at1.arvanstorage.ir
STORAGE_BUCKET=media.assets
STORAGE_USE_PATH_STYLE=false
STORAGE_ACCESS_KEY=${STORAGE_APP_ACCESS_KEY}
STORAGE_SECRET_KEY=${STORAGE_APP_SECRET_KEY}
"""

ENV_BUCKET_IN_HOST = """\
STORAGE_PROVIDER_PROFILE=arvancloud
STORAGE_ENDPOINT=https://media-assets.s3.ir-thr-at1.arvanstorage.ir
STORAGE_BUCKET=media-assets
STORAGE_USE_PATH_STYLE=true
STORAGE_ACCESS_KEY=${STORAGE_APP_ACCESS_KEY}
STORAGE_SECRET_KEY=${STORAGE_APP_SECRET_KEY}
"""

TEST_FIXTURE_GO = """\
package storage

var env = map[string]string{
	"STORAGE_ACCESS_KEY": "fixture-key",
	"STORAGE_SECRET_KEY": "fixture-secret",
}
"""


def is_scanned_in(root, relative):
    """True when `relative` survives collection under `root`, ignore rules applied."""
    target = os.path.join(root, relative)
    return target in collect_files(root, load_ignored(root))


def write_fixture(base, name, files):
    directory = os.path.join(base, name)
    os.makedirs(directory, exist_ok=True)
    for relative, content in files.items():
        target = os.path.join(directory, relative)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(content)
    return directory


def self_test():
    """Build fixtures outside any repository and assert the rules that fire."""
    base = tempfile.mkdtemp(prefix="object-storage-posture-selftest-")
    failures = []
    try:
        bad = write_fixture(base, "bad", {
            "docker-compose.yml": COMPOSE_BAD,
            ".env.example": ENV_BAD,
            "scripts/provision.sh": PROVISION_BAD,
        })
        good = write_fixture(base, "good", {
            "docker-compose.yml": COMPOSE_GOOD,
            "scripts/provision.sh": PROVISION_GOOD,
            "scripts/lifecycle.json": LIFECYCLE_GOOD,
            ".env.example": ENV_LOCAL_OK,
            ".gitignore": GITIGNORE,
            ".env": ENV_UNTRACKED,
            "internal/storage/s3_test.go": TEST_FIXTURE_GO,
        })
        dotted = write_fixture(base, "dotted", {".env.example": ENV_DOTTED_BUCKET})
        in_host = write_fixture(base, "in-host", {".env.example": ENV_BUCKET_IN_HOST})

        cases = [
            ("bad fixture fires ROOT_CREDENTIAL_SHARED", bad, "ROOT_CREDENTIAL_SHARED", True),
            ("bad fixture fires PLAINTEXT_ENDPOINT", bad, "PLAINTEXT_ENDPOINT", True),
            ("bad fixture fires CREDENTIAL_LITERAL", bad, "CREDENTIAL_LITERAL", True),
            ("bad fixture fires LIFECYCLE_RULE_ABSENT", bad, "LIFECYCLE_RULE_ABSENT", True),
            ("bad fixture fires MC_CREDENTIAL_ON_COMMAND_LINE", bad,
             "MC_CREDENTIAL_ON_COMMAND_LINE", True),
            ("bad fixture fires VERSIONING_WITHOUT_NONCURRENT_RULE", bad,
             "VERSIONING_WITHOUT_NONCURRENT_RULE", True),
            ("good fixture clears ROOT_CREDENTIAL_SHARED", good, "ROOT_CREDENTIAL_SHARED", False),
            ("good fixture clears PLAINTEXT_ENDPOINT", good, "PLAINTEXT_ENDPOINT", False),
            ("good fixture clears CREDENTIAL_LITERAL", good, "CREDENTIAL_LITERAL", False),
            ("good fixture clears LIFECYCLE_RULE_ABSENT", good, "LIFECYCLE_RULE_ABSENT", False),
            ("good fixture clears MC_CREDENTIAL_ON_COMMAND_LINE", good,
             "MC_CREDENTIAL_ON_COMMAND_LINE", False),
            ("good fixture clears VERSIONING_WITHOUT_NONCURRENT_RULE", good,
             "VERSIONING_WITHOUT_NONCURRENT_RULE", False),
            ("bad fixture fires PROVIDER_PROFILE_WITHOUT_PINNED_VALUES", bad,
             "PROVIDER_PROFILE_WITHOUT_PINNED_VALUES", True),
            ("good fixture clears PROVIDER_PROFILE_WITHOUT_PINNED_VALUES", good,
             "PROVIDER_PROFILE_WITHOUT_PINNED_VALUES", False),
            ("a dotted bucket under virtual-hosted style fires "
             "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", dotted,
             "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", True),
            ("a bucket already in the endpoint host under path style fires "
             "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", in_host,
             "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", True),
            ("good fixture clears ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", good,
             "ADDRESSING_STYLE_CONTRADICTS_ENDPOINT", False),
            ("a dotted bucket is not also a profile finding", dotted,
             "PROVIDER_PROFILE_WITHOUT_PINNED_VALUES", False),
        ]
        results = {}
        for label, directory, rule, expected in cases:
            if directory not in results:
                results[directory] = {f.rule for f in run(directory)}
            fired = rule in results[directory]
            status = "ok" if fired == expected else "FAILED"
            if fired != expected:
                failures.append(label)
            print(f"[{status}] {label}")

        loopback_only = {f.rule for f in run(good)}
        expected_clean = loopback_only == set()
        print(f"[{'ok' if expected_clean else 'FAILED'}] good fixture produces no finding at all")
        if not expected_clean:
            failures.append("good fixture produces no finding at all")

        detail = [f for f in run(bad) if f.rule == "CREDENTIAL_LITERAL"]
        one_literal = len(detail) == 1 and detail[0].line == 3
        print(f"[{'ok' if one_literal else 'FAILED'}] literal credential is reported once, at its line")
        if not one_literal:
            failures.append("literal credential is reported once, at its line")

        mc_findings = [f for f in run(bad) if f.rule == "MC_CREDENTIAL_ON_COMMAND_LINE"]
        both_families = (
            len(mc_findings) == 2
            and any("mc alias set" in f.detail for f in mc_findings)
            and any("mc admin user add" in f.detail for f in mc_findings)
        )
        print(f"[{'ok' if both_families else 'FAILED'}] both mc credential families "
              "are reported, once each")
        if not both_families:
            failures.append("both mc credential families are reported, once each")

        # An alias configured without a credential carries two positionals, so the
        # threshold must not fire on it; a flag must end the run.
        below_threshold = mc_positional_count('local "${STORAGE_ENDPOINT}" --api S3v4 --json') == 2
        print(f"[{'ok' if below_threshold else 'FAILED'}] a credential-free mc alias set "
              "is below the threshold")
        if not below_threshold:
            failures.append("a credential-free mc alias set is below the threshold")

        # Versioning alone fires; versioning paired with a noncurrent rule does not.
        # The good fixture proves the paired case above, because it enables
        # versioning in scripts/provision.sh and carries NoncurrentVersionExpiration
        # in scripts/lifecycle.json and still produces no finding at all.

        # The good fixture also proves the three scope limits, because it contains
        # a gitignored .env with literal credentials, a Go test fixture with
        # literal credentials, and a non-storage TLS flag set false, and still
        # produces no finding above.
        for label, ok in [
            ("gitignored file is not scanned", not is_scanned_in(good, ".env")),
            ("test file is excluded from CREDENTIAL_LITERAL",
             is_test_path("internal/storage/s3_test.go")),
            ("non-storage TLS key is not a storage finding",
             not any(token in "RABBITMQ_TLS_ENABLED" for token in STORAGE_KEY_TOKENS)),
        ]:
            print(f"[{'ok' if ok else 'FAILED'}] {label}")
            if not ok:
                failures.append(label)
    finally:
        shutil.rmtree(base, ignore_errors=True)

    if failures:
        print(f"\nself-test FAILED: {len(failures)} case(s)")
        return 3
    print("\nself-test passed")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="check_object_storage_posture.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exit codes:\n"
            "  0  no finding; continue to the service's own tests\n"
            "  1  findings printed; fix each one or record it as an accepted defect\n"
            "     with an owner and a date before shipping\n"
            "  2  bad arguments or an unreadable root; nothing was checked\n"
            "  3  --self-test failed; the checker's verdicts are untrustworthy\n"
        ),
    )
    parser.add_argument("--root", help="repository root to check")
    parser.add_argument("--self-test", action="store_true",
                        help="run the checker against its own fixtures and exit")
    parser.add_argument("--version", action="version", version=VERSION)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.root:
        print("error: --root is required unless --self-test is given", file=sys.stderr)
        return 2
    if not os.path.isdir(args.root):
        print(f"error: not a directory: {args.root}", file=sys.stderr)
        return 2

    root = os.path.abspath(args.root)
    findings = run(root)
    if not findings:
        print(f"No finding in {root}.")
        print("This is a static result: it proves what the repository declares, "
              "not how the running bucket is configured.")
        return 0

    print(f"{len(findings)} finding(s) in {root}:\n")
    for finding in findings:
        print("  " + finding.render(root))
    print("\nObligations:")
    for rule in sorted({f.rule for f in findings}):
        print(f"  {rule}: {OBLIGATIONS[rule]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

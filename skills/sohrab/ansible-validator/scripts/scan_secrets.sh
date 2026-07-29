#!/usr/bin/env bash
#
# scan_secrets.sh - detect credential shapes that Checkov's ansible framework
# does not model, and do not report a correctly vaulted or indirected value.
#
# Division of labour with Checkov, stated once here and once in
# references/security_checklist.md:
#   checkov --framework secrets   catches generic credential shapes: AWS keys,
#                                 private-key blocks, high-entropy literals.
#   checkov --framework ansible   catches TLS, HTTPS and GPG policy only. It
#                                 found zero of the six secrets planted in
#                                 test/fixtures/secrets/planted-secrets.yml on
#                                 2026-07-29; --framework secrets found all six.
#   this script                   catches the Ansible-specific shapes neither
#                                 framework models: a var name that reads as a
#                                 credential, a DSN with an inline password, and
#                                 the absence of vault indirection.
#
# Requires bash 4.0 or newer. Exit codes: 0 clean, 1 findings, 2 could not run,
# 64 usage error.

set -uo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

av_print_help() {
    cat <<'EOF'
scan_secrets.sh - scan Ansible YAML for hardcoded credentials.

Usage:
  bash scripts/scan_secrets.sh <playbook.yml|role-dir|directory> [options]
  bash scripts/scan_secrets.sh --self-test

What it asserts:
  No line in scope assigns a literal value to a key whose name reads as a
  credential, and no line contains a private-key block, an AWS access key ID,
  or a database DSN with an inline password.

What it deliberately does not report:
  A value that is a Jinja expression ({{ ... }}), a reference to a vault_-
  prefixed variable, an inline !vault block, or a lookup() call. Those are the
  correct patterns. A scanner that red-lights the correct pattern gets switched
  off, so this filter applies to every pattern, not only to the password one.
  Pass --no-allow-vaulted to report them anyway when auditing whether the
  indirection resolves.

Extended regular expressions are used throughout (grep -E). The pre-repair
version wrote extended syntax and called basic grep, so AKIA[A-Z0-9]{16}
matched a literal "{16}" and the single highest-signal credential shape in the
list was undetectable.

Additional options:
      --no-allow-vaulted        Report vaulted and Jinja-indirected values too.

EOF
    av_common_flag_help
}

ALLOW_VAULTED=1

run_self_test() {
    local here="$0" fx
    fx="$(av_fixture_dir)"
    echo "self-test: scan_secrets.sh"
    av_expect_exit 64 "no argument is a usage error" bash "$here"
    av_expect_exit 0  "--help exits clean" bash "$here" --help
    av_expect_exit 2  "missing target cannot run" bash "$here" "$fx/fixtures/secrets/no-such-file.yml"
    av_expect_exit 1  "all six planted secrets are found" bash "$here" "$fx/fixtures/secrets/planted-secrets.yml"
    av_expect_exit 0  "a correctly vaulted playbook is not red-lighted" bash "$here" "$fx/fixtures/secrets/vaulted-clean.yml"

    # Named-shape assertions. The exit code alone would not prove that the AWS
    # key ID is detected, because five other findings would carry the exit.
    echo ""
    echo "  named-shape assertions against planted-secrets.yml:"
    local out
    out="$(NO_COLOR=1 bash "$here" "$fx/fixtures/secrets/planted-secrets.yml" 2>&1 || true)"
    local shape
    for shape in \
        "hardcoded password" \
        "AWS access key ID" \
        "AWS secret access key" \
        "API token" \
        "database connection string" \
        "private key block"; do
        if printf '%s' "$out" | grep -qi -- "$shape"; then
            printf "  %bok%b   %s reported\n" "$COLOR_GREEN" "$COLOR_RESET" "$shape"
            AV_ST_PASS=$((AV_ST_PASS + 1))
        else
            printf "  %bFAIL%b %s NOT reported\n" "$COLOR_RED" "$COLOR_RESET" "$shape"
            AV_ST_FAIL=$((AV_ST_FAIL + 1))
        fi
    done
    av_self_test_summary
}

# --- argument handling -----------------------------------------------------
ARGS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --no-allow-vaulted) ALLOW_VAULTED=0; shift ;;
        *) ARGS+=("$1"); shift ;;
    esac
done
av_parse_common_flags ${ARGS+"${ARGS[@]}"}

if [ "$AV_SELF_TEST" -eq 1 ]; then
    run_self_test
fi

if [ "${#AV_ARGS[@]}" -lt 1 ]; then
    av_usage_error "a file or directory to scan is required"
fi

TARGET="${AV_ARGS[0]}"

if [ -f "$TARGET" ]; then
    TARGET_ABS="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"
    SCAN_TYPE=file
elif [ -d "$TARGET" ]; then
    TARGET_ABS="$(cd "$TARGET" && pwd)"
    SCAN_TYPE=directory
else
    av_cannot_run "target not found: $TARGET"
fi

command -v grep >/dev/null 2>&1 || av_cannot_run "grep is not on PATH"

if [ "$AV_FORMAT" = "text" ]; then
    av_banner "Ansible Hardcoded Secret Scan"
    echo "Target: $TARGET_ABS"
    echo ""
fi

# A value is indirected, and therefore correct, when it is a Jinja expression,
# a vault_-prefixed variable, an inline !vault block, or a lookup() call.
INDIRECTION_RE='(\{\{|!vault|\$ANSIBLE_VAULT|vault_|lookup\()'

scan() {
    # scan <extended-regex> <human description> <ERROR|WARNING>
    local pattern="$1" description="$2" severity="$3" results=""

    if [ "$SCAN_TYPE" = file ]; then
        results="$(grep -n -i -E -- "$pattern" "$TARGET_ABS" 2>/dev/null || true)"
    else
        results="$(grep -r -n -i -E --include='*.yml' --include='*.yaml' -- "$pattern" "$TARGET_ABS" 2>/dev/null \
            | grep -v '/\.git/' || true)"
    fi

    # Drop commented lines and indirected values before deciding.
    if [ -n "$results" ]; then
        results="$(printf '%s\n' "$results" | grep -v -E '^[^:]*:[0-9]+: *#' || true)"
    fi
    if [ -n "$results" ] && [ "$ALLOW_VAULTED" -eq 1 ]; then
        results="$(printf '%s\n' "$results" | grep -v -E -- "$INDIRECTION_RE" || true)"
    fi

    [ -n "$results" ] || return 0

    if [ "$severity" = ERROR ]; then
        av_add_error "$description" "references/security_checklist.md"
    else
        av_add_warning "$description" "references/security_checklist.md"
    fi
    if [ "$AV_FORMAT" = "text" ]; then
        printf '%s\n' "$results" | while IFS= read -r line; do
            echo "    $line"
        done
    fi
}

# --- credential-shaped keys assigned a literal -----------------------------
# Each pattern anchors on the whole key name, so db_password, admin_password and
# mysql_root_password all match the password shape. A key name that ends in a
# credential word is a credential regardless of its prefix.
scan '^ *-? *[a-z0-9_]*(password|passwd|passphrase): *["'"'"']?[^ "'"'"'#{]' "hardcoded password" ERROR
scan '^ *-? *[a-z0-9_]*(api_?key|secret_key|client_secret|secret): *["'"'"']?[^ "'"'"'#{]' "hardcoded API key or client secret" ERROR
scan '^ *-? *[a-z0-9_]*token: *["'"'"']?[^ "'"'"'#{]' "hardcoded API token" ERROR
scan '^ *-? *[a-z0-9_]*private_key: *["'"'"']?[^ "'"'"'#{|>]' "hardcoded private key value" ERROR
scan '^ *-? *ansible_(ssh_pass|become_pass|password): *["'"'"']?[^ "'"'"'#{]' "hardcoded Ansible connection password" ERROR

# --- AWS credentials --------------------------------------------------------
# Both of these need extended regular expressions. Under basic grep the first
# matches a literal '?' and the second a literal '{16}'.
scan 'aws_access_key_id: *["'"'"']?[A-Z0-9]{16,}' "hardcoded AWS access key ID assigned to a variable" ERROR
scan '(^|[^A-Z0-9])AKIA[A-Z0-9]{16}([^A-Z0-9]|$)' "AWS access key ID shape (AKIA + 16 characters) present in the file" ERROR
scan 'aws_secret_access_key: *["'"'"']?[A-Za-z0-9/+=]{20,}' "hardcoded AWS secret access key" ERROR

# --- connection strings -----------------------------------------------------
scan '(mysql|postgres|postgresql|mongodb|redis|amqp)(\+[a-z]+)?://[^ :/]+:[^ @]+@' "database connection string with an inline password" ERROR

# --- key material -----------------------------------------------------------
scan '-----BEGIN (RSA |OPENSSH |EC |DSA |PGP |ENCRYPTED )?PRIVATE KEY-----' "private key block embedded in the file" ERROR

# --- lower-confidence shapes ------------------------------------------------
scan '^ *-? *(credentials|creds): *["'"'"']?[^ "'"'"'#{]' "value named credentials assigned a literal" WARNING

if [ "$AV_FORMAT" = "text" ] && [ $AV_ERRORS -gt 0 ]; then
    cat <<'EOF'

Remediation, in the order to try them:
  1. ansible-vault encrypt_string 'value' --name 'variable_name'
     and reference the variable, not the literal.
  2. "{{ lookup('env', 'DB_PASSWORD') }}" when the value reaches the control
     node as an environment variable from the CI job.
  3. "{{ lookup('community.hashi_vault.hashi_vault', 'secret=...') }}" when an
     external secret store owns it.
  4. Set no_log: true on the task, so the value does not reach the log even
     when the task fails. references/security_checklist.md states the exact
     condition under which no_log is required.

Whether a finding here blocks the run is not this skill's decision:
/alaa-security-review ($alaa-security-review) owns fail-closed. A secret-scan
finding is fail-closed by default, because proceeding with a leaked credential
lets something through that must not get through.
EOF
fi

av_summary "scan_secrets" "$TARGET_ABS"
exit $?

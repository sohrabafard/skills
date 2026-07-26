#!/bin/sh
# check-ci-determinism.sh - lexical determinism checks over a CI configuration.
# POSIX sh; no dependencies beyond grep, sed and mktemp.
set -u

PROG="check-ci-determinism.sh"
FIND=""
DELEGATED=0
SCANNED=0

usage() {
    cat <<'USAGE'
check-ci-determinism.sh [--repo DIR] [--self-test] [--help] [FILE...]

Checks a CI configuration for determinism and disguised-gate defects. It reads
lines, not the YAML tree: a clean exit means no finding at the lexical level,
never that the pipeline is deterministic.

  IMAGE      a job or service image whose tag does not name a major and a minor
  CACHEKEY   a cache block whose key is not derived from a lockfile hash
  TOOLCHAIN  a PHP or Composer version in CI that disagrees with composer.json
  NOTAGATE   a step that cannot fail the pipeline: allow_failure,
             continue-on-error, "|| true", "|| exit 0"
  RETRY      a retry declared as a bare count, which retries assertion failures

Options
  --repo DIR    root to scan (default: .). Discovers .gitlab-ci.yml and
                .github/workflows/*.yml|*.yaml when no FILE is given.
  --self-test   run built-in fixtures and verify each check fires. Exit 1 means
                this script is broken; fix it before trusting a clean run.
  --help        this text.

Exit codes, and what each obliges (see references/10-gate-register.md)
  0  no finding. Report the determinism claim as static proof, nothing stronger.
  1  findings printed. Fix each, or record it in the repository's deviation
     register, before calling the change done. A finding is not a warning.
  2  usage error. Re-invoke correctly; never report this as a pass.
  3  no CI configuration found. Report that the check did not run.
  4  every file scanned only includes configuration from elsewhere. Re-run in
     the repository owning the included file; report both results.
USAGE
}

report() { printf '%s\t%s\t%s\n' "$1" "$2" "$3" >>"$FIND"; }

# --- IMAGE ------------------------------------------------------------------
check_images() {
    f="$1"
    grep -nE '^[[:space:]]*(-[[:space:]]+)?(name|image):[[:space:]]*[^[:space:]]' "$f" 2>/dev/null |
    while IFS= read -r hit; do
        n=${hit%%:*}
        key=$(printf '%s' "$hit" | sed -e 's/^[0-9]*://' -e 's/^[[:space:]]*-\{0,1\}[[:space:]]*//' -e 's/:.*$//')
        if [ "$key" = "name" ]; then
            # a bare "name:" is an image only inside services:; elsewhere it is a
            # step, environment or workflow name.
            start=$((n - 20)); [ "$start" -lt 1 ] && start=1
            sed -n "${start},${n}p" "$f" | grep -qE '^[[:space:]]*services:' || continue
        fi
        ref=$(printf '%s' "$hit" | sed -e 's/^[0-9]*://' -e 's/^[[:space:]]*-\{0,1\}[[:space:]]*//' \
            -e 's/^\(name\|image\):[[:space:]]*//' -e 's/[[:space:]]*#.*$//' \
            -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'\$//" -e 's/[[:space:]]*$//')
        case "$ref" in
            ''|'|'*|'>'*|\**|\&*) continue ;;
            *'$'*) report IMAGE "$f:$n" "image goes through a variable ($ref); pin it where the variable is set"; continue ;;
            *@sha256:*) continue ;;
            *[!A-Za-z0-9._:/@+-]*) continue ;;
        esac
        tag=${ref##*:}
        if [ "$tag" = "$ref" ]; then tag=""; else case "$tag" in */*) tag="" ;; esac; fi
        if [ -z "$tag" ]; then
            report IMAGE "$f:$n" "no tag on $ref; resolves to a different image on every rebuild"
        elif echo "$tag" | grep -qE '^v?[0-9]+\.[0-9]+'; then
            :
        elif echo "$tag" | grep -qE '^v?[0-9]+([-_]|$)'; then
            report IMAGE "$f:$n" "tag $tag names only a major; the minor floats, so a rebuild can change behaviour with no review"
        else
            report IMAGE "$f:$n" "tag $tag names no version"
        fi
    done
}

# --- CACHEKEY ---------------------------------------------------------------
check_cache_keys() {
    f="$1"
    grep -nE '^[[:space:]]*(cache:|-[[:space:]]*uses:[[:space:]]*actions/cache)' "$f" 2>/dev/null |
    while IFS= read -r hit; do
        n=${hit%%:*}
        end=$((n + 12))
        window=$(sed -n "${n},${end}p" "$f")
        if echo "$window" | grep -qE 'composer\.lock|package-lock\.json|yarn\.lock|pnpm-lock\.yaml|go\.sum|Cargo\.lock|hashFiles\('; then
            :
        else
            report CACHEKEY "$f:$n" "cache key not derived from a lockfile hash; a cross-version cache survives a dependency change"
        fi
    done
}

# --- NOTAGATE / RETRY -------------------------------------------------------
check_gates() {
    f="$1"
    grep -nE 'allow_failure:[[:space:]]*true|continue-on-error:[[:space:]]*true|\|\|[[:space:]]*true|\|\|[[:space:]]*exit[[:space:]]+0' "$f" 2>/dev/null |
    while IFS= read -r hit; do
        n=${hit%%:*}
        report NOTAGATE "$f:$n" "cannot fail the pipeline; classify it as advisory in the gate register, or remove the escape"
    done
    grep -nE '^[[:space:]]*retry:[[:space:]]*[0-9]' "$f" 2>/dev/null |
    while IFS= read -r hit; do
        n=${hit%%:*}
        report RETRY "$f:$n" "bare-count retry also retries assertion failures; scope it to named infrastructure classes"
    done
}

# --- TOOLCHAIN --------------------------------------------------------------
# One repository, one PHP minor and one Composer version across manifest, CI and image.
check_toolchain() {
    repo="$1"; shift
    [ -f "$repo/composer.json" ] || return 0
    want=$(grep -E '"php"[[:space:]]*:' "$repo/composer.json" | head -1 |
        sed -e 's/.*"php"[[:space:]]*:[[:space:]]*"//' -e 's/".*//' |
        grep -oE '[0-9]+\.[0-9]+' | head -1)
    [ -n "${want:-}" ] || return 0
    for f in "$@" "$repo/Dockerfile"; do
        [ -f "$f" ] || continue
        grep -noE '(php:|PHP_VERSION[^0-9]{0,4}|php-version:[[:space:]]*.?)[0-9]+\.[0-9]+' "$f" 2>/dev/null |
        while IFS= read -r hit; do
            n=${hit%%:*}
            got=$(printf '%s' "$hit" | grep -oE '[0-9]+\.[0-9]+$')
            [ "$got" = "$want" ] || report TOOLCHAIN "$f:$n" \
                "PHP $got here, composer.json wants $want; the pipeline proves a combination that never ships"
        done
    done
    seen=""
    for f in "$@" "$repo/Dockerfile"; do
        [ -f "$f" ] || continue
        for v in $(grep -hoE '(composer:|COMPOSER_VERSION[^0-9]{0,4})[0-9]+\.[0-9]+(\.[0-9]+)?' "$f" 2>/dev/null |
                   grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | sort -u); do
            case " $seen " in *" $v "*) ;; *) seen="$seen $v" ;; esac
        done
    done
    set -- $seen
    [ "$#" -le 1 ] || report TOOLCHAIN "$repo" \
        "more than one Composer version pinned:$seen; bump them in one change"
}

# --- driver -----------------------------------------------------------------
scan_file() {
    f="$1"
    SCANNED=$((SCANNED + 1))
    if grep -qE '^[[:space:]]*include:' "$f" && ! grep -qE '^[[:space:]]*(-[[:space:]]*run:|script:|- script:)' "$f"; then
        DELEGATED=$((DELEGATED + 1))
        printf 'note\t%s\tincludes configuration this script cannot resolve; scan the including repository too\n' "$f" >>"$FIND"
    fi
    check_images "$f"
    check_cache_keys "$f"
    check_gates "$f"
}

self_test() {
    d=$(mktemp -d) || return 1
    cat >"$d/bad.yml" <<'FIXTURE'
services:
  - name: postgres:latest
  - name: rabbitmq:4-management
test:
  image: php:8.4-cli
  retry: 2
  allow_failure: true
  cache:
    key: "static-key"
    paths: [vendor]
  script:
    - vendor/bin/phpstan analyse || true
FIXTURE
    cat >"$d/good.yml" <<'FIXTURE'
services:
  - name: postgres:18.3
test:
  image: php:8.5-cli
  cache:
    key:
      files:
        - composer.lock
    paths: [.composer-cache]
  script:
    - vendor/bin/phpstan analyse
FIXTURE
    printf '{ "require": { "php": "^8.5" } }\n' >"$d/composer.json"
    rc=0
    out=$(sh "$0" --repo "$d" "$d/bad.yml" 2>&1); [ "$?" -eq 1 ] || { echo "self-test: bad.yml should exit 1"; rc=1; }
    for code in IMAGE CACHEKEY TOOLCHAIN NOTAGATE RETRY; do
        printf '%s' "$out" | grep -q "$code" || { echo "self-test: $code did not fire"; rc=1; }
    done
    printf '%s' "$out" | grep -q 'only a major' || { echo "self-test: major-only tag not detected"; rc=1; }
    sh "$0" --repo "$d" "$d/good.yml" >/dev/null 2>&1 || { echo "self-test: good.yml should exit 0"; rc=1; }
    sh "$0" --repo "$d" "$d/absent.yml" >/dev/null 2>&1; [ "$?" -eq 3 ] || { echo "self-test: missing file should exit 3"; rc=1; }
    rm -f "$d"/*.yml "$d"/composer.json 2>/dev/null
    rmdir "$d" 2>/dev/null
    [ "$rc" -eq 0 ] && echo "self-test: all checks fire"
    return "$rc"
}

REPO="."
SELFTEST=0
FILES=""
while [ "$#" -gt 0 ]; do
    case "$1" in
        --help|-h) usage; exit 0 ;;
        --self-test) SELFTEST=1 ;;
        --repo) [ "$#" -ge 2 ] || { echo "$PROG: --repo needs a directory" >&2; exit 2; }; REPO="$2"; shift ;;
        --repo=*) REPO=${1#--repo=} ;;
        -*) echo "$PROG: unknown option $1" >&2; usage >&2; exit 2 ;;
        *) FILES="$FILES $1" ;;
    esac
    shift
done
[ "$SELFTEST" -eq 1 ] && { self_test; exit "$?"; }
[ -d "$REPO" ] || { echo "$PROG: not a directory: $REPO" >&2; exit 2; }

if [ -z "$FILES" ]; then
    [ -f "$REPO/.gitlab-ci.yml" ] && FILES="$FILES $REPO/.gitlab-ci.yml"
    for f in "$REPO"/.github/workflows/*.yml "$REPO"/.github/workflows/*.yaml; do
        [ -f "$f" ] && FILES="$FILES $f"
    done
fi

FIND=$(mktemp) || exit 2
EXISTING=""
for f in $FILES; do [ -f "$f" ] && EXISTING="$EXISTING $f"; done
if [ -z "$EXISTING" ]; then
    echo "$PROG: no CI configuration found under $REPO - this check did not run" >&2
    rm -f "$FIND"; exit 3
fi
for f in $EXISTING; do scan_file "$f"; done
check_toolchain "$REPO" $EXISTING

[ -s "$FIND" ] && sed -e 's/^/  /' "$FIND"
findings=$(grep -v '^note	' "$FIND" 2>/dev/null | wc -l | tr -d '[:space:]')
notes=$(grep '^note	' "$FIND" 2>/dev/null | wc -l | tr -d '[:space:]')
rm -f "$FIND"
echo "$PROG: $SCANNED file(s) scanned, $findings finding(s), $notes note(s)"
[ "$findings" -gt 0 ] && exit 1
[ "$DELEGATED" -gt 0 ] && [ "$DELEGATED" -eq "$SCANNED" ] && exit 4
exit 0

#!/bin/sh
# architecture-gate.sh - fail a build on Laravel layer-boundary defects.
#
# Detects the five defect classes that no single-file review can see:
#   L1  a Controller reaching persistence instead of going through a Service
#   L2  an internal key or a raw model reaching an HTTP response
#   L3  a write or query composed outside a repository
#   L4  a service provider performing I/O
#   L5  a service provider resolving a service inside register()
#
# Owned by the alaa-laravel-architecture skill. Read
# references/80-acceptance-gate.md for what each finding means, what the gate
# cannot see, and how to waive a finding honestly.
#
# Dependencies: sh, find, grep -nE, awk, sort, mktemp. No PHP, no Composer.
# Exit codes: 0 no findings; 1 findings; 2 usage or configuration error.

set -u

GATE_VERSION='1.0.0'
APP_DIR='app'
ALLOW_FILE='.architecture-gate-allow'
SELF_TEST=0
TAB=$(printf '\t')

usage() {
    cat <<'USAGE'
architecture-gate.sh - Laravel layer-boundary gate

Usage:
  architecture-gate.sh [--app-dir DIR] [--allow-file FILE]
  architecture-gate.sh --self-test
  architecture-gate.sh -h | --help
  architecture-gate.sh --version

Options:
  --app-dir DIR      directory to scan. Default: app
  --allow-file FILE  waiver file. Default: .architecture-gate-allow
  --self-test        run the built-in fixture suite and exit
  -h, --help         print this help and exit
  --version          print the gate version and exit

Waiver file format, one waiver per line, three fields separated by '@@@':
  path_substring@@@check_id@@@reason

  Blank lines and lines starting with '#' are ignored. A waiver with an empty
  path, check, or reason is a configuration error and the gate exits 2, because
  a waiver an agent can write without stating a reason is not an exception.
  Every applied waiver is printed, so no waiver is silent in CI output.

Exit codes:
  0  no findings
  1  at least one finding
  2  usage or configuration error
USAGE
}

# check-id@@@scope regex on the file path@@@detect regex@@@message
read_checks() {
    cat <<'CHECKS'
L1-controller-persistence@@@(^|/)Http/Controllers/@@@(DB::|::query\(|->newQuery\(|RepositoryInterface|::where\(|::find\(|::findOrFail\(|::create\(|::updateOrCreate\(|::firstOrCreate\(|->save\(\)|->delete\(\))@@@Controller reaches persistence. Call a Service; the Service calls the repository interface.
L2-public-id-leak@@@(^|/)Http/(Resources|Controllers)/@@@(['"]id['"] *=> *\$[A-Za-z_][A-Za-z_0-9]*->id[^_a-zA-Z0-9]|->getKey\(\)|response\(\)->json\( *\$)@@@Internal key or raw model reaches the response. Expose the public identifier as id and serialize through a Resource.
L3-repository-bypass@@@(^|/)(Services|Jobs|Listeners|Commands|Policies|Actions|Pipelines)/@@@(DB::table\(|DB::insert|DB::update|DB::delete|DB::statement|->save\(\)|->delete\(\)|::create\(|::updateOrCreate\(|::firstOrCreate\(|::insert\(|::query\(|::where\()@@@Write or query composed outside a repository. Move it behind the repository interface.
L4-provider-io@@@(^|/)Providers/@@@(Cache::(get|put|remember|rememberForever|forget|has|pull|add|increment|decrement)\(|Redis::(get|set|setex|del|exists|hget|hset|eval|pipeline|command|throttle)\(|DB::(table|select|insert|update|delete|statement|connection|transaction|beginTransaction)\(|Http::(get|post|put|patch|delete|send|pool)\(|Storage::(get|put|exists|delete|disk|copy|move)\(|Session::(get|put|has|forget|pull)\(|->remember\(|->rememberForever\(|file_get_contents\(|curl_init\()@@@Service provider performs I/O. A provider that reads Redis, the database, the cache, or the network turns a dependency outage into a boot failure. Defer it.
CHECKS
}

# ------------------------------------------------------------------ scanning

# php_files DIR -> newline-separated relative-ish paths, sorted
php_files() {
    find "$1" -type f -name '*.php' 2>/dev/null | LC_ALL=C sort
}

# scan_grep DIR -> findings as check<TAB>file<TAB>line<TAB>text
scan_grep() {
    sg_dir=$1
    read_checks | while IFS= read -r spec; do
        [ -n "$spec" ] || continue
        c_id=${spec%%@@@*}
        c_r1=${spec#*@@@}
        c_scope=${c_r1%%@@@*}
        c_r2=${c_r1#*@@@}
        c_pat=${c_r2%%@@@*}
        php_files "$sg_dir" | while IFS= read -r f; do
            if printf '%s\n' "$f" | grep -qE "$c_scope"; then
                grep -nE "$c_pat" "$f" 2>/dev/null | while IFS= read -r hit; do
                    h_no=${hit%%:*}
                    h_tx=${hit#*:}
                    printf '%s\t%s\t%s\t%s\n' "$c_id" "$f" "$h_no" "$h_tx"
                done
            fi
        done
    done
}

# scan_register DIR -> L5 findings. Brace-tracked so it reads the register()
# body only, and so a $app->make() inside a binding closure is not a finding.
scan_register() {
    php_files "$1" | while IFS= read -r f; do
        if printf '%s\n' "$f" | grep -qE '(^|/)Providers/'; then
            awk -v file="$f" '
            {
                t = " " $0
                if (!inreg && t ~ /function[ \t]+register[ \t]*\(/) { inreg = 1; depth = 0; started = 0 }
                if (inreg) {
                    # depth 1 is the register() body itself. Anything deeper is
                    # inside a closure, which is deferred resolution and legal.
                    if (started && depth == 1 &&
                        t !~ /(fn[ \t]*\(|function[ \t]*\()/ &&
                        t ~ /(\$this->app->make\(|[^A-Za-z_0-9>$]app\(|[^A-Za-z_0-9>$]resolve\()/) {
                        printf "L5-provider-resolve-in-register\t%s\t%d\t%s\n", file, NR, $0
                    }
                    o = gsub(/\{/, "{"); c = gsub(/\}/, "}")
                    depth += o - c
                    if (o > 0) started = 1
                    if (started && depth <= 0) inreg = 0
                }
            }' "$f"
        fi
    done
}

message_for() {
    read_checks | while IFS= read -r spec; do
        [ -n "$spec" ] || continue
        m_id=${spec%%@@@*}
        [ "$m_id" = "$1" ] || continue
        printf '%s\n' "${spec##*@@@}"
    done
    [ "$1" = 'L5-provider-resolve-in-register' ] && printf '%s\n' \
        'Service resolved inside register(). Bindings only in register(); resolve in a closure, in boot(), or at first use.'
    return 0
}

# ------------------------------------------------------------------- waivers

# apply_waivers FINDINGS_FILE WAIVED_FILE
apply_waivers() {
    aw_in=$1
    aw_out=$2
    : > "$aw_out"
    [ -f "$ALLOW_FILE" ] || return 0
    aw_no=0
    while IFS= read -r raw || [ -n "$raw" ]; do
        aw_no=$((aw_no + 1))
        case "$raw" in
            ''|'#'*) continue ;;
            *@@@*@@@*) ;;
            *)
                printf '%s:%s: a waiver needs three fields: path@@@check@@@reason\n' \
                    "$ALLOW_FILE" "$aw_no" >&2
                exit 2
                ;;
        esac
        w_p=${raw%%@@@*}
        w_r=${raw#*@@@}
        w_c=${w_r%%@@@*}
        w_why=${w_r#*@@@}
        if [ -z "$w_p" ] || [ -z "$w_c" ] || [ -z "$w_why" ]; then
            printf '%s:%s: a waiver with an empty path, check, or reason is not a waiver\n' \
                "$ALLOW_FILE" "$aw_no" >&2
            exit 2
        fi
        awk -F"$TAB" -v p="$w_p" -v c="$w_c" -v why="$w_why" -v wf="$aw_out" \
            'BEGIN { OFS = "\t" }
             ($1 == c && index($2, p) > 0) { print $1, $2, $3, why >> wf; next }
             { print }' "$aw_in" > "$aw_in.next"
        mv "$aw_in.next" "$aw_in"
    done < "$ALLOW_FILE"
    return 0
}

# -------------------------------------------------------------------- report

# report FINDINGS_FILE WAIVED_FILE -> 0 clean, 1 findings
report() {
    rp_in=$1
    rp_wv=$2
    if [ -s "$rp_wv" ]; then
        printf 'Waived findings (each carries the reason from %s):\n' "$ALLOW_FILE"
        awk -F"$TAB" '{ printf "  WAIVED %s  %s:%s  %s\n", $1, $2, $3, $4 }' "$rp_wv"
        printf '\n'
    fi
    if [ ! -s "$rp_in" ]; then
        printf 'architecture-gate: no findings in %s\n' "$APP_DIR"
        return 0
    fi
    rp_last=''
    while IFS= read -r fnd; do
        f_id=${fnd%%	*}
        f_r1=${fnd#*	}
        f_file=${f_r1%%	*}
        f_r2=${f_r1#*	}
        f_line=${f_r2%%	*}
        f_text=${f_r2#*	}
        if [ "$f_id" != "$rp_last" ]; then
            printf '\n%s\n  %s\n' "$f_id" "$(message_for "$f_id")"
            rp_last=$f_id
        fi
        printf '    %s:%s\n      %s\n' "$f_file" "$f_line" "$f_text"
    done < "$rp_in"
    printf '\nFindings: %s. Fix each one, or waive it in %s with a reason.\n' \
        "$(wc -l < "$rp_in" | tr -d ' ')" "$ALLOW_FILE"
    printf 'What each finding means: references/80-acceptance-gate.md\n'
    return 1
}

# ----------------------------------------------------------------- self-test

self_test() {
    st_root=$(mktemp -d 2>/dev/null) || { printf 'mktemp failed\n' >&2; exit 2; }
    st_fail=0
    mkdir -p "$st_root/dirty/Http/Controllers" "$st_root/dirty/Http/Resources" \
             "$st_root/dirty/Services" "$st_root/dirty/Providers" \
             "$st_root/clean/Http/Controllers" "$st_root/clean/Http/Resources" \
             "$st_root/clean/Services" "$st_root/clean/Providers"

    cat > "$st_root/dirty/Http/Controllers/CommentController.php" <<'FIXTURE'
<?php
final class CommentController
{
    public function show(string $id)
    {
        $comment = Comment::where('public_id', $id)->firstOrFail();
        return response()->json($comment);
    }
}
FIXTURE
    cat > "$st_root/dirty/Http/Resources/CommentResource.php" <<'FIXTURE'
<?php
final class CommentResource
{
    public function toArray($request): array
    {
        return ['id' => $comment->id, 'key' => $this->getKey()];
    }
}
FIXTURE
    cat > "$st_root/dirty/Services/CommentService.php" <<'FIXTURE'
<?php
final class CommentService
{
    public function create(array $data): void
    {
        Comment::create($data);
        DB::table('audit')->insert($data);
    }
}
FIXTURE
    cat > "$st_root/dirty/Providers/AppServiceProvider.php" <<'FIXTURE'
<?php
final class AppServiceProvider
{
    public function register(): void
    {
        $flags = Cache::remember('flags', 60, fn () => []);
        $svc = $this->app->make(CommentService::class);
    }
}
FIXTURE

    cat > "$st_root/clean/Http/Controllers/CommentController.php" <<'FIXTURE'
<?php
final class CommentController
{
    public function __construct(private readonly CommentService $service) {}

    public function show(string $publicId): CommentResource
    {
        return new CommentResource($this->service->read($publicId));
    }
}
FIXTURE
    cat > "$st_root/clean/Http/Resources/CommentResource.php" <<'FIXTURE'
<?php
final class CommentResource
{
    public function toArray($request): array
    {
        return ['id' => $this->public_id, 'body' => $this->body];
    }
}
FIXTURE
    cat > "$st_root/clean/Services/CommentService.php" <<'FIXTURE'
<?php
final class CommentService
{
    public function __construct(private readonly CommentRepositoryInterface $repository) {}

    public function create(CommentData $data): CommentData
    {
        return $this->repository->create($data);
    }
}
FIXTURE
    cat > "$st_root/clean/Providers/RepositoryServiceProvider.php" <<'FIXTURE'
<?php
final class RepositoryServiceProvider
{
    public function register(): void
    {
        $this->app->bind(CommentRepositoryInterface::class, function ($app) {
            return new CachedCommentRepository(
                $app->make(PostgresCommentRepository::class),
                $app->make('cache')->store(config('cache.default')),
            );
        });
    }
}
FIXTURE

    cat > "$st_root/clean/Providers/ObservabilityServiceProvider.php" <<'FIXTURE'
<?php
final class ObservabilityServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(Registry::class, fn () => $this->app->make(RegistryFactory::class)->make());
    }

    public function boot(): void
    {
        DB::listen(fn ($event) => $this->app->make(DatabaseTelemetry::class)->record($event));
    }
}
FIXTURE

    st_dirty=$( { scan_grep "$st_root/dirty"; scan_register "$st_root/dirty"; } 2>/dev/null )
    for st_id in L1-controller-persistence L2-public-id-leak L3-repository-bypass \
                 L4-provider-io L5-provider-resolve-in-register; do
        if printf '%s\n' "$st_dirty" | grep -q "$st_id"; then
            printf 'PASS  %s fires on its fixture\n' "$st_id"
        else
            printf 'FAIL  %s did not fire on its fixture\n' "$st_id"
            st_fail=$((st_fail + 1))
        fi
    done

    st_clean=$( { scan_grep "$st_root/clean"; scan_register "$st_root/clean"; } 2>/dev/null )
    if [ -z "$st_clean" ]; then
        printf 'PASS  conforming fixture produces no finding\n'
    else
        printf 'FAIL  conforming fixture produced findings:\n%s\n' "$st_clean"
        st_fail=$((st_fail + 1))
    fi

    if printf '%s\n' "$st_dirty" | grep -q 'clean/'; then
        printf 'FAIL  scan leaked across trees\n'
        st_fail=$((st_fail + 1))
    else
        printf 'PASS  scan stays inside the directory it was given\n'
    fi

    case "$st_root" in
        /tmp/*|/var/folders/*) rm -rf "$st_root" ;;
    esac

    if [ "$st_fail" -eq 0 ]; then
        printf '\nself-test: all checks pass\n'
        return 0
    fi
    printf '\nself-test: %s failure(s)\n' "$st_fail"
    return 1
}

# ---------------------------------------------------------------------- main

while [ $# -gt 0 ]; do
    case $1 in
        --app-dir)
            [ $# -ge 2 ] || { printf -- '--app-dir needs a value\n' >&2; exit 2; }
            APP_DIR=$2
            shift
            ;;
        --allow-file)
            [ $# -ge 2 ] || { printf -- '--allow-file needs a value\n' >&2; exit 2; }
            ALLOW_FILE=$2
            shift
            ;;
        --self-test) SELF_TEST=1 ;;
        -h|--help) usage; exit 0 ;;
        --version) printf 'architecture-gate.sh %s\n' "$GATE_VERSION"; exit 0 ;;
        *)
            printf 'unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
    shift
done

if [ "$SELF_TEST" -eq 1 ]; then
    self_test
    exit $?
fi

if [ ! -d "$APP_DIR" ]; then
    printf 'architecture-gate: %s is not a directory. Pass --app-dir.\n' "$APP_DIR" >&2
    exit 2
fi

TMPD=$(mktemp -d 2>/dev/null) || { printf 'mktemp failed\n' >&2; exit 2; }
{ scan_grep "$APP_DIR"; scan_register "$APP_DIR"; } > "$TMPD/findings" 2>/dev/null
apply_waivers "$TMPD/findings" "$TMPD/waived"
report "$TMPD/findings" "$TMPD/waived"
GATE_RC=$?
case "$TMPD" in
    /tmp/*|/var/folders/*) rm -rf "$TMPD" ;;
esac
exit "$GATE_RC"

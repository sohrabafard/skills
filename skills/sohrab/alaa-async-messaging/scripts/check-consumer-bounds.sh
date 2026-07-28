#!/bin/sh
# check-consumer-bounds.sh - fail a change on the three message-plane defects
# that no single-file review reliably catches.
#
#   C1  a consumer construction site with no explicit prefetch
#   C2  a declared queue with no declared dead-letter target
#   C3  a broker name that the fleet registry's grammar cannot record
#
# Owned by the alaa-async-messaging skill. references/30-consuming-ack-and-prefetch.md
# derives prefetch, references/40-dead-letter-and-replay.md owns the dead-letter
# topology, and alaa-services-contract references/23-queue-and-exchange-registry.md
# owns the grammar and every name.
#
# Dependencies: sh, find, grep -nE, awk, tr, sort. No language runtime.

set -u

VERSION='1.0.0'
ROOT='.'
SELF_TEST=0
SELF=$0

CONSUME_RE='basic_consume\(|->consume\(|\.Consume\(|NewConsumer\(|mqkit\.Consumer|rabbitmq:consume|queue:work'
PREFETCH_RE='basic_qos\(|prefetch_count|PrefetchCount|prefetch-count|Prefetch:|\.Qos\(|MQ_PREFETCH|RABBITMQ_PREFETCH|.prefetch.[ ]*=>'
QDECL_RE='queue_declare\(|queueDeclare\(|QueueDeclare\(|DeclareQueue\(|QueueDecl\{|declareQueue\('
DLQ_RE='x-dead-letter-exchange|x-dead-letter-routing-key|DLQDecl|dead_letter|deadLetter|DeadLetter'
NAMECTX_RE='queue_declare|queueDeclare|QueueDeclare|DeclareQueue|QueueDecl|exchange_declare|ExchangeDeclare|DeclareExchange|ExchangeDecl|[A-Z_]*QUEUE[A-Z_]*=|[A-Z_]*EXCHANGE[A-Z_]*=|routing_key|RoutingKey|routingKey'
BROKER_RE='amqp|AMQP|rabbitmq|RabbitMQ|RABBITMQ|mqkit'

usage() {
    cat <<'USAGE'
check-consumer-bounds.sh - message-plane bounds gate

Usage:
  check-consumer-bounds.sh [--root DIR]
  check-consumer-bounds.sh --self-test
  check-consumer-bounds.sh -h | --help
  check-consumer-bounds.sh --version

Options:
  --root DIR    directory to scan. Default: the current directory
  --self-test   run the shipped fixtures under scripts/fixtures and exit
  -h, --help    print this help and exit
  --version     print the gate version and exit

Checks:
  C1-prefetch-unset      A consumer construction site was found and no prefetch
                         token appears in the same file. A consumer on its
                         library default holds unbounded unacknowledged
                         deliveries.
  C2-queue-without-dlq   A queue declaration was found and no dead-letter token
                         appears in the same file. A queue with no dead-letter
                         target loops a poison message forever or drops it.
                         Declarations of a *.dlq or *.retry queue are exempt,
                         because a dead-letter queue declares no target of its
                         own.
  C3-name-grammar        A broker name literal contains an uppercase letter or a
                         hyphen, or has only one segment. The registry grammar is
                         lowercase, '.' between segments, '_' inside a segment.

Exit codes and what each obliges you to do:
  0  No findings. Report the checks as run and continue.
  1  At least one finding, printed with file and line. Resolve every one before
     reporting the change complete. A finding is not waivable in this script:
     fix the code, or change the registry row that makes the name legal.
  2  Could not determine - no broker lane in the tree, or no recognisable
     consumer or queue declaration. Perform the three checks by hand and report
     the result of each. Exit 2 is never a pass. Detection is narrow: a name
     held in a constant, a consumer built behind a wrapper, and one level of
     indirection all escape it.
USAGE
}

scan_files() {
    find "$1" -type f \( -name '*.go' -o -name '*.php' -o -name '*.py' -o -name '*.rb' \
        -o -name '*.js' -o -name '*.ts' -o -name '*.yml' -o -name '*.yaml' \
        -o -name '*.json' -o -name '*.conf' -o -name '*.env' -o -name '.env*' \
        -o -name '*.env.example' -o -name '*.example' \) 2>/dev/null | LC_ALL=C sort
}

has_broker_lane() {
    scan_files "$1" | while IFS= read -r f; do
        if grep -qE "$BROKER_RE" "$f" 2>/dev/null; then
            printf 'yes\n'
            break
        fi
    done
}

has_site() {
    scan_files "$1" | while IFS= read -r f; do
        if grep -qE "$CONSUME_RE|$QDECL_RE" "$f" 2>/dev/null; then
            printf 'yes\n'
            break
        fi
    done
}

check_prefetch() {
    scan_files "$1" | while IFS= read -r f; do
        grep -qE "$PREFETCH_RE" "$f" 2>/dev/null && continue
        grep -nE "$CONSUME_RE" "$f" 2>/dev/null | while IFS= read -r hit; do
            printf 'C1-prefetch-unset\t%s:%s\t%s\n' "$f" "${hit%%:*}" "${hit#*:}"
        done
    done
}

check_dlq() {
    scan_files "$1" | while IFS= read -r f; do
        grep -qE "$DLQ_RE" "$f" 2>/dev/null && continue
        grep -nE "$QDECL_RE" "$f" 2>/dev/null | grep -vE '\.(dlq|retry)' | while IFS= read -r hit; do
            printf 'C2-queue-without-dlq\t%s:%s\t%s\n' "$f" "${hit%%:*}" "${hit#*:}"
        done
    done
}

check_names() {
    scan_files "$1" | while IFS= read -r f; do
        grep -nE "$NAMECTX_RE" "$f" 2>/dev/null | while IFS= read -r hit; do
            n=${hit%%:*}
            txt=${hit#*:}
            {
                printf '%s\n' "$txt" | tr "'" '"' | awk -F'"' '{for(i=2;i<=NF;i+=2) print $i}'
                printf '%s\n' "$txt" | grep -oE '[A-Z_]*(QUEUE|EXCHANGE)[A-Z_]*=[A-Za-z0-9._-]+' \
                    | sed 's/^[^=]*=//'
            } | while IFS= read -r lit; do
                case "$lit" in
                    ''|*://*|*/*|*' '*|*'$'*|*'{'*|*'%'*|*'.php'*|*'.go'*) continue ;;
                esac
                printf '%s' "$lit" | grep -qE '^[A-Za-z0-9._-]+$' || continue
                printf '%s' "$lit" | grep -qE '[.]' || {
                    printf 'C3-name-grammar\t%s:%s\t%s (single-segment name)\n' "$f" "$n" "$lit"
                    continue
                }
                if printf '%s' "$lit" | grep -qE '[A-Z]'; then
                    printf 'C3-name-grammar\t%s:%s\t%s (uppercase)\n' "$f" "$n" "$lit"
                    continue
                fi
                case "$lit" in
                    *-*) printf 'C3-name-grammar\t%s:%s\t%s (hyphen is not a separator)\n' "$f" "$n" "$lit" ;;
                esac
            done
        done
    done
}

run_checks() {
    rc_root=$1
    if [ ! -d "$rc_root" ]; then
        printf 'check-consumer-bounds: %s is not a directory. Pass --root.\n' "$rc_root" >&2
        return 2
    fi
    if [ -z "$(has_broker_lane "$rc_root")" ]; then
        printf 'undetermined: no broker lane found under %s.\n' "$rc_root"
        printf 'Perform the three checks by hand and report each result. Exit 2 is never a pass.\n'
        return 2
    fi
    if [ -z "$(has_site "$rc_root")" ]; then
        printf 'undetermined: broker configuration is present but no consumer or queue declaration was recognised under %s.\n' "$rc_root"
        printf 'Perform the three checks by hand and report each result. Exit 2 is never a pass.\n'
        return 2
    fi
    rc_out=$( { check_prefetch "$rc_root"; check_dlq "$rc_root"; check_names "$rc_root"; } 2>/dev/null | LC_ALL=C sort -u )
    if [ -z "$rc_out" ]; then
        printf 'ok: no findings under %s.\n' "$rc_root"
        return 0
    fi
    printf '%s\n' "$rc_out"
    printf '\n%s finding(s). Resolve every one before reporting the change complete.\n' \
        "$(printf '%s\n' "$rc_out" | grep -c .)"
    printf 'C1 references/30-consuming-ack-and-prefetch.md | C2 references/40-dead-letter-and-replay.md | C3 alaa-services-contract references/23-queue-and-exchange-registry.md\n'
    return 1
}

self_test() {
    st_dir=$(dirname "$SELF")/fixtures
    st_fail=0
    if [ ! -d "$st_dir" ]; then
        printf 'FAIL  fixtures directory %s is missing\n' "$st_dir"
        return 1
    fi

    st_out=$("$SELF" --root "$st_dir/conforming" 2>&1); st_rc=$?
    if [ "$st_rc" -eq 0 ]; then
        printf 'PASS  conforming fixture exits 0\n'
    else
        printf 'FAIL  conforming fixture exited %s:\n%s\n' "$st_rc" "$st_out"
        st_fail=$((st_fail + 1))
    fi

    st_out=$("$SELF" --root "$st_dir/violating" 2>&1); st_rc=$?
    if [ "$st_rc" -eq 1 ]; then
        printf 'PASS  violating fixture exits 1\n'
    else
        printf 'FAIL  violating fixture exited %s:\n%s\n' "$st_rc" "$st_out"
        st_fail=$((st_fail + 1))
    fi
    for st_id in C1-prefetch-unset C2-queue-without-dlq C3-name-grammar; do
        if printf '%s\n' "$st_out" | grep -q "$st_id"; then
            printf 'PASS  %s fires on its violating fixture\n' "$st_id"
        else
            printf 'FAIL  %s did not fire on its violating fixture\n' "$st_id"
            st_fail=$((st_fail + 1))
        fi
    done

    st_out=$("$SELF" --root "$st_dir/no-broker" 2>&1); st_rc=$?
    if [ "$st_rc" -eq 2 ]; then
        printf 'PASS  no-broker fixture exits 2\n'
    else
        printf 'FAIL  no-broker fixture exited %s:\n%s\n' "$st_rc" "$st_out"
        st_fail=$((st_fail + 1))
    fi

    "$SELF" --help >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        printf 'PASS  --help exits 0\n'
    else
        printf 'FAIL  --help did not exit 0\n'
        st_fail=$((st_fail + 1))
    fi

    "$SELF" --nonsense >/dev/null 2>&1
    if [ $? -eq 2 ]; then
        printf 'PASS  an unknown option exits 2\n'
    else
        printf 'FAIL  an unknown option did not exit 2\n'
        st_fail=$((st_fail + 1))
    fi

    if [ "$st_fail" -eq 0 ]; then
        printf '\nself-test: all checks pass\n'
        return 0
    fi
    printf '\nself-test: %s failure(s)\n' "$st_fail"
    return 1
}

while [ $# -gt 0 ]; do
    case $1 in
        --root)
            [ $# -ge 2 ] || { printf -- '--root needs a value\n' >&2; exit 2; }
            ROOT=$2
            shift
            ;;
        --self-test) SELF_TEST=1 ;;
        -h|--help) usage; exit 0 ;;
        --version) printf 'check-consumer-bounds.sh %s\n' "$VERSION"; exit 0 ;;
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

run_checks "$ROOT"
exit $?

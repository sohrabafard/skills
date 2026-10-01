#!/bin/sh
# Offline test container only; no host ports or network peers.
set -eu
haproxy -v | head -1
haproxy -v | grep -Eq 'HAProxy version 3\.4\.6([-[:space:]])' || exit 2
haproxy -vv | grep 'Built with Lua version'
haproxy -vv | grep -q '+LUA' || exit 2
haproxy -vv | grep -q 'Lua 5.4.8' || exit 2
command -v wget >/dev/null || exit 2
cd /tmp
tail_config() {
    cat <<'EOF'
defaults
    mode http
    timeout connect 1s
    timeout client 2s
    timeout server 2s
frontend probe
    bind 127.0.0.1:18080
    http-request return status 200
EOF
}
printf 'global\n    tune.lua.bool-sample-conversion normal\n    lua-load /pkg/test/runtime/unit-driver.lua\n' > unit.cfg
tail_config >> unit.cfg
haproxy -c -f unit.cfg
echo 'PASS embedded Lua 5.4.8 unit suite'

for libs in default all none string string,math,table,os; do
    echo global > libs.cfg
    if [ "$libs" != default ]; then printf '    tune.lua.openlibs %s\n' "$libs" >> libs.cfg; fi
    printf '    tune.lua.bool-sample-conversion normal\n    lua-load /tmp/libs.lua\n' >> libs.cfg
    if [ "$libs" = none ]; then
        echo 'assert(type(assert) == "function" and type(coroutine.create) == "function"); assert(string == nil and os == nil and package == nil)' > libs.lua
    elif [ "$libs" = string ]; then
        echo 'assert(type(string.byte) == "function" and os == nil and math == nil)' > libs.lua
    else
        echo 'assert(type(os.getenv) == "function" and type(os.date) == "function" and type(os.time) == "function")' > libs.lua
    fi
    tail_config >> libs.cfg
    haproxy -c -f libs.cfg >/dev/null
    echo "PASS openlibs $libs"
done
for fault in missing_os late_load late_perthread late_path invalid mixed_none args13; do
    echo 'global' > bad.cfg
    case "$fault" in
        args13) echo '    lua-load /pkg/test/runtime/probe.lua' >> bad.cfg ;;
        missing_os) printf '    tune.lua.openlibs string\n    lua-load /tmp/needs-os.lua\n' >> bad.cfg
                    echo 'assert(os.getenv("PATH"))' > needs-os.lua ;;
        late_load) printf '    lua-load /pkg/test/runtime/probe.lua\n    tune.lua.openlibs none\n' >> bad.cfg ;;
        late_perthread) printf '    lua-load-per-thread /pkg/test/runtime/probe.lua\n    tune.lua.openlibs none\n' >> bad.cfg ;;
        late_path) printf '    lua-prepend-path /tmp/?.lua\n    tune.lua.openlibs none\n' >> bad.cfg ;;
        invalid) echo '    tune.lua.openlibs banana' >> bad.cfg ;;
        mixed_none) echo '    tune.lua.openlibs none,string' >> bad.cfg ;;
    esac
    tail_config >> bad.cfg
    if [ "$fault" = args13 ]; then echo '    http-request set-var(txn.args) str(x),lua.probe_args(1,2,3,4,5,6,7,8,9,10,11,12,13)' >> bad.cfg; fi
    if haproxy -c -f bad.cfg >bad.log 2>&1; then echo "FAIL accepted $fault"; exit 1; fi
    echo "PASS parser rejects $fault"
done

for mode in normal pre-3.1-bug; do
    cat > runtime.cfg <<EOF
global
    tune.lua.bool-sample-conversion $mode
    lua-load /pkg/test/runtime/probe.lua
defaults
    mode http
    timeout connect 1s
    timeout client 2s
    timeout server 2s
frontend probe
    bind 127.0.0.1:18080
    http-request set-var(txn.nil) str(x),lua.probe_nil
    http-request set-var(txn.false) str(x),lua.probe_false
    http-request set-var(txn.true) str(x),lua.probe_true
    http-request set-var(txn.failed) str(x),lua.probe_error if { path /error }
    http-request set-var(txn.failed) str(x),lua.probe_error_one if { path /error-one }
    http-request set-var(txn.fetch_nil) lua.probe_fetch_nil
    http-request set-var(txn.stale) str(previous)
    http-request set-var(txn.stale) str(x),lua.probe_error if { path /stale }
    http-request set-var(txn.cleared) str(previous)
    http-request unset-var(txn.cleared)
    http-request set-var(txn.cleared) lua.probe_fetch_error if { path /stale }
    http-request set-var(txn.args) str(x),lua.probe_args(1,2,3,4,5,6,7,8,9,10,11,12)
    http-request lua.probe_deny if { path /act-deny }
    http-request set-var(txn.boolean) bool(false)
    http-request lua.probe_bool
    http-request set-var(txn.allowed) bool(false)
    http-request lua.probe_action_error if { path /action-error }
    http-request lua.probe_action_ok if { path /action-ok }
    http-request deny deny_status 403 if { path_beg /action- } !{ var(txn.allowed) -m bool }
    http-request deny deny_status 400 if { path_beg /error } !{ var(txn.failed) -m found }
    http-request return status 200 hdr X-Nil "%[var(txn.nil,ABSENT)]" hdr X-False "%[var(txn.false,ABSENT)]" hdr X-True "%[var(txn.true,ABSENT)]" hdr X-Kind "%[var(txn.kind)]" hdr X-Fetch-Nil "%[var(txn.fetch_nil,ABSENT)]" hdr X-Stale "%[var(txn.stale,ABSENT)]" hdr X-Cleared "%[var(txn.cleared,ABSENT)]" hdr X-Args "%[var(txn.args)]"
EOF
    haproxy -c -f runtime.cfg >/dev/null
    haproxy -db -f runtime.cfg > runtime.log 2>&1 &
    pid=$!
    trap 'kill "$pid" 2>/dev/null || true' EXIT
    ready=0
    for attempt in 1 2 3 4 5; do
        if wget -S -O /dev/null http://127.0.0.1:18080/ 2>response; then ready=1; break; fi
        sleep 0.1
    done
    [ "$ready" = 1 ] || { cat runtime.log; exit 1; }
    grep -qi 'X-Nil: 0' response
    grep -qi 'X-Fetch-Nil: 0' response
    grep -qi 'X-Args: 12' response
    grep -qi 'X-False: 0' response
    grep -qi 'X-True: 1' response
    if [ "$mode" = normal ]; then kind=boolean; else kind=number; fi
    grep -qi "X-Kind: $kind" response
    wget -S -O /dev/null http://127.0.0.1:18080/stale 2>response
    grep -qi 'X-Stale: previous' response
    grep -qi 'X-Cleared: ABSENT' response
    for path in error error-one action-error action-ok act-deny; do
        wget -S -O /dev/null "http://127.0.0.1:18080/$path" 2>response || true
        case "$path" in error*) status=400;; action-error|act-deny) status=403;; *) status=200;; esac
        grep -q "HTTP/1.1 $status" response
    done
    grep -q 'runtime error: probe-zero' runtime.log
    grep -q 'probe.lua:.*probe-one' runtime.log
    grep -q 'probe-action' runtime.log
    echo "PASS $mode samples, booleans, error levels and action denial"
    kill "$pid"
    wait "$pid" || true
    trap - EXIT
done

cd /pkg/examples/haproxy-lua
haproxy -c -f token-guard.cfg >/dev/null
haproxy -db -f token-guard.cfg >/tmp/token.log 2>&1 &
pid=$!
trap 'kill "$pid" 2>/dev/null || true' EXIT
sleep 0.2
for token in abcdefgh abc ABCDEFGH; do
    wget -S --header "X-Example-Token: $token" -O /dev/null http://127.0.0.1:18081/ 2>/tmp/response || true
    case "$token" in abcdefgh) status=200;; *) status=400;; esac
    grep -q "HTTP/1.1 $status" /tmp/response
done
wget -S -O /dev/null http://127.0.0.1:18081/ 2>/tmp/response || true
grep -q 'HTTP/1.1 400' /tmp/response
echo 'PASS example parser and token accepted/rejected/missing HTTP cases'
kill "$pid"
wait "$pid" || true
trap - EXIT

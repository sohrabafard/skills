# Peer identity, compatibility and transport

## Peers preconditions, restated as rules

Three, each of which fails silently:

1. **The local peer must be identifiable.** HAProxy activates a `peers` section only when one of
   its entries matches the local peer name — the machine hostname by default, overridden by the
   `localpeer` keyword in the `global` section or by the `-L` command-line option. When nothing
   matches, HAProxy does not activate the section: it neither dials nor listens. The config still
   passes `haproxy -c -f`, the process still starts, the table is still created, and the limit
   still works per node in isolation, with no error anywhere. With Kubernetes-generated pod names
   the hostname never matches a hand-written peer name, so `localpeer` or `-L` is mandatory there.
2. **Keep replicated table definitions compatible.** Use consistent names, key types/lengths,
   stored data and periods. This package keeps sizing aligned for review, but a size
   difference alone is not a documented universal sync-refusal rule. Verify `show peers`
   and real updates; declaration in the peers section makes the schema reviewable.
3. **The peers port must be authenticated.** The peers protocol carries no authentication of its
   own, and anything that reaches the port can write stick-table entries — raise a victim's
   penalty counter to the deny threshold, or lower an attacker's counter to evade the limit. Put
   TLS with mutual verification on the `bind` line and on every remote `server` line, and restrict
   the port to the peer set at the network layer as well.

`scripts/check_defaults_scope.py` does not cover these; `scripts/check_examples.py` asserts that
any shipped config with a `peers` section sets `localpeer` and puts `ssl` on the peers `bind`.

# Parent correctness review

Verdict: approved for the declared local scope, subject to independent instruction review and final closure gates.

Reviewed the complete 12-file Git diff against HEAD `2a2340d3677945578b505fce49de60e11561037d`. Both skills remain frozen at aggregate SHA256 `978b8b181a5381fe502232d3baa487a50b9ef55df97b4b54da1283068059048a`.

| Acceptance | Evidence and judgment |
|---|---|
| Separate extracted owners | Orientation, core inventory, flow and debugging references assign API/events/audiences to entitlement-api, projection to entitlement-projector, model/mapping to authz-openfga and gateway checker interface to authz-sidecar. This agrees with the sibling extraction owner table. |
| Preserve operational identities | Repository name entitlement-projector is distinguished from runtime identity projector. No metric, environment default, queue, header, permission or wire shape is renamed. |
| Protected-route procedure | Canonical model/mapping edits precede API/projector work, consumer bundle import and gateway exposure. Shared store/model/label pins and fail-closed behavior remain. Immutable imported bundles are not promoted to authoring roots; equality must be checked against the reviewed export. |
| Deny diagnosis | Gateway, imported endpoint mapping, tuples, API events and projection remain distinct debugging hops. Current source pointers go to the extracted owners. The concrete legacy Postman source is retained as historical with destination explicitly unconfirmed. |
| Notification audience | Ownership moves to entitlement-api; interim envelope limitations, reserved bridge, snake_case contract and notification ingress authority remain. |
| Trust source selection | Gateway executable configuration still has edge precedence. The trust source map adds checker/model/business/projection owners without changing trust doctrine. |
| Conformance refresh | Dated conformance, queue registry and deadline references are unchanged. The current service reality table separates extracted repositories and routes OpenFGA trace-export verification to owner configuration without changing observability obligations. |
| Compression and scope | Adjacent invocation pairs become the required single call form only in edited files. Both normalized whole-skill sizes decrease; entrypoints, scripts and metadata remain untouched. No sibling repository edits are present. |

No high-confidence correctness finding. This is a static instruction/source-routing review; runtime authorization, deployed pins and Postman relocation are outside its proof.

## Snapshot-method reconciliation

The verifier initially hashed the JSON file, then hash-first text rows, instead of the declared path/NUL/hash/LF aggregate. Its alternate result is not evidence of candidate drift. Parent recomputation from sorted manifest entries and independently from raw current file bytes produced the declared aggregate, with zero per-file mismatches. The method is stated in candidate-manifest.json; no candidate or manifest correction was required.

## Closure review

The independent major finding was valid: entitlement-api also consumes a pinned bundle. Reviewed the sole two-hunk v1-to-v2 delta. All three consumers are now named, API model SHA equality and migration/admission gates are explicit, compatible version differences remain allowed, and the router still owns retrieval of the shared pin rules. No new correctness finding. Independent instruction closure is APPROVED; affected verification is PASS on v2 aggregate e6fa953819342848986a77ba0ce1e37f63969d0d639e395c478213842fa533cf. Final services size is 430878 bytes, five below baseline; trust remains 135513, twenty-one below baseline.

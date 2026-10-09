# Provider availability acceptance matrix

This is a static requirement oracle for the user clarification, not live deployment evidence. Providers are optional per project. Presence never establishes operation support, authorization, health, freshness, or the correct worktree/environment. Apply those filters before the choices below; treat an ineligible capability as absent for that operation.

For a bounded structural relationship, `C` means CodeGraph is applicable and healthy; `S` means Serena can answer the remaining structural fact for this language; `B` means Boost is available in a Laravel project; `N` means the relevant native read operation is available and authorized. Serena/native structural fallbacks retain their narrower coverage. Runtime/database evidence requires its own environment check.

| C | S | B | Structural question | Exact semantic question | Laravel runtime question |
|---|---|---|---|---|---|
| yes | yes | yes | C | S | B |
| yes | yes | no | C | S | Equivalent authorized native observation, else blocked |
| yes | no | yes | C | Existing native semantic operation if equivalent; otherwise partial read or blocked | B |
| yes | no | no | C | Existing native semantic operation if equivalent; otherwise partial read or blocked | Equivalent authorized native observation, else blocked |
| no | yes | yes | S for supported fact, then N for a gap | S | B |
| no | yes | no | S for supported fact, then N for a gap | S | Equivalent authorized native observation, else blocked |
| no | no | yes | N with coverage limits, else blocked | Existing native semantic operation if equivalent; otherwise partial read or blocked | B |
| no | no | no | N with coverage limits, else blocked | Existing native semantic operation if equivalent; otherwise partial read or blocked | Equivalent authorized native observation, else blocked |

Apply every row with N present and absent. A missing native gate is blocked in either case; provider evidence cannot replace it. An already answered fact requires no new call, regardless of availability. Mutation uncertainty interrupts this selection matrix: reconcile actual state before any continuation.

For PHP without Laravel, Go, and other languages, B is not applicable. The four C/S combinations above still apply, with only supported language/backend operations eligible. A Go native semantic fallback may be the existing project-declared gopls interface; it is not assumed installed. Unsupported language coverage excludes that provider's operation even when the server itself is connected.

A configured provider becoming unhealthy, partial, stale, or unreachable is an operation-state change, not permission to install, reindex, activate effectful setup, or cycle through already attempted owners. An unconfigured or inapplicable provider is skipped without a repair attempt. Restoration only invalidates affected capability evidence after an actual relevant state change.

## Review obligation

The independent instruction reviewer must locate the final skill rule that decides every row and the N-absent, unsupported-language, wrong-context, and uncertain-mutation variations. Report a gap if the rule cannot decide a cell without inventing authority or completeness. This matrix deliberately does not claim that enumerating cases proves the agent executed them.

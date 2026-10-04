# Goal and planning repair evidence

Verified by the read-only goal_research lane on 2026-10-04. No live Desktop goal was executed.

| Question | Evidence | Source |
|---|---|---|
| Claude goal shape | `/goal <condition>`; condition limit 4,000 characters; one active goal; command starts execution | https://code.claude.com/docs/en/goal |
| Evaluator | Transcript evidence only, no tools or independent file reads; Not yet met, Met, Impossible | https://code.claude.com/docs/en/goal |
| Restrictions | Preserves permission mode; workspace trust and hook settings may prevent availability | https://code.claude.com/docs/en/goal |
| Desktop surface | Code tab documents slash commands, skills and goal support | https://code.claude.com/docs/en/desktop |
| Skill activation | Leading skill command directly invokes; a later slash name grants permission but is not direct invocation | https://code.claude.com/docs/en/skills |
| Other Desktop surfaces | Inspected Cowork guide does not establish goal support; absence of documentation is not proof of no support | https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork |

The existing 4,000-character cap agrees with current docs. A parser/cap change is not established. The prior binary evaluator description is stale. The user confirmed the Desktop Code tab. The user supplied the exact composer error below; the full rejected prompt and Desktop version remain unprovided. Static repairs must not be reported as a reproduced or fixed Desktop installation.

## Acceptance and failure cases

- A generated goal uses the selected surface's verified syntax and measures its final rendered condition; a shortness target is labelled house policy, not a vendor cap.
- Long execution and actionable execution-plan requests save a filled plan/checkpoint without another save request. Plan-only does not authorize product edits.
- Native Plan Mode, explicit read-only/chat-only/no-file requests, short advice, and small bounded edits preserve their artifact restrictions.
- Every phase and task resolves concrete skill names, source, load point, conditional trigger and missing-skill action; vague, missing and dangling mappings are rejected for execution.
- A fresh reader recovers next action from plan/checkpoint; completed historical artifacts remain readable.
- Both orchestrators preserve equivalent behavior. Low-noise cannot suppress required plans or mappings.
- Required deterministic gates and independent reviews report observed outcomes; live Desktop acceptance/model compliance remains unverified.

## Curation

Reported user preferences are implemented in their canonical skill owners. The exact incident wording is retained in this task evidence and is also dated in the [prompting guide's Claude Code runtime reference](../../skills/sohrab/alaa-prompting-guide/references/41-claude-code-runtime-features.md). No memory note was created.

## User-observed Desktop Code rejection

Reported on 2026-10-04:

> A command takes file @-mentions but no other @-mentions, slash commands, links, or inline formatting, so nothing was sent. Remove them.

The user reports this especially with skills or file addresses inside goal text. This is direct incident evidence of a composer rejection before sending; no live reproduction occurred here. The inspected official Desktop page does not document this exact restriction, so no release/version claim is inferred. Generated Desktop goals must use plain condition text; skill activation and detailed file references belong in a separate kickoff/plan. If that kickoff is itself a slash command, its arguments also stay plain, with only one leading command; do not move rejected rich tokens into a second command. File @-mentions are expressly permitted by the error, but a generated plain-text checker cannot validate rich mention chips. Static examples/checks cover known rejection forms without claiming complete Desktop parser parity.

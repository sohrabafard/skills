# Lane A ledger: pruned and merged rules

Rule numbers refer to *What to remove or merge* in `lane-brief.md`. "Both" means the Claude file and its Codex twin. For `alaa-reviewer` the Codex twin is `assets/reviewer-contract.md`.

## Removed or merged rules

| Role | Removed or merged text (short) | Reason | Where the behaviour now lives |
|---|---|---|---|
| alaa-reviewer (both) | "You did not write the change." | 2 | Same sentence: "independent owner-level reviewer with fresh context" |
| alaa-reviewer (both) | "Do not filter by importance or confidence" | 5 (merged) | Same bullet: "Report every finding, ordered by severity, including uncertain and low-severity ones", with its reason kept |
| alaa-reviewer (both) | "Report every issue you find" reworded to "Report every finding" | 5 (one term) | Same bullet; "finding" is the term of the FINDINGS item |
| alaa-reviewer (both) | "Do not soften a finding for reassurance." as its own sentence | 5 (merged) | Same bullet: "and soften no finding for reassurance" |
| alaa-reviewer (both) | "Make a style-only comment only when the style obscures a real risk." | 2 | Priority 8 ("not taste-only preferences") excludes the style-only comment; a real risk is a finding under priorities 1-7 and the report-every-finding rule |
| alaa-reviewer (both) | "Never edit a file" (first item of the never bullet) | 1 | `Effective authority` read-only sentence; "Never apply a fix, and accept no intent as evidence" stays |
| alaa-adversarial-reviewer (both) | "Ask a different question from the correctness review, not the same question again." | 2, 3 | First method bullet ("not line-level correctness") and first Boundaries bullet ("Do not re-run the correctness review") |
| alaa-adversarial-reviewer (both) | "Read-only." and "Never edit, ... or apply a patch" | 1 | `Effective authority` read-only sentence; "Never apply a fix." stays |
| alaa-adversarial-reviewer (Codex) | "Use the shell only to inspect and to run authorized checks." | 1 (brief, Codex mechanics list) | `Effective authority` shell clause |
| alaa-adversarial-reviewer (both) | "Say what you could not inspect" | 2 | Output item 5 NOT ASSESSED; "Absent evidence is not an absent problem." stays in the bullet |
| alaa-adversarial-reviewer (both) | "written for a person who decides whether to ship" | 2 | Same paragraph: "Your findings go to the user" |
| alaa-adversarial-reviewer (both) | "When you have no objection, say so" | 2 | Completion line ("an explicit no-objection") and the NO-BLOCKING-OBJECTION token; "Never manufacture an objection." stays in place |
| alaa-instruction-reviewer (both) | "read-only" in the Authority line | 1 | `Effective authority` read-only sentence; the rest of the line is unchanged |
| alaa-instruction-reviewer (both) | "Stop after the review; never fix a finding." | 2 | Fix half: Authority line ("no ... fix ... or external action"). Stop half: Completion line, which ends the work when every changed instruction is compared or listed |
| alaa-security-reviewer (Claude) | "Domain baseline: apply /alaa-security-review and /alaa-trust-gateway-auth when installed." | 4 | Frontmatter `skills:` preloads both. Codex keeps the line as a load call with "when installed" |
| alaa-security-reviewer (both) | "Read-only." | 1 | `Effective authority` read-only sentence; "Never apply a fix." stays |
| alaa-api-contract-reviewer (Claude) | "apply /alaa-services-contract ... when installed" | 4 | Frontmatter `skills:` preloads it. Codex keeps it in the load sentence |
| alaa-api-contract-reviewer (both) | "Read-only. Never edit ... the contract, the spec or the tests." | 1 | `Effective authority` read-only sentence; "Never apply a fix." stays |
| alaa-api-contract-reviewer (Codex) | "Use the shell only to inspect and to run authorized checks." | 1 (brief, Codex mechanics list) | `Effective authority` shell clause |
| alaa-migration-guardian (Claude) | "apply /alaa-data-layer ... when installed" | 4 | Frontmatter `skills:` preloads it; the partitioned-table scope stays as "Apply the preloaded /alaa-partitioned-table-fk-audit to partitioned-table work." |
| alaa-migration-guardian (both) | "or edit a file" | 1 | `Effective authority` read-only sentence; "Never run a migration or connect to production" stays |

## Changed by the dispatch, not pruned

| Role | Change | Where the behaviour now lives |
|---|---|---|
| alaa-reviewer (Claude) | `skills:` loses alaa-php-clean-code, alaa-vue-typescript-clean-code, alaa-golang-clean-code-principles, alaa-services-contract, alaa-trust-gateway-auth | New load paragraph after the priorities, identical in both runtimes; priorities 8 and 9 are unchanged |
| alaa-api-contract-reviewer (Claude) | `skills:` loses alaa-laravel-public-api-contract-pack, alaa-postman-collections | Conditional load sentence in both runtimes; the "installed" exception of the old baseline line is kept |
| Codex security-reviewer, api-contract-reviewer, migration-guardian | "Domain baseline: apply" reworded to "Before you judge, load" | Same line; skills, scope and "when installed" unchanged |

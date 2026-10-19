# PHP source decisions

Implemented under parent-ratified decisions and claimed implementation leaf alaa-6dh.3.2.2; final Phase 4 review remains pending.

AGENT: alaa-implementer. CONFIGURED: unpinned model/effort in role definition. REQUESTED: gpt-6.1-sol/medium in the ratified allocation and dispatch. OBSERVED: unknown; no serving-identity evidence. Authority: workspace-write sandbox; lane restricted to seven assigned skill trees and PHP artifacts. No external, global, Git or Beads mutations delegated.

## Proposed dispositions

| Item | Proposal | Grounding and invariant |
|---|---|---|
| 01:A3; 02:O11 | Adapt | Upgrade SKILL procedure 2-3 classifies majors then applies an unrestricted resolution. Use a classified package allow-list for both scoped preview and apply; inspect every resulting lock move, including transitives, and reject an unintended major. Package scoping alone is insufficient. Keep original authorization and restore-point boundaries. Failure-class cache retry must resume that selected command rather than broaden it. |
| 01:A4 | Adapt | Upgrade description routes framework migration to architecture, which has no migration procedure; architecture source-map incorrectly assigns dependency bumps to PHP craft. Limit upgrade owner to resolution, classification and isolation; report framework code migration as requiring a separately scoped plan and official versioned upgrade guide. Architecture retains boundary changes; PHP retains per-symbol audit points. No new migration capability. |
| 01:A5 | Accept | Octane SKILL Scope condition owns runtime applicability; PHP SKILL Compatibility target has a conflicting package/file predicate. Replace consumers with triggered owner pointers, preserving safe-by-default code consequence and upgrade runtime checks. |
| 01:B1 | Adapt | Async references/60-telemetry-and-proof.md Required tests owns queue redelivery assertions. Driver SKILL keeps unchanged-attempt and ack-versus-release delta. PHP laravel-best-practices run-twice proof retains jobs, listeners and seeders beyond queue deliveries; route queue-specific proof to async owner. |
| 01:B2 | Accept | Async references/30-consuming-ack-and-prefetch/40-prefetch.md owns sizing. Driver SKILL rule 5 retains explicit --prefetch-count and the driver-specific default, then points to sizing owner. |
| 01:B4 | Adapt | Octane SKILL upstream precedence and full-guide cache tiers own once() remedy. PHP laravel-best-practices override row points there without an alternate memoization recipe. Preserve trust, docblock and testing overrides with distinct owners. |
| 01:B5; 02:O10 | Adapt | Postman SKILL owns generation and complete saved examples. PHP documentation-and-artifacts replaces collection/environment generation rules with owner pointer, preserving PHP annotation rules. Contract-pack workflow delegates collection/environment production, keeps pack provenance, secret scan, emission gate and parity audit. Its 4xx/5xx scan minimum must not imply a coverage ceiling or fabricate unreachable errors. |
| 01:A6 consumer portion | Accept | skills/sohrab/AGENTS.md owns one /name form. Replace only the three cited convention sentences; normalize legacy calls only in files otherwise edited. No standalone call-site sweep. |

## Validation proposed

- Task: repeated `python -B scripts/check_fleet_references.py --skill <owned-name>` for the seven assigned skills; bounded exact Markdown-link/encoding/diff assertions over changed files.
- Subtask: inspect changed rule against counterexamples: loose/transitive Composer major, null Octane server, nonqueue seeder rerun, duplicate queue ack, reachable-only Postman errors, unresolved contract emission.
- Native architecture and consumer gate scripts need no run when their executable inputs are unchanged; no application runtime or installed agent compliance claim follows from static checks.
- Capture a deterministic sorted path+NUL+bytes SHA-256 manifest including untracked covered inputs before task checks. Final independent review remains parent Phase 4.

## Official command evidence

Verified 2026-10-18: https://getcomposer.org/doc/03-cli.md#update-u-upgrade, update command and options. Positional package arguments select partial updates; temporary `package:version` constraints must remain within manifest constraints. `--dry-run` simulates; `--with-dependencies` also moves dependencies except root requirements, while `--with-all-dependencies` includes root requirements. Neither dependency option promises minor-only movement. Apply exactly the scoped preview's package list/options without `--dry-run`; inspect the actual lock diff before accepting it. No Composer command was executed against an application.

## Implemented evidence

- A3/O11: upgrade SKILL procedure 3 -> references/20-breaking-change-detection.md:51 scoped preview/apply; both cache retry examples resume the selected command. Added capability: an executable partial-update selection procedure with transitive-major rejection and rollback, previously missing. This explains the upgrade tree's 441-byte growth; the other four changed skill trees shrink. Counts compare LF-normalized bytes to HEAD, not runtime cost.
- A4: upgrade description/procedure and architecture references/source-map.md:25 now distinguish resolution/isolation, per-symbol audit and separately planned framework migration; PHP craft SKILL:26 and laravel-best-practices.md:30 agree.
- A5: PHP SKILL:28 and upgrade references/50-runtime-verification.md:7 point to the unchanged Octane scope owner. No Octane invariants or executable harness changed.
- B1/B2: PHP laravel-best-practices.md:77 retains generic run-twice proof; RabbitMQ SKILL:84 and :147 retain explicit prefetch/default and unchanged-attempt/ack delta while routing architecture assertions to async. Async sources remain unchanged.
- B4: PHP laravel-best-practices.md:103 routes once() to Octane precedence/cache tiers. All PHP docblock rules and distinct upstream comment/test overrides remain.
- B5/O10: PHP documentation-and-artifacts.md:66 routes collection/environment production; contract-pack SKILL workflow 7, agents/openai.yaml and reference 40 coverage align. Pack delivery, parity/version/emission audit, secret provenance and full-tree scan remain owed. Missing reachable cases are gaps, never fabricated errors.
- A6 consumer portion: PHP SKILL:10, architecture SKILL:12, contract-pack SKILL:156 link the canonical pack convention. Legacy forms were normalized only in otherwise modified Markdown; metadata retains runtime-specific dollar invocation.
- Draft/compression: PHP-draft.md records pass one. Final text preserves the distinct nonqueue, driver and pack constraints; no router moved, reference retired or source annotation rule changed.

## Observed checks and limits

`python -B artifacts/skill-pack-optimization-20261018/lanes/PHP-checks.py` from repository root exited 0. It froze all seven trees plus its runner (116 files), ran repeated seven-skill fleet selectors (87 Markdown files, 375 citations, no findings; 3 informational target paths), checked UTF-8-no-BOM/LF and all relative Markdown links in the 13 changed product files (3 links), and ran exact-file `git diff --check` (0). Normal-priority sequential static work; no CPU-heavy check. Commands/output: PHP-checks.json. HEAD, deterministic sorted path+NUL+bytes hash and per-file hashes: PHP-snapshot.json.

Manual counterexample walk: a loose/transitive major is stopped before apply or rejected/restored after lock drift; a null server is decided by the Octane owner; a seeder still needs run-twice proof; queue duplicates retain unchanged attempts and ack; unreachable errors are never invented; unresolved contract version/deprecation still refuses all pack emission. These are source-contract checks, not live agent or application observations.

Diff inspection: full scoped changes plus a call-form-normalized semantic diff were inspected. One inspection helper's stdout hit Windows cp1252 on an existing arrow character; its one UTF-8 byte-output retry passed, with no product or gate change. The stale documentation contents entry was aligned before the final passing snapshot.

Not run: unchanged architecture/consumer/audit script suites, application Composer/runtime/broker tests, full-pack checks or independent review. No external effects, Beads/Git mutation or installed activation. Parent owns closure and Phase 4 acceptance.

Out-of-scope, unverified follow-up lead preserved: alaa-octane-performance references/leak-detection-harness.md, Shape A, states that refreshApplication flushes scoped bindings while a leaked singleton remains the same object. This may undermine its leak oracle; no framework source/runtime verification was performed and no fix is claimed. Parent informed; the file is unchanged.

# Independent instruction review

- Reviewer: /root/instruction_review; requested gpt-6.1-sol / medium; observed identity unknown.
- Initial verdict: CHANGES-REQUESTED. Current scoped verdict: APPROVED after re-review below.
- Candidate: HEAD 183f5c5a19daaa0c31c5aa41ce8ce2868181aa34; parent-identified scoped digest f150e8ee4dcf8a0f351de10a65ef5e38c1269c0c0006ca8189f9648fb0e8bf79.
- Source: read-only reviewer return, persisted by the parent because the role forbids artifact mutations.

Major finding: `skills/sohrab/alaa-testing-strategy/references/110-execution-resources.md:80` loses general service/process safety. HEAD orchestrator SKILL lines 142-143 forbid killing unrelated services, containers or processes and starting duplicate services when a reusable declared service exists. Both runtimes remove these clauses, while the replacement covers only browser dev servers and another worktree's server. Restore both general rules once in the canonical resource owner and add discriminating fixtures.

The reviewer inspected the approved design, instruction/compression owners, metadata/router/new references, mirrored loading/gates/generated instructions, forwarders and workflow recovery. No further actionable prose finding was reported. Checker implementation was outside this review. Live-agent obedience, installed activation and native Windows remain unproven. Independent root-gate failures are separate acceptance blockers; runtime read-only enforcement was not established.

## Re-review, 2026-10-26

The same independent reviewer returned APPROVED with no findings in the stable prose/metadata scope. Both original general service/process safeguards are restored; the Bash-prefix example preserves arguments. The existing tooling skill's exclusion sentence, new metadata and index entries retain its capability-check scope. Active checker changes, final retest and overall acceptance remain outside this verdict.

Verified SHA-256 inputs (paths relative to `skills/sohrab/`):

- `alaa-testing-strategy/references/110-execution-resources.md`: `6ddf8051fdb5ae625a950eb8b509074dfc513a113f2efca4952ffd39c2f7394b`
- `repository-tooling-capability-check/SKILL.md`: `f01bd37adbe09d714defbfbe66c59cd150682fcc458077f34e4dd0651660e3a2`
- `repository-tooling-capability-check/agents/openai.yaml`: `1ba6b1db2e83955d49c6f7290661fa7c9ed7f1e1016053e598cce08522116da2`
- `README.md`: `8c3a4e084684b27598e5ad3486a2aa3f534ec14a732468d05f9e4ede5270a8b9`
- `README.fa.md`: `d3402a38ea2dab137682956e3f5904e7a90b4d9e049336ca137594f44ca0e7ba`

## Final delta check

The same reviewer retained APPROVED after two narrow changes: the shorter metadata description preserves capability discovery, and the Docker-access recovery pointer now respects runtime-ops' declared runtime scope while retaining fallback/authority boundaries. No remaining finding in these deltas; broader foreign changes and final gates remain outside this source verdict.

- Current tooling `agents/openai.yaml`: `aeea19480e01c5f12116a802ac7a14966c4e5059ad48c25dfb93c7cc0506588f`
- Current `110-execution-resources.md`: `d8c379cdf4ce11319aa836f97f91698004c5a1a38a3c5fdfa483b6a88ac1dec0`
- Runtime boundary source at observation, `alaa-codex-runtime-ops/SKILL.md`: `2e252d48d252e0d321ceffe782ffeb9860eec33c84e56cd92311e78cf29fa869`

## Downstream pointer re-review

The same reviewer returned APPROVED for the one-paragraph Laravel-upgrade integration repair. It removes the retired Windows reference, routes through the existing owner router only within that owner's declared scope, and grants no extra authority. No upgrade logic or shell example changed. Broader upgrade policy and the foreign runtime implementation were outside this delta review.

- `alaa-laravel-upgrade-all-packages/references/40-failure-classes.md`: `337e4a84a0d74289d80c6afef6f1136c8c0e79655a285b3547ad8f7c9a45a85d`
- Runtime router `references/00-topic-map.md`: `7b0022bdbd06bacc202380c60a015f937a0e6ca75a48b0026b3627d58088f6af`

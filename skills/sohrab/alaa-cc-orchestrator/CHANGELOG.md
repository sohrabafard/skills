# Changelog

## 3.2.0

- Wired three doctrine skills into the roles that were already gated on their subjects but had no standard behind them. `alaa-architecture-critic` now reviews against `/alaa-system-design`, `alaa-test-strategist` applies `/alaa-testing-strategy`, and `alaa-performance-profiler` measures against the complexity budget `/alaa-algorithms-data-structures` owns. Each is loaded through the agent's `skills` list and named in its dispatch template, so the standard arrives with the lane rather than depending on the lead remembering it.
- Phase A now runs a design pass before implementation on three conditions the architecture critic's gate never covered — a change of data owner, a dependency added or removed between components, and a new deployable unit — so the critic reviews a design record with its decisions made instead of a plan that can only be accepted or rejected whole.
- `alaa-verifier` now names the proof level each `PASS` reached. A check run against an embedded substitute and the same check against the real engine are indistinguishable from the command line, and the level is what tells a reader whether the result needs re-running.
- Replaced the test strategist's restatement of layer placement, failure-mode ordering, and the broken-implementation challenge with a pointer to the skill that owns them, so the two cannot drift apart.

## 3.1.1

- Extended the authoring escalation criterion: the wording of these artifacts carries as much judgment as their structure. In a skill the prose is the executable logic — nothing underneath enforces what a sentence failed to say — so drafting the text is the judgment rather than the write-up of it.

## 3.1.0

- Closed a routing gap found in use: the escalation criteria were all software-shaped, so a judgment-dense lane that touched no API, boundary, migration or concurrency surface matched nothing and fell to the default implementer. Authoring or rewriting a skill, prompt, agent definition, instruction file, architecture document, or any standard other agents follow is now a named escalation criterion in its own right. The policy did not change — the criteria list now matches the policy it was always meant to serve.

## 3.0.0

Breaking revision. Re-read `references/model-effort-policy.md` before relying on any prior pin.

- Migrated off Opus 4.8 and Fable 5 entirely. Opus 5 is now the lead and the whole top tier. Opus 4.8 is superseded at identical pricing by a materially more capable model; Opus 5 reaches near-parity with Fable 5 on published coding and agentic benchmarks at substantially lower cost, which removed the argument for a fourth tier.
- Lead calibration inverted for the new flagship, which behaves opposite to Opus 4.8 on three axes. It delegates readily rather than under-spawning, so delegation guidance now caps instead of encouraging. It verifies and self-corrects without prompting, so the "add a final verification step" and "double-check your work" instructions were removed as pure cost. It runs longer and narrates more, so reports and written deliverables now carry explicit length calibration.
- Verification reframed explicitly as an authority boundary rather than redundancy, so the verifier, reviewer and specialist gates survive the removal above and are never skipped on the grounds that a lane already checked itself.
- New effort ladder with an explicit tier ceiling: Sonnet is capped at `high`, and a lane needing more changes model rather than effort. `max` is no longer a legal pin anywhere — it survives only as a named per-invocation retry after a documented failure at `xhigh`.
- Pin corrections: the implementer moved from `xhigh` to `high` under the new ceiling; the explorer rose from `low` to `medium`; the documenter stepped down from `high` to `medium`.
- Added `references/model-effort-policy.md` as the single owner of every model and effort decision, and `references/agent-catalog.md` for parity with the companion pack.
- Six new roles, each conditionally gated: `alaa-implementer-opus` (escalated implementation, now a first-class agent rather than a fragile per-invocation model override), `alaa-spec-analyst`, `alaa-adversarial-reviewer`, `alaa-api-contract-reviewer`, `alaa-dependency-auditor`, `alaa-accessibility-reviewer`. Catalog is now 21 roles.
- Reviewer now reports every finding including uncertain and low-severity ones, leaving ranking to a downstream step, and no longer carries the adversarial lens that `alaa-adversarial-reviewer` now owns.
- Added `scripts/validate_pack.py`: validates every agent's frontmatter, model and effort pin and identity line, enforces the Sonnet ceiling and the no-`max`-pin rule, checks that the skill, routing matrix and catalog agree with the agents on disk, and sweeps the whole pack for cross-runtime leaks.

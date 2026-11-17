# Agent roles by stack, exception-only returns, specialist rewrite (2026-11-17)

Beads issue: `alaa-5h8xt`. Base: `main` at `e0e1adc2`. This record is dated evidence; verify current repository facts before you reuse a conclusion.

## Request

The pack owner asked for three changes in `alaa-cc-orchestrator`, `alaa-codex-orchestrator`, the `alaa-prompting-guide` rule-writer and, where it depends on them, `alaa-workflow`:

1. Remove, or cut to one line, the fixed header that every lane return started with (agent, configured, requested and observed model and effort, and the loaded-skills list). The lead holds those facts in its dispatch.
2. Give every implementation role one stack. A role must not carry another stack's instructions.
3. Rewrite the specialist definitions: same or better behaviour with fewer words.

All writing and review lanes ran on Fable 5.2 by the owner's selection.

## Outcome

Both packs are at version 8.0.0.

- **Returns.** No definition asks for a model, effort or loaded-skills line. The lead reports each lane's pair from its own allocation record. A lane still blocks on an observable control that cannot realize the pair, and names that control.
- **Implementation roles.** Each pack ships six: `alaa-implementer` (a stack with no bound role, or an inseparable two-family lane), `alaa-implementer-go`, `alaa-implementer-laravel`, `alaa-implementer-frontend`, `alaa-implementer-haproxy` and `alaa-implementer-delivery`. The owned files select the role. The fit table still selects model and effort.
- **Retired.** Twenty definitions moved to `_to_delete/20261117-agents-by-stack/`: the roles named for a model or an effort, `alaa-implementer-infra`, `alaa-planner-high` and the Codex `alaa-reviewer-deep`.
- **Preloads.** Six Claude roles no longer preload a stack-specific skill; they load it by a stated condition.
- **`alaa-workflow`.** Read for dependents; nothing there consumed the header or named a retired role. Unchanged.

## Measured sizes

Bytes of the agent definitions, base against this change:

| Group | Claude Code pack | Codex pack |
|---|---|---|
| Implementation roles | 11 files, 110,267 to 6 files, 56,236 (-50%) | 14 files, 139,155 to 6 files, 57,162 (-59%) |
| Other roles | 23 files, 98,365 to 21 files, 86,408 (-13%) | 24 files, 107,235 to 21 files, 92,594 (-14%) |
| Managed roles | 33 to 27 | 37 to 27 |

One implementation definition: the generic role fell from 9,484 to 8,292 bytes, and a stack-bound role from about 11,000 to between 9,017 and 10,005.

Skill text that a Claude Code role preloads at the start of every run, as the sum of the `SKILL.md` sizes in its `skills:` list:

| Role | Before | After |
|---|---|---|
| `alaa-architecture-critic` | 90,113 | 30,864 |
| `alaa-reviewer` | 77,999 | 20,128 |
| `alaa-implementer-frontend` | 58,609 | 41,522 |
| `alaa-performance-profiler` | 42,536 | 21,786 |
| `alaa-test-strategist` | 39,915 | 22,008 |
| `alaa-implementer` | 39,095 | 22,008 |
| `alaa-api-contract-reviewer` | 32,300 | 13,523 |
| `alaa-release-guardian` | 30,602 | 5,281 |

## What the specialist rewrite achieved

The three lanes cut the role-specific text of a specialist by 0 to 17 percent. The structural changes produced most of the reduction, not the sentence rewrite. About 1,500 characters of every definition are shared blocks, and the rest is mostly authority limits, scope lists that a completion line measures, and output items. Three definitions grew slightly in text, because the load conditions of their former preloads now stand in the body.

A larger cut in an implementation definition needs an owner decision: the Beads `Task tracking:` block (about 1,240 characters) and the seven `Verification:` rules (about 1,600) are the largest remaining parts.

## Design decisions

| Decision | Source |
|---|---|
| Role identity is the stack; retire the model-named identities | Owner, this session |
| `alaa-implementer-haproxy` and `alaa-implementer-delivery` replace `alaa-implementer-infra`; Ansible, standalone Makefile and shell lanes use the generic role | Owner, this session |
| Retire `alaa-planner-high` and `alaa-reviewer-deep` under the same rule | Proposed in the plan; owner approved the plan |
| Preload only what the role needs without a stack condition, where practical | Proposed in the plan; owner approved the plan, with the trade-off stated |
| Keep the lane-side block on an unrealizable observable control | Proposed in the plan; owner approved the plan |

The preload trade-off: the 2026-11-14 session evidence showed that a lane skips a merely mentioned skill more often than a called one. Each condition is therefore written as a call with an observable trigger. No session evidence exists yet for the new conditions.

## Review outcome

One independent instruction review (`alaa-instruction-reviewer`, Fable 5.2) read the source diff. Verdict: CHANGES-REQUESTED, with 3 major, 12 minor and 2 groups of nits. No confirmation pass ran.

| Finding | Severity | Disposition |
|---|---|---|
| 1. Lanes on the generic role lost the generated-file, proof and unlisted-surface rules of the retired infrastructure binding | major | Repaired: the three rules are execution rules of the shared contract |
| 2. The reviewer loaded the contract and trust skills only on a condition it needs those skills to recognise | major | Repaired: the trigger lists observable diff contents |
| 3. Three new load sentences dropped the "when installed" exception | major | Repaired, with a `NOT ASSESSED` entry for an absent owner |
| 4. One Codex line still named the retired reviewer identity | minor | Repaired |
| 6. No mapping for a retired planner or reviewer identity in a resumed plan | minor | Repaired |
| 7b. The dispatch template did not tell the lead to list an incidental file and its skill | minor | Repaired |
| 8. No absence action for a skill that a binding names | minor | Repaired |
| 9. "recorded invariants" narrowed "invariants" | minor | Repaired |
| 10. The reviewer judged all Go against the kit-era clean-code skill | minor | Repaired |
| 11, 12. Two load conditions were not observable | minor | Repaired |
| 13. "Write neither in your report" could silence a block report | minor | Repaired: "unless you block on it" |
| 14. The catalog claimed that every preload is unconditional | minor | Repaired: the sentence now states what the lists hold |
| 15. Ambiguous Codex load sentence for two skills | minor | Repaired |
| 5. "high-effort workhorse" in the exceptional-model admission has lost its defining catalog row | minor | Open, item 1 below |
| 7a. No test separates an incidental file from a two-family lane | minor | Open, item 2 below |
| 13, owner question. A mismatch outside the three block causes is silent | minor | Open, item 3 below |
| 16. Wording that still says "variant" or "profile" for the single planner and for a pair | nit | Not repaired |
| 17. Ledger rows and two widened or dropped details | nit | Ledger corrected in `pruned-rules.md`; text not changed |

The reviewer did not compare old and new for every Codex TOML: it compared each new Codex body with its new Claude twin and with the ledgers.

## Validation observed

On the branch after the review repairs, each exited `0`: the four repository checkers, both orchestrators' `render_agents.py --check`, `validate_pack.py`, `check_agent_grants.py` and `check_agent_contracts.py`, the three `alaa-prompting-guide` checkers, `alaa-testing-strategy` `check_execution_contracts.py`, and the installer unit test (17 tests). No fixture, self-test or model comparison ran. A static gate proves neither installed activation nor instruction compliance.

## Records

- `pruned-rules.md`: rules removed, merged or changed by the lead, and corrections to the lane ledgers.
- `ledger-a.md`, `ledger-b.md`, `ledger-c.md`: one row per rule that a lane removed or merged.
- `lane-brief.md`: the shared dispatch contract of the three lanes.
- `tools/codex_body.py`: the helper the lanes used to read and write a Codex agent body.

## Open items for the owner

1. **"High-effort workhorse".** `references/routing-matrix.md` admits the exceptional model after "documented inadequacy of the high-effort workhorse". The catalog row that named the workhorse routes is gone. The reviewer proposes "the non-exceptional model of the lane's fit row at `high` effort or above". This changes an admission rule, so it was left for a decision.
2. **Incidental file against two-family lane.** No rule says when a foreign file is incidental. The reviewer's candidate: no acceptance criterion of the lane is about the file.
3. **Silent mismatch.** A lane blocks on three causes. An observable mismatch outside them, such as a model substituted by an allowlist, is now reported by nobody. Decide whether it is a fourth block cause.
4. **Conditional preloads that remain.** `alaa-octane-performance`, `alaa-quasar-app-vite-v3`, `alaa-golang-clean-code-principles`, the migration guardian's `alaa-partitioned-table-fk-audit` and the architecture critic's `alaa-services-contract` are preloaded although each applies by condition.
5. **Session evidence.** Remeasure skill loading by lane after a week of sessions, as the 2026-11-14 record did, to see whether the conditional calls are followed.

## Merge and install

The installed skill directories of both runtimes are symbolic links into this checkout, and agent definitions are copied. Skill text is therefore live at the merge, and the agents are live at the install. The work ran in a separate worktree so that `main` stayed unchanged until both could land together.

- Merge: `work/agents-by-stack` merged into local `main` as `0f9414ed` with `git merge --no-ff`, by the owner's instruction of this session. `main` had not moved, so the merged tree equals the gated branch tip `686137d9`. The worktree and its branch were removed. Rollback of the skills: revert that merge commit.
- Claude Code agents: `python3 scripts/install_claude_agents.py --apply`. Each of the 27 installed managed files has the SHA-256 that the 8.0.0 manifest records, and a second dry run reported 28 files unchanged, the rule-writer included. The eight retired definitions were moved to `agents-retired/20261117-agents-by-stack` under the Claude home, beside the agents directory, because that directory is scanned recursively.
- Codex agents: `bash skills/sohrab/alaa-codex-orchestrator/scripts/install-agents.sh` exited 0 with 27 definitions installed or updated; the version marker reads 8.0.0. The twelve retired definitions were moved to `agents-retired/20261117-agents-by-stack` under the Codex home. The Codex rule-writer file was copied and equals its source.
- Codex postcheck: the 27 installed files equal a fresh `check_agent_grants.py --materialize` output. `check_agent_grants.py --resolved-agents-dir` exits 1 with two findings only: `alaa-ent-specialist` and `alaa-rule-writer` are uncatalogued. Both are agents that this pack does not manage, and both were in that directory before this change.
- Installation proves file placement, not agent behaviour.

## Curation

Final scan of this engagement under `/alaa-extract-agent-lessons`: no candidate was admitted for durable memory. One promotion candidate needs an owner: the Codex postcheck that `README-fa.md` documents fails whenever an agent of another owner (the Ent specialist, the rule-writer) is installed in the same directory, so a clean install cannot exit 0. The owner is the Codex pack's `scripts/check_agent_grants.py` and `references/installation.md`.

## Not done

No push and no tag. No change to the Beads task-tracking block, the output rule or the implementer verification rules.

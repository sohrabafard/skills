# Orchestrator pair drift repair, 2026-11-15

This file records the repair of the findings in `audit.md` beside it. Both packs moved from 6.0.1 to 6.0.2. Paths are relative to `skills/sohrab/`.

Owner direction, 2026-11-15: the two packs behave identically, each difference takes the stronger side, and a mechanics difference is expressed in each runtime's idiom.

## Findings

| id | Result | Where |
|---|---|---|
| D01 | Repaired | Claude `assets/profile-wrappers.json` uses the Codex load wording in the four stack bindings. `alaa-verifier` and `alaa-instruction-reviewer` list their one skill by plain name. `references/agent-catalog.md` claims a preload only for a plain-name entry. `scripts/check_agent_grants.py` accepts a plain entry in the reach test for a role without `Skill`. |
| D02 | Repaired | Codex `agents/alaa-documenter.toml` |
| D03 | Repaired | Codex `agents/alaa-explorer.toml`, body and description |
| D04 | Repaired | Codex `agents/alaa-browser-qa.toml` uses the Claude scope paragraph and the Claude boundary-state bullet |
| D05 | Repaired | Claude `assets/implementation-contract.md` |
| D06 | Repaired | Codex `assets/planner-contract.md`, `assets/reviewer-contract.md` and 18 hand-written roles. 36 of 37 Codex roles now carry the sentence. `alaa-instruction-reviewer` is unchanged: its authority line already forbids delegation, and a second statement would duplicate the rule. |
| D07 | Repaired | Claude `SKILL.md` section 0 |
| D08 to D12 | Repaired | One union body per role in both packs: adversarial reviewer, spec analyst, dependency auditor, API contract reviewer, accessibility reviewer. D09 and D12 also share one description. D12 uses the conditional RTL wording. |
| D13 | Repaired | Both `alaa-architecture-critic` bodies |
| D14 | Repaired | Codex `SKILL.md` section 7, as the audit proposes |
| D15, D18 | Repaired | Codex `references/agent-catalog.md` |
| D16 | Repaired | Claude `references/routing-matrix.md` |
| D17 | Repaired | Both `assets/implementation-contract.md` files hold one identical passage. The Claude checker pin still matches it, so the checker did not change. |
| D20 | Repaired | Both `SKILL.md` section 4 carry the same two sentences |
| D21, D23 | Repaired | Codex `SKILL.md` |
| D22 | Repaired | Claude `SKILL.md` section 7 |
| D24 | Repaired | Codex `CHANGELOG.md` |
| D25 | Repaired | Claude `agents/alaa-security-reviewer.md` |
| D19 | Left | Mechanics. The Codex instruction reviewer reads files through shell and Git commands, which is the Codex idiom for file inspection. The Claude reviewer holds `Read`, `Glob` and `Grep`. |

## Differences that remain by design

- D06: Claude roles outside the implementation contract carry no "Start no subagent" sentence. Every Claude role omits or denies the `Agent` tool, and `scripts/check_agent_grants.py` enforces that.
- D08, D10, D11: the description strings of these three roles still differ in wording between the packs. The audit classes role descriptions as rewordings with the same obligation.
- The five union bodies differ only in the pack name, the Claude `Runtime:` line, the Codex shell-access sentence, the Codex no-subagent bullet, the Codex CodeGraph sentence, and the reviewer identity name.

## Open follow-ups

No checker logic was built for these. Each needs an owner decision.

1. Claude `scripts/check_agent_contracts.py` pins the exceptional-admission sentence. The Codex checker has no counterpart. Neither pins the three admission arms.
2. Claude `scripts/check_agent_contracts.py` checks the bounded-semantic-branch predicates. The Codex checker checks neither its bounded route nor its bug route.
3. Codex `scripts/check_agent_contracts.py` checks the Sol eligibility sentence. Claude has none, because the rule is bound to the model family.
4. Claude `scripts/check_agent_grants.py` checks every role's native tool set and rejects unapproved metadata fields. The Codex checker requires `read-only` only for the instruction reviewer and the planners.
5. Claude `scripts/check_agent_grants.py` enforces the `Agent` deny. The Codex checker has no rule for the "Start no subagent" sentence.
6. Claude `scripts/check_agent_contracts.py` runs its "dispatched-only command source widened" check only on names that end in `.toml`, so it never runs in the Claude pack.
7. Claude `scripts/check_agent_grants.py` accepts a `/name` entry as reach for a role without `Skill`, although such an entry preloads nothing. The plain form on `alaa-verifier` and `alaa-instruction-reviewer` is an authoring rule that no checker enforces.
8. No checker compares a Claude role body with its Codex counterpart. The union bodies were compared once with a scratch script.
9. Every other `/name` entry in a Claude `skills:` list still preloads nothing. Conversion stays an owner cost decision.
10. Codex `agents/alaa-browser-qa.toml` writes `$playwright`. The Claude role writes `/playwright`.
11. The module docstring of Claude `scripts/check_agent_grants.py` still says that `skills:` preloads the doctrine of a role.
12. The Codex runtime may or may not block nested spawning. The repair adds the instruction and proves no enforcement.
13. Installed copies under the user's agent directories were not updated. An install needs its own authorization.

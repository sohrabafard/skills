# Baseline

Measured on `work/core-skills-compression` at b5671a13, 2026-11-16, with `measure.py` in this directory.

| Skill | Frontmatter | SKILL.md body | References | Assets | Hand-written agents | Generated agents | Other | Source total |
|---|---|---|---|---|---|---|---|---|
| `alaa-testing-strategy` | 112 | 3986 | 14635 | 0 | 0 | 0 | 240 | 18973 |
| `alaa-cc-orchestrator` | 102 | 2564 | 14370 | 4270 | 13324 | 19091 | 27 | 34657 |
| `alaa-codex-orchestrator` | 101 | 2554 | 14757 | 4977 | 12270 | 23862 | 608 | 35267 |
| `alaa-workflow` | 113 | 1116 | 16389 | 1800 | 0 | 0 | 31 | 19449 |
| `alaa-code-intelligence-routing` | 105 | 753 | 9273 | 0 | 0 | 0 | 47 | 10178 |
| `alaa-low-noise` | 77 | 965 | 1604 | 0 | 0 | 0 | 29 | 2675 |
| `alaa-prompting-guide` | 89 | 797 | 36913 | 4507 | 0 | 0 | 49 | 42355 |

Source total, all seven skills: 163554 words. Generated agents, CHANGELOG.md and scripts are excluded from it.

| Checker | Tuple | String constants |
|---|---|---|
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `EXECUTION` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `RESOURCES` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `CLASSIFICATION` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `REQUIREMENTS` | 213 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `NORMATIVE_DUPLICATES` | 105 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `EXPECTED_NORMATIVE_INVENTORY_SHA256` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `CONTRADICTIONS` | 19 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `EQUIVALENT_REQUIREMENTS` | 6 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `BOUNDED_REQUIREMENTS` | 14 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `IMPLEMENTER_REQUIREMENTS` | 17 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `GATE_REQUIREMENTS` | 24 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_MODEL_CLAUSES` | 3 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_REQUIREMENTS` | 12 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `CADENCE_REQUIREMENTS` | 36 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_REQUIREMENTS` | 17 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_SEAMS` | 28 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_CONTRADICTIONS` | 11 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_REQUIREMENTS` | 29 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_CONTRADICTIONS` | 7 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `EQUIVALENT_REQUIREMENTS` | 6 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `BOUNDED_REQUIREMENTS` | 14 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `IMPLEMENTER_REQUIREMENTS` | 16 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `GATE_REQUIREMENTS` | 24 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_MODEL_CLAUSES` | 4 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_REQUIREMENTS` | 12 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `CADENCE_REQUIREMENTS` | 36 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_REQUIREMENTS` | 17 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_SEAMS` | 28 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_CONTRADICTIONS` | 11 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_REQUIREMENTS` | 29 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_CONTRADICTIONS` | 7 |

## Gate results before any edit

| Gate | Exit |
|---|---|
| `.: python3 -B scripts/validate_sohrab_skill_pack.py` | 0 |
| `.: python3 -B scripts/check_skill_index.py` | 0 |
| `.: python3 -B scripts/check_fleet_references.py` | 0 |
| `.: python3 -B scripts/check_lifecycle_contract.py` | 0 |
| `skills/sohrab/alaa-testing-strategy: python3 -B scripts/check_execution_contracts.py` | 0 |
| `skills/sohrab/alaa-cc-orchestrator: python3 -B scripts/render_agents.py --check` | 0 |
| `skills/sohrab/alaa-cc-orchestrator: python3 -B scripts/validate_pack.py` | 0 |
| `skills/sohrab/alaa-cc-orchestrator: python3 -B scripts/check_agent_contracts.py` | 0 |
| `skills/sohrab/alaa-cc-orchestrator: python3 -B scripts/check_agent_grants.py` | 0 |
| `skills/sohrab/alaa-codex-orchestrator: python3 -B scripts/render_agents.py --check` | 0 |
| `skills/sohrab/alaa-codex-orchestrator: python3 -B scripts/validate_pack.py` | 0 |
| `skills/sohrab/alaa-codex-orchestrator: python3 -B scripts/check_agent_contracts.py` | 0 |
| `skills/sohrab/alaa-codex-orchestrator: python3 -B scripts/check_agent_grants.py` | 0 |
| `skills/sohrab/alaa-prompting-guide: python3 -B scripts/check_rule_writer_grants.py` | 0 |
| `skills/sohrab/alaa-prompting-guide: python3 -B scripts/check_claude_model_policy.py` | 0 |
| `skills/sohrab/alaa-prompting-guide: python3 -B scripts/check_codex_model_policy.py --agent-root assets/rule-writer/codex` | 0 |

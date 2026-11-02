# Checker lane evidence

Outcome: scoped implementation and focused validation passed; independent review and integrated gates remain pending.
Actor: `codex:01a1747c:checks`; issue: `alaa-xw5h.1.3`.
HEAD: `183f5c5a19daaa0c31c5aa41ce8ce2868181aa34`.
Scoped SHA-256: `f10812a6195e584a5579527102afc6de5701da5fc1104f6b71296a20d30a601b`.
Manifest and method: `checker-tested-manifest.sha256`, `checker-tested-snapshot.json`; 279 regular files in the five recorded skill scopes, including untracked scripts, excluding bytecode. Snapshot verified unchanged after the contract checks; POSIX probes write only synthetic temporary fixtures.

## Changed files and decision

Both runtime `scripts/check_agent_contracts.py` consume canonical generic assertions while retaining runtime authority/cadence seams. Both `scripts/validate_pack.py` resolve canonical policy/runners and browser preservation. Testing strategy owns `scripts/check_execution_contracts.py` and `scripts/test_execution_runners.py`. Both renderer-owned agent projections/manifests were regenerated through their owning scripts only.

The single authorized polarity repair removes only the complete explicit negative review prohibition from normalized matching text before applying the unchanged forbidden patterns. Three negative variants and two positive variants distinguish accepting the prohibition from suppressing a conflicting positive instruction. No assertion or gate was removed by this repair.

## Final focused evidence

All commands below ran from repository root (`.`), sequentially in WSL. No CPU-heavy designation or additional runner/cap was supplied for these bounded commands. No native Windows command was run during the repair.

| Exact command | Exit | Observed result | Log |
|---|---|---|---|
| `python3 -B skills/sohrab/alaa-testing-strategy/scripts/check_execution_contracts.py --self-test` | 0 | 945 structural mutation fixtures | `execution-contract-self-test-polarity-fix.txt` |
| `python3 -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py --self-test` | 0 | 1677 structural fixtures, including shared fixtures and polarity cases | `codex-contract-self-test-polarity-fix.txt` |
| `python3 -B skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py --self-test` | 0 | 1620 structural fixtures, including shared fixtures and polarity cases | `cc-contract-self-test-polarity-fix.txt` |
| `python3 -B skills/sohrab/alaa-testing-strategy/scripts/test_execution_runners.py --platform posix` | 0 | 12 subprocess probes across canonical runner and both adapters, spaced paths/external cwd, argv/environment/stdout/stderr, success/nonzero exits and original help rejection | `posix-runner-smoke-polarity-fix.txt` |

Both repaired Python sources compiled through `compile()` without bytecode; the earlier six-file syntax check also passed. The two-file repair diff and prior complete lane diff passed `git diff --check`. Issue lint passed. Earlier unchanged renderer inputs passed both `render_agents.py --write` and `--check` (34/30 outputs); both `check_agent_grants.py` calls passed (33/29 roles). Generator and grant source code was not modified.

## Coverage and limits

The canonical checker covers body/router/consumer pointers (including broken prefixes/suffixes), each generic policy clause, conflicting old policies with positives retained, selection versus execution, collection/early repair/full-list retest, resource allocation/timing dispersion and workflow liveness/ownership recovery. The 62-row `checker-legacy-assertion-inventory.md` maps removed/moved legacy assertions. Runtime self-tests include the shared fixtures; do not count those common fixtures as independent behavioral proof or dispatch them again merely to inflate coverage.

No pack aggregate, repository-wide suite or independent acceptance gate ran in this lane. Structural fixtures prove source contracts, not live-agent compliance. Native Windows behavior is unverified: earlier attempts stopped at WSL startup/execution policy before runner probes; those historical failures remain in their original logs. No host policy change, bypass, installation, commit or publication occurred. User-owned source/index hashes remained unchanged.

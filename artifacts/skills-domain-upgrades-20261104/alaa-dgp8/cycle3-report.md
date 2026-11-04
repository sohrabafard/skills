# Authorized quoted-name repair

The user authorized one additional repair and independent review cycle after the blocked
`0f8348f2` candidate. The scope is the confirmed phantom CREATE declaration. Only the checker
and its CLI test changed. The [manifest](cycle3-source.sha256) identifies the frozen source and
unchanged runtime proof inputs.

The outer lexer already supplies one statement slice starting at its first token. Anchor the
CREATE TABLE match to that position. A valid-looking declaration inside an unsupported quoted
table name cannot substitute for the real name. The checker reports CH011 and exit 2. A
subsequent real declaration in the same file remains checked. The existing grammar still admits
ordinary quoted qualified names.

## Focused evidence

Host commands ran from the skills root using Python 3.14.4 and one sequential worker. The WA
audit ran from the read-only WA worktree.

| Check | Command or evidence | Observed result |
| --- | --- | --- |
| Discriminating regression | `python3 -B -m unittest discover -s skills/sohrab/clickhouse-performance-schema-ops/scripts -p test_review_clickhouse_ddl.py -k cycle3 -v` | [Before repair](cycle3-regression-before.txt) exited 1 because the checker returned 0 instead of 2. [After repair](cycle3-regression-after.txt) exited 0, one method with poisoned-only, mixed-bundle and valid quoted-name cases. |
| Exact reported fixture | `python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py artifacts/skills-domain-upgrades-20261104/alaa-dgp8/blocked-quoted-name.sql` | Original [exit 0](blocked-quoted-name-result.json) retained. Identical fixture hash now produces [CH011 and exit 2](cycle3-quoted-name-result.json). [Output](cycle3-quoted-name-output.txt). |
| Bounded task CLI suite | `python3 -B -m unittest discover -s skills/sohrab/clickhouse-performance-schema-ops/scripts -p test_review_clickhouse_ddl.py` | Exit 0, [24 methods](cycle3-unittest.txt). |
| CLI help | `python3 -B skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py --help` | Exit 0. [Output](cycle3-help.txt). |
| Negative controls | Same isolated mutations and selectors as [initial author evidence](report.md). | Both expected exit 1. [Index exemption](cycle3-control-blanket-exemption.txt), [omitted dimension](cycle3-control-missing-dimension.txt). |
| WA checkpoint | [No-install invocation](report.md#wa2-continuation-draft), [input hashes](cycle3-wa-identities.tsv). | [Exit 2](cycle3-wa-checker.txt), 32 findings and four proof gaps. Byte comparison to cycle 2 exited 0. The [finding disposition](wa-disposition.md) still applies. |
| Scoped whitespace | `git diff --check -- skills/sohrab/clickhouse-performance-schema-ops artifacts/skills-domain-upgrades-20261104/alaa-dgp8` | Exit 0. [Output](cycle3-scoped-diff.txt). |

The runtime fixture and cancellation probe have the same hashes as the independent 24.8
verification inputs. No Docker process was started for this lexical repair. See the
[independent verification ledger](../checker-verification/cycle2/commands.tsv) and
[probe identity](../checker-verification/cycle2/cancellation-after.sha256). Cancellation during
Docker creation and current 26.x runtime remain outside the observed proof.

The input files at WA worktree HEAD `3a86419f3244b6597b86ee24bf4781e3721d1d5d` remain
byte-identical to checkpoint `cfa54adac0bea630beaa0ff2789ba772d016b37c`. No WA state was
mutated. The parent owns independent retest, correctness and security review, commit and issue
closure. The extra cycle grants no further repair authority.

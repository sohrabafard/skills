# Operations implementation evidence

> Citation notation: `<repo>/` denotes this repository root; resolve it before invoking a command. Path lists use this display prefix only; strip it when reproducing a recorded hash manifest. [Original exact evidence](./operations-evidence.raw.txt.gz) preserves the pre-normalization text.

Status: all six assigned skills implemented and source-frozen; independent Bash,
security, release, observability and instruction gates pending.
AGENT: operations_implementation; configured alaa-implementer-sol / gpt-6-astra / high;
requested override: none; observed runtime identity: unknown.

## Authority and continuity

Parent WRITE RELEASE authorized six operations skill directories and this evidence family.
No install, live cluster/API operation, credential issuance, commit, staging or push occurred.
Other lanes and the index were preserved. Local workspace-write sandbox is observed;
role scope is narrower than the sandbox. Other enforcement details are unknown.
Read the parent plan/checkpoint and operations-research.json before resuming.
The staged-plus-unstaged source selection is git diff HEAD plus untracked files.
`operations-source.sha256` records all six domains, including untracked source.
`operations-source.diff` captures tracked staged-plus-unstaged changes against HEAD;
untracked source bytes remain at the hashed paths.

## Read and authoring coverage

Complete Docker bundle read: SKILL, all 14 references, all seven script/library files,
all shipped fixtures and agents/openai.yaml. Complete Arvan bundle read: SKILL,
references, scripts, fixtures, assets and agent metadata. The raw OpenAPI JSON was
intentionally excluded from direct reading per the skill's specific summarizer rule.
No model-specific policy duplicated; policy remains owned by alaa-prompting-guide.
Each instruction change was drafted around its predicate, authority, failure state,
compatibility and evidence requirement, then compressed without weakening those fields.
The three Docker correctness changes were discovered during full reading and explicitly
added to scope by parent; no new tuning mandate or consumer floor was introduced.

## Implemented invariants and design

- Docker Engine29.8.1 / Compose5.5.1 are dated upstream observations (2026-09-29).
  Other ledger rows retain their historical date. Executable --versions matches the ledger.
  Official image tags exist, but examples retain prior pins without compatibility proof.
- Compose file secrets are host-backed bind mounts; uid/gid/mode fields are ignored for
  file sources. The example removes those misleading fields and requires effective access proof.
- Swarm host publishing bypasses routing mesh but is not loopback isolation; infrastructure
  stays unpublished absent a verified approved network boundary.
- Go1.25+ cgroup-aware GOMAXPROCS replaces the unconditional manual integer-quota mandate;
  runtime/module defaults and overrides still require inspection.
- Arvan discovery cannot infer version/scope from absence or permission from a visible kind.
  Required discovery failure or ambiguous permission returns2; actual missing/denied capability1.
  Unknown server version is explicit; server-only /version is queried separately.
- Optional runner ServiceAccount preserves NS [runner-sa] CLI but now requires an already
  authenticated matching auth-whoami principal. Unavailable/mismatch blocks2, with no token
  mint or impersonation fallback. No runner argument proves only caller permissions.
- Render output is newly created with restrictive umask, chmod600 and mode verification before
  Helm. Existing --out files/symlinks are refused, never truncated. Failure leaves no rendered bytes.
  Tests use synthetic mocks; no real cluster, Helm render, credentials or Secret data were used.

Rejected alternatives: API-absence version inference; catalog-as-authorization; automatic token
issuance; silently ignored chmod; replacing image pins from release numbers; raising Ansible floors.
CLI behavior transitions are documented in the owning skill/references/operator templates.

## Focused verification observed

1. Docker check-image-pinning.mjs --self-test: exit0, 11 assertions.
2. Docker check-image-pinning.mjs --versions: exit0, refreshed rows dated2026-09-29,
   unchanged rows dated2026-07-29. Version output inspected.
3. python -B <repo>/scripts/check_fleet_references.py --skill alaa-docker-production --skill
   caas-arvan-kuber: initial failure from one new section-sign encoded with Windows default;
   repaired that byte and verified both entire bundles decode UTF-8, then one retry exit0:
   2skills,22Markdown files,156citations, no findings,10 informational target paths.
4. git diff HEAD --check -- both owned paths: exit0; no untracked source paths.
5. Bash syntax attempt, default PowerShell invoking explicit Git Bash path: exit1 before
   parsing, signal-pipe Win32 error5. One escalated retry used Git Bash outer shell but an
   unqualified inner bash; WSL /bin/bash missing, exit1. No syntax success is claimed.
   Diagnostic lane received both exact commands; independent verifier owns final supported launch.
6. Native ShellCheck initial exit1 from CRLF artifacts. One repair normalized scripts to LF;
   retry exit1 for unused SCRIPT_DIR and two unquoted substitutions. Those source findings were
   fixed, but no further retry was run. Final ShellCheck is UNVERIFIED, not PASS.
7. New Arvan verify-cluster20-case and render-helm9-case mocked self-tests, Bash syntax,
   shfmt and OpenAPI summarizer checks remain UNRUN by this lane. Final independent gate required.

Exact failed syntax commands:
- PowerShell: & <Git>/bin/bash.exe -n <repo>/skills/sohrab/caas-arvan-kuber/scripts/verify-cluster.sh
  <repo>/skills/sohrab/caas-arvan-kuber/scripts/render-helm.sh
- exec shell=<Git>/bin/bash.exe, login=false, escalated: bash -n
  <repo>/skills/sohrab/caas-arvan-kuber/scripts/verify-cluster.sh
  <repo>/skills/sohrab/caas-arvan-kuber/scripts/render-helm.sh

No CPU-heavy operation executed; final heavy gates must use the orchestrator low-priority runner
with BelowNormal and CpuCount2. Full runtime/deployment proof is absent and was not authorized.

## Official sources observed 2026-09-29

- https://docs.docker.com/engine/release-notes/29/ :29.8.1 released2026-09-15.
- https://github.com/docker/compose/releases :5.5.1 released2026-09-03.
- https://raw.githubusercontent.com/docker-library/official-images/master/library/docker :
  29.8.1-cli and29.8.1-dind exist; existence does not prove consumer compatibility.
- https://docs.docker.com/reference/compose-file/services/#secrets :file source fields ignored.
- https://docs.docker.com/engine/swarm/services/#publish-a-services-ports-directly-on-the-swarm-node
- https://go.dev/doc/go1.25#runtime :container-aware default, updates, explicit override limits.
- https://kubernetes.io/releases/ :supported upstream1.37/1.36/1.35, not Arvan vendor proof.
- https://kubernetes.io/docs/tasks/administer-cluster/enable-disable-api/
- https://kubernetes.io/docs/reference/access-authn-authz/authorization/
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_auth/kubectl_auth_whoami/

## Remaining four domains: prepared evidence, not implementation

Full SKILL entrypoints read; selected references read only. Complete bundle prerequisite pending.
- GitLab19.4 stable: https://docs.gitlab.com/releases/19/gitlab-19-4-released/ . Preserve old
  helper/Runner snapshot as historical; verify exact Runner19.4 source before claiming it.
- HAProxy https://www.haproxy.org/ lists3.4.6,3.3.16,3.2.25,3.0.29,2.8.30 (Sep28),
  2.6.34 (Sep24);3.5-dev7 is preview. Preserve historical runtime checks and example3.4.1 pins.
  SOURCES and version-reference prose incorrectly calls all3.1-and-below unsupported despite
  supported3.0/2.8/2.6 rows; correct that after full read.
- https://packages.clickhouse.com/ now stable26.9.5.2 / LTS26.8.14.3 (Sep28), superseding
  operations-research.json26.9.4.3/26.8.13.2 historical observation. SigNoz0.143.0 chart collector
  0.144.11 and bundledClickHouse25.12.5 remain separate; no consumer floor or alert proof change.
- https://pypi.org/project/ansible-core/ :2.21.4 stableSep8;2.22b1 preview.
  https://pypi.org/project/ansible/ :14.4.0 stableSep8;15alpha preview.
  https://docs.ansible.com/projects/ansible/latest/porting_guides/porting_guide_core_2.21.html :
  custom module/action results must explicitly mark failure (failed:true/fail_json/exception),
  rc-only inference is deprecated, warning begins2.22, not already removed. Preserve requirements
  floors; old dated comment is a historical observation, not a constraint to raise.

## Residual review questions

Arvan ServiceAccount proof intentionally blocks old/denied whoami; this is documented instead of
silently substituting operator proof. POSIX0600 may be unverifiable on Windows filesystems and
must remain blocked. Explicit output-directory trust and race behavior merit security review.
No finding was converted into an approval to mutate live services or mint credentials.

## Continuation checkpoint: four more bundle states

- SigNoz full bundle completed (76 files); alaa-signoz-clickhouse-docs/references/90-versions.md upstream release row
  refreshed only. Fleet-reference check exit0, diff check exit0. Bundled version, floor,
  local runtime proof and historical September26 entries preserved.
- GitLab full bundle completed (35 files before two new fixtures); six references plus
  validate_gitlab_ci.py and two synthetic fixtures changed. Full-read occurred before edits.
  Official September29 sources: https://docs.gitlab.com/releases/19/gitlab-19-4-released/
  (19.4 released September17), https://docs.gitlab.com/ci/yaml/workflow/ (no match creates no
  pipeline), https://docs.gitlab.com/api/resource_groups/ (project scope),
  https://docs.gitlab.com/ci/resource_groups/ (four queue modes, no implicit discard),
  https://docs.gitlab.com/ci/yaml/ (variable paths, compare_to support from17.2).
  rules-path-var identifier retained but severity changed warning->note: this checker cannot
  resolve external variable scope. No expansion is attempted; undefined changes variables
  can remain literal. Supported list/mapping/exists/compare_to and independent bad rules:if
  fixtures discriminate against rejecting all variables or suppressing unrelated findings.
  `python skills/sohrab/alaa-gitlab-ci-cd/scripts/validate_gitlab_ci.py --self-test`: exit0,
  10 fixtures. Scoped git diff HEAD --check: exit0. One read command named a nonexistent
  feature-version-matrix.md; exact inventory resolved feature-version-notes.md, read in full.
- HAProxy full bundle completed (all references, examples, scripts, fixtures and metadata).
  Six files changed: branch/source ledger, core mechanics, QUIC, companion, canary comment.
  https://docs.haproxy.org/3.4/configuration.html checked September29: timeout queue inherits
  timeout connect; map indexing depends on matching; limited-quic requires compiled compat
  support and manual distinguishes OpenSSL before/after3.5.2. Historical3.4.0 runtime proof
  unchanged; example3.4.1 pins unchanged without new runtime compatibility proof.
  `python skills/sohrab/alaa-haproxy/scripts/check_examples.py --structure-only`: exit0,
  20 configs, zero findings, parsed0. Scoped git diff HEAD --check: exit0.
- Ansible full-read IN PROGRESS: SKILL, requirements, source-map, module_alternatives read;
  all other bundle files still pending. No Ansible edits yet.

Draft/compression comparison for these additions retained each owner, version context,
unknown-state boundary, public checker identifier and historical validation date. Removed only
redundant slash/dollar pairs in touched prose. No minimum dependency increase or live action.

Independent review finding: HAProxy alaa-haproxy/references/80-gate-register.md final paragraph treats all
parser warnings as future-only; check_examples.py prints warnings as notes. A warning such as
an ACL that can never match may invalidate a required control today. Recommend documented
warning classification and explicit required-control review, not blanket acceptance; script
policy change was not made in this lane. Also note historical examples claim3.4.2 validation
while source log records3.4.0; neither was relabeled as newly observed runtime proof.

## Final frozen checkpoint

- [x] Full six-domain bundle reads complete before each domain's edits. Ansible remaining
  scripts/libraries, metadata/assets, all fixtures and the vendored integration fixture read;
  one truncated output was completed with the exact replication.yml file. No fixture refreshed.
- [x] Ansible 2.21.4/core and 14.4.0/community observed September29, released September8;
  previews excluded. Historical tool facts and requirements floors preserved.
- [x] Custom module/action results explicitly report failed state; rc inference is deprecated,
  with warnings starting2.22. Source: official core2.21 porting guide already cited above.
- [x] Parent-authorized security expansion completed in Ansible: common.sh default bootstrap
  disabled; AV_ALLOW_BOOTSTRAP=1 requires prior installation authority; AV_NO_BOOTSTRAP wins.
  No mkdir/pip is reachable through bootstrap before that opt-in. Existing CLI flags preserved.
- [x] scan_secrets.sh retains categories/severity/count accumulator/JSON shape, redacts source
  matches to path/line in text, and no longer teaches a secret literal in shell history.
- [x] test_role.sh counts dependency, prepare and destroy failures; teardown still attempted.
  Missing executables remain blocked. No false inference that nonzero means an absent stage.
- [x] Added test_security_regressions.py: four test methods with subcases for opt-in/override,
  blocked tools, six credential sentinels/file/directory/JSON, and mocked Molecule failures.
  No real driver, Python installer, Ansible or network command is used by its test fixtures.
- [x] Fixture-refresh documentation requires authorized scoped retirement and size preservation.
- [x] Final draft/compression review preserves authority, exit codes, compatibility and ownership.
- [x] AST parse of new Python harness exit0; six-scope git diff HEAD --check exit0.
- [x] Six-skill fleet check exit0:94 Markdown files,412 citations,zero findings,27 informational
  target paths. No fixture/runtime verdict inferred from that structural check.
- [ ] Independent Bash syntax, Arvan20+9 self-tests, final ShellCheck, and Ansible harness execution.
- [ ] Independent instruction/security/release/observability review and parent combined gates.

Additional official sources checked September29:
- https://pypi.org/project/ansible-core/
- https://pypi.org/project/ansible/
- https://docs.ansible.com/projects/molecule/workflow/
- https://docs.ansible.com/projects/ansible/latest/vault_guide/vault_encrypting_content.html

Observed focused result totals: Docker11 self-test assertions and versions inspection;
GitLab10 fixtures; HAProxy20 configs checked structurally,zero runtime parses; final fleet
94 Markdown/412 citations; new Python harness AST valid. Prior failures remain recorded above.
No aggregate runtime pass is asserted: Arvan29 cases and Ansible4 methods remain unexecuted.
Inspection/help/source-read calls are not test runs. No source write after this checkpoint.

## Independent verifier commands (not run by this lane)

Resolve an installed Git Bash executable explicitly, and set child PATH to its tool directory;
do not use an unqualified child bash that can resolve to WSL. Run each syntax command separately.
Replace $gitBash/$shellcheck/$python only with observed installed executable paths. For CPU-heavy
runs use Invoke-AlaaLowPriority.ps1 -Priority BelowNormal -CpuCount 2 -TimeoutSeconds 60 with
-FilePath and -ArgumentList below; never install missing tools. A missing interpreter blocks.

```powershell
& $gitBash -n <repo>/skills/sohrab/caas-arvan-kuber/scripts/verify-cluster.sh
& $gitBash -n <repo>/skills/sohrab/caas-arvan-kuber/scripts/render-helm.sh
& $gitBash -n <repo>/skills/sohrab/ansible-validator/scripts/lib/common.sh
& $gitBash -n <repo>/skills/sohrab/ansible-validator/scripts/scan_secrets.sh
& $gitBash -n <repo>/skills/sohrab/ansible-validator/scripts/test_role.sh
& $gitBash <repo>/skills/sohrab/caas-arvan-kuber/scripts/verify-cluster.sh --self-test
& $gitBash <repo>/skills/sohrab/caas-arvan-kuber/scripts/render-helm.sh --self-test
& $shellcheck -x -P SCRIPTDIR <repo>/skills/sohrab/caas-arvan-kuber/scripts/verify-cluster.sh <repo>/skills/sohrab/caas-arvan-kuber/scripts/render-helm.sh <repo>/skills/sohrab/ansible-validator/scripts/lib/common.sh <repo>/skills/sohrab/ansible-validator/scripts/scan_secrets.sh <repo>/skills/sohrab/ansible-validator/scripts/test_role.sh
& $python <repo>/skills/sohrab/ansible-validator/scripts/test_security_regressions.py --bash $gitBash
```

Compatibility transitions: caller-SA proof can block on unavailable whoami; rendered --out must
be new and POSIX0600 provable; Ansible automatic installation is now opt-in; previously swallowed
Molecule errors now fail. Rollback must not restore credential minting, source-secret logging,
or false PASS. Historical image pins and actual dependency floors are unchanged.

Frozen source count: 43 (42 tracked delta paths, 1 untracked).
Per-domain counts: alaa-docker-production:6, alaa-gitlab-ci-cd:9, alaa-haproxy:6, alaa-signoz-clickhouse-docs:1, ansible-validator:10, caas-arvan-kuber:11.
Source hash manifest SHA256: 895cc928ea03a3fd468350d481efe02a41b42ee64e5af8f9f3d89656f5bcc7bb.
Tracked diff SHA256: 09dfacf50f69462b186945c15cac547e741898da55abb0e22584556679ea42d1.

## Exact patch preservation

The diff pointer now routes to [losslessly compressed original patch bytes](./operations-source.diff.gz). The uncompressed hash and size are recorded in [encoding metadata](./patch-evidence-encoding.json). Original whitespace is preserved on decompression; no patch line or source file was trimmed to satisfy Git whitespace checks.

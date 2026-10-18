# PLATFORM source decisions

Source dispositions below were ratified by the parent before implementation. Implementation evidence follows the original decision record.

## Controls and authority

- AGENT: alaa-implementer. Plan allocation: gpt-6.1-sol / medium, grounded platform/resource and validator-owner reconciliation. Source and installed role definitions carry neither model nor effort pins. Requested pair: gpt-6.1-sol / medium. Observed serving pair: unknown; no observable mismatch.
- Active sandbox: workspace-write; repository and visualization writable roots. Parent scope is narrower: eight assigned skill directories and PLATFORM evidence only. MCP grants do not prove enforcement. No subdelegation, installation, live cluster/runner actions, sibling edits, Git effects, global configuration or memory writes.
- Markdown evidence owner: native text/JSON inspection under alaa-code-intelligence-routing. The immutable intake snapshot, not edited report queues, supplies proposal text. The plan and current routing matrix admit normal semantic implementation; mechanical/Luna admission is inapplicable.

## Proposed dispositions

Paths below are relative to `skills/sohrab/` unless prefixed otherwise. Anchors identify the current intake source, not future line positions.

| Item | Verdict | Source evidence and proposed complete change |
|---|---|---|
| 01:A1 | ADAPT | `caas-arvan-kuber/SKILL.md:10` is the narrow load test; its source precedence remains intact. Repair `alaa-haproxy/references/90-companion-boundary.md:29` and `alaa-docker-production/references/90-companion-boundary.md:30` to route Arvan-specific facts through that test; remove Docker's false delegation of GitLab rollout mechanics. Generic manifests remain with k8s-helm and runner mechanics with gitlab-ci-cd. Root README/README.fa routing edits belong to parent integration, outside this lane. No Arvan platform contract changes. |
| 01:A2, 02:O12 | ACCEPT pointer alternative | `ansible-generator/references/playbook.md:226-253` already supplies all five checks, exit-2 blocking, exemptions and bounded failure loop. `SKILL.md:42-46`, best-practices A13 and the section-7 Checks line omit module currency. Replace duplicate lists/acceptance text with section-6 pointers; delivery reports every command/result from that section. Keep module currency as its own command: validator `validate_playbook.sh` explicitly owns three parse/lint stages, while validator `references/playbook.md` separately owns currency stage 5. No executable gate expansion or script edit is necessary. |
| 01:A40 | ACCEPT | Docker `SKILL.md` rule 2 merges final-image posture with runtime keys. Split its citation: non-root USER and absent build tooling to `references/10-dockerfile-authorship.md`; cap_drop, security_opt and read-only root with writable mounts to `references/20-compose-authorship.md` section 6. Keep every existing obligation and unmet-item reporting requirement. |
| 01:A47 | ADAPT | HAProxy/Lua completion blocks use undefined materially different retry. Define the operational distinction once in HAProxy gate register: a retry changes the cause-relevant prerequisite or execution path and tests the same failed property; repeating an unchanged command is not different. Point Lua to that definition; preserve one repair/one retry and authority limits. GitLab `pipeline-authoring/10-pipeline-creation-and-paths.md:23-35` already explains explicit fallback but never names terminal arm. Name it there as the final unconditional rule (`when: never` or deliberately `always`), and point the body there. Preserve mandatory workflow fallback versus optional job fallback. |
| 01:A48 | ADAPT | k8s-helm `SKILL.md:26` already requires affirmative authorization. Add explicit unavailable/unreachable proof behavior there: state unknown/assumption, emit only independently valid namespaced resources, and report a required cluster-scoped dependency blocked. Never replace a CRD/ClusterRole/StorageClass with a namespaced lookalike or imply the incomplete chart can deploy. No cluster observation or deployment is needed for this instruction repair. |
| 02:O16 | REJECT optional trimming | Historical passages are on-demand; they preserve concrete failure rationale and retired-rule provenance. Deleting them produces no required capability and creates a retirement/archive scope expansion. Preserve them. A2's gate-list consolidation still removes actual contradictory duplication. No history relocation to outputs is proposed. |
| 02:O17 | ADAPT | `check-image-pinning.mjs:61-138` is a local dated register; `--versions` prints it without fetching. `references/00-source-map.md:21` calls the printer a freshness procedure. Correct that claim and Dockerfile section 5: the table is a dated snapshot; printer locates per-row official sources/dates; verify those primary sources before choosing/changing a current default. Do not re-date observations, assert current upstream versions or change image pins from printer output. No checker behavior change. |
| 03:N1, 03:V7 | ADAPT existing owner | The runner reference covers executor/configuration/RBAC, not the Compose hosting handoff. Add a small conditional runner-container section there: identify the host/container/executor boundary, persistent config location, authentication-token source and TLS trust decision; keep Compose expression with Docker reference 20 and host-specific bootstrap scripts in the consumer repository. Do not invent three universal TLS modes, a no-spaces platform rule, scripts or a new skill. Add the trigger to its existing topic-map row; no second router. |
| Cross-owner 01:A46 | LIMITED ADAPT | Only substantively changed SKILL descriptions may gain a leading noun phrase. Preserve every capability, trigger, negative and named alternative. No description sweep, checker or metadata change. Apply the parent's central authoring decision; no local description policy. |

## Official evidence checked 2026-10-18

- [GitLab runner container installation](https://docs.gitlab.com/runner/install/docker/): runner configuration needs persistent storage; container hosting is separate from job execution. This establishes a portable handoff gap, not a tested Compose bootstrap.
- [GitLab runner custom CA guidance](https://docs.gitlab.com/runner/configuration/tls-self-signed/): use the documented trust paths for the actual runner/job context. Consumer mode labels are not GitLab API names.
- [GitLab workflow rules](https://docs.gitlab.com/ci/yaml/workflow/): workflow controls creation before jobs; final unconditional fallback is deliberate. No GitLab release number or new feature claim is introduced.
- No new upstream image-version fact is needed for O17's provenance correction. Existing dated version values remain historical evidence; their current accuracy is unverified.

## Ratification checks and implementation constraints

Before skill edits, finish full reads of each changed skill's SKILL, references and scripts under pack AGENTS; inspect assets only where they constrain the change and preserve the machine-only OpenAPI no-open rule. Inspect exact call sites and keep every external router. Draft changed controlling paragraphs, then apply ref60's behavior-preserving rewrite. Record counterexamples: generic Arvan task stays generic; Arvan-only admission adds platform owner; currency cannot be skipped; unavailable proof never authorizes cluster objects; an unchanged failed command does not qualify for the allowed materially different retry and must not be repeated; workflow and job fallback remain distinct; local printer never refreshes provenance; container runner does not imply Docker executor.

Proposed bounded task acceptance, repository root, ordinary serial low-cost execution (no CPU-heavy checks):

1. `python -B scripts/check_fleet_references.py --skill caas-arvan-kuber --skill alaa-docker-production --skill alaa-haproxy --skill alaa-haproxy-lua --skill alaa-k8s-helm --skill alaa-gitlab-ci-cd --skill ansible-generator --skill ansible-validator`
2. `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files <exact changed Markdown paths>`; inspected parser supports this selector. Freeze exact paths after edits, include this evidence file.
3. `git diff --check -- <exact changed PLATFORM paths>` plus UTF-8/no-BOM/LF, scope and deterministic sorted path/NUL/bytes SHA-256 manifest evidence. Preserve untracked inputs and record HEAD.
4. Owner executable validators only if their actual covered artifact inputs change. Current proposal changes controlling Markdown, not Dockerfiles, Lua modules, cfg/YAML/TOML, Ansible artifacts or checker logic; product/parser/runtime/Molecule/self-test suites would not test these prose repairs and are not proposed. No new tests mirroring wording. Final independent instruction review and pack aggregate remain parent Phase 4 gates.

## Risks and boundary handoff

Arvan root README wording remains a parent integration obligation. O17 deliberately does not certify old version data current. Existing on-demand maps remain. Runner hosting instructions gain only a portable boundary capability and require consumer validation before any external effect. All instruction edits are locally reversible; no live configuration or data changes.

## Implemented mapping

- A1: Docker companion90 and HAProxy companion90 plus delivery70 use the canonical Arvan-only fact test. No caas-arvan-kuber contract changed; Kubernetes and GitLab retain their owners even on Arvan.
- A2/O12: generator SKILL step5 and best-practices A13 point at playbook section6; section7 requires every command/result. Section6's five commands, zero-only acceptance, exit2 blocking, exemptions and stopping condition remain intact. ansible-validator remains unchanged.
- A40: Docker SKILL rule2 separates final-image and runtime keys and retains unmet-item MR reporting.
- A47: HAProxy gate-register Failed-operation boundary defines the bounded retry; both HAProxy and Lua body consumers point there. GitLab pipeline creation reference defines terminal arm, and SKILL routes there. Workflow mandatory fallback and optional job fallback remain distinct.
- A48: Kubernetes SKILL explicitly marks unavailable permission unknown and required cluster dependencies blocked; namespaced lookalikes and incomplete deployability claims are excluded.
- O16: no history trimmed, moved or retired. O17: Docker source-map and Dockerfile reference label local printer/snapshot evidence accurately; dates, values and pins remain unchanged.
- N1/V7: GitLab existing runner reference adds conditional manager-hosting bootstrap, with its existing topic-map row extended. Preserved shell isolation, protected-ref preconditions, executor choice, persistent config, token source, TLS trust and separate job evidence. No new skill or executable script.
- A46: noun-led descriptions only for already-substantively-changed Docker, GitLab and generator SKILL files; capability and negative-trigger tails preserved. Other descriptions unchanged.
- A41 (parent-approved extension): Docker interpolation25, HAProxy SKILL and replication child `references/40-rate-limiting-and-peers/30-replication-and-partitions.md`, Kubernetes failure-and-load section6, GitLab companion90 route the generic discriminator to security SKILL's exact heading. Retained register classes/disabling defaults; overload-versus-credential-limiter cases; partition bound, non-atomic quota limitation; readiness/degraded-response consequences; initContainer bounded-wait advice; GitLab mechanism/decision boundary.
- C2: Docker Compose20 and Kubernetes openshift-and-managed-platforms cite security ref60 Part3 Container. Read-only defaults, writable mounts, Docker's unmovable-path condition and explicit paths/reason/compensating-control exception evidence remain. No cluster resource substitution.

## Inspection and authoring provenance

`PLATFORM-read-manifest.json` records all 47 observed nontruncated chunks covering every reference and script under the six changed skill roots, in addition to the six full SKILL reads. Also read Lua's six test/runtime/example scripts outside scripts/. Untouched caas-arvan-kuber and ansible-validator were inspected for relevant owner contracts, not claimed fully read. Assets unrelated to these prose changes were not read; no generated/binary asset inspection claim. A UTF-8 stdout correction resolved a source-read transport encoding error; it was not an acceptance gate. Missing guessed reference paths were resolved from the recorded manifest, not treated as missing capability.

`PLATFORM-draft.md` records the initial controlling-paragraph draft and compression counterexamples before edits. Full owned diff inspected after editing; only the named 23 skill Markdown files changed. Native semantic inputs, checker implementations and external topic-map placement are preserved. No independent review was performed in this lane.

## Verification record

The tested manifest, exact command arguments, results and source limits are recorded in `PLATFORM-verification.json`. All commands use repository root as cwd and ordinary serial low-cost execution; no CPU-heavy or live commands. Runtime, deploy, cluster, runner provisioning, full-pack aggregates and independent review are unrun in this lane and remain outside its acceptance claim.

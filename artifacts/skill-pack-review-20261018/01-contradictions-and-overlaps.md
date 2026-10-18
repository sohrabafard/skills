# Skill pack review 01: contradictions, errors and overlaps

Scope: the 69 skills under `skills/sohrab/`. Date of review: 2026-10-18.
Companion files: `02-optimization.md`, `03-new-skill-proposals.md`.

## Method and evidence status

- Repository checkers were run first: `validate_sohrab_skill_pack.py` (exit 0; warnings only for long bodies in 21 skills), `check_skill_index.py` (no findings), `check_lifecycle_contract.py` (no findings), `check_fleet_references.py` (informational list only).
- Seven read-only reviewer lanes read the skills group by group. Their reports were treated as leads.
- Each item carries one status tag:
  - `[V]` the parent re-read the cited lines or ran a grep that confirms the claim.
  - `[R]` reported by a reviewer lane. Cited lines were not re-read by the parent. Treat as a lead until checked.
- No reviewer lane had a recorded model and effort pair. Their verdicts are advisory. They do not certify control compliance.
- Coverage is partial. Each lane read all `SKILL.md` files in its group and only a sample of `references/`. Absence of a finding in an unread file is unknown, not clean.
- Paths below are repository-relative (`skills/sohrab/...`), or relative to `skills/sohrab/` when the prefix is omitted.
- Where a reference is cited by its numeric prefix alone (for example `references/31:108-110`), the full file name is the file in that directory that begins with that prefix.

## A. Contradictions

Each entry states the two sides, the reason it is a contradiction, and the owner the fix should point to. "Owner" follows `skills/sohrab/AGENTS.md` where that file settles it.

### Major

**C-01 Arvan routing trigger.** `[V]` for the two sides below; `[R]` for the sibling tables.
- `skills/sohrab/README.fa.md:30-32` loads `caas-arvan-kuber` whenever the work targets ArvanCloud CaaS. "Arvan-first wins" applies.
- `skills/sohrab/caas-arvan-kuber/SKILL.md:10-12` states that being on Arvan alone is not a reason to load the skill. It loads only when a fact is true of Arvan and false of stock Kubernetes.
- `[R]` `alaa-haproxy/references/90-companion-boundary.md:29` and `alaa-docker-production/references/90-companion-boundary.md:30` route on "whenever the target is Arvan CaaS". `alaa-k8s-helm/SKILL.md:19` and `references/openshift-and-managed-platforms.md:58` keep the generic skill for Arvan clusters.
- Reason: one routing decision has two triggers. An agent routes the same Arvan Helm task differently depending on which file it reads.
- Owner to point to: `caas-arvan-kuber` deciding test in its `SKILL.md`. Restate that trigger identically in the README and both boundary tables.

**C-02 Ansible delivery gate defined three ways.**
- `[V]` `ansible-generator/SKILL.md:42-46` lists four commands. No module-currency check.
- `[V]` `ansible-generator/references/playbook.md:228-244` lists four sibling commands plus `check_module_currency.py`. Accept condition: exit 0 from every command.
- `[R]` `ansible-generator/references/best-practices.md:234-239` repeats the four-command form.
- Reason: an agent following the SKILL gate skips the currency check. A module name that resolves only through a redirect then passes.
- Owner: `playbook.md` section on the delivery gate. SKILL and best-practices point to it.

**C-03 Laravel upgrade sweep: the procedure contradicts itself.** `[V]`
- `skills/sohrab/alaa-laravel-upgrade-all-packages/SKILL.md:23-24` step 2 says split each major bump into its own change.
- Same file, step 3 runs `composer update --with-all-dependencies` and "Apply the remaining set". The text of step 2 says this flag applies majors under loose constraints. "Remaining set" is never defined.
- Reason: the sweep can apply a major bump in the same change it claims to exclude.
- Fix: define the allowed set and the command that applies only it.

**C-04 Laravel 12 to 13 upgrade has conflicting owners.** `[V]` for php-clean-code; `[R]` for the rest.
- `alaa-php-clean-code/SKILL.md:26-29` says the upgrade belongs to `alaa-laravel-upgrade-all-packages`. Consistent with the upgrade skill.
- `[R]` `alaa-laravel-architecture/references/source-map.md:25` holds dependency bumps for 12 to 13 in `alaa-php-clean-code/references/laravel-best-practices.md`.
- `[R]` `alaa-laravel-upgrade-all-packages/SKILL.md:3,47` routes major framework migration to `alaa-laravel-architecture`.
- Reason: the migration can reach zero owners or two.
- Owner: `alaa-laravel-upgrade-all-packages`. The other two point to it.

**C-05 Octane scope predicate defined two ways.** `[V]`
- `skills/sohrab/alaa-php-clean-code/SKILL.md:28` treats Octane as in scope unless `composer.json` lacks `laravel/octane` **and** there is no `config/octane.php`.
- `skills/sohrab/alaa-octane-performance/SKILL.md:3,16-19` says scope is `config('octane.server')` non-null, "not from the package list".
- Reason: a repository with `config/octane.php` and a null server is in scope under the first rule and out of scope under the second.
- Owner: `alaa-octane-performance` predicate. The clean-code skill points to it.

**C-06 Dual call form written as the instruction.** `[V]` for three files; `[R]` for the rest.
- `[V]` `alaa-php-clean-code/SKILL.md:10`: "both forms appear at every call site".
- `[V]` `alaa-go-chi-development/SKILL.md:13`: "Cross-skill names appear as `/name` (`$name`)".
- `[R]` `alaa-services-contract/SKILL.md:80-81`, `alaa-algorithms-data-structures/SKILL.md:8`, `alaa-security-review/SKILL.md:10`, `alaa-keyset-pagination/SKILL.md:10`, `alaa-system-design/SKILL.md:12`, `service-runtime-kit-governance/SKILL.md:8`, `clickhouse-performance-schema-ops/SKILL.md:3`.
- `[V]` `alaa-codex-runtime-ops/SKILL.md:100` and `references/20-command-and-path-discipline.md:38` use a bare `$service-runtime-kit-governance` call. AGENTS allows bare `$` only in `openai.yaml` `default_prompt`.
- `[V]` a grep found the `/name (`$name`)` pattern in 37 `SKILL.md` files.
- AGENTS.md `skills/sohrab/AGENTS.md:58-60` requires one `/name` form. Dual call sites already in place are legacy and convert only when the file is edited for another reason (AGENTS.md:60).
- Reason: the sentences above instruct a new agent to write the duplicate form. The legacy call sites are tolerated; the convention sentences are not.
- Fix: rewrite the convention sentences only. Do not sweep call sites.

**C-07 Keyset and services-contract disagree on the offset exception.** `[V]`
- `skills/sohrab/alaa-keyset-pagination/references/10-route-mode-and-sort-allowlist.md:15-23` lists five conditions. Condition 3 is "an exact-total query requirement" plus a documented operational requirement. There is no condition that the list size stays bounded against tenant growth.
- `skills/sohrab/alaa-services-contract/references/25-end-to-end-flow-and-boundaries.md:341-355` lists five different conditions. Condition 3 is "the list's size does not grow with tenant data".
- `[V]` `keyset` 10:15 says the contract "currently forbids" offset. The services-contract text now records the exception, so the statement is stale.
- Reason: an agent following keyset can admit a tenant-growing offset route that services-contract forbids.
- Owner: `alaa-services-contract` `references/25-…`. Keyset points to it.

**C-08 Request-time checker timeout: two status codes.** `[V]`
- `skills/sohrab/alaa-trust-gateway-auth/SKILL.md:66-67` and `references/30-fail-closed-cases.md:57-64` deny a timed-out checker with `403 AUTHZ_DENIED`.
- `skills/sohrab/alaa-services-contract/references/26-request-time-authorization-openfga/40-decision-and-enforcement.md:9` lists `AUTHZ_SERVICE_TIMEOUT` as `503`, gateway-owned.
- Reason: AGENTS.md assigns codes and wire shapes to services-contract. Two status codes for one failure leave an agent unable to choose.
- Owner: services-contract for the code row. Trust-gateway points to it and keeps the deny behaviour.

**C-09 Auth deny-code registry: two owners and a status mismatch.** `[R]`
- `alaa-trust-gateway-auth/references/50-deny-codes.md:7-9` says the taxonomy belongs to services-contract. Lines 42-55 define `AUTH_*` and `TENANT_*` locally.
- `alaa-trust-gateway-auth/SKILL.md:66` gives `AUTH_CONTEXT_MISSING` as a flat 401. `50-deny-codes.md:42` says "401 or 403 by service policy".
- The services-contract tree does not define several of these codes (grep, `[R]`).
- Owner: one code-registry owner, named in AGENTS.md.

**C-10 Permission generator: the rule against frozen numbers is broken by the same file.** `[V]`
- `skills/sohrab/alaa-permission-generator/SKILL.md:70` states `MaxPermissionID()` values: tusd 95, news 119, wa 1.
- `SKILL.md:74-76` says no permission count, maximum id or fingerprint may enter code, a comment, a test or a report.
- `SKILL.md:78-83` gives dated ranges ("correct on 2026-07-27") and two blocks.
- Reason: the rule forbids the frozen values the paragraph states.
- Fix: remove the frozen numbers and dated ranges, or move them to a dated, sourced reference.

**C-11 Codex runtime ops grants standing approval for unsandboxed commands.** `[V]` for the heading and first entries; `[R]` for the rest.
- `skills/sohrab/alaa-codex-runtime-ops/references/40-project-fallbacks.md:3-9` declares "standing maintainer approval for unsandboxed execution" of named gates, including `yarn test` and quasar dev.
- `SKILL.md:22` and `references/20-command-and-path-discipline.md:77-79` require per-command escalation with justification.
- Reason: a skill cannot grant host sandbox permission. The global contract states that activation grants none. The repository holds no grant record.
- Fix: delete the standing-approval section. Use the per-command path.
- Confidence medium on whether the user authorized the grant elsewhere. The repository does not show it.

**C-12 Workflow phase prompt budget: two rules, one silent.** `[V]`
- `skills/sohrab/alaa-workflow/SKILL.md:71` says the target yields only "when the user requests an exhaustive prompt".
- `skills/sohrab/alaa-workflow/references/phase-prompts.md:46` says it yields "whenever exhaustive or required behavior-affecting content does not fit: exceed it rather than drop any, say so".
- Reason: an agent following SKILL alone truncates required behaviour content and does not disclose it.
- Fix: one rule. Use the reference's clause "exceed rather than drop, and say so".

**C-13 Service runtime kit commits by default.** `[V]`
- `skills/sohrab/service-runtime-kit-governance/SKILL.md:55` step 5: "Commit the regenerated outputs."
- `AGENTS.md` and the global contract require explicit user authority before any commit.
- Fix: replace with "leave the outputs uncommitted and report the pending commit".

**C-14 Memory OS: a store-neutral shape file requires vault schema.** `[R]`
- `alaa-memory-os/references/knowledge-shape.md:22-32, 108-111` requires vault frontmatter (permalink, tags, canonical source paths, last verified) and a file-based checker.
- `alaa-memory-os/references/prompt-3-publishing.md:42-46, 79` publishes to vault paths.
- `alaa-memory-os/SKILL.md:26-29` names such assumptions as policy leaks.
- `alaa-memory-os/references/store-hindsight.md` maps no fields or paths. With `ACTIVE_ADAPTER: hindsight`, the staleness fields and publication locations are undefined.
- Confidence medium. The full hindsight mechanics were not read.
- Fix: move the vault schema to a vault adapter. Give hindsight its own mapping or mark each field not applicable.

**C-15 Go: fire-and-forget allowed in one file, forbidden by P9 in another.** `[V]` for the allowance text; `[R]` for P9.
- `skills/sohrab/alaa-golang/references/11-orchestration-and-overlap-guide.md:115-119` says it restates P9 and "does not soften it", yet allows a "documented fire-and-forget" goroutine.
- `skills/sohrab/alaa-golang-clean-code-principles/SKILL.md:89` and `references/30-runtime-and-observability.md:8-9` require owner, cancellation, drain and a metric name.
- Owner: P9 in clean-code. Point file 11 at it and delete the clause.

**C-16 Go: WithoutCancel used as a drain with no timeout.** `[R]`
- `skills/sohrab/alaa-golang-clean-code-principles/references/30-runtime-and-observability.md:25` shows `context.WithoutCancel(ctx)` as the RIGHT drain.
- `skills/sohrab/alaa-golang/references/45-failure-behavior-at-the-call-site.md:252-253` forbids `WithoutCancel` without a following `WithTimeout`. The compliant form is at line 241.
- Fix: bound the clean-code example.

**C-17 Go: signal handling assigned two ways.** `[R]`
- `alaa-golang/references/45-failure-behavior-at-the-call-site.md:210-219` tells a service to create its own `signal.NotifyContext`.
- Same file, lines 227-230, forbids a kit service from implementing signal handling or drain ordering, and assigns both to runkit.
- Fix: scope lines 210-219 to standalone mode.

**C-18 Go: race and whole-suite gate defined in three files.** `[R]`
- `alaa-golang/SKILL.md:66-72` assigns the whole-suite run to an authority other than the authoring lane, with one list of `-race` triggers.
- `alaa-golang-fiber/SKILL.md:88-91` and `references/30-validation-testing.md:122-126, 168-169` give different triggers.
- `alaa-golang-fiber/references/40-production-readiness.md:150` requires `go test -race ./...` unconditionally at pre-ship.
- Fix: Fiber points at the alaa-golang gate and keeps only Fiber-specific triggers.

**C-19 Go: a dated phase gate restated in the clean-code skill.** `[R]`
- `alaa-golang-clean-code-principles/SKILL.md:26-37` restates the phase files and pins "KIT_FIRST_STABILIZATION was active on 2026-07-26".
- `alaa-go-chi-development/references/05-phase-and-source-truth.md:42-55` says its matrix is "the only place the answer lives" and that the dated paragraph is stale.
- `05-…:73-77` needs a specific request plus a stated phase. Clean-code `31-34` adds an "explicit go-ahead".
- `alaa-golang/references/00-topic-map.md:82` routes to "the phase gate in SKILL.md", which is the clean-code copy.
- Fix: delete the restated gate and point to `05` and `phase-check.sh`.

**C-20 Frontend: sanitizer placement stated as input-time only.** `[R]`
- `alaa-frontend-developer/references/25-frontend-security.md:31-33` says sanitize "at the single boundary where the value enters the app ... never in the template".
- `alaa-security-review/references/25-browser-trust-and-output.md:22` and `alaa-vue-typescript-clean-code/references/72-frontend-security-binding.md:30` require output-time sanitizing at render.
- Fix: restate frontend `25:31-33` as render-time sanitizing and point to the owner.

**C-21 Frontend: navigation caching has three variants.** `[R]`
- `alaa-frontend-developer/references/30-pwa-sw-and-offline.md:22` says navigation HTML is network-only.
- `alaa-quasar-app-vite-v3/references/30-service-worker-excellence.md:11` allows a precached NavigationRoute shell or NetworkFirst.
- `alaa-quasar-app-vite-v3/references/34-frontend-failure-and-degradation.md:40` defines "works offline" as a precached shell.
- `alaa-frontend-developer/references/50-qa-and-verification.md:45-46` names a third variant.
- Owner: Quasar `30`. Align the others.

**C-22 Frontend: client telemetry classes disagree.** `[R]`
- `alaa-frontend-developer/references/47-frontend-observability.md:19-26` lists four required signals, including request outcome and connection state.
- `alaa-quasar-app-vite-v3/references/36-client-observability-contract.md:11-18` says exactly four classes exist and anything else needs a services-contract entry first. Its four omit both of file 47's classes.
- Owner: Quasar `36`. File 47 points to it.

**C-23 Frontend: who may read `import.meta.env`.** `[R]`
- `alaa-frontend-devops/references/30-serving-caching-and-public-path.md:9` lets any file read `import.meta.env.BASE_URL`.
- `alaa-frontend-developer/references/48-config-and-environment.md:27` forbids reading it from more than one module.
- `alaa-frontend-devops/references/15-build-time-vs-runtime-config.md:24` and `alaa-vue-typescript-clean-code/references/50-quasar-vite-pinia-contract.md:89` require one accessor.
- Fix: route devops `30:9` through the single config module.

**C-24 Frontend: font byte budget.** `[R]`
- `alaa-frontend-developer/references/41-lighthouse-and-web-vitals.md:133-134` gives fonts "< 100 KB subset".
- `alaa-ui-ux-design-system/references/45-render-and-asset-budgets.md:34` and `05-rtl-and-persian.md:68` give 150 KB for first-party fonts on the initial route.
- File 41 `:141` defers the design budget to ui-ux 45, yet restates a number.
- Fix: remove the font number from 41 and point to 45.

**C-25 Repo docs: source comments routed to a skill whose scope excludes them.** `[R]`
- `alaa-repo-docs/SKILL.md:12` and `:29` route all source comments and docblocks to `alaa-frontend-doc-annotations`.
- `alaa-frontend-doc-annotations/SKILL.md:3` scopes itself to Vue, Quasar and Vite files.
- `alaa-php-clean-code/SKILL.md:197` keeps PHP docblock rules in its own references.
- Reason: backend comment work has no working route.
- Fix: scope repo-docs to frontend files and name php-clean-code for PHP.

**C-26 Repo docs: runtime mechanic inside a rule that bans mechanics.** `[R]`
- `alaa-repo-docs/SKILL.md:102` states Task-tool and parent-thread spawning mechanics, then says not to write runtime mechanics into a documentation rule.
- Fix: delete the runtime names and route to `alaa-prompting-guide`.

**C-27 Repo docs: the link checker exits 2 yet can pass.** `[R]`
- `alaa-repo-docs/references/10-language-and-links.md:206-207` says exit 2 proves nothing "except when a declared origin is unavailable".
- Lines 265-267 say the same case exits 2 and proves nothing for unproven links.
- `AGENTS.md` treats exit 2 as a failed gate. Fix: delete the exception clause at line 207.

**C-28 Tusd upload hooks: fail-open and fail-closed classified against the stated question.** `[R]`
- `tusd-upload-platform/references/45-hooks.md:7-12, 22-23` states the question: a call that decides whether a caller may act denies on failure.
- The post-receive re-check that stops revoked uploads is fail-open ("upload continues"). That lets a revoked caller keep writing.
- The pre-finish hook is fail-closed, which denies an already stored upload.
- Fix: classify each hook by what its failure lets through. Keep one citation of AGENTS.md:32.
- Not verified: whether tusd honours `StopUpload` from post-receive.

**C-29 Object storage: part-size defaults in two planes.** `[V]`
- `alaa-minio-object-storage/references/05-environment-contract.md:60` gives `STORAGE_PART_SIZE_BYTES` 16 MiB as an estimate.
- `tusd-upload-platform/references/25-upstream-library.md:62` and `35-storage-lifecycle.md:30` give `PreferredPartSize` 50 MiB.
- No file maps one knob to the other. The tus plane has no statement of which governs it.

**C-30 Object storage: required variables with a profile default.** `[R]`
- `alaa-minio-object-storage/references/05-environment-contract.md:50, 52, 209-211` says unset required variables are refused and never defaulted.
- Lines 147-150 supply profile endpoint values.
- `alaa-arvan-object-storage/references/15-environment-contract-deltas.md:22-23` labels `STORAGE_ENDPOINT` as the Arvan default.
- The contract does not say whether an unset endpoint refuses startup or resolves the Arvan endpoint. Wrong-region writes are the hazard the file names.

**C-31 Object storage: a variable cited that the owner does not carry.** `[R]`
- `alaa-arvan-object-storage/references/15-environment-contract-deltas.md:77-81` calls Constraint 5 "the live example" of a boolean client-abort variable.
- The minio variable table has no such row. Only `STORAGE_MULTIPART_ABORT_DAYS` appears at `:66`.

**C-32 Object storage: a forbidden command form in an executable block.** `[R]`
- `alaa-minio-object-storage/references/75-mc-command-line-client.md:18-22` shows positional access and secret key arguments, labelled "repo-verified".
- Lines 25-29 forbid that form. The safe alternatives at `:33-40` are marked unverified.

**C-33 Provider skills cite the wrong metric lines.** `[V]`
- `alaa-bale-provider/SKILL.md:94-95` cites `alaa-services-contract/references/24-metric-registry.md:107-110` for the four `alaa_dependency_*` families.
- Lines 107-110 are `alaa_db_*` rows. The `alaa_dependency_*` rows are at lines 146-151.
- `[R]` `alaa-sms-provider-mediana/SKILL.md:65, 71, 40` and `references/30-failure-and-ambiguity.md:20` cite lines in the Mediana contract that do not contain the rule they name.

**C-34 Vector: an observability binding that the owner does not state.** `[V]`
- `vector-rust-observability-pipelines/SKILL.md:33-35` says `when_full: drop_newest` is required "as `/alaa-observability-soc` binds".
- `[V]` a grep of `alaa-observability-soc` finds no `drop_newest` or `when_full`. The nearest text, in `vector` `90-source-map.md:36`, says only "must never block application traffic" `[R]`.
- Fix: attribute only the block rule to observability-soc. Mark `drop_newest` as a Vector choice.

**C-35 Pipeline gate: a sweep audit that writes permanent repo files.** `[R]`
- `alaa-partitioned-table-fk-audit/SKILL.md:3, 19, 49-56` requires permanent test installation and CI wiring "even when the request is only an audit".
- AGENTS authority rule: edit only inside the requested scope.
- Fix: make the installation conditional on an explicit request. Report the missing test as a finding.

**C-36 Permission generator: same-change apply against the default authorization rule.** `[R]`
- `alaa-permission-generator/SKILL.md:72-73` requires applying the consumer map in the same change as the seed.
- Lines 36-48 say applying needs explicit words and "add a permission" authorizes neither.
- Fix: make the same-change rule conditional on the seed being authorized.

**C-37 Orchestrators: the mirrored pair has drifted.** `[R]`
- `alaa-cc-orchestrator/SKILL.md:65, 67` contains "Correct sparingly" and "Calibrate length". `alaa-codex-orchestrator/SKILL.md:61` contains "Keep dispatches lean". Neither rule exists in the other file.
- `AGENTS.md:17` allows divergence only in runtime mechanics and delegation polarity.
- Fix: port each paragraph to the other orchestrator in the same change.

**C-38 Memory and workflow trigger lists disagree.** `[R]`
- `alaa-extract-agent-lessons/SKILL.md:3` lists "accepted or rejected work" and "validation failures" as triggers.
- `alaa-workflow/references/context-curation.md:7-15` admits only seven signals. It has no rejected-work signal.
- Fix: align the two lists to one set.

**C-39 Low-noise claims per-model profiles that the file disclaims.** `[V]` for the file; `[R]` for the SKILL.
- `alaa-low-noise/references/model-output-profiles.md:1-5` says "No model profile or effort policy is defined here".
- `alaa-low-noise/SKILL.md:56, 72` says the file holds per-model profiles and makes an unsourced universal claim that effort does not change length.
- Fix: route per-model guidance to `alaa-prompting-guide`. Source the claim or drop it.

**C-40 Vue: a validation command set hard-coded to npm.** `[R]`
- `alaa-vue-typescript-clean-code/references/60-validation-gates.md:66-72` hard-codes npm.
- `alaa-quasar-app-vite-v3/SKILL.md:19` says follow the lockfile. `references/75-testing-ci-playbook.md:86-111` uses `<pm>`.
- Owner: the lockfile rule. Vue `60` points to it.

**C-41 Haproxy and Docker: a rule that the owner does not state.** `[R]`
- `alaa-docker-production/SKILL.md:40-43` rule 2 says the final stage is the whole security posture. It lists runtime keys a Dockerfile cannot set. Its only citation is the Dockerfile file.
- The runtime keys are in `references/20-compose-authorship.md:138-165`.
- Fix: split the rule. Dockerfile items stay. Runtime keys point to `20`.

**C-42 Fail-closed membership decided in two places.** `[R]`
- `alaa-docker-production/references/25-fail-closed-interpolation.md:140-146` applies the fail-closed test to decide membership. AGENTS.md assigns fail-closed doctrine and threat classes to security review.
- Fix: docker keeps the interpolation form. Membership cites security review.

### Minor and nit

**C-43 Ops and CI wording.** `[R]`
- `alaa-haproxy/SKILL.md:19-21` has a code span broken across a line.
- Descriptions that open with a verb rather than a noun phrase (AGENTS.md:97): `alaa-docker-production/SKILL.md:3`, `ansible-generator/SKILL.md:3`, `ansible-validator/SKILL.md:3`, `alaa-gitlab-ci-cd/SKILL.md:3`.
- "materially different retry" is undefined (`alaa-haproxy/SKILL.md:89-92`, `alaa-haproxy-lua/SKILL.md:69`). "terminal arm" is undefined (`alaa-gitlab-ci-cd/SKILL.md:61`).
- `alaa-k8s-helm/SKILL.md:26` requires `auth can-i` before a cluster-scoped object and has no branch for an unreachable cluster.

**C-44 Shell and orchestrator wording.** `[R]`
- `alaa-cc-orchestrator/SKILL.md:39` and `alaa-codex-orchestrator/SKILL.md:39` say "should not implement". Section 2 of the same file says "must not". Use "must not" in section 1.
- `alaa-bash-shell/SKILL.md:56` forbids any lane whose only job is re-checking another lane. The global rule gives the orchestrator independent acceptance. State the exception.
- `alaa-cc-orchestrator/SKILL.md:136` and `alaa-codex-orchestrator/SKILL.md:135` say "Preserve every explicit --browser chromium argument" with no rationale and no conflict behaviour.
- `alaa-project-constitution/SKILL.md:152` uses `python3`. AGENTS.md uses `python`. Not checked on this host.

## B. Overlaps where a specialist skill exists (mode 1)

For each, the owner already exists. The other skill should point to it with a trigger rather than re-teach it.

**M1-01 Redelivery test shape.** `[R]` Owner: `alaa-async-messaging`. Restated in `alaa-laravel-job-rabbitmq/SKILL.md:144-153` (the one required test), `alaa-async-messaging/SKILL.md:76-77`, and `alaa-php-clean-code/references/laravel-best-practices.md:77, 81-87`. The three definitions differ in shape, so an agent can satisfy one and fail another.

**M1-02 Prefetch rule and its report obligation.** `[R]` Owner: `alaa-async-messaging`. Restated in `alaa-laravel-job-rabbitmq/SKILL.md:84-89, 205-208` and `alaa-async-messaging/SKILL.md:25-26, 94-97`.

**M1-03 Provider boot rule.** `[R]` Owner: `alaa-laravel-architecture` (`SKILL.md:3, 38`). Restated in `alaa-laravel-job-rabbitmq/SKILL.md:132-136`.

**M1-04 Upstream-override list.** `[R]` Four places disagree on count and list. `alaa-octane-performance/SKILL.md:105-118`, `alaa-php-clean-code/references/laravel-best-practices.md:87, 100-104`, `alaa-php-clean-code/references/00-topic-map.md:54` (says "four"), and `alaa-testing-strategy/SKILL.md:31` (owns the removal rule). Owner: testing-strategy for the removal rule; one list for the rest.

**M1-05 Postman generation and conventions.** `[R]` Owner: `alaa-postman-collections` (`SKILL.md:13-15, 37-55`). Restated in `alaa-laravel-public-api-contract-pack/SKILL.md:70-71` (performs generation), `references/40-consumer-discovery-pinning-and-secret-hygiene.md:94-101, 111`, and `alaa-php-clean-code/references/documentation-and-artifacts.md:66-91`, `alaa-php-clean-code/SKILL.md:197`.

**M1-06 Trust-gateway and services-contract: the fail-open and fail-closed discriminator.** `[R]` Owner: `alaa-security-review` (gate side) and `alaa-reliability-sla` (contributor side). Restated in three files: `alaa-security-review/SKILL.md:42-50`, `alaa-reliability-sla/SKILL.md:18-31`, `alaa-observability-soc/SKILL.md:36-37`.

**M1-07 Audit-write boundary.** `[R]` `alaa-observability-soc/SKILL.md:36-37` and `alaa-security-review/SKILL.md:47-48` give different failure behaviour for an audit write. Neither states the boundary. Owner: security review.

**M1-08 Request-time checker and code registry.** `[R]` See C-08 and C-09. Owner: services-contract.

**M1-09 Keyset envelope and limit values.** `[R]` `alaa-keyset-pagination/SKILL.md:50, 56-58` and `references/40-wire-contract-limits-and-errors.md:9-36` restate the `meta` envelope, the `has_more` exclusion and the request shape. Also keyset `40` states the default limit 20 and maximum 100, which services-contract says are route-documented. Owner: services-contract `25`/`26`. Keyset keeps only the algorithm rationale.

**M1-10 Keyset cursor error codes not in the owner.** `[R]` `alaa-keyset-pagination/references/40-wire-contract-limits-and-errors.md:52-58` defines four cursor codes. Keyset `40:5-7` says services-contract owns the codes. A grep of the services-contract tree finds none of the four. Unverified: whether a committed code registry exists outside the pack.

**M1-11 Testing enumeration pointer.** `[R]` `alaa-testing-strategy/references/60-coverage.md:28` says `70-failure-mode-first` owns the enumeration. File 70 and `SKILL.md:181` say the enumeration table lives in observability `10-signal-model.md:13-25`. Point 60 at observability.

**M1-12 Service-worker and storage rules restated.** `[R]` "Cache Storage holds Request/Response only; structured data is IndexedDB" appears in five files: `alaa-frontend-developer/references/30-pwa-sw-and-offline.md:8-13`, `46-resilience-and-degradation.md:47`, `70-companion-skill-routing.md:27-29`, `alaa-quasar-app-vite-v3/references/30-service-worker-excellence.md:30, 94`, `34-frontend-failure-and-degradation.md:47`. "No token in browser storage" appears in three. Owners: `alaa-indexeddb-browser-storage` (`references/61`) and Quasar `30`.

**M1-13 Service-worker verification runbook: two homes.** `[R]` `alaa-frontend-developer/references/50-qa-and-verification.md:33-36` claims "the only copy". `alaa-quasar-app-vite-v3/references/75-testing-ci-playbook.md:35-52` and `30-service-worker-excellence.md:78` also name a list. The lists already differ. Keep one list in 75.

**M1-14 Frontend routers.** `[R]` `alaa-frontend-developer/SKILL.md:69-85` ("Also load" table) versus `references/00-topic-map.md:10-29`. `alaa-quasar-app-vite-v3/SKILL.md:36-47` ("Mandatory pairings") versus `references/00-topic-map.md:3`, which says there is no routing table. The two routers differ. The motion pointer exists only in frontend `SKILL.md:85`.

**M1-15 Services-contract and reliability routers.** `[R]` `alaa-reliability-sla/SKILL.md:107-119` and `alaa-services-contract/SKILL.md:53-73` each carry a full router table while both have 9 or more references. AGENTS.md:52 requires one pointer line in the body. The services-contract body table has no row for `05`, `29`, or the `26-request-time-authorization-openfga/` subfolder, all listed in its topic map.

**M1-16 Go: P5 forbidden-import list differs.** `[R]` `alaa-golang-clean-code-principles/references/20-domain-data-and-consistency.md:45-46, 75-76` omits `net/http`, `database/sql`, gofiber and kit transport packages. `alaa-golang/references/62-import-direction-and-boundaries.md:29-36` includes them. Point P5 at file 62.

**M1-17 Go: the TDD sequence.** `[R]` `alaa-golang-fiber/references/30-validation-testing.md:117-121` gives three steps. `alaa-golang/references/63-tdd-and-testing-discipline.md:15-29` adds a failure-reason check. Point Fiber at 63.

**M1-18 Go: Fiber restates owners.** `[R]` `alaa-golang-fiber/references/40-production-readiness.md:36-40` mandates a semaphore, `TryAcquire` and 503 shedding. Load shedding belongs to reliability (AGENTS.md:27). `alaa-golang/references/46-chi-under-load.md:62-68` routes shedders to a change request. Fiber also restates singleflight, TTL jitter, authorization caching, measure-first, cardinality and the signal list. Point each at its owner.

**M1-19 Go: the correlation contract appears three times in Fiber.** `[R]` `alaa-golang-fiber/references/40-production-readiness.md:81-88`, `references/20-routing-middleware-errors/20-errors-and-correlation.md:33-36`, and `references/30-validation-testing.md:149`. Header names belong to services-contract (AGENTS.md:23).

**M1-20 Go: telemetry requirement in a cache reference.** `[R]` `alaa-golang/references/61-redis-cache-layer.md:122-126` states a cache counter requirement. AGENTS.md:21-22 assigns requirement levels to observability-soc.

**M1-21 Go: the Redis and error-text rules.** `[R]` "No driver error text in responses" is in `alaa-golang/references/31:108-110`, `45:178-180`, and `alaa-golang-fiber/references/20:16-17`. The four decode checks are in `alaa-golang/references/31:154-155`, `45:260`, `alaa-golang-fiber/references/30:60-67`, `50:33`. Kit Redis facts are in `clean-code/references/20:155-162` and `alaa-golang/references/61:18-25`.

**M1-22 Vector and observability.** See C-34. Vector restates "fail open or closed follows what the data is for" with a pointer that does not name the rule.

**M1-23 Bale and Mediana: credential and PII egress.** `[R]` The five-egress rule is restated in `alaa-bale-provider/SKILL.md:76-80, 99-100` and `alaa-sms-provider-mediana/SKILL.md:62, 73`. `alaa-haproxy/references/90-companion-boundary.md:26` assigns "what may be logged" to security review. The masks have drifted: Bale `98912****000`, Mediana `+9891****0000`.

**M1-24 Bale and Mediana: connect-refused versus timeout.** `[R]` `alaa-bale-provider/SKILL.md:84-90` and `references/30-failure-classes.md:24-27, 39-43`; `alaa-sms-provider-mediana/SKILL.md:67-73` and `references/30-failure-and-ambiguity.md:9-18`. Owner: `alaa-reliability-sla/references/20-retries.md:22-33`. Bale `30:7-8` says general rules are "never restated", which its own lines 24-43 contradict.

**M1-25 Jitsi and the trusted header.** `[R]` `jitsi-platform-architect/SKILL.md:38-39` restates rule 6 owned by `alaa-trust-gateway-auth/SKILL.md:8`.

**M1-26 Shaka and IndexedDB: verbatim copy.** `[R]` `alaa-shaka-player/references/50-offline-and-in-app-download.md:11-19` says "carried here verbatim" against `alaa-indexeddb-browser-storage/references/72-offline-media-store.md:20-25`. Minio `20-lifecycle-and-retention.md:57-61` restates the tusd-only `upload.asset.expired` fact that `tusd references/35-storage-lifecycle.md:5-7` says is stated once.

**M1-27 Object-storage key rules: two owners.** `[R]` "Write or change an object key" routes to `alaa-minio-object-storage/references/10-buckets-and-object-keys.md:32-49`. "Build an object key" and "decide part sizes" route to `tusd-upload-platform/references/35-storage-lifecycle.md:28-49`. "Choose a multipart part size" routes to minio `50`. The tenant and no-client-segment key rules are stated in both. Assign one owner per decision.

**M1-28 Chat and ClickHouse: the tenant exception stated three times.** `[R]` `alaa-signoz-clickhouse-docs/SKILL.md:50-54` and `clickhouse-performance-schema-ops/SKILL.md:47-52` (same text verbatim); `alaa-signoz-clickhouse-docs/SKILL.md:14` and `clickhouse-performance-schema-ops/references/15-fleet-clickhouse-boundary.md:44-63`. The worked instance at `15:83-110` bakes in a commit hash and line numbers.

**M1-29 Memory OS and workflow: the dispatch return contract.** `[R]` See C-37 for the mirrored pair. The return contract is claimed by `alaa-low-noise/references/workflow-integration.md:32` (line bound), `alaa-workflow/SKILL.md:63` and `references/context-continuity.md:128-132` (structure), and `alaa-cc-orchestrator/references/delegation-prompts.md:20, 24-26` (envelope field, plus a restatement of low-noise's rationale).

**M1-30 Workflow restates its own when-to-write rules.** `[R]` `alaa-workflow/SKILL.md:33, 91` restates `context-continuity.md:77-85`. `SKILL.md:91` claims the router table is the only place triggers are written, which `SKILL.md:55` contradicts.

**M1-31 Prompting-guide and gate economics.** `[R]` The rule "keep focused checks and independent acceptance; remove repetition only without a new change, failure or unresolved concern" appears five times: `alaa-cc-orchestrator/SKILL.md:63`, `alaa-codex-orchestrator/SKILL.md:63`, `alaa-prompting-guide/SKILL.md:65`, `alaa-low-noise/references/model-output-profiles.md:16-18`, `alaa-workflow/SKILL.md:43`. Gate economics belong to the orchestrator's verification-and-gates reference.

**M1-32 Code-intelligence and documentation routing.** `[R]` See C-25. `alaa-code-intelligence-routing/references/20-documentation-routing.md:3` repeats the wrong routing.

## C. Overlaps with no owner (mode 2)

For each, several skills teach the same thing and no single skill owns it. The proposal is to create one central skill in `skills/sohrab/` and point the others at it. Where I think a central skill is the wrong size, I say so and name the smaller alternative. Details for the new-skill candidates are in `03-new-skill-proposals.md`.

**M2-01 Sensitive-data masking and log egress.** `[R]` The rule and the masks are restated in four provider and storage skills (see M1-23 and C-33). Security review is named as owner in `alaa-haproxy/references/90` but holds no masking spec, so each skill writes its own mask. Proposal: a central skill for sensitive-output redaction, with masks and field-name rules, that security review cites. Smaller alternative: a reference inside `alaa-security-review`. I recommend the reference first, because the masking rule is short.

**M2-02 Container runtime-hardening baseline.** `[R]` Non-root, no escalation, dropped capabilities and a read-only filesystem are stated for Docker in `alaa-docker-production/SKILL.md:40-41` and `references/20-compose-authorship.md:138-165`, and for Kubernetes in `alaa-k8s-helm/references/kubernetes-resource-patterns.md:95-106` and `openshift-and-managed-platforms.md:102`. AGENTS.md has no owner row for it. Proposal: name `alaa-docker-production` as the owner in AGENTS.md. A new skill is not needed.

**M2-03 Uncertainty-marker family.** `[R]` `alaa-php-clean-code/SKILL.md:143` uses `NEEDS_<PROVIDER>_CONFIRMATION` or `[gap]`. `alaa-laravel-public-api-contract-pack/SKILL.md:97-103` uses `NEEDS_BACKEND_CONFIRMATION`. The grounding rule in the global contract uses `NEEDS_CONFIRMATION` and `[question]`/`[todo]`. Three conventions, no owner. Proposal: one owner, most naturally `alaa-prompting-guide` for authored artifacts. This is a convention, not a skill.

**M2-04 Dispatch return envelope.** See M1-29. The clauses are split across three owners. I do not propose a new skill. Assign one owner per clause, as the reviewer suggested.

**M2-05 Cache versus IndexedDB rule in frontend.** Covered by M1-12. Owners exist, so this stays in mode 1.

## D. Items reviewed and not reported

- No ALWAYS, NEVER, MUST, CRITICAL or IMPORTANT walls in the reviewed skills, with the exceptions quoted from references. Lanes reported zero or near-zero counts.
- No angle brackets in any `description` field (grep, all lanes).
- No broken cross-skill reference was confirmed beyond those listed in C-33 and C-19. Reviewers reported only a few; the checkers passed.
- `alaa-shaka-player/assets/templates/offlineDownload.ts` is not referenced by any file in that skill (`[R]`, nit). Keep for the optimization file's asset review.

## E. Not assessed

- Model and effort control for every reviewer lane. Blocked. The parent pair was never recorded.
- Most `references/` files. Coverage per lane is listed in each lane's report; the parent did not read them.
- Scripts were read for existence only. Behaviour and exit codes were not run.
- Upstream facts (Fiber defaults, Vector 0.57.0, Node and Alpine versions, Arvan and tusd numbers, Mediana and Bale vendor rules) were not checked against sources.
- Out-of-repo owners: service repositories, `alaa-go-chi` `docs/CONSUMERS.md`, the global test-environment reference, and any committed code registry.

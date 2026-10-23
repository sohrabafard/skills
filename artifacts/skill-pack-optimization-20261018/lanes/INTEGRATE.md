## INTEGRATE lane result

A1 routes the Arvan CaaS load decision through the canonical `caas-arvan-kuber/SKILL.md` deciding-test section; the two READMEs apply Arvan-first precedence only when that test fires. A6 states `/name` as the cross-skill source-reference form in the three assigned skills and updates only the two assigned runtime-ops references.

Files changed:
- `skills/sohrab/README.md`, `skills/sohrab/README.fa.md`: point to the canonical deciding-test section; precedence is conditional on its result. Persian remains Persian.
- `skills/sohrab/alaa-postman-collections/SKILL.md`, `skills/sohrab/alaa-algorithms-data-structures/SKILL.md`, `skills/sohrab/alaa-system-design/SKILL.md`: describe `/name` as the source-reference convention, without asserting runtime invocation syntax.
- `skills/sohrab/alaa-codex-runtime-ops/SKILL.md`, `skills/sohrab/alaa-codex-runtime-ops/references/20-command-and-path-discipline.md`: convert only the two assigned bare `$service-runtime-kit-governance` references.

Protected: generic Kubernetes/Helm/GitLab owners; conditional A1 precedence; `agents/openai.yaml` `default_prompt` Codex `$` sigils; runtime-generated prompt rules; no blanket legacy-call-site sweep.

Full-read provenance: all four affected skill trees were read completely after the initial edits: 4 skill files, all 35 references, all 3 scripts. The initial edits preceded those reads; the later full reads resolved that evidence gap. Canonical relevant-input manifest: `artifacts/skill-pack-optimization-20261018/lanes/INTEGRATE-input-manifest.json` (54 sorted relative-POSIX paths, path + NUL + raw-byte SHA-256: `3fa287188381304840681eee0e6da28a2800cad09eddb1fb8f012323afc33b0f`).

Draft/compression decisions: `INTEGRATE-draft.md` records A1/A6. A1 points to the canonical narrow trigger instead of restating its test; A6 removes dual-runtime invocation text while retaining source-reference convention, the metadata exception, and the limited call-site scope.

Verification from `/home/sohrab/project/skills` (workspace-write, ordinary host execution):
- `python -B scripts\check_fleet_references.py --skill alaa-postman-collections --skill alaa-algorithms-data-structures --skill alaa-system-design --skill alaa-codex-runtime-ops` â€” exit 0; findings none; 3 informational unmarked target-repository paths in Postman.
- `python -B skills\sohrab\alaa-repo-docs\scripts\check_markdown_links.py . --files skills/sohrab/README.md skills/sohrab/README.fa.md skills/sohrab/alaa-postman-collections/SKILL.md skills/sohrab/alaa-algorithms-data-structures/SKILL.md skills/sohrab/alaa-system-design/SKILL.md skills/sohrab/alaa-codex-runtime-ops/SKILL.md skills/sohrab/alaa-codex-runtime-ops/references/20-command-and-path-discipline.md` â€” exit 0; seven Markdown files validated.
- `git diff --check -- <same seven paths>` â€” exit 0.
- `python -B -` focused assertions â€” exit 0; all seven files UTF-8/no BOM/LF, both README canonical pointers and conditional precedence, three source-reference clauses, two scoped runtime references, and four metadata `$` default-prompt sigils.

Earlier initial checks ran once with `python` without `-B`; no new cache artifact was identified. Existing cache provenance remains unknown (parent had already observed the repo-docs cpython313 and Postman cpython314 caches). No runtime claim. Independent review and Phase 4 acceptance remain unrun.

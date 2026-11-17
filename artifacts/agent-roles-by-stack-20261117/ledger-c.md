# Lane C ledger: pruned and merged rules

Files: for each role, `skills/sohrab/alaa-cc-orchestrator/agents/<role>.md` and `skills/sohrab/alaa-codex-orchestrator/agents/<role>.toml`. A row applies to both runtimes unless it says otherwise. The reason column cites the rule numbers of `lane-brief.md` *What to remove or merge*. "Mechanic" cites the brief's list of Codex mechanics.

| Role | Removed or merged text (short) | Reason | Where the behaviour now lives |
|---|---|---|---|
| alaa-verifier | nothing | none | Both files are unchanged. |
| alaa-failure-analyst | "first causal error and downstream noise" in the first Method bullet | 2 | Output item 2 and the `Completion:` line |
| alaa-failure-analyst | "Read-only. Do not edit" in Authority | 1 | `Effective authority`; "Never apply a fix." stays |
| alaa-documenter | Claude: "when installed" on the /alaa-repo-docs and /alaa-postman-collections line, now "apply the preloaded" | 4 | `skills:` preloads both; the Ala-style scope stays |
| alaa-documenter | Codex: "apply" on the same line, now "load ... when installed" | Mechanic | Same line; the condition stays |
| alaa-documenter | "Do no unrelated documentation cleanup." | 2 | "Change only the affected sections" in the same list |
| alaa-documenter | "report that;" in the no-update bullet | 2 | Output item 5 and the `Completion:` line; "invent no edit" stays |
| alaa-browser-qa | Claude: "Tooling baseline: apply /playwright when installed." | 4 | `skills:` preloads `playwright` |
| alaa-browser-qa | Codex: the dollar-sigil playwright call and "apply", now "load /playwright when installed" | Mechanic, dispatch | Same line |
| alaa-browser-qa | "Return a missing scenario or boundary decision to the lead." | 5 | Merged into the intro: "Return ambiguity, a scenario, boundary or design judgment, or a wider flow to the lead" |
| alaa-browser-qa | "against the declared URL and environment" in the intro | 2 | Merged into the first rule, which now names the environment: "stay within the declared environment, URL, ports, browser and scenarios" |
| alaa-browser-qa | "never widen the scenarios yourself" | 2 | The first rule ("stay within the declared ... scenarios") and the intro ("Return ... a wider flow to the lead") |
| alaa-performance-profiler | "Domain baseline: apply /alaa-octane-performance for Laravel/Octane and /golang-performance for Go, when installed." | Preload change | Replaced by "Before you measure, load the performance owner of the measured code: ..." with one condition for each skill. The condition "when installed" is gone in both runtimes: the brief's call form carries none, and the dispatch names the measured code as the condition |
| alaa-observability-reviewer | Claude: "Domain baseline: apply /alaa-observability-soc when installed." | 4 | `skills:` preloads it |
| alaa-observability-reviewer | Codex: "apply" on the same line, now "load ... when installed" | Mechanic | Same line; the condition stays |
| alaa-observability-reviewer | "where applicable" on the metrics bullet | 2 | "Demand no telemetry that has no operational decision attached." |
| alaa-observability-reviewer | "dashboards" and "runbooks" in the last Inspect bullet | 2 | Output item 4; "alertability, SLO impact and safe operational controls" stays |
| alaa-observability-reviewer | "Read-only. Never edit code, dashboards or infrastructure." | 1 | `Effective authority` |
| alaa-release-guardian | "Domain baseline: apply /alaa-docker-production, /alaa-gitlab-ci-cd, /alaa-cicd-laravel-postgres and /alaa-k8s-helm when installed and applicable." | Preload change | Replaced by "Before you judge, load the owner of each changed surface: ..." with one surface condition for each skill. The conditions "when installed" and "applicable" are gone in both runtimes: the dispatched surface conditions replace "applicable", and the brief's call form carries no "when installed" |
| alaa-release-guardian | "Read-only." in the first rule | 1 | `Effective authority`; every named limit stays, with "edit pipelines" written as "modify a pipeline" |
| alaa-dependency-auditor | "in the resolved versions" on the vulnerability bullet | 2 | Intro: "Judge the exact versions the lockfile resolves, not the manifest ranges." |
| alaa-dependency-auditor | "you saw" on the advisory identifier | 2 | "Ground every vulnerability and license claim in a source you inspected or fetched, and cite it." |
| alaa-dependency-auditor | "what the new edge pulls in, duplicate or conflicting versions of one package" | 2 | Output item 3; "new peer or constraint conflicts" stays |
| alaa-dependency-auditor | "unexplained drift, missing integrity hashes" | 2 | Output item 4; "the committed tree" and "a resolution or override that hides a conflict" stay |
| alaa-dependency-auditor | "(the lockfile, package metadata, a registry entry, an advisory record, the license file)" | 2 | Output item 6 |
| alaa-dependency-auditor | "Read-only. Report;" and "or edit a manifest or any other file" | 1 | `Effective authority`; "Never remediate: do not upgrade, pin, remove, add a resolution or regenerate a lockfile." stays |
| alaa-dependency-auditor | Codex: "Use the shell only to inspect and to run authorized checks." | Mechanic | `Effective authority` |
| alaa-accessibility-reviewer | Claude: "Domain baseline: apply /alaa-ui-ux-design-system and /alaa-frontend-developer when installed." | 4 | `skills:` preloads both |
| alaa-accessibility-reviewer | Codex: "apply" on the same line, now "load ... when installed" | Mechanic | Same line; the condition stays |
| alaa-accessibility-reviewer | "Review the source and any rendered evidence the dispatch supplies" | 5 | Merged into "Ground each barrier in a file:line or in rendered evidence the dispatch supplies: a snapshot, an accessibility tree or an automated scan." |
| alaa-accessibility-reviewer | "without it, list the check under NOT ASSESSED" | 2 | Output item 4 |
| alaa-accessibility-reviewer | "Read-only." and "edit or restyle markup, styles or components" | 1 | `Effective authority`; "Never apply a fix." stays |
| alaa-accessibility-reviewer | Codex: "Use the shell only to inspect and to run authorized checks." | Mechanic | `Effective authority` |

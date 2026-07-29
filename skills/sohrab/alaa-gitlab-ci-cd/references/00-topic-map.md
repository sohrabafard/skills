# Topic map

The one router for this skill. Open the narrowest file whose trigger matches the
task in front of you. Do not read every file.

| Open | When the task involves |
|---|---|
| `pipeline-authoring.md` | pipeline creation itself: `workflow:rules`, job `rules:`, `include:`, components, child pipelines, hidden jobs and the reuse ladder |
| `job-graph-and-scheduling.md` | which job runs when: `stages` versus `needs:`, `parallel:` and `parallel:matrix`, `resource_group`, `interruptible`, job `timeout:`, `retry:` and its failure classes, and the cost of the critical path |
| `cache-artifacts-and-pinning.md` | a cache key, `policy:`, `fallback_keys`, where a cache lives, artifact scoping and `expire_in`, and how an image reference is pinned in each of the five places one can appear |
| `variables-and-inputs.md` | variable precedence, masking, protected and file variables, `spec:inputs`, `id_tokens:`, the `secrets:` block, secure files, dotenv, and downstream forwarding |
| `runner-shell-and-kubernetes.md` | runner architecture: executor choice, `config.toml`, Helm `values.yaml` versus embedded TOML, RBAC and namespaces, restricted clusters, `concurrent`, distributed cache, `image_pull_secrets` and `helper_image` |
| `container-build-strategies.md` | choosing a build path: rootless BuildKit, Docker-in-Docker, a shell runner against a host daemon, Podman or Buildah, and registry cache wiring |
| `security-and-hardening.md` | runner isolation, credential handling, merge-request and fork exposure, pull policy, privileged mode, and credentials that outlive a job |
| `validation-and-debugging.md` | validating before you ship, and triaging a failure that already happened: the five failure classes, the symptom map, and what each bundled checker can and cannot see |
| `feature-version-notes.md` | whether a feature is generally available, experimental, deprecated or limited, and how to compute the current supported GitLab baseline instead of reading a stale one |
| `90-companion-boundary.md` | any question about whether this skill decides the matter, and which skill does if not |
| `00-source-map.md` | a claim that must be current: which official page is authoritative for it, and the order in which conflicting sources are resolved |

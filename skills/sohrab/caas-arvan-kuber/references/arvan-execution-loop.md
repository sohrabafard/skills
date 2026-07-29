# Delivering to Arvan: what to do, and what to do when it fails

Organised by what you are facing rather than by phase number, so an agent that arrives mid-incident does not read three ladders to reach the one paragraph it needs.

Everything generic — chart shape, validation gates, rollout debugging — belongs to `/alaa-k8s-helm` (`$alaa-k8s-helm`). What is here is the Arvan-specific step or the Arvan-specific cause.

## A. Starting a delivery task

1. **Detect the line.** Run the Step 1 block in `SKILL.md`, or `bash scripts/verify-cluster.sh NS [runner-sa]`. Write the answer into the deliverable. Everything after this depends on it.
2. **Read the budget.** `kubectl -n NS get resourcequota,limitrange -o yaml`. The LimitRange tells you whether `ephemeral-storage` is expected and what maximum a container may request; the ResourceQuota tells you how many replicas the namespace can hold at all.
3. **Read the existing exposure.** The jsonpath in `references/arvan-constraints.md` section 4 tells you which exposure mode the cluster already uses. Match it rather than introducing a second one.
4. **State the constraints that are active** for this workload — parity, stateless-only scaling, disk lifecycle, exposure mode — and only those. A constraint listed but not applicable is noise that hides the ones that matter.
5. **Build the chart or manifests with `/alaa-k8s-helm`**, then apply the Arvan facts from `references/arvan-constraints.md`.
6. **Gate it.** Run the register in `alaa-k8s-helm references/validation-workflows.md`, and add `python3 alaa-k8s-helm scripts/check_manifests.py rendered.yaml --profile arvan` for the Arvan predicates.
7. **Hand it over.** When the scope is production or stateful, emit `assets/README.operator.md.template` and `assets/RUNBOOK.operator.md.template` filled in, and confirm that every filename that can hold a decoded Secret is in the repository's ignore rules.

**When there is no shell access to the cluster**, say so in the first line of the deliverable, generate for the more restrictive of the two lines — that is column A, the pinned line — mark every line-dependent choice as an assumption, and hand the operator the exact discovery commands that settle each one.

## B. The render or lint failed

Symptom: `helm lint` or `helm template` returns an error, so nothing reached the cluster.

1. `bash scripts/render-helm.sh --chart CHART --namespace NS --values values.yaml` reproduces it deterministically and writes nothing world-readable.
2. Almost always one of: a wrong chart path, a dependency that was never built (`helm dependency build`), or YAML indentation or quoting inside a template.
3. This is a chart problem, not an Arvan problem. `/alaa-k8s-helm` (`$alaa-k8s-helm`) owns it from here.

## C. Admission rejected the manifest

Symptom: `helm template` succeeded and the API server refused the object.

1. **A container without resources, or `requests` not equal to `limits`, is the first hypothesis** — it is the constraint Arvan documents and enforces. `python3 alaa-k8s-helm scripts/check_manifests.py rendered.yaml --profile arvan` names the container.
2. Check the LimitRange: a request above `max`, or below `min`, is rejected with a message naming the LimitRange rather than the container.
3. Migration, init, and hook Jobs are containers too, and are the usual place a resource block is forgotten.

## D. A kind was rejected as unknown

Symptom: `no matches for kind` or `the server could not find the requested resource`.

1. Re-run the line detection. A manifest written for the wrong column produces exactly this.
2. Look the kind up in `references/arvan-capability-matrix.md` for the discovered line.
3. If the kind is absent on that line, follow "How to act when a kind is absent" in the matrix: say so, offer the alternative, and do not emit the object with a hopeful comment.
4. If discovery says the kind **is** served and the matrix says it is not, discovery wins. Run `bash scripts/summarize-openapi.sh --check` and record that the vendored spec no longer describes the platform, because that is the signal that Arvan has upgraded.

## E. A job is forbidden while the release looks healthy

This is the alias-versus-canonical case and it has its own file. Collect the evidence and run the conclusive token check in `references/arvan-rbac-namespace-facts.md` **before** touching any RoleBinding. Broadening a binding here grants a real permission to the wrong principal and leaves the mismatch in place.

Two adjacent causes to rule out at the same time, both owned by `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`): the job pod's pull secrets, and a runner job that tried `kubectl get namespace` or `helm --create-namespace` and died on a scope it never had.

## F. The rollout never completed

Symptom: `helm upgrade` returned, and the pods are not ready.

1. `kubectl -n NS rollout status deploy/NAME` and `kubectl -n NS get events --sort-by=.lastTimestamp`.
2. If the pods are `Pending`, read the ResourceQuota: on a tenant platform, exhausted quota looks exactly like insufficient cluster capacity.
3. If the pods are `ImagePullBackOff`, the pull Secret is the cause; `/alaa-docker-production` (`$alaa-docker-production`) owns registry and image policy and `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns the runner's copy of it.
4. Everything else — probe timing, `maxSurge`, PDB deadlock, endpoint-removal races — is `/alaa-k8s-helm` (`$alaa-k8s-helm`) `references/failure-and-load.md`.

## G. A stateful workload needs to scale

There is no in-place answer. Arvan disables both manual and automatic scaling while persistent storage is enabled. The only paths are to run more independent instances with their own disks, or to detach storage, which restarts the application. Both are runbook actions, and the RUNBOOK must contain the chosen one before anyone needs it. `/alaa-reliability-sla` (`$alaa-reliability-sla`) decides which is acceptable for the service's availability target.

## H. Rotating a secret or a registry credential

1. Update the Secret, by editing `values.secret.yaml` for a chart-managed Secret or by updating the existing Secret directly for the reference mode.
2. A change to a mounted Secret does not restart pods by itself. Add a checksum annotation on the Pod template so the chart's own upgrade rolls the workload, or restart it explicitly and say so.
3. Verify a new pod actually pulls and starts before declaring the rotation done. A pull credential that is wrong is invisible until the next pull.
4. Never pass a secret through `--set`; it lands in shell history and in the release's stored values.

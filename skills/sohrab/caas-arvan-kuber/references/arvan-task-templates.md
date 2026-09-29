# Task templates

Three scaffolds. Fill in every angle-bracketed slot before using one; a slot left unfilled is a fact nobody discovered.

Each template assumes Step 1 in `SKILL.md` has already run, because every one of them has a field that depends on the answer. A path written with a leading skill name means a file inside that skill: `/alaa-k8s-helm` for the gate register and the manifest checker, `/caas-arvan-kuber` for the Arvan references.

## Template 1: Helm or manifest implementation

When implementing or validating a Helm chart or rendered manifest, use this payload to capture discovery, active constraints, validation and delivery details. Read the complete [template](./arvan-task-templates/10-helm-or-manifest-implementation.md).

## Template 2: RBAC incident triage

When investigating an authorization failure, use this payload to separate observed namespace and principal facts from Kubernetes guarantees and Arvan observations. Read the complete [template](./arvan-task-templates/20-rbac-incident-triage.md).

## Template 3: Exposure mode selection

When selecting an application exposure mode, use this payload to record the existing namespace pattern, ingress evidence, and required operator prerequisites. Read the complete [template](./arvan-task-templates/30-exposure-mode-selection.md).

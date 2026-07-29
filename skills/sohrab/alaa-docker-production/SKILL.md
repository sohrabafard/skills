---
name: alaa-docker-production
description: "Use when writing or reviewing a Dockerfile, .dockerignore, Compose file, Swarm stack file, build secret, attestation flag, registry or mirror reference, healthcheck, rollout or resource-limit key, or the interpolation form of a variable in a production-shaped file. It owns how the image and runtime file are expressed and decides no gate. Not for gate policy (alaa-frontend-devops), runner expression (alaa-gitlab-ci-cd), Kubernetes or Helm (caas-arvan-kuber, alaa-k8s-helm), which generator variable exists (service-runtime-kit-governance), or proxy directives (alaa-haproxy)."
---

# Alaa Docker Production

This skill owns the container layer of a fleet running at 99.99%: every Dockerfile, Compose file
and Swarm stack file, and the interpolation form of every variable in them. It is sole owner of
the Dockerfile: `service-runtime-kit` generates none (`README.md:182`).

## Ownership, and when not to use this skill

`alaa-docker-production` owns how the build and runtime images and any Compose or Swarm stack file
are expressed — the Dockerfile and its stages, the order and contents of its layers, what survives
into the final image, and every key in a Compose or stack file including the interpolation form of
every variable written into it — and it decides no gate: `/alaa-frontend-devops`
(`$alaa-frontend-devops`) owns the frontend delivery gate register and states the obligations an
image must satisfy, `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns how a gate is expressed on a
runner, and `/alaa-haproxy` (`$alaa-haproxy`) owns how a cache or routing decision is expressed as
a directive. When a gate names a property of an image or a Compose file, this skill writes the
instruction or key that satisfies it and does not change the gate.

`/service-runtime-kit-governance` (`$service-runtime-kit-governance`) owns which generator variable
expresses a runtime value — its name, its tracked default, which contract file holds it, and
whether changing it forces a re-render. This skill owns the Docker or Compose construct that
variable is interpolated into and the interpolation form it is written in. A new knob goes there;
a change to what the generated file looks like comes here. Where a variable's
default would silently disable a safety control, the interpolation form is this skill's call, and
it is `${VAR:?message}` with no default, whatever tracked default the generator carries.

## Three rules that never cost a hop

1. **A production-shaped file fails closed on every safety control.** Mandatory is `${VAR:?why}`;
   optional is `${VAR:-default}`, and writing that asserts the default is correct in production. A
   credential, key, token, cap, auth toggle or TLS flag takes `:?` with no default permitted,
   including `:-0` and bare `:-`, because an empty password and a cap of zero both mean "no
   control". Compose interpolation reads the shell and `--env-file` only, never a service's
   `env_file:` key. `references/25-fail-closed-interpolation.md`.
2. **The final stage is the whole security posture.** Non-root `USER`, `cap_drop: [ALL]`,
   `security_opt: [no-new-privileges:true]`, read-only root filesystem with named writable mounts,
   and no package manager, compiler or dev dependency in the image; anything unmet is named in the
   merge request. `references/10-dockerfile-authorship.md`.
3. **Verify the rendered model, not the file you wrote.** Run `docker compose config` and the
   `scripts/` checkers on the generated files before `up` or `stack deploy`. Exit 0 is clean, 1 is
   a violation, 2 means the tree could not be read and is not a pass.

## Navigation

`references/00-topic-map.md` routes every task and symptom here to one file; open it when you do
not know which file you need. Model and effort decisions belong to `/alaa-prompting-guide`
(`$alaa-prompting-guide`), `references/50-effort-and-thinking.md`; never write a model name or an
effort key into anything this skill emits.

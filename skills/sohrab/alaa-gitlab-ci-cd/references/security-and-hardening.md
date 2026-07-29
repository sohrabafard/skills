# Security and hardening

How a hardened pipeline and runner are expressed. Threat classification, exposure
severity, rotation and disclosure are `/alaa-security-review`
(`$alaa-security-review`)'s decisions; bring it in whenever a finding needs a
severity or a credential needs a rotation plan.

## Table of contents

- Threat model by runner type
- Privileged mode and daemon risk
- Credentials: the order to try
- Credentials that outlive a job
- Merge request and fork exposure
- Pull policy and image trust
- Job token scope
- Security review checklist

## Threat model by runner type

**Shell runner.** Highest host exposure. The job script runs as the runner user
on the host; the build directory, the cache directory and anything the job writes
outside them persist between jobs and between projects on that host.

**Kubernetes executor.** Better isolation by default. The real posture still
depends on whether the runner is privileged, whether namespaces are shared, how
nodes are isolated, what RBAC the service account holds, and how tight
`allowed_images` and `allowed_services` are.

**Shared persistent runners.** Higher cross-project risk than ephemeral dedicated
ones. The shared surfaces are the cache, the fetched working tree, cached image
layers and any credential that reaches the job environment.

## Privileged mode and daemon risk

Treat as high risk: privileged containers, Docker-in-Docker, a mounted host
`docker.sock`, and shell-runner jobs with host-level container tooling.

Where one of these is required, the hardened form is a dedicated runner fleet, a
node selector that keeps it off general-purpose nodes, restriction to protected
refs and trusted projects, and a note in the answer stating the boundary. Where
even the hardened form is unavailable, the design does not ship on a request
alone; `/alaa-security-review` (`$alaa-security-review`) decides whether an
exception exists. Name that owner in the answer rather than granting it yourself.

## Credentials: the order to try

1. **`id_tokens:`** — a short-lived OIDC token minted per job. Generally
   available on all tiers.

   ```yaml
   deploy:
     id_tokens:
       VAULT_ID_TOKEN:
         aud: https://vault.example.com
     script:
       - vault write -field=token auth/jwt/login role=ci jwt="$VAULT_ID_TOKEN"
   ```

   `CI_JOB_JWT` and `CI_JOB_JWT_V2` are removed; a pipeline still using them gets
   `401 Unauthorized`.

2. **A supported `secrets:` integration** — the secret is fetched by the runner
   and exposed as a file path, so nothing long-lived lives in project settings.

3. **GitLab secure files** for a credential that is a file by nature: a
   keystore, a provisioning profile, a signing key. Download them with
   `glab securefile`; the older `download-secure-files` tool was deprecated in
   GitLab 18.6.

4. **Protected file or masked variables**, when there is no native integration.

Rules that hold at every level:

- Never write a secret literal into YAML. `validate_gitlab_ci.py` reports
  `secret-inline`.
- Never print a secret value. Shell tracing prints expanded arguments, so masking
  does not survive it; `validate_gitlab_ci.py` reports `set-x` and `debug-trace`.
- Use a file variable when a tool expects a path, and write a plain variable to a
  temp file inside the job when it does not have one — under `umask 077`, removed
  by an `EXIT` trap.

## Credentials that outlive a job

A credential is only as short-lived as the most persistent place it is written.
On a shell runner the workspace survives the job, so:

- **Never `git remote set-url` with a token in the URL.** That writes the token
  in cleartext into `.git/config`, which persists in the build directory between
  jobs and between projects on the host. Use `git -c http.extraHeader="PRIVATE-TOKEN: $TOKEN"`
  per invocation, or a credential helper pointed at a file the job deletes.
  `validate_gitlab_ci.py` reports `script-credential-in-url`.
- **Never leave a registry login in place.** `docker login` writes
  `~/.docker/config.json`. Log out, or remove the file, in `after_script`.
- **Never write a secret to a path under the build directory.** Use a temp file
  outside it, created with a restrictive umask and removed on exit.
- **Never put a secret in a `reports:dotenv` artifact.** It is stored as an
  artifact with the artifact's retention and the project's download rules.

The same reasoning applies to data: an artifact containing a database dump or an
export of production data is a copy of that data governed by artifact retention.
Whether the data class may be copied at all is `/alaa-security-review`
(`$alaa-security-review`)'s call.

## Merge request and fork exposure

A CI configuration change is a code change and is reviewed as one.

Before enabling anything sensitive in merge request pipelines, establish:

- Whether the pipeline runs in the source project or the parent project.
- Whether the source is a fork.
- Whether the ref is protected — `$CI_COMMIT_REF_PROTECTED == "true"`, which is
  what decides access to protected variables and protected runners, and is not
  the same predicate as "this is the default branch".
- Whether the runner fleet that would pick the job up is trusted for that path.

Where the task touches fork merge requests, protected refs or deploy credentials,
state the exposure explicitly in the answer.

## Pull policy and image trust

On a shared or less-trusted runner, use `always` for private images: with
`if-not-present`, a layer already cached on the node under a reused tag is served
to the next project that asks for that tag. Allow `if-not-present` only where
every image and every user of that runner is trusted, and say which of those two
you are relying on.

Keep `allowed_images` and `allowed_services` as real allowlists. An entry that
wildcards a whole registry or namespace admits everything in it.

## Job token scope

Treat `CI_JOB_TOKEN` as a credential. Keep the project allowlist tight rather
than broadly permissive, prefer project or environment scoping over instance-wide
access, and package registry authentication tightly around the push or pull step
rather than at the top of the job.

## Security review checklist

- Are all secrets externalised, scoped, and absent from YAML?
- Does any credential survive the job on a persistent runner?
- Is any privileged behaviour isolated, justified, and attributed to a named
  approver?
- Are runner tags and trust boundaries explicit?
- Do the merge-request and fork paths test `$CI_COMMIT_REF_PROTECTED` where
  protected access is assumed?
- Are images pinned and allowlists narrow?
- Does any artifact carry data that should not leave its store?
- Would another engineer be able to state the risk after one read-through?

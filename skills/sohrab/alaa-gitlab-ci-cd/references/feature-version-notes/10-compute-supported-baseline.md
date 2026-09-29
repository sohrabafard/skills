# Compute the supported baseline

Use this reference when the task needs current version-sensitive behavior. Every entry retains its re-derivation source; check those sources at use time.

For the dated release and baseline calculation, see [the source map](../00-source-map.md).

## Compute the baseline, do not read it

GitLab's published release and maintenance policy:

- **Major releases: yearly, in May.** GitLab 19.0 was released 2026-05-21.
- **Minor releases: monthly, on the third Thursday of each month.**
- **Patch releases: twice monthly**, the Wednesday before and the Wednesday after
  the monthly minor.
- **Backports:** bug fixes go to the current stable release only; security fixes
  go to the current stable release plus the previous two monthly releases.

From that: the current supported line is the newest minor, and anything older
than two minors behind receives no security backport. Do not write a baseline
version into a design. Write "the current stable line" and, when a specific
number is needed for an answer, derive it at that moment:

| To find | Run or open |
|---|---|
| the current stable GitLab version and cadence | https://docs.gitlab.com/policy/maintenance/ |
| what a specific release changed | https://docs.gitlab.com/releases/ |
| the GitLab Runner version the docs describe | https://docs.gitlab.com/runner/ |
| the newest published runner helper image tag | https://hub.docker.com/r/gitlab/gitlab-runner-helper/tags |
| the version of a live instance | the instance's `/help` page, or `glab api /version` |
| the version of a live runner | `gitlab-runner --version` on the host |

Keep the Runner's `major.minor` in step with the GitLab instance's. An older
runner usually works against a newer GitLab, but features gated on the newer
version are unavailable and some fail without a clear message.

**As of 2026-07-29** the maintenance policy page named **19.2** as the current
stable release and the Runner documentation described **19.0**; the newest
published helper image tag was `x86_64-v19.1.2`. Those three numbers are here as
a dated observation, not as a baseline to design against.

**2026-09-29 refresh:** GitLab 19.4 was released on 2026-09-17:
https://docs.gitlab.com/releases/19/gitlab-19-4-released/. The July Runner/helper
observations above remain historical; this refresh does not validate newer helper
image tags or change the consuming instance minimum. Match its actual version.

## Writing an answer when the target versions are unknown

1. State that the design targets the current stable line and name the page that
   defines it, rather than naming a version you did not check.
2. Name any feature whose status is experimental, and say what a stable
   alternative would be.
3. Where a design would differ on an older instance, give the difference in one
   sentence rather than designing for the older instance by default.

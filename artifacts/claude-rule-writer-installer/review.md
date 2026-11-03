# Claude rule-writer installer review

- Plan: `beads:alaa-hv28`; final phase: `alaa-hv28.1`.
- Scope: `scripts/install_claude_rule_writer.py`, `install-skills.md`, and its linked `docs/install-skills/` guides.
- Base: `ff6bd5acf8a1886ea7b6648f79d5c6b8a913358c` on `main`; initially clean.
- Reviewed installer SHA-256: `a48e57592c94375556b2d8c170542410fd49273a05044b6fe90a574e181b31d8`.
- Evidence: [independent focused verification](independent-verification.md).

## Review judgments

The parent authored no installer code and independently reviewed its complete behavior.
Correctness: APPROVED-WITH-NITS. Preview is read-only. Updates preserve manifest bytes and unowned files.
The update publishes one managed file atomically after retaining the previous bytes.
Fresh installation publishes the validated candidate directory. Cooperating installers use a directory lock.

Security specialist: PASS. No actionable finding under the local-operator, trusted-PATH boundary.
The validator runs with an isolated profile and a bounded timeout. Managed path symlinks are rejected.

Release specialist: READY after reviewing the final installation procedure. Documentation explains
apply authority, recovery, reload, dependency checks, and the following limits.

- No concurrent manual or plugin-manager writes to the same target during apply.
- The lock does not protect against unrelated filesystem writers or power loss.
- Candidate validation covers the manifest and canonical wrapper, not unowned plugin components or runtime behavior.
- An unchanged wrapper skips validation. Customized manifests requiring additional staged files may be rejected.
- Validator errors currently report status without detailed validator output.
- A missing old wrapper has no backup; recovery must preserve any pre-existing manifest and other files.

## Live inspection and authority

The observed inventory listed 19 enabled plugins: all 18 previously listed plugins plus
`alaa-rule-writer@skills-dir`. This proves inventory continuity, not every plugin's functionality.
The earlier manual command wrote only this plugin's manifest and agent file.
No snapshot from before that manual command exists, so historical byte equality is not claimed.

This task performed no live installation or update. The real-home preview reported `unchanged`.
Hashes of the existing shared settings, marketplace registry, and this plugin's manifest and agent
matched before and after task validation. Missing optional registry/settings files remained absent.
No model session, agent invocation, or skill preload was exercised.

## Final candidate

The prior 301-line installation guide was split by topic to meet its documentation gate.
Both generated spans and the machine-read source-root section remain byte-identical.
The root and two cohesive procedure pages are YELLOW; four short child guides are GREEN.
The root keeps entry points, canonical paths and parser data together. Vendor management and
rule-writer recovery each remain one procedure. Further splits would fragment these topics.
The [final gates](final-gates.md) passed, including all 15 shell examples' syntax and the existing
skill installer's read-only run with zero conflicts. Installer behavior evidence remains valid
because the reviewed source SHA did not change.

`IMPLEMENTED` and `MERGE_CANDIDATE` are proven for this local repository change.
`RELEASE_CANDIDATE` and `PUBLISHED` were not requested. No push, remote sync or live update occurred.

## Curation

No separate durable-memory candidate is admitted. The installer and installation guide own the
reusable procedure and limitations. No memory write or publication is authorized or required.

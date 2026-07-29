# Verification and Rollback

Open this file to close out a delivery change and state what was validated. For a live failure, go to `references/45-deploy-failure-playbook.md` instead.

## The verification loop

1. Build in the deployment mode named in the task — `quasar build -m ssr`, `-m pwa`, or the SPA default. A dev-server check does not satisfy this step, because the dev server does not emit the artifact this skill governs.
2. Run `scripts/verify-artifact-contract.mjs <dist-root>` against the emitted tree, and read its exit code as `SKILL.md` defines it.
3. If the change touched routing, `publicPath`, a remote asset base, or the serving layer, request one representative runtime URL of each affected response class and record the status code and the `Cache-Control` header returned.
4. Re-run the exact reproduction that opened the task and include its output. If no reproduction existed, state in the closeout that no pre-change failure was observed.

Step 4 is the one that is skipped. A delivery change that was never demonstrated to fix anything is a delivery change that was never demonstrated.

## Proof levels

Which of the six proof levels a given check occupies, and what a level obliges, is owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`). Map each check above to a level there rather than inventing a parallel vocabulary here. The artifact-contract gate is an assertion on a produced artifact, not a unit test, and calling it one misreports the strength of the evidence.

## The rollback path

"Be ready to describe what to revert" is not a rollback path. A rollback path is a command that has been run, or a set of files that has been verified present. Before a delivery change merges, write these four lines into the merge request:

1. **The rollback unit.** Name the exact thing that gets reverted: an image tag, an artifact bundle, or a commit. For a frontend deployment the unit is normally the image tag, because reverting a commit rebuilds and produces new hashed filenames, which is a fresh deploy and not a rollback.
2. **The command.** The literal command or pipeline action that puts the previous unit back, written out. If it is a manual pipeline job, name the job.
3. **The precondition.** What must still exist for the rollback to work — most often, the previous release's hashed assets still present at the serving origin. Confirm they are present before merging, not after failing.
4. **The irreversible part.** Anything the change does that a rollback does not undo: a published secret, a lifecycle rule that already deleted the previous assets, a service worker already installed in users' browsers, a cache entry with a long `max-age` already handed out. If this line is empty, say so explicitly.

A change whose fourth line is non-empty is not rolled back; it is rolled *forward*, and the forward fix is designed before the change ships.

## Closeout

Report, in this order:

- what changed in the build or delivery path, named by file
- the provenance values of the artifact that was produced: commit, build mode, build timestamp
- which gates ran, and their exit codes
- which runtime URLs were requested and what they returned
- the four rollback lines above
- what remains unverified and requires deploy-time confirmation, stated as a question someone can answer rather than as a reassurance

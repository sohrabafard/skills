# Feature delivery
1. Requirements: derive acceptance examples and non-goals; scout current execution path.
2. Lead: classify risk, identify shared contracts and assign ownership.
3. API/architect: settle only decisions necessary for implementation.
4. Engineers: implement independent slices after contracts stabilize. Test designer
   derives edge cases independently; test engineer owns separate test paths.
5. Integrator: assemble the final state; freeze the reviewed diff.
6. Reviewer: inspect actual changes. Security/data specialists join only when the
   changed surface warrants them. Findings can be empty.
7. Integrator: apply accepted fixes, rerun affected/required checks, refresh stale review.
8. Lead: deliver acceptance evidence and rollout implications. No automatic deployment implied.

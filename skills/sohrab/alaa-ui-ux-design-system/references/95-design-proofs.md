# Design Proofs

Read this file when you claim a design change is correct, or when someone asks what proves it. **A design change with no artefact is a claim, not a result.**

This file states what each verification must leave behind. Test design and the proof levels that classify these — what counts as a unit, an integration, a contract or an end-to-end proof, and which level a given risk demands — are owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`). Where baselines are stored, how they are versioned, and how CI runs them is owned by `/alaa-frontend-devops` (`$alaa-frontend-devops`). This file owns only what a design change must produce.

## The artefact table

| Claim | Artefact | Produced by |
|---|---|---|
| "The palette passes contrast" | the printed pair-by-pair ratio table, per theme | `scripts/check-design-system.mjs --contrast` |
| "The theme is complete" | the list of roles per theme block with the diff between them | `--themes` |
| "There are no raw values in components" | the `file:line` list, empty or explained | `--tokens` |
| "Direction-bearing icons are handled" | the `file:line` list of unwrapped physical-direction icon names | `--icons` |
| "The layout works in both directions" | one screenshot pair per changed route, same viewport, real Persian content | a browser, headed or headless |
| "Reduced motion is honoured" | one screenshot or recording pair per animated surface, preference on and off | a browser with the preference emulated |
| "It works at 375px and at 200% zoom" | one screenshot per changed route at each | a browser |
| "It is keyboard operable" | the ordered list of stops for each primary flow, walked, not inferred | a person at a keyboard |
| "It passes an automated scan" | the scan output, or a statement that the scan could not run and what was done instead | the repo's integration, or `npx @axe-core/cli` |
| "Nothing else changed visually" | the visual-regression diff set | the repo's visual-regression suite |

**A row with no artefact is reported as unverified.** Never as passing.

## Which surfaces a token change touched

The question a reviewer actually needs answered before approving a token edit: **what does this change, and where?**

1. **Find every consumer of the token** before changing it. A token with many consumers is a system-wide change; a token with one is a component token in the wrong place.
2. **Print the affected file list with the diff.** A reviewer who cannot see the blast radius is approving on trust.
3. **A token with zero consumers is dead** — delete it rather than updating it. A token with exactly one is premature abstraction — inline it or justify it.
4. **A colour token change is a contrast change.** Re-run the contrast report and attach both the before and the after; a ratio that moved from 4.9 to 4.4 is a regression the diff image will not show.
5. **A spacing, radius or motion token change is a visual-regression change** across every consumer, which is exactly what visual-regression baselines exist for.

## Visual regression

- **Baseline what is stable, not everything.** A suite that flakes is a suite that gets disabled, and a disabled suite proves nothing.
- **Exclude by construction, not by threshold.** Freeze time, seed randomness, stub avatars and user-supplied content, disable animation for the capture. A tolerance percentage tuned until the suite passes has been tuned until it cannot fail.
- **Capture both themes and both directions** for any component that renders in more than one — those are the cells that break.
- **A diff is reviewed by a person, and the reason for accepting it is recorded.** "Baseline updated" with no reason is how an unintended change becomes the new truth.
- Storage, retention and CI wiring: `/alaa-frontend-devops` (`$alaa-frontend-devops`).

## What is proven by construction

Not everything needs an artefact, and knowing which is the difference between a proportionate check and theatre.

- A component built entirely from semantic tokens and logical properties **cannot** drift in colour or direction; the checker proves the construction and no per-cell rendering is needed.
- A variant drawn from a closed enum **cannot** receive an arbitrary visual value; the type proves it.
- A direction-bearing icon resolved through a role **cannot** point the wrong way in one direction; the wrapper proves it.

**This is the payoff of the token, enum and logical-property rules:** they convert a combinatorial verification problem into a linear one (`45-render-and-asset-budgets.md`). A change that needs many cells rendered is telling you it bypassed one of them.

## The delivery note

Every UI delivery states, in this order:

1. What changed, in design terms.
2. Which gates were verified and how — with the artefact, or its absence named.
3. Which theme-matrix cells were rendered, and which were not.
4. Which assumptions were taken from a default rather than answered (`10-design-workflow.md`).
5. What was deliberately not done, and why.

**Never report a check that was not observed.** A check that could not run in this environment is reported as could-not-run, with what was done instead — which is a different statement from clean, and the difference is the whole point.

## Anti-patterns

- "Verified" with no artefact.
- A visual-regression tolerance raised until the suite passed.
- A baseline updated with no recorded reason.
- A contrast claim made by looking at the screen.
- A token changed with no list of what it touched.
- A keyboard walk reported as done because the component "uses native elements".
- An accessibility scan reported as clean when the tool was not installed.

## Pairing

- The gates these artefacts prove: `90-quality-gates-and-review.md`
- Which cells are mandatory: `45-render-and-asset-budgets.md`
- The checker: `scripts/check-design-system.mjs --help`
- Accessibility verification detail: `85-accessibility-patterns.md`

# UX Writing and Microcopy

Read this file when writing or reviewing any string a user will read: buttons, errors, empty states, confirmations, notifications, onboarding. Copy is part of the design system and carries the same consistency rules as color and spacing.

Persian mechanics — direction, ZWNJ, digits, dates — are in `05-rtl-and-persian.md`. This file covers voice, register and wording.

## Voice and register

- Derive voice from the design brief (`10-design-workflow.md`). A fintech dashboard and a children's learning app do not share a voice. Record the decision in `MASTER.md` and hold it; register drift across pages reads as broken.
- Default posture: plain, direct, confident. Say what happens. Skip filler, hype and blame.
- Sentence case for UI text; title case only where the brand explicitly demands it.
- **One concept, one word, everywhere.** A "course" never becomes a "class" two screens later. When you introduce a term, add it to the terminology list in `MASTER.md`; when you find a synonym in the repo, replace it rather than adding a third.

## Actions and buttons

- A call-to-action is a verb plus an outcome: "Start learning free", "Save changes". Never "Submit", "OK", "Click here".
- Destructive actions name their consequence in the button, not in the question: "Delete 3 lessons", not "Are you sure?" with Yes and No. The confirming button repeats the action verb rather than saying "Confirm".
- Paired buttons are never ambiguous. "Save" and "Discard changes", not "Yes" and "No" for anything with stakes.
- A button's label states what will happen, not what state the system is in. "Saving..." is a state, and it belongs in the button's loading state, not in its label.

## Errors, empty states and feedback

- **Errors state cause and fix in the user's language:** "This code has expired. Request a new one." Never a bare code, never blame ("You entered an invalid..."), never "An error occurred".
- The recovery path is part of the message, not a separate discovery. If there is nothing the user can do, say that, and give them the reference from `28-ui-diagnosability.md` so someone else can.
- **Never ask the user to reformat input the product can normalize itself.** "Please use English numbers" means the digit fold is missing, not that the user made a mistake.
- Empty states teach and invite: what this area is, plus the one action that fills it. Two short lines beat a paragraph. The visual design of the state is in `15-designed-failure-states.md`; this file owns the wording.
- Success feedback is brief and specific: "Lesson published". Loading copy states what is happening when it runs long: "Uploading video, 40%".
- Toasts carry one idea each, front-loaded, no more words than fit at a glance. A toast never carries the only copy of an error message.

## Persian register

- **Register decision first:** formal or conversational, per product, recorded in `MASTER.md`, then absolutely consistent. Mixed register in one flow is a defect.
- Never literal-translate an English UI idiom. Write the Persian a native product would use, and keep the count of Latin technical terms inside Persian sentences low.
- Persian punctuation is used throughout, including in error and validation strings, which are the most commonly left in a half-translated state.
- The mechanics of half-spaces, digits, dates and direction are in `05-rtl-and-persian.md`; a reviewer checks both files on any Persian copy change.

## Length as a design constraint

- Every string has a designed maximum. Write the longest realistic case, not the demo case, and check it at 375px.
- Persian translations of English UI strings commonly run longer. A layout tuned to the English label will clip.
- A label that must be truncated to fit is a layout problem, not a copy problem. Fix the layout.

## Anti-patterns

- "Submit", "OK", "Click here"; "An error occurred" with no cause or fix.
- Jokey copy on payments and deletions; robotic copy in a playful product.
- Placeholder text used as the field's instructions (`60-components-states-and-ux.md`).
- Walls of onboarding text nobody reads.
- A second word for a concept that already has one.
- Asking the user to reformat something the product can normalize.
- Copy written and checked only in English on a Persian-first product.

## Pairing

- Where copy sits inside components: `60-components-states-and-ux.md`
- The states this copy describes: `15-designed-failure-states.md`
- The reference an error message carries: `28-ui-diagnosability.md`
- Persian mechanics: `05-rtl-and-persian.md`
- Voice source and persistence: `10-design-workflow.md`

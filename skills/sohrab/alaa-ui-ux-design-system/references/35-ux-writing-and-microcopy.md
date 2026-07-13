# UX Writing and Microcopy

Use this file when writing or reviewing interface copy: buttons, errors, empty states, confirmations, notifications, onboarding. Copy is part of the design system — same consistency rules as color and spacing.

## Voice and register

- Derive voice from the design brief (`10-design-workflow.md`): a fintech dashboard and a kids' learning app do not share a voice. Record the decision in MASTER.md and keep it — register drift across pages reads as broken.
- Default posture: plain, direct, confident. Say what happens; skip filler ("Please note that..."), hype, and blame.
- Sentence case for UI text; title case only where the brand explicitly demands it. Terminology is fixed: one concept, one word, everywhere (a "course" never becomes a "class" two screens later).

## Actions and buttons

- CTA copy is verb + outcome: "Start learning free", "Save changes" — never "Submit", "OK", "Click here".
- Destructive actions name their consequence: "Delete 3 lessons", not "Are you sure?" with Yes/No. Confirmation buttons repeat the action verb, not "Confirm".
- Paired buttons are never ambiguous: "Save / Discard changes", not "Yes / No" or "OK / Cancel" for anything with stakes.

## Errors, empty states, and feedback

- Errors: cause + fix in the user's language ("This code has expired — request a new one"), never raw codes alone, never blame ("You entered an invalid..."). Recovery path is part of the message (`60-components-states-and-ux.md`).
- Empty states teach and invite: what this area is + the one action that fills it. Two short lines beat a paragraph.
- Success feedback is brief and specific ("Lesson published"); loading copy states what is happening when it takes long ("Uploading video — 40%").
- Notifications/toasts: one idea each, front-loaded, no more words than fit at a glance.

## Farsi microcopy (mandatory for Farsi products)

- Register decision first: formal (شما) vs conversational — per product, recorded in MASTER.md, then absolutely consistent. Mixed register in one flow is a defect.
- Half-space (نیم‌فاصله) discipline: correct ZWNJ in compounds and affixes (می‌شود، کتاب‌ها) — its absence reads as careless in every label.
- Persian punctuation (، ؛ ؟) with RTL-safe placement; digits follow the product-wide decision from `30-typography-and-color.md`, applied in copy, numbers, and dates alike.
- Never literal-translate English UI idioms; write the Farsi a native product would use. When mixing scripts (Latin brand/technical terms inside Farsi text), keep the term count low and mark direction so punctuation does not scramble.
- Dates and numbers localized deliberately (Jalali vs Gregorian per product decision), not left to library defaults.

## Anti-patterns

- "Submit / OK / Click here"; "An error occurred" with no cause or fix.
- Jokey copy on high-stakes actions (payments, deletion); robotic copy in a playful product — voice ignoring the brief.
- Placeholder text as instructions (`60-components-states-and-ux.md`); walls of onboarding text nobody reads.
- Farsi UI with missing نیم‌فاصله, mixed formal/informal register, or half-translated English idioms.

## Pairing guidance

- Voice source and persistence: `10-design-workflow.md` + MASTER.md
- Where copy lives in components (labels, helpers, errors): `60-components-states-and-ux.md`
- Typography/digits/RTL mechanics: `30-typography-and-color.md`

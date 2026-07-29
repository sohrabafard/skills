# RTL and Persian Rendering

Read this file whenever the product renders right-to-left text. On `client` that is every route, so this file applies to every `client` design task.

RTL is a configuration axis, not a translation step. Every rule below names a mechanism, a value, or a list you can check.

## 1. Direction is set in CSS and markup, never with characters

The house pattern, live in `client`: direction is expressed as the `dir` attribute plus CSS `direction` and `unicode-bidi`. It inserts no characters into the string.

- A run of text whose direction is **known and fixed** (an OTP code, a TOTP secret, an email address, a URL, a version string) gets `dir="ltr"` on its own element, and `direction: ltr` plus `text-align: left` in its stylesheet. Live examples: `src/auth/AuthOtpPanel.vue:38`, `src/auth/totp/TotpSecretCopy.vue:22`.
- A run of text whose direction is **not known until runtime** (a user-supplied title, a server error detail, a log line, a pasted value) gets `unicode-bidi: plaintext` on its container, which resolves direction per paragraph from the first strong character. Live examples: `src/auth/AuthErrorNotice.scss:45`, `src/auth/totp/TotpSecretCopy.scss:61`.
- A run whose direction is known but which sits inside surrounding text of the other direction gets `unicode-bidi: isolate` with an explicit `dir`, so its neighbours' punctuation cannot be reordered by it.

**Prohibited, with the reason:** never insert U+200E (LRM), U+200F (RLM) or U+2066-U+2069 (the directional isolates) into displayed copy, translation files, or any value that will be stored or submitted. Those characters travel with the string: they change its length, break equality and sorting, survive copy-paste into a second system, and are invisible to the person trying to debug the mismatch. The CSS mechanisms above produce the same visual result and leave the string byte-identical.

**Checkable:** no source file under `src/` may contain a literal U+200E, U+200F, U+2066, U+2067, U+2068 or U+2069 outside a test fixture. `scripts/check-design-system.mjs` reports these.

## 2. Icon mirroring

The single most common RTL design defect is an icon that points the wrong way. An icon whose meaning is *direction of travel* mirrors with the writing direction. An icon whose meaning is *a physical object or a fixed convention* does not.

**Must mirror** (`arrow`, `caret`, `chevron`, `caret-double`, `arrow-u-*`, `arrow-bend-*`, `paper-plane`/send, `reply`, `share`, `text-indent`, `list-numbers` markers, `arrow-line-*`, back, forward, next, previous, undo, redo, tab-forward, tree-expand):

Their names encode a physical side (`arrow-left`) but their meaning is logical (`next`). Resolve the glyph from direction at render time, or render one glyph and apply `transform: scaleX(-1)` under `[dir="rtl"]`. Never hardcode the physical name at the call site.

**Must not mirror** (mirroring them is itself the defect):

`clock`, `clock-counter-clockwise` and every timepiece, `check` and `check-circle` and every checkmark, `play`, `pause`, `stop`, `fast-forward` and the media transport cluster, the product logo and every third-party logo, `magnifying-glass` when its handle is drawn on a neutral diagonal, `x`/close, `plus`, `trash`, `warning-circle`, `info`, `eye`, `user`, and any glyph containing a Latin or Persian letterform.

**Live defect this rule catches on `client`:** `ph:arrow-left` is hardcoded as the *forward* affordance in at least seven components (`src/auth/AuthOtpPanel.vue:73`, `src/auth/AuthTermsPanel.vue:15`, `src/bookmarks/BookmarkContentDetail.vue:31`, `src/bookmarks/BookmarkCourseCard.vue:21`, `src/bookmarks/BookmarksHero.vue:52`, `src/content-management/ContentStudioRoutePage.vue:75`, `src/content-ops/OpsItemsList.vue:34`) and `ph:caret-left` as *expand* or *next* in at least four more. They are visually correct only because the app is hardcoded `dir="rtl"`. Every one of them inverts the moment a surface renders LTR, and `client` already renders LTR islands.

**The rule:** a direction-bearing icon is referenced by its logical role, resolved through a direction-aware wrapper or a computed name. A physical-direction icon name written literally at a call site in an RTL-capable product is a defect. `scripts/check-design-system.mjs` reports each occurrence with `file:line`.

## 3. Directional motion

Motion carries direction the same way icons do.

- A drawer, sheet, panel or toast that enters from the inline start enters from the **right** under RTL and the **left** under LTR. Express it with logical values (`inset-inline-start`, `translate: -100% 0` under a `[dir]` selector) or with a token whose sign flips with direction. A fixed `translateX(-100%)` in an RTL-capable product is a defect.
- Slide-based route transitions follow navigation direction, which is inline-start-to-inline-end. "Forward" moves toward the inline end in both directions.
- Motion that carries no direction — fade, scale, opacity crossfade — needs no flip and is the safer default for any surface that renders in both directions.
- Progress fills from the inline start. A progress bar, stepper or loading bar that fills left-to-right under RTL reads as counting down.
- Sliders and range inputs increase toward the inline end: the maximum sits on the left under RTL. Verify the control's own value mapping, not just its visual track.

## 4. LTR islands inside an RTL form

These field types are LTR content even in a fully Persian product, and each gets `dir="ltr"` on the input plus `text-align: left`: email address, URL, phone number in international form, IBAN and card number, one-time code and TOTP secret, username and slug, file path, version string, hex color, and any identifier the user will read back to support.

Two consequences the pattern must handle:

- The **label** stays RTL while the **value** is LTR. Set direction on the input element, not on the field wrapper, or the label flips with it.
- Punctuation that belongs to the surrounding Persian sentence must stay outside the LTR element, or it will render on the wrong side of the value.

A phone or code field also needs a `maxlength` matching the canonical length, so a paste of a separator-laden value is visibly truncated rather than silently submitted.

## 5. Layout and data display under RTL

- Build with logical properties from the start: `margin-inline-start`, `padding-inline`, `inset-inline`, `border-inline-start`, `text-align: start`. A physical `margin-left`, `padding-right`, `left:`, `right:`, `border-left` or `text-align: left|right` in an RTL-capable product is a defect unless it is inside an LTR island from section 4. `scripts/check-design-system.mjs` reports them, and allowlists declarations that sit in the same rule as `direction: ltr` or `unicode-bidi: plaintext`.
- Focus order follows visual order. `flex-direction: row-reverse` and CSS `order` break that in either direction; under RTL they are twice as easy to get wrong.
- **Chart axis order:** a category axis reads inline-start to inline-end, so the first category sits on the **right** under RTL. A time axis is the exception: time runs left-to-right in both directions, because that is the reading convention for time series in Persian publications as well. State which convention a chart uses in its own documentation; do not leave it to the charting library's default.
- Tables: column order flips, numeric alignment does not. Numbers stay aligned on their decimal separator with `font-variant-numeric: tabular-nums`.
- Trees, breadcrumbs and steppers grow toward the inline end; their separators mirror.

## 6. Persian typography

- **Family.** Use a Persian face that carries the full weight range you use, with a Latin face of matching x-height for mixed content. `client` ships IRANSansXFaNum with nine weights, self-hosted from `public/fonts/`. Vazirmatn is the safe open default: it is published under the SIL Open Font License by its author and distributed through Google Fonts (`read: 2026-07-28`).
- **Licensing, with an adjudicator.** A non-OFL face may ship only if the repository contains a license file naming this product. If it does not, use Vazirmatn and state the substitution in the delivery note. IRANSansX-class faces are not published under an open license (`read: unverified as of 2026-07-28`) — treat them as requiring the license file. **`client` fails this rule today:** `public/fonts/iransansxfanum/` ships nine weights in two formats with no license file anywhere under `public/fonts/`.
- **Byte budget.** Persian faces are heavy. Ship at most three weights per family in `woff2` only, subset to the Arabic and Latin ranges plus U+200C, with a total first-party font budget of **150 KB** transferred for the initial route and no more than two `<link rel="preload">` font files. Drop `woff` entirely unless the repo's browser-support matrix names a browser that lacks `woff2`. Measure with the transferred size in the network panel, not the file size on disk.
- **Line height.** Persian body text needs more leading than Latin at the same size because of ascenders and descenders. Set Persian body line-height to **1.7** and relaxed body to **1.8**; heading line-height **1.35**. These are the values live in `client` (`--alaa-typography-line-height-body`, `-relaxed`, `-heading`) and they are the defaults here.
- **Size.** Persian body text sits one step above the Latin equivalent in the same scale at equal perceived size.
- **Verification with an artefact.** Before approving a type scale, render the longest real label in the product plus a 200-word real Persian paragraph at 375px width and at 200% zoom, and confirm no clipping, no `text-overflow` ellipsis on a label meant to be read, and no horizontal scroll. Lorem text does not exercise Persian ascender and descender collisions.
- **ZWNJ (U+200C), the half-space.** Persian compounds and affixes take U+200C, not a space and not nothing. Its absence reads as careless in every label. It is a **content** character, unlike the bidi controls in section 1: it belongs in the string, must survive paste and storage, and must never be stripped by a normalizer or a trim routine. Say so explicitly wherever paste handling is specified.

## 7. Digits: the display side is ours, the fold is not

Two separate decisions that are constantly confused.

**Ours — the display decision.** Pick one digit system for the whole product and apply it everywhere: labels, numbers, dates, chart axes, table cells. Mixed digit systems in one view are a defect. The mechanism matters:

| Mechanism | What the user sees | What is in the DOM and the clipboard |
|---|---|---|
| A font with Persian numeral glyphs mapped onto ASCII code points, or `font-feature-settings`/`font-variant-numeric` | Persian digits | **ASCII digits, unchanged** |
| `Intl.NumberFormat("fa-IR")` or an explicit character map | Persian digits | Persian digit code points |

`client` uses the first mechanism: the shipped face is IRANSansX**FaNum**, so the rendered digits are Persian while the DOM value stays ASCII. That is the correct default, because copy-paste, screen-reader output, browser find-in-page, and sorting all keep working.

**The standing rule:** a displayed Persian digit is never evidence that the stored value is Persian, and a rendering choice never substitutes for normalization at the input boundary. If a value must be Persian in the DOM — an image alt text, a value read by an external tool — use the second mechanism deliberately and record why.

**Not ours — the fold.** Converting Persian, Arabic and other non-ASCII digits to ASCII at every input boundary is owned by `/alaa-input-normalization` (`$alaa-input-normalization`), which holds the canonical implementations and the conformance corpus. This skill neither restates the character table nor defines where the fold runs. `client` consumes it as `@alaa/digit-normalizer`. Design rule that follows: **never design a field whose correctness depends on the user typing ASCII digits**, and never show an error that asks the user to "use English numbers" — the fold makes that error unnecessary and its presence means the fold is missing.

## 8. Dates

- The **wire value** — the format, calendar and timezone a date is stored and transmitted in — is owned by `/alaa-services-contract` (`$alaa-services-contract`). Never infer it from what a screen shows.
- The **render** is ours. Pick Jalali or Gregorian per product and apply it to every date surface including relative times, chart axes, date pickers and exported filenames. A view that mixes calendars is a defect.
- Any surface where the two could be confused — an audit log, an export, a legal timestamp — labels the calendar next to the value.
- A date picker's calendar must match the display calendar; a Jalali display with a Gregorian picker is the defect this rule exists to prevent.

## Anti-patterns

- Inserting LRM, RLM or isolate characters to fix punctuation order.
- `ph:arrow-left` or any physical-direction icon name written literally at a call site.
- `translateX(-100%)` for a drawer in a product that can render either direction.
- A Persian UI verified only with English strings, or a type scale approved on lorem text.
- Stripping U+200C during input cleanup because it looked like whitespace.
- Asking the user to retype numbers in English digits.
- Shipping a non-open Persian face with no license file in the repo.

## Pairing

- Token names and theme wiring for the values above: `20-design-tokens-and-theming.md`
- Type scale and contrast: `30-typography-and-color.md`
- Persian voice, register and copy: `35-ux-writing-and-microcopy.md`
- Icon families and sizes: `80-icons-assets-and-imagery.md`
- Motion tokens the direction rules apply to: `70-motion-contract.md`
- The RTL gate and how it is proven: `90-quality-gates-and-review.md`, `95-design-proofs.md`

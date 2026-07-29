# The Seam With the Provider Skills, and the Items It Left Open

**The seam in one sentence: this skill normalizes and never rejects; the provider skills
validate and render, and their input is this skill's output.**

## The division, and it is settled

Owned by `/alaa-bale-provider` (`$alaa-bale-provider`) and `/alaa-sms-provider-mediana`
(`$alaa-sms-provider-mediana`), and not restated here:

- The two wire renderings, `989xxxxxxxxx` and `+989xxxxxxxxx`, and the rule that a normaliser
  takes the target channel as a parameter.
- The MSISDN grammar `^(?:\+98|0098|98|0|)(9\d{9})$`, the international-prefix ruling, the
  landline, label and length rejections, and "rejection is a rejection, never a repair".
- The closed reason-code set and the `--normalize` CLI.
- `scripts/phone-conformance-corpus.json`: 80 cases, two byte-identical copies, digest
  `80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc`. **Not forked, not
  moved, not copied into this skill.**

Owned here: the fold and its scope, the not-folded list, the NFC mandate, the `text`/`typed`
split, both enforcement points, and the four canonical implementations.

## The separator rule is theirs, reproduced here rather than moved

`typed` mode's separator handling **is** the provider skills' rule — the same five Unicode
categories `{Cf, Zs, Zl, Zp, Pd}`, the same whitespace controls, the same literal set
`()._/`. It is reproduced in these implementations, with the provider files named as the
owner, exactly as the two providers reproduce it from each other today.

It was not moved here on purpose. The rule's stated scope is "recipient normalisation for
the Bale channel and the Mediana channel"; moving it widens that scope, and a scope change
is the owner's decision rather than a side effect of this work. Revisit when a second typed
field — a national code, a postal code — actually needs it, and move it in one commit that
touches both provider skills.

## The corpus relationship

`scripts/normalization-corpus.json` carries all 80 phone-corpus **inputs** as normalization
cases — `input -> text_expected, typed_expected` — and **none** of their expectations. The
`mediana_expected` and `bale_expected` columns stay where they are.

That is what lets a reviewer prove "the value the phone normaliser receives is the value the
browser produced" without duplicating a single rendering decision, and it is what made the
settled item below measurable rather than theoretical.

## Settled 2026-07-28 — the Devanagari case

**The measurement that raised it.** Running the phone grammar over the `typed` output of all
80 phone inputs gave **49 accepted / 31 rejected** against the recorded **48 / 32**. One case
differed and no other: `०९१२३८३००००`, Devanagari digits, recorded as rejected by both
providers because the phone fold covered two digit families only.

**The ruling.** Option (b): keep the wide fold and re-ratify the case as rendered. The owner
approved it on 2026-07-28 and it landed in one commit touching both provider skills and both
copies of the phone corpus. The corpus now records 49 accepted and 31 rejected, and
`corpus_sha256` moved from `7a4250cf64e730d51ef92512975e864cbcfa5da919f658e0f974c50e8d54b548`
to `80dcb3723e83d848236ab0cbfbfc62447eec524c62a434737d85682aa653d7dc`.

**Why (b) rather than (a) or (c).** The browser package shipped in `client` already folds
every `Nd` family, so the recorded rejection described a path no browser user could reach:
the value arriving at the backend was already `09123830000`. Narrowing the fold would have
regressed two shipped browsers and returned the contract to the enumerated-list failure mode,
and exempting phone fields would have created two normalization regimes at one input
boundary, which is the condition this contract exists to remove.

**The part of the providers' original reasoning that survives, and matters.** Their rule was
justified by saying that folding every Unicode digit family accepts superscripts *and*
Devanagari. Only half of that is affected: **superscripts are category `No`, not `Nd`**, and
this contract folds `Nd` alone. The superscript case in the phone corpus is still recorded as
rejected and both validators still reject it. A future proposal to widen the fold to `\p{N}`
or to any `isdigit()`-style predicate would break that case, and it must be refused.

**What the change touched, so a reviewer can retrace it.** Both copies of
`alaa-bale-provider` / `alaa-sms-provider-mediana` `scripts/phone-conformance-corpus.json` (one expectation, the case order re-applied per the
file's own invariant, `corpus_version` 3 → 4, the digest); the fold step in both providers'
normalisation contract, which now folds by category and names this skill as the owner; both
providers' validators, whose enumerated two-family table became a category test; and the
corpus counts and digest wherever they were quoted. Both provider harnesses pass, and the
Bale harness verifies the digest as part of its self-test.

## Open item — one implementation per language, four copies to retire

These are the same rule written four times, and none of them is under the harness:

- `client/packages/digit-normalizer` — a complete, tested, shipped package with a 75-entry
  family table.
- `entekhabat-front/packages/alaa-digit-normalizer` — a byte-different, semantically
  identical fork of that package.
- `CharacterCommon::convertToEnglish()` in `auth`, `vod` and `ticket` — two literal digit
  families plus two HTML-entity forms.
- `to_valid_mobile_number()` and `standardNationCode()` in `auth` — a third phone normaliser,
  divergent from both providers, which strips `+` unconditionally and left-pads a national
  code with zeros.

Each becomes a copy of the canonical implementation for its language, or is deleted. Retire
them one repository at a time, each with the harness output in the change record.

## Adoption order, and where the change request goes

Defect first, then adoption. `client` and `auth` carry live defects; `content`,
`comment-service`, `notification`, `ticket` and `assessment-service` are adoption; the Go
side lands once in `alaa-go-chi` and reaches `news`, `notif`, `tusd` and the entitlement
services from there; `gateway` gets a change request that **records the decision not to
normalize at the edge** so it is not re-litigated.

The change-request directory differs by repository and is not guessable — nine repositories
use `docs/requests-for-change/` with `YYYYMMDD-HHMMSS_slug.md`, `client` uses
`docs/change-requests/` with that same filename form, and `alaa-go-chi` uses
`docs/change-requests/` with `YYYY-MM-DD-slug.md`. List the directory before writing into
it, and where neither exists — `ticket`, `assessment-service`, `news`, `notif`,
`entekhabat-front` — create the one its siblings use rather than inventing a third form.

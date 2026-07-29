---
name: alaa-input-normalization
description: "Fold Persian, Arabic and every other non-ASCII decimal digit to ASCII at both input boundaries - the browser at submit and every backend service in middleware - under one contract with four canonical implementations, one corpus and a conformance harness. Use when writing or reviewing a form submit path, an input validator or formatter, a new request middleware, an OTP, mobile or national-code field, or a free-text field such as a description, a news body or a comment that carries numbers; and when a value typed in Persian digits fails a validation rule, a length rule, a unique index or an idempotency lookup. Do not use it for phone grammar, rejection rules or provider wire formats, owned by /alaa-bale-provider ($alaa-bale-provider) and /alaa-sms-provider-mediana ($alaa-sms-provider-mediana); for how digits are displayed, owned by /alaa-ui-ux-design-system ($alaa-ui-ux-design-system); or for length limits and other values, owned by /alaa-services-contract ($alaa-services-contract)."
---

# Alaa Input Normalization

Every non-ASCII decimal digit becomes an ASCII digit before a value is validated, stored,
compared or sent. The browser folds at submit; every backend service folds again in
middleware. The two must agree byte for byte, so one corpus and one harness decide whether
they do, and a document asserting parity is not evidence of it.

**The backend middleware is the contract; the browser fold is a convenience.** A service
that trusts the browser has no contract: `content` and `news` have no browser on their
write path, `entekhabat-front` ships a forked copy of the browser package, and any HTTP
client skips the browser entirely.

## When NOT to use

Stop and route when the task is how digits are **displayed** rather than what is stored or sent, since a rendering choice never substitutes for a fold at the input boundary; when it is a length limit or any other registered value; when it is rendering a phone number onto a provider wire, the MSISDN grammar, or a rejection reason, because this skill normalizes and never rejects; or when it is an identifier codec rather than user-entered text. Companion routing below names each owner.

## Router

Every row states a situation you can observe before you act. Read the one that matches.

| You are about to | Read |
| --- | --- |
| decide whether one character folds — a digit family, a separator, a letter, a combining mark | `references/10-normalization-contract.md` |
| write or change a submit path, a validator, a formatter, or an input component in a browser application | `references/20-browser-binding.md` |
| register or change request middleware in a Laravel or Go service, or ask whether the gateway can fold instead | `references/30-backend-middleware-binding.md` |
| diagnose a value that arrived wrong — a rejected OTP, a length rule the two sides disagree on, a phone number a provider refused | `references/40-failure-classes.md` |
| change any canonical implementation, add a case, or explain a harness exit code | `references/50-corpus-and-harness.md` |
| normalize a phone number, or reconcile this contract with the 80-case phone corpus | `references/60-provider-seam-and-open-items.md` |
| stand up normalization in a repository, or catch yourself about to write a digit table | `assets/input-normalization/` |

## Rules

- Call one of the four canonical implementations in `assets/input-normalization/`. Do not write a digit table, a character class, or a per-field replace in application code: a second implementation is a second answer, and only one of them is under the harness.
- Copy an implementation unchanged except for its namespace, package clause or import path, so the harness result still describes the copied code.
- Change all four implementations in one effort, then run `scripts/normalization-conformance.sh` and record its output, because a change proved in one runtime is not proved in the other three.
- Ship nothing while the harness reports a disagreement, and fix the implementation rather than the corpus: the corpus is the evidence, and regenerating it to pass destroys it.
- Treat a skipped runtime as unproved rather than passing, and an input the corpus does not carry as untested. Add the case first, then fix the implementations.
- Normalize before validation, never instead of it. Normalization is total: it never rejects, never throws and never repairs. A value still wrong after folding is rejected by validation.
- Apply `text` mode to every string in the request. Opt a field into `typed` mode by naming that field, and record the name where a reviewer can see it.

## Companion routing

- `/alaa-bale-provider` (`$alaa-bale-provider`) and `/alaa-sms-provider-mediana` (`$alaa-sms-provider-mediana`): the phone grammar, the rejection rulings, the wire renderings, and the 80-case phone corpus.
- `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/05-rtl-and-persian.md`: digit rendering, and the rule that a rendering choice never substitutes for folding at the input boundary.
- `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`): the Vue-shaped submit pipeline this fold attaches to.
- `/alaa-services-contract` (`$alaa-services-contract`): field length limits, envelope shapes and every other value.
- `/alaa-security-review` (`$alaa-security-review`): every threat class, including a normalized value that crosses a trust boundary.
- `/alaa-testing-strategy` (`$alaa-testing-strategy`): what this harness proves, what it leaves unproved, and the six proof levels.
- `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`): identifier encoding and decoding, which this contract never does.
- `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) and `/alaa-go-chi-development` (`$alaa-go-chi-development`): the middleware shape each stack expects.
- `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`: model and effort selection for any of this work.

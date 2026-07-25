# Request Documentation Blocks

Read this file when writing or reviewing a request description.

`assets/request-documentation-block.md` is the structure. Copy it into the request's
`request.description` and fill in every heading. This file owns the rules about
documentation; the asset owns what each heading must answer.

## Who the documentation is for

Two named readers, and the description is finished when both can work from it without
opening the backend repository:

- a **frontend developer** implementing the call, who needs the input shape, the output
  shape, the states the response forces the UI to have, and what is safe to retry
- a **security engineer** testing the route, who needs the isolation boundary, the
  identifiers that address another actor's data, the headers the gateway strips, and
  the limits that fire

"Document it well" is not a rule an agent can comply with or violate. The eight
headings in the asset are, because their presence and their answers are observable.

## Where each fact goes

Put a fact at the smallest level where it is true, once:

- **collection description**: the environment contract, the base URL and prefix model,
  the auth model at the boundary, the shared conventions, and how to run the collection
  from the first request to a working session
- **folder description**: what is true for that bounded context or service — its shared
  headers, its shared auth, its shared error behaviour
- **request description**: the eight headings, filled for this route

A fact stated at two levels drifts. When a rule moves up to the folder or collection,
delete it from the request rather than leaving a summary behind.

Shared prose is not a licence to leave a request undocumented. A request whose
description says only "see the folder description" fails the self-containment test for
both readers above: neither of them is reading this collection top to bottom.

## Constraints on the writing

- Every heading from the asset is present, spelled exactly as the asset spells it, in
  the asset's order. A renamed heading reads as a missing section to the gate.
- A heading with nothing to say for this route carries one sentence saying so and why.
  Deleting it makes an answered question indistinguishable from an unasked one.
- The `## Errors` table has one row per status the route can actually return, and every
  row has a matching saved example on the same request.
  `41-response-contract-and-error-coverage.md` owns how that set is enumerated.
- Plain Markdown that renders in Postman's generated documentation: short paragraphs,
  short bullet lists, inline code for variable names, headers, and field names. No
  decorative Markdown, no ASCII art, no nested tables.
- Simple English throughout, including example names and comments.
- No credential, no real personal data, and no production hostname in any description.

## Length is a floor, not a target

A minimum description length is a gate against an empty description, not a writing
target. Meeting it with padding is worse than failing it, because a padded description
passes the gate and still leaves both readers guessing. Raise coverage by answering the
eight headings; the length follows.

Never lower the threshold to make a run pass. When a threshold is genuinely wrong for a
repository, say so in the task output and leave the decision to the repository owner.

## Mechanical gate

The heading names below are the machine form of the asset's structure. Keep the two in
step: if the asset's headings change, this command changes in the same task.

```shell
python3 "$SKILL_DIR/scripts/validate_postman_artifacts.py" path/to/collection.json \
  --env path/to/environment.json \
  --min-description-chars 400 \
  --require-doc-section Purpose \
  --require-doc-section "Flow position" \
  --require-doc-section Request \
  --require-doc-section Response \
  --require-doc-section Access \
  --require-doc-section Errors \
  --require-doc-section "Frontend notes" \
  --require-doc-section "Security notes"
```

The gate matches a Markdown heading line whose text equals the given name exactly, so
`## Request` satisfies `--require-doc-section Request` and `## Request contract` does
not. `60-validation-and-output-contract.md` holds the full flag set and the exit codes.

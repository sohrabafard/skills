# The Corpus and the Harness

One corpus, four implementations, one harness that drives every implementation over that
corpus and fails on any disagreement. A document asserting parity is not evidence of it.

## The pieces

| Path | What it is |
| --- | --- |
| `scripts/normalization-corpus.json` | 145 cases, two expectations each (`text_expected`, `typed_expected`), 290 answers. `corpus_sha256` = `cd81fcdc7048ece0c5f2253bbf9e24b8151481f18ec3913c77d7a14ef24cddaf`. |
| `scripts/_phone_inputs.b64` | A gzip+base64 capture of the 80 phone-corpus inputs, byte-exact. Several carry `U+000B`, `U+0085` and bidi controls that do not survive being retyped, so the capture is load-bearing and ships with the skill. |
| `scripts/normalization-conformance.sh` | The harness. |
| `assets/input-normalization/` | The four canonical implementations: `normalize_reference.py`, `input-normalization.ts`, `InputNormalization.php`, `input_normalization.go`. |

The Python file is both a canonical implementation and the generator the corpus was produced
from, so every expectation in the corpus was produced by running code rather than asserted.

## Running it

```
scripts/normalization-conformance.sh            # every installed runtime, over the corpus
scripts/normalization-conformance.sh --self-test # the comparator and the checksum only
scripts/normalization-conformance.sh --verbose  # every answer, not only the failures
scripts/normalization-conformance.sh --help     # options, runtimes, environment, exit codes
```

Paste the output into the change record. "I ran it" is not the evidence; the output is.

| Exit | Meaning | Caller obligation |
| --- | --- | --- |
| 0 | Every runtime that ran matched the corpus on every case, and at least two ran | none |
| 2 | Usage error | fix the invocation; do not retry unchanged |
| 3 | A runtime disagreed, a driver failed to execute, or a runtime's Unicode data is older than the pin | treat the contract as broken; ship no implementation, no middleware and no browser change |
| 4 | Fewer than two runtimes ran | install a toolchain and rerun; **do not record as a pass** |
| 5 | The comparator failed its own self-test | fix the harness before trusting any result |
| 6 | The corpus is missing or drifted, or an implementation file is absent | find which copy drifted and reconcile before reading any result |

Exit `4` is deliberately set at *two* runtimes rather than one: this contract's entire claim
is that two enforcement points agree, so one runtime answering correctly is not evidence
for it.

## What the harness does before it reports anything

1. **Verifies the corpus digest** against the cases it covers, and refuses to run on a
   mismatch. Two runtimes can agree perfectly on a corpus that is wrong.
2. **Self-tests its own comparator** against five synthetic vectors — answers that match,
   an answer that differs, an answer that differs *only in Unicode composition*, a driver
   that skipped an answer, and a metadata line that must not be counted as an answer — plus
   the Unicode version guard in both directions. A comparator that cannot detect a
   disagreement cannot report the absence of one.
3. **Probes each runtime** and reports an absent one as `skipped: <reason>`, excluded from
   the comparison. **The harness never reports a pass for a runtime it did not run.**

Each driver compares its answer against the corpus rather than against a reference runtime.
With four implementations and one corpus, "everyone agrees" and "everyone is right" become
the same statement.

Answers cross the process boundary as the lowercase hex of the UTF-8 bytes, because the
values under test contain tabs, newlines, bidi controls and zero-width characters, and
because two runtimes must not be able to disagree about how to escape them. A mismatch
prints both the hex and a readable rendering.

Each driver also reports its Unicode data version, which the harness prints beside the
result and compares against the pinned minimum of 14.0.0. Seeing four different Unicode
versions agree on all 290 answers is the strongest evidence this harness produces.

## Runtimes, and what makes one skip

- **python3** — no dependencies.
- **node** with TypeScript type stripping (22.6 or newer) or `tsx`.
- **php** 8.2 or newer with class `Normalizer` reachable. No image on this fleet installs
  `ext-intl`, so point `COMPOSER_AUTOLOAD` at a `vendor/autoload.php` that provides
  `symfony/polyfill-intl-normalizer`; otherwise PHP skips with that reason.
- **go**, plus `golang.org/x/text/unicode/norm` from a module cache, a network, or a local
  checkout named by `ALAA_XTEXT_DIR`. The standard library has no NFC. A build failure whose
  text shows the module could not be fetched, or that the installed Go is older than the
  module wants, is reported as a skip and prints the build error; any other build failure is
  a driver failure and fails the run.

## Changing something

**An implementation.** Change all four in one effort, run the harness, record the output. A
change proved in one runtime is not proved in the other three — and the first execution of
this harness caught a real defect in one implementation that all four had been written to
avoid.

**A case.** Add the input to `NEW_CASES` in `normalize_reference.py` with a note saying what
it pins and why, regenerate with `--emit-corpus`, and rerun the harness. Adding a case never
changes an existing expectation; if it does, the contract changed and that is a different
decision.

**The contract itself.** This changes existing expectations, so it needs a ratified decision
before the corpus is regenerated, and the same commit must carry the four implementations,
the corpus, the new digest, and the harness output. Never regenerate the corpus to make a
failing implementation pass: that destroys the only evidence the harness produces and leaves
no trace that it was destroyed.

## Canonicalisation, so two copies can be compared with `cmp`

On disk the corpus is `json.dump(document, handle, ensure_ascii=True, indent=2)` with a
single trailing newline, so the file is **pure ASCII** and a zero-width character in a case
is visible in review as an escape rather than invisible as a byte.

`corpus_sha256` is the lowercase hex SHA-256 of
`json.dumps(cases, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')`
— the parsed cases re-serialised with the real characters in UTF-8, not the on-disk escapes,
so Go, PHP and JavaScript can reproduce it without reimplementing Python's escaper. Case
order is part of the hashed bytes and is fixed: ascending by the tuple of code points of
`input`, ties broken by `note`.

Reproduce it from the file alone:

```
python3 -c "import hashlib,json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); \
print(hashlib.sha256(json.dumps(d['cases'],ensure_ascii=False,sort_keys=True,\
separators=(',',':')).encode()).hexdigest())" scripts/normalization-corpus.json
```

This is the same recipe the 80-case phone corpus uses, so the two are checked the same way.

## What a green run does not prove

It bounds what its corpus covers and nothing else. It says nothing about an input the corpus
does not carry, nothing about a skipped runtime, and nothing about whether the middleware is
actually registered on the route that matters — that last one is a wiring fact, and
`/alaa-testing-strategy` (`$alaa-testing-strategy`) owns which level of proof a claim needs.

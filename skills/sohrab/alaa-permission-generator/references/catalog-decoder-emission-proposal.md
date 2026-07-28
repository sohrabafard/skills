# Proposal: Emit The Decoder, Not Only The Map

**Status: proposal.** Nothing here has been implemented, and this skill does not edit
`alaa-permission-catalog`. It is written so someone with authority over that repository can
decide, and so the next agent does not re-derive the problem.

## What the tool does today

`alaa-permission-catalog` allocates permission ids and emits maps. It does not encode or
decode a bitmap in any language, and no file under its `src/` performs a base64 operation or
a bit operation.

- `src/Support/GoPermissionEmitter.php` emits name constants, two unexported lookup maps, and
  five functions: `MaxPermissionID`, `PermissionName`, `PermissionID`, `PermissionNamesByID`,
  and `Decode`. At lines 86-87 the emitted `Decode` is a one-line delegation:
  `return DecodePermissionSet(access, generatedPermissionNamesByID, MaxPermissionID())`.
  `Set`, `Set.Has`, and `DecodePermissionSet` are **not emitted**. The generated file does not
  compile alone; the owning package must already supply them.
- `src/Support/PhpArrayEmitter.php` emits two array shapes and nothing else — `authSeed` and
  `serviceConfig`. The generated `config/permissions.php` is a keyed data array with no
  decode function and no generated-file header.
- `src/Support/TypeScriptPermissionEmitter.php` emits constants and two typed maps. The word
  "decode" does not appear in it. The artifact's own header states its constants are
  unverified UI hints and not an authorization decision.

The consequence is that the bit work lives in a hand-written file inside each consuming
service. `tusd/internal/authz/bitmap.go` is one such file, and it is good; it is also one
service's copy, so a defect in it is fixed in one service and stays live in the rest. That is
the outcome the generator exists to prevent for the *map* and does not yet prevent for the
*decoder*.

## What the emitter would have to produce

For each language the fleet consumes, a decoder covering the whole contract, not the
delegation stub:

- **Go** — `Set`, `Set.Has`, `Set.Names`, `DecodePermissionBitmap`, `DecodePermissionSet`, the
  base64url unpacking, the encoded-length cap, and the error values. Emitted as a sibling
  generated file in the same package, not appended to `permissions_gen.go`, so the two files
  can be applied and reviewed independently.
- **PHP** — the same surface as a class. It cannot go into `config/permissions.php`: that file
  is a pure data array that `src/Support/PhpArrayLoader.php` reads back during import, and
  executable code in it would change what the importer parses. It needs a new
  `generated_targets` entry pointing at a class path.
- **TypeScript** — the same surface as a module beside `permission-catalog.ts`, subject to the
  emitter's 80-column line cap, which today constrains permission-key length and would then
  constrain every line of decoder source.

`assets/permission-bitmap/` in this skill is the working reference for all three. Each file
already carries the full surface, and `scripts/bitmap-conformance.sh` proves the three agree
over `scripts/permission-bitmap-corpus.json`. An emitter implementation should emit those
files rather than re-derive them, and the corpus should move into the catalog repository as
that emitter's own test data.

## What it breaks

Each of these is a real breakage, not a risk to monitor.

1. **Every Go service that already supplies `Set` and `DecodePermissionSet` stops compiling on
   the next apply**, because the emitted declarations collide with the hand-written ones.
   `tusd` is in exactly this state today. The service must delete its hand-written decoder in
   the same change that applies the emitted one; there is no ordering in which both exist.
2. **Drift turns red across the fleet the moment the new target is registered.** Drift compares
   the applied file against generated output byte for byte, so every service whose
   hand-written decoder differs from the emitted one — all of them, in whitespace at least —
   reports drift until it applies. Registering the target and applying it are one change per
   service, not a fleet-wide flag day.
3. **A new `input_shape` and a new `generated_targets` path family are needed for PHP**, since
   the existing `service_config` shape is a data array. That is a descriptor change in
   `catalog/services.json`, which the drift analyzer and the importer both read.
4. **The 80-column emitter refusal now applies to decoder source, not only to key names.** A
   decoder line over 80 columns makes generation exit `2` with
   `Generated TypeScript line exceeds the client formatter print width of 80 columns`, so the
   emitted source must be written to that width and stay there.
5. **The generated-file rule gains teeth it did not have.** A service that patches an emitted
   decoder during an incident now silently diverges from every other service, and for the PHP
   config the missing generated-file header means nothing detects it.

## What deciding it needs

- A decision on whether the emitted decoder is a **sibling file per language** or an addition to
  the existing artifacts. The sibling shape is what avoids breakages 1 and 3 becoming worse,
  and it is what this proposal assumes.
- A **per-service migration order**, since breakage 1 makes the transition atomic per service:
  register the target, apply the emitted decoder, delete the hand-written one, run the
  service's tests, all in one change.
- An owner for the **emitted decoder's tests**. Today the catalog's `php tests/run.php` tests
  emitters against expected strings; testing an emitted Go decoder means either compiling Go
  in the catalog's CI or trusting the corpus harness this skill owns.
- A decision on whether **`corpus_sha256` becomes a catalog artifact**, so a consuming service
  can assert the corpus it tests against is the one the emitter was built for.

## Until it is decided

`SKILL.md` carries the interim rule: a service copies the canonical implementation from
`assets/permission-bitmap/` and does not hand-write one, and a defect is fixed in this skill
and re-propagated. That is one source plus a propagation discipline. Emission would remove the
discipline, which is the whole point of the change; the discipline is what fails quietly when
nobody is watching.

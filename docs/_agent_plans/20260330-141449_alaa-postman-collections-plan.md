## Goal

Create a new reusable skill at `skills/sohrab/alaa-postman-collections/` that owns Postman collection and environment generation, update, synchronization, validation, and documentation, while preserving import compatibility with the free version of Insomnia. Then narrow `skills/sohrab/alaa-docs-farsi/` so it routes detailed Postman work to the new skill.

## Assumptions

- The new skill should be Postman-first and should emit Postman Collection Format v2.1 JSON as the primary portable artifact.
- The skill should preserve compatibility with free Postman and free Insomnia by avoiding paid-only or cloud-only requirements.
- Existing Postman artifacts in target repos should be inspected and updated minimally instead of being replaced by default.

## Constraints

- Use only official OpenAI, Postman, and Insomnia/Kong sources for version-sensitive guidance.
- Keep the top-level `SKILL.md` routing-first and push detail into `references/`.
- Keep diffs small and preserve existing Sohrab skill style.
- Only add helper scripts if they materially improve repeatable validation or deterministic updates.

## Phases

### Phase 1 — Verify sources and local patterns
- Inputs:
  - official OpenAI docs
  - official Postman docs and collection schema
  - official Insomnia/Kong docs and pricing pages
  - nearby Sohrab skills and validators
- Outputs:
  - distilled design constraints for the skill
- Validation:
  - every version-sensitive claim in the skill can map back to a primary source
- Status:
  - Completed

### Phase 2 — Author the new skill package
- Inputs:
  - Phase 1 constraints
  - requested file list
- Outputs:
  - new `alaa-postman-collections` skill files
  - optional helper validation script if justified
- Validation:
  - top-level skill remains compact
  - references stay focused and non-duplicative
  - `agents/openai.yaml` matches real scope
- Status:
  - In progress

### Phase 3 — Decouple docs skill ownership
- Inputs:
  - current `alaa-docs-farsi` files
  - new skill ownership boundary
- Outputs:
  - minimal routing updates in docs skill files
- Validation:
  - docs skill still covers docs alignment work
  - Postman-specific workflow ownership routes to the new skill
- Status:
  - Pending

### Phase 4 — Validate and close
- Inputs:
  - edited skill files
  - local validator(s)
- Outputs:
  - validation notes
  - final residual limitations
- Validation:
  - `scripts/validate_sohrab_skill_pack.py` passes
  - any helper script runs on at least a smoke-test fixture or on itself where applicable
- Status:
  - Pending

## Parallelization notes

- Source verification and repo pattern inspection were safe in parallel.
- File authoring should stay mostly sequential because the new skill references must align tightly with the top-level routing file and the docs-skill routing change.

## Exit criteria

- all requested new skill files exist and read coherently
- the docs skill no longer owns detailed Postman workflow guidance
- validation runs are recorded clearly
- residual compatibility gaps, if any, are stated explicitly rather than implied away

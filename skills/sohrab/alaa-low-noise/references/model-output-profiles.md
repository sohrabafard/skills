# Output calibration routing

## Introduction

Calibration controls output length and cadence without losing required content. Shorter reports do not prove better reasoning. Fewer calls do not prove equivalent coverage.

## Ownership

This skill owns output shape and context economy, not model profiles, effort policy, or universal behavioral guarantees.

Before model-specific claims or model/effort selection, read `/alaa-prompting-guide`. Follow its conditional topic router for current model guidance.

## Calibration rules

- When responses, artifacts, or progress updates are too long, calibrate them separately.
- State required content and useful cadence.
- Preserve evidence, caveats, findings, blockers, and the user's requested detail.
- Do not control verbosity through reasoning effort. Do not infer that lower effort meets an output-length target.
- When tool output dominates context, bound retrieval at its source. Keep a path to useful full evidence.
- Do not repeat discovery to appear thorough.

## Validation rules

- Before removing validation instructions, distinguish focused implementer checks, independent acceptance gates, and redundant repetition. Preserve the first two.
- Remove repeated checks only when no new change, failure, or unresolved concern justifies them.
- Evaluate calibration changes on representative tasks with the same required content and acceptance criteria.
- Keep a change only when coverage and authority compliance survive.

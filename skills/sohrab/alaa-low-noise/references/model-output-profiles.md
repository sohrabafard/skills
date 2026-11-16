# Output calibration routing

Calibration controls output length and cadence without losing required content. Shorter reports do not prove better reasoning, and fewer calls do not prove equivalent coverage.

`SKILL.md` *Model calibration* states what this skill does not own. Before a model-specific claim or a model and effort selection, read `/alaa-prompting-guide` and follow its conditional topic router for current model guidance.

## Calibration rules

- When responses, artifacts or progress updates are too long, calibrate each separately: state the required content and the useful cadence.
- Preserve evidence, caveats, findings, blockers and the user's requested detail.
- Do not control verbosity through reasoning effort, and do not infer that lower effort meets an output-length target.
- When tool output dominates context, bound retrieval at its source, and keep a path to useful full evidence.
- Do not repeat discovery to appear thorough.

## Validation rules

- Before removing validation instructions, distinguish focused implementer checks, independent acceptance gates and redundant repetition. Preserve the first two.
- Remove repeated checks only when no new change, failure or unresolved concern justifies them.
- Evaluate calibration changes on representative tasks with the same required content and acceptance criteria. Keep a change only when coverage and authority compliance survive.

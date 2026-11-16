# Output calibration routing

Calibration changes output length and cadence, never required content. A shorter report does not prove better reasoning, and fewer calls do not prove equal coverage. This skill defines no model profile and no effort policy: before a model-specific claim or a model and effort selection, read `/alaa-prompting-guide` and follow its topic router.

- Calibrate responses, artifacts and progress updates separately. For each, state the required content and the useful cadence.
- Preserve evidence, caveats, findings, blockers and the detail that the user requested.
- Do not control verbosity through reasoning effort, and do not infer that lower effort meets an output-length target.
- When tool output dominates context, bound retrieval at its source, and keep a path to the full evidence.
- Shortening never removes a focused implementer check or an independent acceptance gate. Before you remove a repeated check, read `alaa-prompting-guide references/80-subagent-authoring.md`; it decides which repetition is redundant.
- Before you keep a calibration change, apply `alaa-prompting-guide references/60-skill-authoring.md`: required content, coverage and authority compliance must survive.

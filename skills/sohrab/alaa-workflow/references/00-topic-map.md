# Alaa Workflow Topic Map

Read only the smallest section you need.

## Fast routing

- Need trigger boundaries or ownership?
  - Read `full-guide.md#trigger-boundaries-and-ownership`
- Need path selection, file naming, or artifact continuity?
  - Read `full-guide.md#artifact-path-and-naming-rules`
- Need a deep implementation-ready plan?
  - Read `full-guide.md#plan-mode`
  - Open `../assets/plan-template.md`
- Need the required same-stem phase prompt pack?
  - Read `phase-prompts.md`
  - Open `../assets/phase-prompts-template.md`
- Need execution discipline during a long run?
  - Read `full-guide.md#execution-mode`
- Need resume, handoff, compaction safety, or durable memory?
  - Read `full-guide.md#state-files`
  - Open `../assets/state-template.json`
  - Open `../assets/continuation-state-template.md`
- Need subagents, parallel jobs, worktrees, or background tasks?
  - Read `full-guide.md#delegated-execution-and-subagents`
  - Open `../assets/lane-plan-template.md`
- Need review mode?
  - Read `review-mode.md`
- Need stack-specific pairing?
  - Read `companion-routing.md`
- Need PowerShell-safe commands or Windows-specific notes?
  - Read `windows-powershell.md`
- Need deterministic scaffolding?
  - Run `../scripts/init_workflow_files.py --help`
- Need artifact validation?
  - Run `../scripts/validate_workflow_files.py --help`
- Need source priority, freshness triggers, or GPT/Claude model-use notes?
  - Read `90-source-map.md`

## Reading rule

- Start with the relevant section only.
- Do not read the entire guide unless the task actually needs broad coordination rules.
- Prefer assets and scripts when you need structure, not prose.
- For any resume, review, or execution run, read the main plan before acting even if you read a summary first.

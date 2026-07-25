# First Message: the prompts that start a constitution run

Copy one of the two launchers below into your first message. Each one already contains the four
clauses the canonical-launcher test in `references/interactive-decision-workflow.md` requires, so
a run started with it finalizes and binds the constitution when you defer no decision, and leaves
an unbound draft when you defer one. You do not have to remember that wording.

Invoke the skill as `/alaa-project-constitution` in Claude Code and `$alaa-project-constitution`
in Codex, then paste the launcher.

## CREATE — the repository has no constitution yet

```text
From the repository root, create or update `CONSTITUTION.md` using the constitution template
bundled with this skill. Reuse the existing constitution as prior governance when present. Infer
the project's intent from my context and repository truth, match its project archetypes,
prescribe the obligations an enterprise-grade service of those kinds owes even where the code
does not implement them yet, verify the current value of every obligation's metric from primary
sources, and ask only essential unresolved owner decisions with a recommendation. If I defer none
of them, finalize and bind it; otherwise leave it an unbound draft and tell me exactly how to
finish it.
```

## UPDATE — a constitution already exists

```text
From the repository root, update `CONSTITUTION.md` using the constitution template bundled with
this skill. Read the existing constitution first and treat it as prior governance: preserve its
rules, ratification data, amendment history, exceptions, and TODO IDs, and apply only the
supported normative delta. Re-inspect repository truth, re-match the project archetypes, add
every obligation a newly matched archetype makes mandatory, and refresh any obligation value
whose primary source has changed. Ask only essential unresolved owner decisions with a
recommendation. If I defer none of them, finalize and bind it; otherwise keep the current binding
baseline unchanged and report the proposed amendment as an unbound draft.
```

To finish a draft an earlier run left behind, paste the continuation prompt that run printed in
its final response — it names the unresolved decision IDs — instead of the UPDATE launcher.

## What to attach, and where to name it

The skill inspects the repository itself, so nothing about the code needs attaching. Three things
it cannot find on its own, because they live outside the repository or under a name it cannot
guess:

- **Your RFP, specification, or design brief.** Attach the file to the same message, or add a line
  giving its repository path. This is what the run uses to infer the project's intent and to
  expect the right archetypes; without it, intent is inferred from the code alone.
- **Reference articles or prior art you want honoured.** Attach the files, give their repository
  paths, or paste the URLs.
- **An existing constitution that is not at `./CONSTITUTION.md`.** Give its path. A constitution at
  the repository root is found without being named, including a misspelled one.

Paste this block under the launcher and fill in only the lines that apply:

```text
Context for this run:
- RFP or specification: <attached file name, or repository path>
- Reference material: <attached file names, repository paths, or URLs>
- Existing constitution: <path, when it is not ./CONSTITUTION.md>
- Read these first: <repository paths worth reading before the rest>
- Decisions already made: <one decision per line>
```

## You do not need to copy the template

An earlier version of this workflow expected `constitution-template.md` to be copied into the
repository root before the first run. That step is gone. The template ships inside this skill at
`assets/constitution-template.md` and is read from there, so no repository carries a copy that
goes stale the next time the skill is upgraded. Ask for the template to be installed into a
repository only when it must be usable where this skill is not installed — the one case its
self-contained form exists for.

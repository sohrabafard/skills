# Manual Review Checklist

Use this checklist when reviewing any skill routing result:

- The intended skill triggered for the positive prompt.
- The skill did not over-trigger on the hard negative.
- Companion skills were suggested only when the task crossed a real boundary.
- The top-level `SKILL.md` stayed concise and routed to a smaller reference branch.
- The advice stayed inside the skill's domain and did not silently become a generic super-skill.
- The answer used current repo constraints and did not bypass `AGENTS.md` or pack policy.
- References, examples, and scripts mentioned in the top-level file actually exist.

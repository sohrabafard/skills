# Skills

Agent Skills for coding work: folders of instructions, references, and scripts that Claude Code and
Codex both load. Invoke a skill with `/name` in Claude Code and `$name` in Codex; both forms name the
same skill.

Three files answer almost every question about this repository:

- [`skills/sohrab/README.md`](skills/sohrab/README.md) — the map of the first-party pack: every skill
  it ships, what each one owns, and when to load it.
- [`install-skills.md`](install-skills.md) — authoritative for install paths. It carries the script
  that links the packs in this repository into `~/.codex/skills` and `~/.claude/skills`, and the
  source-root list that script walks.
- [`AGENTS.md`](AGENTS.md) — the rules for changing anything here, and the checkers to run before you
  call a change done. Read it before your first edit.

Third-party skills sit under `skills/.curated/` and `skills/.system/`. Upstream packs are committed
under `vendor/` and listed below.

## Vendored upstream skills

Upstream skill packs are committed under [`vendor/`](vendor/) as ordinary tracked files, so a clone
of `origin` already has them and needs no subtree pull of its own. Metadata-backed entries use
`git subtree`; pinned and source-path snapshots are committed directories refreshed by hand. The
manifest that defines all of them is [`vendor/subtrees.json`](vendor/subtrees.json).

<!-- vendor-subtrees:readme-list:start -->
Current vendored upstreams:
- [`vendor/openfga-agent-skills`](vendor/openfga-agent-skills/) from `https://github.com/openfga/agent-skills.git`
- [`vendor/cc-skills-golang`](vendor/cc-skills-golang/) from `https://github.com/samber/cc-skills-golang.git`
- [`vendor/claude-plugins-official`](vendor/claude-plugins-official/) from `https://github.com/anthropics/claude-plugins-official.git`
- [`vendor/knowledge-work-plugins`](vendor/knowledge-work-plugins/) from `https://github.com/anthropics/knowledge-work-plugins.git`
- [`vendor/basic-memory`](vendor/basic-memory/) from `https://github.com/basicmachines-co/basic-memory.git`
- [`vendor/skill-temporal-developer`](vendor/skill-temporal-developer/) from `https://github.com/temporalio/skill-temporal-developer.git`
- [`vendor/hindsight-skills`](vendor/hindsight-skills/) from `https://github.com/vectorize-io/hindsight-skills.git`
<!-- vendor-subtrees:readme-list:end -->

That list is generated from the manifest by `python scripts\vendor_subtrees.py refresh-docs`; an edit
between the markers is discarded by the next run. The commands that add a vendor, sync it, enable
hook-driven sync, and expose selected vendored skills all live in
[`install-skills.md`](install-skills.md), which also documents how the installer's source-root list
is generated and how to change what it contains.

## License

A vendored pack under `vendor/` carries whatever license file its upstream ships, at the top of its
directory. A skill under `skills/.curated/` or `skills/.system/` carries a `LICENSE.txt` inside the
skill's own directory. The first-party pack under `skills/sohrab/` ships no per-skill license file.

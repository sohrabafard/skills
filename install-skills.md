# Install local skills

The host is WSL Linux with Bash. From the repository root, the installer links skills into both
agent homes using the source-root list below.

> The source-root lines between the `# vendor-subtrees:codex-src-roots` markers below are generated
> from `vendor/subtrees.json`. To change which directories the installer scans, read [Vendored
> source roots](docs/install-skills/10-vendored-source-roots.md) for the generator rules and
> [Vendor setup and management](docs/install-skills/20-vendor-management.md) for update procedures.

## Source roots

This block is data. `install-skills.wsl.sh` reads it and `scripts/vendor_subtrees.py` writes it. Each
entry is one line: a double-quoted repo-relative path with forward slashes and no indent. A line that
starts with `#` is a comment. Any other line stops the installer before it makes a link.

```text
"skills/.curated"
"skills/sohrab"
# vendor-subtrees:codex-src-roots:start
"vendor/openfga-agent-skills/skills"
"vendor/cc-skills-golang/skills"
"vendor/knowledge-work-plugins/design/skills"
"vendor/knowledge-work-plugins/product-management/skills"
"vendor"
"vendor/hindsight-skills/skills"
"vendor/skills/skills"
"vendor/security-audit-skill/skills"
# vendor-subtrees:codex-src-roots:end
```

## WSL installer

Run the committed Bash installer from the Linux clone. It derives the repository root from its own
location. It reads the source-root block above. It ignores comments and fails on any unrecognized
line before it makes a link. It fetches no dependencies.

```bash
cd ~/project/skills
bash install-skills.wsl.sh --dry-run
```

After reviewing the output:

```bash
bash ~/project/skills/install-skills.wsl.sh
```

It scans only immediate non-hidden directories with `SKILL.md` and links them into `~/.codex/skills`
and `~/.claude/skills`. Missing roots, real destination directories and different symlinks are
reported and skipped. Correct links remain unchanged. Duplicate skill names follow source-root
order: an earlier link is kept and a later conflicting source is skipped. The final summary counts
skipped conflicts; exit zero does not mean every skill was installed. Existing real Gortex
directories are reported and skipped like other real destinations; this installer never moves or
overwrites them. The setup guide verifies shared skill links.

## Where a skill is installed, and how it is invoked

This file is authoritative for install paths. Three facts follow, and no document in this repository
may contradict them.

**A personal skill installs under the user's home.** Both destinations are user-level:
`~/.codex/skills` for Codex and `~/.claude/skills` for Claude Code. A skill installed there follows
the user into every repository, which is what a general-purpose skill wants.

**This installer uses `~/.codex/skills` for personal Codex skills** and keeps repository-local
skills under `.agents/skills`. Current Codex documentation also supports `~/.agents/skills` as a
personal discovery root; do not install a second copy there when using this installer's root.
See [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills).

The adapted Gortex task recipes live in `skills/gortex/`; `skills/sohrab/alaa-code-routing-gortex`
remains their shared policy owner. `skills/gortex/provenance.json` records the supplied installer
snapshot and adaptations. Do not refresh this pack by running Gortex's installer or profile
switch against installed symlinks: those operations can write through the links into this repository.
The setup guide describes Git synchronization and shared-link verification.

**Invocation is `/name` in Claude Code and `$name` in Codex**, and both forms name the same skill.
Whether a skill may be selected without being named is declared once per skill, in its
`agents/openai.yaml` under `policy.allow_implicit_invocation`. Read the value out of that file. A
sentence of prose asserting a value for it is a second copy of a fact the runtime reads from the
YAML, and the two will eventually disagree.

For agent or browser setup, use the guides below:

- [Install agents](docs/install-skills/40-agent-installation.md) for personal Claude agents and Codex wrappers.
- [Install the rule-writer agent](docs/install-skills/50-rule-writer.md) for the focused Claude migration and Codex agent file.
- [Set up browser tools](docs/install-skills/60-browser-setup.md) for Playwright MCP setup.

## Vendored skill packs

This repository tracks upstream skill packs under `vendor/`. Metadata-backed entries use `git subtree`; pinned or source-path snapshots are committed vendor directories and are refreshed manually.

<!-- vendor-subtrees:install-list:start -->
Current vendored upstreams:
- [`vendor/openfga-agent-skills`](vendor/openfga-agent-skills/) from `https://github.com/openfga/agent-skills.git`
- [`vendor/cc-skills-golang`](vendor/cc-skills-golang/) from `https://github.com/samber/cc-skills-golang.git`
- [`vendor/claude-plugins-official`](vendor/claude-plugins-official/) from `https://github.com/anthropics/claude-plugins-official.git`
- [`vendor/knowledge-work-plugins`](vendor/knowledge-work-plugins/) from `https://github.com/anthropics/knowledge-work-plugins.git`
- [`vendor/skill-temporal-developer`](vendor/skill-temporal-developer/) from `https://github.com/temporalio/skill-temporal-developer.git`
- [`vendor/hindsight-skills`](vendor/hindsight-skills/) from `https://github.com/vectorize-io/hindsight-skills.git`
- [`vendor/skills`](vendor/skills/) from `https://github.com/caldoai/skills.git`
- [`vendor/security-audit-skill`](vendor/security-audit-skill/) from `https://github.com/cloudflare/security-audit-skill.git`
<!-- vendor-subtrees:install-list:end -->

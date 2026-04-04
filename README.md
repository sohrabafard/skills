# Agent Skills

Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform at specific tasks. Write once, use everywhere.

Codex uses skills to help package capabilities that teams and individuals can use to complete specific tasks in a repeatable way. This repository catalogs skills for use and distribution with Codex.

Learn more:
- [Using skills in Codex](https://developers.openai.com/codex/skills)
- [Create custom skills in Codex](https://developers.openai.com/codex/skills/create-skill)
- [Agent Skills open standard](https://agentskills.io)

## Installing a skill

Skills in [`.system`](skills/.system/) are automatically installed in the latest version of Codex.

To install [curated](skills/.curated/) or [experimental](skills/.experimental/) skills, you can use the `$skill-installer` inside Codex.

Curated skills can be installed by name (defaults to `skills/.curated`):

```
$skill-installer gh-address-comments
```

For experimental skills, specify the skill folder. For example:

```
$skill-installer install the create-plan skill from the .experimental folder
```

Or provide the GitHub directory URL:

```
$skill-installer install https://github.com/openai/skills/tree/main/skills/.experimental/create-plan
```

After installing a skill, restart Codex to pick up new skills.

## Vendored Upstream Skills

This repository also commits third-party skill packs under [`vendor/`](vendor/) using `git subtree`.

<!-- vendor-subtrees:readme-list:start -->
Current vendored upstreams:
- [`vendor/openfga-agent-skills`](vendor/openfga-agent-skills/) from `https://github.com/openfga/agent-skills.git`
- [`vendor/cc-skills-golang`](vendor/cc-skills-golang/) from `https://github.com/samber/cc-skills-golang.git`
<!-- vendor-subtrees:readme-list:end -->

These directories are regular tracked files in this repository. If you sync vendor updates locally and push them to `origin`, any later clone of `origin` already receives the vendored content without running extra subtree pulls.

The only clone-local setup is Git configuration. To make plain `git pull` also refresh all configured vendors in a clone, run once:

```powershell
python scripts\vendor_subtrees.py install-hooks
```

Manual sync remains available:

```powershell
python scripts\vendor_subtrees.py sync
```

To headlessly add a new vendor from only its Git URL:

```powershell
python scripts\vendor_subtrees.py add https://github.com/org/repo.git
```

The command derives the subtree name, detects the default branch, adds the subtree under `vendor/`, updates `vendor/subtrees.json`, and refreshes the vendored-skill docs blocks.

It does not auto-enable hooks and it does not auto-install the vendored skills into Codex. Those remain explicit manual steps.

The manifest for all managed subtree remotes lives in [`vendor/subtrees.json`](vendor/subtrees.json).

## License

The license of an individual skill can be found directly inside the skill's directory inside the `LICENSE.txt` file.

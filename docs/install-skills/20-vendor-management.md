# Vendor setup and management

Run commands from the repository root.

When adding or refreshing OpenFGA, follow [Install the OpenFGA vendor](30-openfga-vendor.md) for its subtree commands and generated-agent build step.

## Vendored skill packs

`vendor/subtrees.json` is the source of truth for subtree definitions.

Important behavior:
- vendored files are committed into this repository like normal files
- when you sync vendor updates locally and push to `origin`, every future clone of `origin` already gets those vendor files
- another clone does not need a separate subtree pull unless you want to refresh directly from upstream vendors again
- local Git configuration does not travel through `origin`, so subtree remotes and hook activation still need one setup command per clone

One-time setup per clone to make plain `git pull` also sync all configured subtrees:

```bash
python3 scripts/vendor_subtrees.py install-hooks
```

That command:
- configures `core.hooksPath=.githooks` for the current clone
- ensures all subtree remotes from `vendor/subtrees.json` exist locally

After that, the repo-managed `post-merge` and `post-rewrite` hooks call the shared sync script after pull, merge, and rebase flows.

Manual subtree commands are still available:

```bash
python3 scripts/vendor_subtrees.py list
python3 scripts/vendor_subtrees.py ensure-remotes
python3 scripts/vendor_subtrees.py sync
python3 scripts/vendor_subtrees.py refresh-docs
```

Notes:
- `python3 scripts/vendor_subtrees.py sync` fetches each syncable vendor remote and runs `git subtree pull --squash` for existing subtree-backed prefixes
- if a syncable configured prefix is missing locally, the script bootstraps it with `git subtree add --squash`
- pinned or source-path snapshots are reported and skipped because they do not have subtree metadata to pull from
- `python3 scripts/vendor_subtrees.py sync` requires a clean worktree; hook-driven sync skips automatically when the worktree is dirty
- when `openfga-agent-skills` changes, the sync script also runs `node vendor/openfga-agent-skills/scripts/build-agents-md.js`

To headlessly add a new vendor from only its Git URL:

```bash
python3 scripts/vendor_subtrees.py add https://github.com/org/repo.git
```

Optional overrides are available when needed:

```bash
python3 scripts/vendor_subtrees.py add https://github.com/org/repo.git --branch main --name repo --prefix vendor/repo --remote repo-upstream
```

That command only vendors the repository, updates `vendor/subtrees.json`, and refreshes the docs. It does not auto-enable hooks and it does not auto-link the new vendored skills into Codex.

Recommended pattern as vendored packs grow:
- keep vendors committed under `vendor/`
- expose only the specific skills you want Codex to see
- avoid bulk-linking every vendored skill pack unless you really want all of them routed

Selective vendored skill exposure is managed with:

```bash
python3 scripts/vendor_skill_links.py vendors
python3 scripts/vendor_skill_links.py list --vendor cc-skills-golang
python3 scripts/vendor_skill_links.py link --vendor cc-skills-golang --skill golang-testing --skill golang-troubleshooting
python3 scripts/vendor_skill_links.py link --vendor cc-skills-golang --skill-prefix golang-samber- --dry-run
python3 scripts/vendor_skill_links.py unlink --vendor cc-skills-golang --all --dry-run
```

Notes:
- `vendors` shows each vendored pack that has a `skills/` directory
- `list` shows available vendored skills plus whether each one is already linked into `~/.codex/skills`
- `link` creates only the symlinks you explicitly selected
- `unlink` removes only matching symlinks that point at the expected vendored skill directories
- the script refuses to overwrite conflicting existing destinations

To link vendored skills, add the relevant vendored `skills/` directory to
[Source roots](../../install-skills.md#source-roots). The vendored source-root lines there are refreshed by
`python3 scripts/vendor_subtrees.py refresh-docs`.

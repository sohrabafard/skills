# Final documentation and packaging gates

- Candidate scope: `install-skills.md`, `docs/install-skills/10-vendored-source-roots.md`, `20-vendor-management.md`, `30-openfga-vendor.md`, `40-agent-installation.md`, `50-rule-writer.md`, and `60-browser-setup.md`.
- Execution: serial; bounded under 120 seconds. No network, live home writes, installation, or scenario rerun.
- Installer scenario evidence: see `independent-verification.md`; the installer SHA remained unchanged, so its nine acceptance cases were not rerun.

## Results

| Check | Result | Evidence |
|---|---|---|
| Repository Markdown links and line budget | PASS, exit 0 | All 7 requested files validated. Grades: install-skills.md YELLOW (99 lines); 10 GREEN (39); 20 YELLOW (83); 30 GREEN (20); 40 GREEN (28); 50 YELLOW (60); 60 GREEN (30). |
| Source roots section until next `##` compared with `git show HEAD:install-skills.md` | PASS | Exact text equal. |
| `#vendor-subtrees:codex-src-roots` start/end marker span compared with HEAD | PASS | One span, exact text equal. |
| `<!--vendor-subtrees:install-list` start/end marker span compared with HEAD | PASS | One span, exact text equal. |
| `bash -n` on fenced Bash blocks via stdin | PASS | 15 blocks syntax-checked; no examples executed. |
| `bash install-skills.wsl.sh --dry-run` | PASS, exit 0 | `links=0 existing/skipped=354 conflicts=0 dry-run=true`. |
| `git diff --check` | PASS, exit 0 | No whitespace errors. |
| Installer source SHA-256 | PASS | Matches frozen value `a48e57592c94375556b2d8c170542410fd49273a05044b6fe90a574e181b31d8`. |

The first marker comparison attempt used an incorrect delimiter assumption and stopped before comparison. After inspecting the file's actual `start`/`end` markers, the exact-section and both marker comparisons passed. This was a verifier helper issue; it did not modify repository files or affect any executed product behavior.

The dry-run only previewed destinations. It reported 354 existing/skipped destinations and zero links or conflicts; it did not install files. Fenced examples were passed to `bash -n` on stdin and never executed.

## Snapshot hashes

SHA-256 values for the frozen installer and each scoped document:

| Path | SHA-256 |
|---|---|
| `scripts/install_claude_rule_writer.py` | `a48e57592c94375556b2d8c170542410fd49273a05044b6fe90a574e181b31d8` |
| `install-skills.md` | `270f418e377a1ecb74419b46cfca83fe5c6980c99eaff397e5996d536a6e3aa9` |
| `docs/install-skills/10-vendored-source-roots.md` | `be15debb649958689ffdff8d56db2c4ce530b24c8f4d95f5c24f53e9ee25ef3a` |
| `docs/install-skills/20-vendor-management.md` | `b296170440285800099d1659afef75a52de9a153f0a6a367a579d993a6803a47` |
| `docs/install-skills/30-openfga-vendor.md` | `f4491e025be46132f6b3a859548bcb78e683fa4e005b7401e1f94e88080ffb5c` |
| `docs/install-skills/40-agent-installation.md` | `e88ce5ea13afcbf80f6327756c9d4acd8d02638f02ab3412bca813fa3ee483d2` |
| `docs/install-skills/50-rule-writer.md` | `a6171765e5552325ca6aaf37bfd8fd46d010eeb8175621bd83f576a2b445a478` |
| `docs/install-skills/60-browser-setup.md` | `379a535a175b95e1630d1d90aaafefd7221b516bc2fe79e5c64a4cc76c346b49` |

## Normalized commands

- `python3 <alaa-repo-docs>/scripts/check_markdown_links.py . --files install-skills.md docs/install-skills/10-vendored-source-roots.md docs/install-skills/20-vendor-management.md docs/install-skills/30-openfga-vendor.md docs/install-skills/40-agent-installation.md docs/install-skills/50-rule-writer.md docs/install-skills/60-browser-setup.md --line-budget` — PASS.
- `bash install-skills.wsl.sh --dry-run` — PASS.
- `bash -n` for each of 15 fenced Bash blocks, source passed on stdin — PASS.
- `git diff --check` — PASS.
- Installer SHA-256 check against frozen value — PASS.

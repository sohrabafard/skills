# Version gaps and upgrade guides

## Inventory

Run `composer outdated --direct --format=json`. Each row gives `version`, `latest`, `latest-status` and `abandoned`. When a `package.json` exists, run `npm outdated --json`; each row gives `current` and `latest`. Field names observed on Composer 2.9.5 and npm 9.2.0, 2026-11-16; check `--help` after an upgrade of either tool.

- **Platform.** Composer reports the latest release that the resolving platform can install. That platform is `config.platform` when the manifest sets it, and the local PHP otherwise. Confirm that it equals the production image before you trust the inventory. To find a package that the platform holds back, compare with `composer outdated --direct --ignore-platform-reqs --format=json`: a row whose `latest` differs meets the first condition in `SKILL.md` *Stop and ask*. Use that flag for this read only, never for a resolution.
- **Latest stable** is the `latest` value under the repository's `minimum-stability`. Never move to an alpha, beta, RC or dev version, unless the manifest already requires that stability for that package.
- `latest-status: semver-safe-update` means the current constraint already allows the latest release. `update-possible` means the constraint must be raised.
- A row whose `latest` is not a version, such as a private package that the configured repositories do not list, is reported as not resolvable and left where it is.
- Inventory direct dependencies only. Transitive packages follow the resolution.

Classify each row by the leftmost version component that changes.

| Change | Gap class |
|---|---|
| `1.4.2` to `1.4.7` | patch |
| `1.4.2` to `1.7.0` | minor |
| `1.4.2` to `2.0.0` | one major |
| `1.4.2` to `4.1.0` | several majors |
| Any component of a `0.x` release, `0.4.2` to `0.5.0` | one major, because semver puts the breaking change in the leftmost non-zero component |

## Guides

Read a guide only for a major move of a direct dependency. A patch or minor move needs none. Read a changelog for a patch or minor move only when a failing gate points at that package.

Use official sources only, in this order:

1. The upgrade guide on the project's own documentation site for each target major. For the framework, use the guide of the target version, not the installed one.
2. The `UPGRADE` file in the package repository at the target tag.
3. The release notes of the major tag.
4. The `CHANGELOG` at the target tag.

A blog post, a forum answer or recalled knowledge is not a source. Laravel Boost documentation search describes the installed version, so it does not replace the target version's guide. Record the URL and the date read for each guide.

- **One major.** Read the guide for that major.
- **Several majors.** Use a consolidated guide when the maintainer publishes one. Otherwise read the guide of every intermediate major in ascending order, and merge the required changes. On the same item, the later guide wins.
- **No guide.** When none of the four sources exists, record `no upgrade guide published` for that package. The move still goes ahead, and the final gates are its proof.

## Plan table

Write one table in the run record:

| Package | From | To | Gap | Guide | Required change | Applies here | Action |
|---|---|---|---|---|---|---|---|

- Enter one row for each required change that a guide lists, and one row for each package with no required change.
- Decide `Applies here` by searching the repository for the affected class, method, configuration key, signature or published file. Use the code-intelligence operation that the repository binding routes. No use in the repository means `not applicable`; write the search that showed it.
- Order the actions: a change that must precede the move, the move, the code and configuration changes, then the regeneration.
- The plan needs no owner approval, except for a row that meets a condition in `SKILL.md` *Stop and ask*.

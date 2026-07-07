#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "vendor" / "subtrees.json"
HOOKS_PATH = ROOT / ".githooks"
SYNC_ENV_VAR = "SKILLS_VENDOR_SYNC_ACTIVE"
README_PATH = ROOT / "README.md"
INSTALL_SKILLS_PATH = ROOT / "install-skills.md"


def load_manifest() -> list[dict[str, object]]:
    raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = raw.get("subtrees")
    if not isinstance(entries, list):
        raise ValueError(f"{MANIFEST_PATH} must define a 'subtrees' list")
    required_keys = {"name", "prefix", "remote", "url", "branch"}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("each subtree entry must be an object")
        missing = sorted(required_keys - set(entry))
        if missing:
            raise ValueError(f"subtree entry missing keys: {', '.join(missing)}")
    return entries


def save_manifest(entries: list[dict[str, object]]) -> None:
    MANIFEST_PATH.write_text(
        json.dumps({"subtrees": entries}, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def run(
    args: list[str],
    *,
    capture: bool = False,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=capture,
        env=env,
    )


def git(
    args: list[str],
    *,
    capture: bool = False,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], capture=capture, check=check, env=env)


def git_head() -> str:
    return git(["rev-parse", "HEAD"], capture=True).stdout.strip()


def git_config_get(key: str) -> str:
    result = git(["config", "--local", "--get", key], capture=True, check=False)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def working_tree_dirty() -> bool:
    status = git(["status", "--short"], capture=True)
    return bool(status.stdout.strip())


def ensure_remote(entry: dict[str, object]) -> None:
    remote = str(entry["remote"])
    url = str(entry["url"])
    current = git(["remote", "get-url", remote], capture=True, check=False)
    if current.returncode != 0:
        print(f"[vendor-subtrees] adding remote {remote} -> {url}")
        git(["remote", "add", remote, url])
        return
    current_url = current.stdout.strip()
    if current_url != url:
        print(f"[vendor-subtrees] updating remote {remote} -> {url}")
        git(["remote", "set-url", remote, url])


def ensure_remotes(entries: list[dict[str, object]]) -> None:
    for entry in entries:
        ensure_remote(entry)


def subtree_exists(prefix: str) -> bool:
    return (ROOT / prefix).exists()


def normalize_prefix(prefix: str) -> str:
    normalized = prefix.replace("\\", "/").strip("/")
    if not normalized:
        raise ValueError("subtree prefix cannot be empty")
    return normalized


def snapshot_skip_reason(entry: dict[str, object]) -> str:
    source_path_value = entry.get("source_path")
    pinned_commit_value = entry.get("pinned_commit")
    source_path = str(source_path_value) if source_path_value else ""
    pinned_commit = str(pinned_commit_value) if pinned_commit_value else ""
    if source_path and pinned_commit:
        return f"source_path snapshot ({source_path}) pinned at {pinned_commit[:12]}"
    if source_path:
        return f"source_path snapshot ({source_path})"
    if pinned_commit:
        return f"pinned snapshot at {pinned_commit[:12]}"
    return ""


def subtree_env() -> dict[str, str]:
    env = os.environ.copy()
    env[SYNC_ENV_VAR] = "1"
    return env


def run_post_sync(entry: dict[str, object]) -> None:
    commands = entry.get("post_sync", [])
    if not commands:
        return
    if not isinstance(commands, list):
        raise ValueError(f"post_sync for {entry['name']} must be a list")
    for command in commands:
        if not isinstance(command, list) or not command:
            raise ValueError(f"invalid post_sync command for {entry['name']}")
        printable = " ".join(command)
        print(f"[vendor-subtrees] post-sync: {printable}")
        run([str(part) for part in command], env=subtree_env())


def sync_entry(entry: dict[str, object]) -> bool:
    name = str(entry["name"])
    prefix = str(entry["prefix"])
    remote = str(entry["remote"])
    branch = str(entry["branch"])

    ensure_remote(entry)
    skip_reason = snapshot_skip_reason(entry)
    if skip_reason:
        if not subtree_exists(prefix):
            raise SystemExit(
                f"[vendor-subtrees] cannot refresh {name}: {skip_reason} "
                f"is missing from {prefix}; restore it manually"
            )
        print(
            f"[vendor-subtrees] skipping {name}: {skip_reason}; "
            "refresh it manually"
        )
        return False

    print(f"[vendor-subtrees] syncing {name} ({prefix}) from {remote}/{branch}")
    git(["fetch", remote, branch])

    head_before = git_head()
    env = subtree_env()
    if subtree_exists(prefix):
        git(["subtree", "pull", "--prefix", prefix, remote, branch, "--squash"], env=env)
    else:
        git(["subtree", "add", "--prefix", prefix, remote, branch, "--squash"], env=env)
    head_after = git_head()
    changed = head_before != head_after
    if not changed:
        print(f"[vendor-subtrees] {name} already up to date")
    return changed


def install_hooks() -> None:
    if not HOOKS_PATH.exists():
        raise FileNotFoundError(f"missing hooks directory: {HOOKS_PATH}")
    git(["config", "--local", "core.hooksPath", ".githooks"])
    print("[vendor-subtrees] configured core.hooksPath=.githooks for this clone")


def hooks_installed() -> bool:
    return git_config_get("core.hooksPath") == ".githooks"


def print_manifest(entries: list[dict[str, object]]) -> None:
    for entry in entries:
        print(
            f"- {entry['name']}: prefix={entry['prefix']} "
            f"remote={entry['remote']} branch={entry['branch']}"
        )


def derive_repo_name(repo_url: str) -> str:
    cleaned = repo_url.rstrip("/")
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]
    tail = cleaned.rsplit("/", 1)[-1]
    tail = tail.rsplit(":", 1)[-1]
    if not tail:
        raise ValueError(f"could not derive repo name from URL: {repo_url}")
    return tail


def slugify_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-").lower()


def detect_default_branch(repo_url: str) -> str:
    result = git(["ls-remote", "--symref", repo_url, "HEAD"], capture=True)
    for line in result.stdout.splitlines():
        if line.startswith("ref: refs/heads/") and line.endswith("\tHEAD"):
            return line[len("ref: refs/heads/") :].split("\t", 1)[0]
    return "main"


def vendor_list_markdown(entries: list[dict[str, object]]) -> str:
    lines = ["Current vendored upstreams:"]
    for entry in entries:
        prefix = str(entry["prefix"])
        url = str(entry["url"])
        lines.append(f"- [`{prefix}`]({prefix}/) from `{url}`")
    return "\n".join(lines)


def codex_src_roots_block(entries: list[dict[str, object]]) -> str:
    skill_roots = [str(entry["prefix"]) for entry in entries if subtree_exists(f"{entry['prefix']}/skills")]
    if not skill_roots:
        return "$srcRoots = @()"
    lines = ["$repoRoot = (Resolve-Path \".\").Path", "$srcRoots = @("]
    for index, prefix in enumerate(skill_roots):
        suffix = "," if index < len(skill_roots) - 1 else ""
        lines.append(f"    (Join-Path $repoRoot \"{prefix.replace('/', '\\')}\\skills\"){suffix}")
    lines.append(")")
    return "\n".join(lines)


def replace_marker_span(path: Path, start: str, end: str, body: str) -> None:
    raw = path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(start) + r"[\s\S]*?" + re.escape(end), re.MULTILINE)
    replacement = f"{start}\n{body}\n{end}"
    updated, count = pattern.subn(lambda _: replacement, raw, count=1)
    if count != 1:
        raise ValueError(f"marker block not found exactly once in {path}: {start} ... {end}")
    path.write_text(updated, encoding="utf-8")


def refresh_docs(entries: list[dict[str, object]]) -> None:
    replace_marker_span(
        README_PATH,
        "<!-- vendor-subtrees:readme-list:start -->",
        "<!-- vendor-subtrees:readme-list:end -->",
        vendor_list_markdown(entries),
    )
    replace_marker_span(
        INSTALL_SKILLS_PATH,
        "<!-- vendor-subtrees:install-list:start -->",
        "<!-- vendor-subtrees:install-list:end -->",
        vendor_list_markdown(entries),
    )
    replace_marker_span(
        INSTALL_SKILLS_PATH,
        "# vendor-subtrees:codex-src-roots:start",
        "# vendor-subtrees:codex-src-roots:end",
        codex_src_roots_block(entries),
    )
    print("[vendor-subtrees] refreshed README.md and install-skills.md from vendor/subtrees.json")


def entry_conflicts(entries: list[dict[str, object]], new_entry: dict[str, object]) -> str:
    for existing in entries:
        for key in ("name", "prefix", "remote", "url"):
            if str(existing[key]) == str(new_entry[key]):
                return f"{key} already exists in manifest: {existing[key]}"
    return ""


def add_subtree_from_repo_url(
    entries: list[dict[str, object]],
    repo_url: str,
    *,
    branch: str | None,
    name: str | None,
    prefix: str | None,
    remote: str | None,
) -> None:
    if working_tree_dirty():
        raise SystemExit("[vendor-subtrees] add requires a clean worktree")

    repo_name = name or derive_repo_name(repo_url)
    slug = slugify_name(repo_name)
    entry = {
        "name": repo_name,
        "prefix": normalize_prefix(prefix or f"vendor/{slug}"),
        "remote": remote or f"{slug}-upstream",
        "url": repo_url,
        "branch": branch or detect_default_branch(repo_url),
    }
    conflict = entry_conflicts(entries, entry)
    if conflict:
        raise SystemExit(f"[vendor-subtrees] cannot add subtree: {conflict}")
    if subtree_exists(str(entry["prefix"])):
        raise SystemExit(f"[vendor-subtrees] prefix already exists on disk: {entry['prefix']}")

    ensure_remote(entry)
    if not hooks_installed():
        print(
            "[vendor-subtrees] note: .githooks is not enabled in this clone; "
            "run 'python scripts\\vendor_subtrees.py install-hooks' when you want automatic post-pull sync"
        )
    print(
        f"[vendor-subtrees] adding {entry['name']} "
        f"at {entry['prefix']} from {entry['remote']}/{entry['branch']}"
    )
    git(["fetch", str(entry["remote"]), str(entry["branch"])])
    git(
        [
            "subtree",
            "add",
            "--prefix",
            str(entry["prefix"]),
            str(entry["remote"]),
            str(entry["branch"]),
            "--squash",
        ],
        env=subtree_env(),
    )
    entries.append(entry)
    save_manifest(entries)
    refresh_docs(entries)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage vendored git subtrees for this repo.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List configured subtrees.")
    subparsers.add_parser("ensure-remotes", help="Create or update all subtree remotes.")
    subparsers.add_parser("install-hooks", help="Configure this clone to use repo-managed hooks.")
    subparsers.add_parser("refresh-docs", help="Regenerate vendor doc sections from the manifest.")

    sync_parser = subparsers.add_parser("sync", help="Fetch and sync every configured subtree.")
    sync_parser.add_argument("--from-hook", action="store_true", help=argparse.SUPPRESS)
    sync_parser.add_argument("--source", default="manual", help=argparse.SUPPRESS)

    hook_parser = subparsers.add_parser(
        "sync-from-hook",
        help="Internal command used by repo-managed hooks after pull/merge/rebase flows.",
    )
    hook_parser.add_argument("--source", default="hook", help=argparse.SUPPRESS)

    add_parser = subparsers.add_parser(
        "add",
        help="Headlessly add a new vendored subtree from a Git repository URL.",
    )
    add_parser.add_argument("repo_url", help="Git repository URL, for example https://github.com/org/repo.git")
    add_parser.add_argument("--branch", help="Override the detected default branch")
    add_parser.add_argument("--name", help="Override the manifest name and derived defaults")
    add_parser.add_argument("--prefix", help="Override the vendor prefix path")
    add_parser.add_argument("--remote", help="Override the Git remote name")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    entries = load_manifest()

    if args.command == "list":
        print_manifest(entries)
        return 0

    if args.command == "ensure-remotes":
        ensure_remotes(entries)
        return 0

    if args.command == "install-hooks":
        install_hooks()
        ensure_remotes(entries)
        return 0

    if args.command == "refresh-docs":
        refresh_docs(entries)
        return 0

    if args.command == "add":
        add_subtree_from_repo_url(
            entries,
            args.repo_url,
            branch=args.branch,
            name=args.name,
            prefix=args.prefix,
            remote=args.remote,
        )
        return 0

    if args.command in {"sync", "sync-from-hook"}:
        if os.environ.get(SYNC_ENV_VAR) == "1":
            print("[vendor-subtrees] recursive hook sync suppressed")
            return 0
        if working_tree_dirty():
            if args.command == "sync-from-hook":
                print("[vendor-subtrees] hook sync skipped because the worktree is dirty")
                return 0
            print(
                "[vendor-subtrees] sync requires a clean worktree; commit, stash, or discard local changes first",
                file=sys.stderr,
            )
            return 1
        changed_any = False
        changed_entries: list[dict[str, object]] = []
        for entry in entries:
            changed = sync_entry(entry)
            changed_any = changed or changed_any
            if changed:
                changed_entries.append(entry)
        for entry in changed_entries:
            run_post_sync(entry)
        if not changed_any:
            print("[vendor-subtrees] all subtrees are already up to date")
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"[vendor-subtrees] command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        raise
    except Exception as exc:  # pragma: no cover - defensive CLI surface
        print(f"[vendor-subtrees] error: {exc}", file=sys.stderr)
        raise SystemExit(1)

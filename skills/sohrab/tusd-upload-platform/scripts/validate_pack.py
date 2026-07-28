#!/usr/bin/env python3
"""Validate the tusd-upload-platform skill pack.

Ten checks run against a skill directory. Each violation names the file, the
line where one exists, what is wrong, and what the agent must do about it.

Exit codes
  0  every check passed. Nothing is owed.
  1  at least one check failed. Fix every violation printed and re-run; a
     violation is a defect in the pack, never a reason to relax the check.
  2  the script was misused or could not run: a bad argument, a root that is
     not a skill directory, or a missing dependency. Correct the invocation.
     Exit 2 is not evidence that the pack is clean.

Usage
  python3 scripts/validate_pack.py --root .
  python3 scripts/validate_pack.py --self-test
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SKILL_NAME = "tusd-upload-platform"
DESCRIPTION_HARD_LIMIT = 1024
DESCRIPTION_AUTHOR_TARGET = 950
ROUTER_THRESHOLD = 9
TOPIC_MAP = "references/00-topic-map.md"

TEXT_SUFFIXES = {
    ".md", ".yaml", ".yml", ".json", ".ts", ".vue", ".cfg", ".conf",
    ".example", ".py", ".sh",
}

REQUIRED_TUSD_FLAGS = ("-max-size", "-behind-proxy", "-disable-download")

# A trigger in Codex form. Lowercase kebab only, so shell variables like
# ${TUSD_IMAGE}, $UPLOAD_THRESHOLD and JavaScript's $& never match.
CODEX_TRIGGER = re.compile(r"\$([a-z][a-z0-9]*(?:-[a-z0-9]+)+)")

# A three-part release string. `github.com/tus/tusd/v2` has two parts and does
# not match; `v2.9.2` does.
VERSION_STRING = re.compile(r"\bv\d+\.\d+\.\d+")

# A Compose interpolation with whatever follows the variable name. Compose
# expands these at render time from the shell and --env-file, never from a
# service-level env_file, so a bare ${VAR} silently renders an empty argument.
INTERPOLATION = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)([^}]*)\}")

# Variables that must abort the render when absent, with no default of any
# kind: a default upload cap - including 0, which tusd treats as unlimited -
# is a policy decision no asset may make on the deployment's behalf.
NEVER_DEFAULT = frozenset({"TUSD_MAX_SIZE"})

PACK_PATH = re.compile(r"`((?:references|assets|scripts)/[^`]+)`")


@dataclass(frozen=True)
class Violation:
    check: str
    path: str
    line: int | None
    message: str
    obligation: str
    #: A warning is printed and does not fail the run. Only the author target
    #: for the description is a warning; every other finding is a violation,
    #: because the runtimes reject or mis-route the skill outright.
    warning: bool = False

    def render(self) -> str:
        where = self.path if self.line is None else f"{self.path}:{self.line}"
        label = "WARN" if self.warning else self.check
        return (
            f"[{label}] {where}\n"
            f"    problem:    {self.message}\n"
            f"    obligation: {self.obligation}"
        )


class Misuse(Exception):
    """The script cannot run. Distinct from a pack violation."""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def text_files(root: Path) -> list[Path]:
    found = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or ".git" in path.parts:
            continue
        if path.suffix in TEXT_SUFFIXES:
            found.append(path)
    return found


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def line_of(text: str, needle: str) -> int | None:
    for number, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return number
    return None


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise Misuse("SKILL.md has no YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise Misuse("SKILL.md frontmatter is not terminated")
    return parts[1], parts[2]


def content_references(root: Path) -> list[Path]:
    directory = root / "references"
    if not directory.is_dir():
        return []
    return sorted(
        p for p in directory.glob("*.md") if p.name != "00-topic-map.md"
    )


def topic_map_paths(root: Path) -> list[tuple[str, int]]:
    path = root / TOPIC_MAP
    if not path.exists():
        return []
    found = []
    for number, line in enumerate(read(path).splitlines(), start=1):
        for match in PACK_PATH.findall(line):
            found.append((match.split()[0].rstrip(".,;"), number))
    return found


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def check_single_router(root: Path) -> list[Violation]:
    """1 - exactly one router, in the place the reference count requires."""
    out: list[Violation] = []
    body = read(root / "SKILL.md")
    mentioned = re.findall(r"references/[A-Za-z0-9_.-]+", body)
    count = len(content_references(root))
    has_map = (root / TOPIC_MAP).exists()

    if count >= ROUTER_THRESHOLD and not has_map:
        out.append(Violation(
            "single-router", TOPIC_MAP, None,
            f"{count} content references is at or above the {ROUTER_THRESHOLD}-reference "
            "threshold, so the router belongs in the topic map, which is missing",
            "move the router out of SKILL.md into references/00-topic-map.md, "
            "preserving every row",
        ))
    if count < ROUTER_THRESHOLD and has_map:
        out.append(Violation(
            "single-router", TOPIC_MAP, None,
            f"{count} content references is below the {ROUTER_THRESHOLD}-reference "
            "threshold, so the router belongs in SKILL.md and the topic map must not exist",
            "move every topic-map row into a SKILL.md table, then retire the topic map",
        ))
    if has_map and mentioned != [TOPIC_MAP]:
        extra = [m for m in mentioned if m != TOPIC_MAP]
        out.append(Violation(
            "single-router", "SKILL.md", line_of(body, extra[0]) if extra else None,
            "SKILL.md names reference files other than the topic map: "
            + ", ".join(sorted(set(extra)))
            + "; two routers drift and the agent follows whichever it reads first",
            "leave exactly one pointer line in SKILL.md and route everything "
            "else from references/00-topic-map.md",
        ))
    return out


def check_topic_map_covers_pack(root: Path) -> list[Violation]:
    """2 - every reference and asset is routed, and every routed path resolves."""
    out: list[Violation] = []
    if not (root / TOPIC_MAP).exists():
        return out

    routed = topic_map_paths(root)
    routed_set = {p for p, _ in routed}

    for path, number in routed:
        if not (root / path).exists():
            out.append(Violation(
                "topic-map", TOPIC_MAP, number,
                f"routes to {path}, which does not exist",
                "create the file or correct the row; a dead router row costs "
                "the agent a wasted hop",
            ))

    expected = [rel(root, p) for p in content_references(root)]
    assets = root / "assets"
    if assets.is_dir():
        expected += [rel(root, p) for p in sorted(assets.rglob("*")) if p.is_file()]
    scripts = root / "scripts"
    if scripts.is_dir():
        expected += [
            rel(root, p) for p in sorted(scripts.rglob("*.py"))
            if "__pycache__" not in p.parts
        ]

    for path in expected:
        if path not in routed_set:
            out.append(Violation(
                "topic-map", TOPIC_MAP, None,
                f"{path} ships in the pack but no router row reaches it",
                "add a row stating the observable condition under which an "
                "agent should open that file",
            ))
    return out


def check_image_pinned(root: Path) -> list[Violation]:
    """3 - no floating container tag."""
    out: list[Violation] = []
    for path in text_files(root):
        if path.name == Path(__file__).name:
            continue
        for number, line in enumerate(read(path).splitlines(), start=1):
            if re.search(r"\btusd:latest\b", line) or re.search(
                r"image:\s*\S*tusd:\s*$", line
            ):
                out.append(Violation(
                    "image-pin", rel(root, path), number,
                    "a floating tusd tag makes a rollback unreproducible",
                    "pin an exact release through the TUSD_IMAGE variable and "
                    "record the version in references/10-source-map.md",
                ))
    return out


def check_required_flags(root: Path) -> list[Violation]:
    """4 - every tusd invocation carries the three mandatory flags."""
    out: list[Violation] = []
    candidates = list((root / "assets" / "docker-compose").glob("*.y*ml")) \
        if (root / "assets" / "docker-compose").is_dir() else []
    for path in sorted(candidates):
        text = read(path)
        for flag in REQUIRED_TUSD_FLAGS:
            if flag not in text:
                out.append(Violation(
                    "required-flags", rel(root, path), None,
                    f"the command block does not set {flag}",
                    "add it; an unset -max-size means unlimited, an unset "
                    "-behind-proxy means a wrong Location, and an unset "
                    "-disable-download exposes the bytes over GET",
                ))
    for path in sorted((root / "references").glob("*.md")) if (root / "references").is_dir() else []:
        text = read(path)
        for block in re.findall(r"```(?:bash|sh)\n(.*?)```", text, re.S):
            if not re.search(r"(^|\s)tusd\s", block):
                continue
            for flag in REQUIRED_TUSD_FLAGS:
                if flag not in block:
                    out.append(Violation(
                        "required-flags", rel(root, path), line_of(text, block.splitlines()[0]),
                        f"a tusd CLI baseline omits {flag}",
                        "add the flag, or delete the baseline and let the "
                        "Compose assets be the single source",
                    ))
    return out


def check_fail_closed_interpolation(root: Path) -> list[Violation]:
    """4b - every Compose interpolation is fail-closed or has a default.

    A bare ${VAR} in a Compose file renders as an empty string when the
    variable is absent from the render-time environment, because the
    service-level env_file is applied to the container only, never to
    interpolation. An empty `-max-size=` is an unlimited upload configuration,
    so every variable must either abort the render (${VAR:?message}) or carry
    a deliberate default (${VAR:-value}).
    """
    out: list[Violation] = []
    directory = root / "assets" / "docker-compose"
    if not directory.is_dir():
        return out
    for path in sorted(directory.glob("*.y*ml")):
        for number, line in enumerate(read(path).splitlines(), start=1):
            # Comments are stripped before Compose interpolates, so a ${VAR}
            # mentioned in one is documentation, not a rendered value.
            if line.lstrip().startswith("#"):
                continue
            for match in INTERPOLATION.finditer(line):
                name, modifier = match.group(1), match.group(2)
                if name in NEVER_DEFAULT:
                    if not modifier.startswith(":?"):
                        out.append(Violation(
                            "fail-closed-interpolation", rel(root, path), number,
                            f"${{{name}{modifier}}} carries a default or is bare; {name} "
                            "must abort the render when absent, because any default - "
                            "including 0, which tusd treats as unlimited - silently "
                            "removes the upload cap",
                            f"write ${{{name}:?message}} with no default",
                        ))
                    continue
                if modifier.startswith(":?") or modifier.startswith(":-"):
                    continue
                out.append(Violation(
                    "fail-closed-interpolation", rel(root, path), number,
                    f"${{{name}{modifier}}} is not fail-closed: when {name} is missing "
                    "from the render-time environment it silently becomes an empty "
                    "argument, and an empty -max-size means unlimited uploads",
                    f"write ${{{name}:?message}} so the render aborts, or "
                    f"${{{name}:-default}} if the value is deliberately optional",
                ))
    return out


def check_version_in_one_file(root: Path) -> list[Violation]:
    """5 - the release version string lives in exactly one file."""
    holders: dict[str, int] = {}
    for path in text_files(root):
        if path.name == Path(__file__).name:
            continue
        text = read(path)
        match = VERSION_STRING.search(text)
        if match:
            holders[rel(root, path)] = line_of(text, match.group(0)) or 1
    if len(holders) <= 1:
        return []
    return [
        Violation(
            "version-single-source", path, number,
            "a release version string appears in more than one file: "
            + ", ".join(sorted(holders)),
            "keep the version snapshot in references/10-source-map.md only, "
            "and have every other file take it from a variable or point here",
        )
        for path, number in sorted(holders.items())
    ]


def check_no_route_literal_in_client(root: Path) -> list[Violation]:
    """6 - client assets contain no hardcoded upload route."""
    out: list[Violation] = []
    directory = root / "assets" / "client"
    if not directory.is_dir():
        return out
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        for number, line in enumerate(read(path).splitlines(), start=1):
            if "/files/" in line or "/files'" in line or '/files"' in line:
                out.append(Violation(
                    "client-route-literal", rel(root, path), number,
                    "a hardcoded upload route stops matching when the "
                    "deployment path changes, and the failure is silent",
                    "take the base path as an argument or from configuration",
                ))
    return out


def check_description(root: Path) -> list[Violation]:
    """7 - the description fits, names the skill, and carries a negative clause."""
    out: list[Violation] = []
    text = read(root / "SKILL.md")
    frontmatter, _ = split_frontmatter(text)

    name = re.search(r"^name:\s*(.+)$", frontmatter, re.M)
    if not name or name.group(1).strip() != SKILL_NAME:
        out.append(Violation(
            "description", "SKILL.md", line_of(text, "name:"),
            f"frontmatter name is not {SKILL_NAME}",
            "set the name to the directory name; the runtimes key on it",
        ))

    match = re.search(r'^description:\s*"(.*)"\s*$', frontmatter, re.M | re.S)
    if not match:
        raise Misuse("SKILL.md frontmatter has no double-quoted description")
    description = match.group(1)

    if len(description) > DESCRIPTION_HARD_LIMIT:
        out.append(Violation(
            "description", "SKILL.md", line_of(text, "description:"),
            f"description is {len(description)} characters, over the hard "
            f"limit of {DESCRIPTION_HARD_LIMIT}; plugin validation rejects it",
            "cut it to the author target and re-run",
        ))
    elif len(description) > DESCRIPTION_AUTHOR_TARGET:
        out.append(Violation(
            "description", "SKILL.md", line_of(text, "description:"),
            f"description is {len(description)} characters, over the author "
            f"target of {DESCRIPTION_AUTHOR_TARGET}; one added clause breaks the build",
            "cut it back to the target so there is headroom",
            warning=True,
        ))

    if not re.search(r"\bDo not use\b", description):
        out.append(Violation(
            "description", "SKILL.md", line_of(text, "description:"),
            "description has no negative clause, so the skill over-triggers "
            "and an over-triggering library is unusable",
            "add a sentence starting 'Do not use it for…' that names the "
            "alternative skill",
        ))
    return out


def check_trigger_forms(root: Path) -> list[Violation]:
    """8 - no Codex trigger without its Claude Code twin."""
    out: list[Violation] = []
    for path in text_files(root):
        relative = rel(root, path)
        if relative == "agents/openai.yaml" or path.name == Path(__file__).name:
            continue
        text = read(path)
        for number, line in enumerate(text.splitlines(), start=1):
            for name in CODEX_TRIGGER.findall(line):
                if f"/{name}" not in text:
                    out.append(Violation(
                        "trigger-forms", relative, number,
                        f"${name} appears with no /{name} twin in the same file; "
                        "Claude Code and Codex both load this pack",
                        f"write it as /{name} (${name})",
                    ))
    return out


def check_openai_policy(root: Path) -> list[Violation]:
    """9 - agents/openai.yaml parses and allows implicit invocation."""
    path = root / "agents" / "openai.yaml"
    if not path.exists():
        return [Violation(
            "openai-policy", "agents/openai.yaml", None,
            "the Codex metadata file is missing",
            "add it with an interface block and a policy block",
        )]
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise Misuse(f"PyYAML is required to validate agents/openai.yaml: {exc}")
    try:
        data = yaml.safe_load(read(path)) or {}
    except yaml.YAMLError as exc:
        return [Violation(
            "openai-policy", "agents/openai.yaml", None,
            f"the file is not valid YAML: {exc}",
            "fix the syntax; Codex will not load the skill otherwise",
        )]
    policy = data.get("policy") or {}
    if policy.get("allow_implicit_invocation") is not True:
        return [Violation(
            "openai-policy", "agents/openai.yaml", line_of(read(path), "policy"),
            "policy.allow_implicit_invocation is not true, so Codex will not "
            "reach this skill unless the user names it",
            "add:  policy:\\n  allow_implicit_invocation: true",
        )]
    return []


CHECKS = (
    ("single-router", check_single_router),
    ("topic-map", check_topic_map_covers_pack),
    ("image-pin", check_image_pinned),
    ("required-flags", check_required_flags),
    ("fail-closed-interpolation", check_fail_closed_interpolation),
    ("version-single-source", check_version_in_one_file),
    ("client-route-literal", check_no_route_literal_in_client),
    ("description", check_description),
    ("trigger-forms", check_trigger_forms),
    ("openai-policy", check_openai_policy),
)


def run_checks(root: Path) -> list[Violation]:
    if not (root / "SKILL.md").is_file():
        raise Misuse(f"{root} is not a skill directory: SKILL.md is missing")
    violations: list[Violation] = []
    for _, check in CHECKS:
        violations.extend(check(root))
    return violations


# --------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------

GOOD_DESCRIPTION = (
    "Upload platform skill for tus and tusd, covering the server, the browser "
    "client and this repository's own service. Use it to design, review or "
    "debug an upload plane. Do not use it for presigned uploads; for buckets "
    "use /alaa-minio-object-storage."
)


def build_fixture(directory: Path) -> None:
    """Build a minimal pack that passes every check."""
    (directory / "references").mkdir(parents=True)
    (directory / "assets" / "client").mkdir(parents=True)
    (directory / "assets" / "docker-compose").mkdir(parents=True)
    (directory / "agents").mkdir()
    (directory / "scripts").mkdir()

    (directory / "SKILL.md").write_text(
        "---\n"
        f"name: {SKILL_NAME}\n"
        f'description: "{GOOD_DESCRIPTION}"\n'
        "---\n\n"
        "# Fixture\n\n"
        "Routing lives in `references/00-topic-map.md`.\n",
        encoding="utf-8",
    )

    names = [f"{n:02d}-topic-{n}.md" for n in range(10, 100, 10)]
    rows = []
    for name in names:
        (directory / "references" / name).write_text(f"# {name}\n", encoding="utf-8")
        rows.append(f"| you are about to touch {name} | `references/{name}` |")
    rows.append("| you are about to write client code | `assets/client/upload.ts` |")
    rows.append("| you are about to deploy | `assets/docker-compose/tusd.compose.yaml` |")
    rows.append("| you are about to finish a change | `scripts/validate_pack.py` |")

    (directory / TOPIC_MAP).write_text(
        "# Topic Map\n\n| condition | file |\n|---|---|\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    (directory / "references" / "10-topic-10.md").write_text(
        "# Source\n\nPinned release: v2.9.2, read 2026-04-24.\n", encoding="utf-8"
    )
    (directory / "assets" / "client" / "upload.ts").write_text(
        "export const basePath = process.env.UPLOAD_BASE_PATH\n", encoding="utf-8"
    )
    (directory / "assets" / "docker-compose" / "tusd.compose.yaml").write_text(
        "services:\n  tusd:\n    image: ${TUSD_IMAGE:?pin it}\n    command:\n"
        '      - "-behind-proxy"\n      - "-disable-download"\n'
        '      - "-max-size=${TUSD_MAX_SIZE:?set the cap}"\n',
        encoding="utf-8",
    )
    (directory / "agents" / "openai.yaml").write_text(
        "interface:\n  display_name: \"Fixture\"\npolicy:\n"
        "  allow_implicit_invocation: true\n",
        encoding="utf-8",
    )
    shutil.copyfile(Path(__file__).resolve(), directory / "scripts" / "validate_pack.py")


MUTATIONS = {
    "single-router": lambda d: (d / "SKILL.md").write_text(
        read(d / "SKILL.md") + "\nAlso read `references/20-topic-20.md`.\n",
        encoding="utf-8",
    ),
    "topic-map": lambda d: (d / "references" / "95-orphan.md").write_text(
        "# orphan\n", encoding="utf-8"
    ),
    "image-pin": lambda d: (d / "assets" / "docker-compose" / "tusd.compose.yaml").write_text(
        read(d / "assets" / "docker-compose" / "tusd.compose.yaml").replace(
            "${TUSD_IMAGE:?pin it}", "tusproject/tusd:latest"
        ),
        encoding="utf-8",
    ),
    "required-flags": lambda d: (d / "assets" / "docker-compose" / "tusd.compose.yaml").write_text(
        read(d / "assets" / "docker-compose" / "tusd.compose.yaml").replace(
            '      - "-max-size=${TUSD_MAX_SIZE:?set the cap}"\n', ""
        ),
        encoding="utf-8",
    ),
    "fail-closed-interpolation": lambda d: (d / "assets" / "docker-compose" / "tusd.compose.yaml").write_text(
        read(d / "assets" / "docker-compose" / "tusd.compose.yaml").replace(
            "${TUSD_MAX_SIZE:?set the cap}", "${TUSD_MAX_SIZE}"
        ),
        encoding="utf-8",
    ),
    # A defaulted cap is as unsafe as a bare one: 0 means unlimited in tusd,
    # so `:-0` must fire the same check even though `:-` is fail-closed for
    # every other variable.
    "fail-closed-interpolation@default-cap": lambda d: (d / "assets" / "docker-compose" / "tusd.compose.yaml").write_text(
        read(d / "assets" / "docker-compose" / "tusd.compose.yaml").replace(
            "${TUSD_MAX_SIZE:?set the cap}", "${TUSD_MAX_SIZE:-0}"
        ),
        encoding="utf-8",
    ),
    "version-single-source": lambda d: (d / "references" / "20-topic-20.md").write_text(
        "# duplicate\n\nAlso v2.9.2 here.\n", encoding="utf-8"
    ),
    "client-route-literal": lambda d: (d / "assets" / "client" / "upload.ts").write_text(
        "export const basePath = '/files/'\n", encoding="utf-8"
    ),
    "description": lambda d: (d / "SKILL.md").write_text(
        read(d / "SKILL.md").replace(
            " Do not use it for presigned uploads; for buckets use /alaa-minio-object-storage.",
            "",
        ),
        encoding="utf-8",
    ),
    "trigger-forms": lambda d: (d / "references" / "30-topic-30.md").write_text(
        "# triggers\n\nUse $alaa-reliability-sla for retries.\n", encoding="utf-8"
    ),
    "openai-policy": lambda d: (d / "agents" / "openai.yaml").write_text(
        'interface:\n  display_name: "Fixture"\n', encoding="utf-8"
    ),
}


def self_test() -> int:
    """Build fixtures outside the repository and prove each check fires."""
    workspace = Path(tempfile.mkdtemp(prefix="tusd-skill-selftest-"))
    if workspace.is_relative_to(Path(__file__).resolve().parents[1]):
        raise Misuse("self-test fixtures must not be built inside the skill")
    print(f"self-test workspace: {workspace}")
    failures = 0
    try:
        clean = workspace / "clean"
        clean.mkdir()
        build_fixture(clean)
        baseline = [v for v in run_checks(clean) if not v.warning]
        if baseline:
            failures += 1
            print("FAIL  clean fixture produced violations:")
            for violation in baseline:
                print("      " + violation.render().replace("\n", "\n      "))
        else:
            print("ok    clean fixture is clean")

        for name, mutate in MUTATIONS.items():
            # A key may carry an `@variant` suffix so one check can have
            # several mutations; the expected check name is the part before it.
            expected = name.split("@", 1)[0]
            case = workspace / name
            shutil.copytree(clean, case)
            mutate(case)
            fired = {v.check for v in run_checks(case)}
            if expected in fired:
                print(f"ok    {name} fires when broken")
            else:
                failures += 1
                print(f"FAIL  {name} did not fire; checks that fired: {sorted(fired) or 'none'}")
    finally:
        shutil.rmtree(workspace, ignore_errors=True)

    checked = len(MUTATIONS) + 1
    if failures:
        print(f"\nself-test: {failures} of {checked} expectations failed")
        return 1
    print(f"\nself-test: {checked} of {checked} expectations held")
    return 0


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_pack.py",
        description="Validate the tusd-upload-platform skill pack.",
        epilog=(
            "exit 0  every check passed; nothing is owed.\n"
            "exit 1  a check failed; fix every violation printed and re-run. "
            "A violation is a defect in the pack, never a reason to relax the check.\n"
            "exit 2  misuse or a missing dependency; correct the invocation. "
            "Exit 2 is not evidence that the pack is clean."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--root",
        default=os.environ.get("SKILL_ROOT"),
        help="skill directory to validate; defaults to $SKILL_ROOT, then to the "
             "parent of this script",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="build fixtures in a temporary directory outside the repository and "
             "prove every check fires when its rule is broken",
    )
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            return self_test()

        root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
        if not root.is_dir():
            raise Misuse(f"{root} is not a directory")
        violations = run_checks(root)
    except Misuse as exc:
        print(f"MISUSE: {exc}", file=sys.stderr)
        return 2

    failures = [v for v in violations if not v.warning]
    warnings = [v for v in violations if v.warning]

    for violation in failures + warnings:
        print(violation.render())

    if failures:
        print(f"\n{len(failures)} violation(s), {len(warnings)} warning(s) in {root}")
        return 1

    print(f"\nOK: {root} passed all {len(CHECKS)} checks "
          f"({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

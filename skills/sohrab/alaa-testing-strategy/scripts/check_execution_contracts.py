#!/usr/bin/env python3
"""Topic: execution ownership; layer: structural source contract.

Finite reviewed clauses detect source regressions, not live agent obedience.
Exit 0 clean, 1 findings, 2 unavailable input.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys
from types import MappingProxyType
from typing import Mapping

ROOT = Path(__file__).resolve().parent.parent
EXECUTION = "references/100-test-execution.md"
RESOURCES = "references/110-execution-resources.md"
CLASSIFICATION = "references/120-result-classification.md"

# Complete reviewed decisions, including conditions and exceptions. Whitespace
# and case are irrelevant; changing semantics requires independent review.
REQUIREMENTS = MappingProxyType({
    "body": (
        "For any direct or delegated validation run",
        "references/00-topic-map.md",
        "python3 scripts/check_execution_contracts.py",
        "`0` clean, `1` findings, `2` unavailable",
        "Either nonzero blocks the affected claim",
        "never treat `2` as a pass",
        "This maintainer check does not run on ordinary application tasks",
    ),
    "router": ("100-test-execution.md", "110-execution-resources.md", "120-result-classification.md"),
    "execution": (
        "Repository validation policy takes precedence",
        "Runtime orchestrators own role authority, observer independence, allocation and phase/review scheduling",
        "Scope tiers: how much of the suite runs, and when",
        "A result stays valid until something named invalidates it",
        "A failing tier is classified before it is repaired",
        "required gates, exact commands and scoped inputs, cwd, timeout, environment/resource limits, expected cases, declared case dependencies, aggregate-to-child coverage and eligible citations",
        "Record each command's machine-readable reporter when available and retain its output",
        "retain raw exit/output when none exists",
        "Record the tested content snapshot, relevant untracked inputs and tool versions",
        "Keep check inputs stable during the pass",
        "For a new or changed test command, or one with a recorded harness failure, confirm selection before citing its result",
        "run that as a separate selection check before the first execution",
        "otherwise compare the first run's selected cases with the recorded expected cases",
        "Preserve selected and executed counts, case identities and skip/setup reasons, including every covered child of an aggregate",
        "a valid collect-only result proves selection alone",
        "Non-test lint/type/build/render commands need no case selection check",
        "Inspect aggregate execution: a name proves no coverage",
        "inputs, environment, flags and required observer match demonstrably",
        "observer authority remains a caller constraint",
        "Count underlying checks once and run uncovered gates separately",
        "One failure never cancels independent remaining checks",
        "Record each command's exit/result and each unrun check's blocker",
        "A dependent case whose precondition failed is skipped with that precondition named",
        "A fail-fast aggregate proves only executed coverage",
        "use its supported keep-going mode or exact uncovered child commands while preserving failure exits",
        "Stop unsafe or contaminated cases and name them",
        "Combine the collection's failures verbatim, classify their causes first",
        "A clear owner or cheap fix does not bypass collection",
        "Only an obstruction blocking all or most remaining checks permits minimal early repair",
        "record the cause and blocked checks, repair only that obstruction, then resume the full collection, including previously blocked checks",
        "Review waits for checks required before it",
        "Acceptance waits for all required checks and retests",
        "Rerun failed or invalidated checks on the frozen repaired snapshot, including invalidated citations",
        "Run any remaining checks whose preconditions are now satisfied",
        "Cite valid passing evidence unless fresh proof is required",
        "Repeat the whole list only when all its evidence is invalidated or the governing gate requires a fresh whole-list run",
        "Collect new failures within the existing budget",
        "Preserve the original result, repair and retest separately",
        "Never weaken assertions, suppress findings, lower thresholds, widen tolerances, add assertion retries or alter fixtures to conceal failure",
        "Environment recovery changes require their own authority and evidence",
        "Unresolved required checks block acceptance",
        "is not reset by collection or a new agent",
    ),
    "doctrine": (
        "**Focused** | the smallest test/path/scenario distinguishing the subtask's changed behavior",
        "**Task acceptance** | bounded acceptance selectors combining that task's subtasks",
        "**Affected** | selectors of topics reachable from changed surfaces",
        "**Exhaustive** | the whole suite and only the race, end-to-end and higher-level proofs the claims require",
        "Labels never narrow an actual command's scope",
        "A clean integration is no exception",
        "integrate first and then run, or run again after integrating",
        "the tracked tree at the paths the check reads",
        "the tool, runner, and dependency versions",
        "the environment and service state the check depends on",
        "the flags, seed, configuration, and working directory it ran under",
        "cite the result with its original command and timestamp",
        "When one of them changes, say which one, and re-run every result downstream of it",
        "A failed, flaky, contaminated, timed-out or environment-blocked result cannot discharge a required check",
        "Reuse passing evidence only where its inputs, observer and freshness requirements still match",
        "covered inputs, environment, flags and required observer match demonstrably",
        "a documentation-only difference proves no equivalence",
        "A phase transition, new agent or compaction alone invalidates nothing",
        "A required exhaustive tier on the final candidate is always fresh",
        "every required check has valid evidence, including a fresh exhaustive tier on the final candidate when required",
        "Markdown/templates may be checker inputs",
        "A case failing never stops an independent case from running",
        "reported `SKIPPED` naming that precondition",
        "makes every later result over that state `CONTAMINATED`",
        "Classify first, then act",
        "Four classes stay separate",
        "A tier is never made to pass by deleting an assertion, widening a tolerance, adding a retry, skipping a case, or lowering a threshold",
    ),
    "resources": (
        "OS process priority (`BelowNormal` by default, which is `nice 10`)",
        "Optional CPU affinity/count",
        "Tool/runtime concurrency (`GOMAXPROCS`, package parallelism, test workers, browser workers)",
        "Lower priority does not limit parallelism. Configure both",
        "The runner returns the child exit code and emits stdout/stderr",
        "Use `Idle` only for explicitly background-grade benchmark/fuzz/full-profile work",
        "`-p` controls package/build concurrency",
        "`-parallel` controls tests using `t.Parallel` inside a test binary",
        "`GOMAXPROCS` controls runtime CPU parallelism. They are not interchangeable",
        "Test-result caching is separate from build caching",
        "including affected-tier checks against external dependency state",
        "retain the build cache",
        "`./...` is exhaustive-only",
        "Use repository scripts exactly",
        "Do not run package installation merely because a command is missing",
        "do not introduce ParaTest or process isolation during verification",
        "Preserve explicit `--browser chromium`",
        "Preserve configured user-data/profile paths",
        "Do not kill unrelated services, dev servers, containers, or processes",
        "Do not start duplicate services when a reusable declared service already exists",
        'bash "<TESTING_SKILL_ROOT>/scripts/run-low-priority.sh"',
        "Limit browser workers through the repository-supported mechanism only",
        "Do not kill or reuse another worktree's server without explicit ownership",
        "Declare one allowed artifact directory in the execution record",
        "Write run artifacts only there plus unavoidable tool temp directories allowed by the sandbox",
        "Unexpected tracked file changes contaminate the run",
        "Run only one CPU-heavy verification or profiling command at a time per host in this workflow",
        "A gate's supported internal parallel mode counts as that one command",
        "Priority alone is not a CPU limit",
        "including container/VM/cgroup quotas, affinity restrictions and reserved capacity",
        "an unavailable capacity observation is unknown, never unlimited",
        "allocate explicit CPU budgets across every concurrent container and host worker",
        "Their simultaneous allocations must fit effective host capacity with the declared reserve",
        "Set container `--cpus` limits below the host logical CPU count and within that effective budget",
        "align each gate's worker/package/runtime counts with its container allocation",
        "Record dependency-container allocations as well as the test-container allocation",
        "Defer work when a safe concurrent budget cannot be established",
        "read-only source mount, complete copy into the container filesystem (including required Git metadata)",
        "The container CPU limit replaces the host low-priority wrapper for that run",
        "make one host fallback under the low-priority wrapper when repository policy and authority permit",
        "never call it container proof",
        "Under Codex, invoke /alaa-codex-runtime-ops for Docker-access permission failures within its declared runtime scope before fallback",
        "Installation, pulling an undeclared image, permission changes or starting an unowned service require separate authority",
        "Never substitute another image",
        "Measure performance only for a named question with a comparable baseline and a declared budget",
        "A before/after performance claim requires an idle host: no unrelated CPU-heavy work and no overlapping validation",
        "Verify and record host load before and during samples",
        "discard or label contaminated samples rather than presenting them as improvement",
        "Loaded or slower-host runs remain valid flake diagnosis under `50-flake.md`; they do not support a speed comparison",
        "Keep CPU allocation/affinity, worker counts, workload/case selection, dependency state, tool versions, image, setup and cache state identical between candidates",
        "Declare warmup, warm/cold cache policy, sample count and interleaved before/after order before measurement",
        "do not measure every baseline first and every candidate second",
        "Record timer identity, timer resolution, raw samples, units, spread/dispersion and deviations/outliers with their causes",
        "Retain machine-readable timing output when the tool supports it",
        "leaves the performance claim unverified",
        "The canonical implementation is `scripts/run-low-priority.sh` in this skill",
        "preserve arguments, child stdout/stderr and exit status from any cwd, including paths with spaces",
        "it never triggers installation or falls back to copied logic",
        "The runner uses Bash and `nice`, with optional `taskset`",
    ),
    "classification": (
        "Use one primary classification per command and record secondary factors separately",
        "## PASS", "## PRODUCT-FAILURE", "## TEST-INFRA-FAILURE", "## ENVIRONMENT-BLOCKED",
        "## TIMEOUT", "## FLAKY", "## CONTAMINATED", "## SKIPPED",
        "including whole-suite discovery and each covered child of an aggregate",
        "whose selection is empty or differs from the expected cases recorded for it is `TEST-INFRA-FAILURE`, never `PASS`",
        "inside a container run, an incomplete copy or mount is instead `ENVIRONMENT-BLOCKED`",
        "selected cases but executed none takes the class its skip reasons name",
        "A list or collect selection check executes no case by design: it is `PASS` when it lists exactly the expected cases",
        "A scoped lint, type-check or build command whose scope matches no file is `TEST-INFRA-FAILURE`",
        "before changing code", "combined repair record under `100-test-execution.md`",
        "Do not disguise this as a product failure or install/change the environment without authority",
        "Preserve partial logs and process/resource evidence",
        "an unavailable diagnosis remains unresolved",
        "including fail-then-pass. Never promote it to PASS",
        "Do not revert automatically",
        "Unexecuted checks are never implied passes",
        "The command line was parsed by a shell other than the intended one",
        "A container runtime is not running, an image is absent, a mount failed, or the daemon refused the socket",
        "A file, directory, port, or device was refused, locked, or held open by another process",
        "A required executable, service, credential, browser, or platform capability is absent",
        "A build, dependency, module, or test cache served an artifact from before the change",
        "The harness, fixture, factory, seed, or generated setup broke independently of the behaviour under test",
        "Never repair the product in response to any row above",
        "Clearing a cache, installing a tool, changing a permission, or starting a service is a declared and reported action, never a silent retry step",
        "Identify the first causal error, not the last stack trace",
        "Confirm command/cwd/environment/resource limits",
        "Compare initial/final git status and concurrent changes",
        "if one authorized rerun exists",
        "Inspect the owning code/test/config path",
        "Classify owner: product, test infrastructure, environment, or unresolved ownership",
        "Route the smallest grounded next action",
        "recurring with the same first causal error earns no further full run",
        "within the active retry budget while safe independent checks continue",
    ),
    "flake": (
        "classified as one of the two before any other action",
        "A blanket retry is never the response to either",
        "A test classified as a product defect is not quarantined at all",
        "A retry keyed to a named infrastructure failure class, which never retries an assertion failure",
    ),
    "economy": ("A failure alone never justifies deleting a test", "## Existing tests on a touched topic"),
    "workspace": (
        "Continue in the same checkout and preserve its diff",
        "Do not create a branch or worktree automatically",
        "Allow one active writer per file, generated output or shared runtime resource, not one writer per worktree",
        "separate files permit concurrent writers only when their generated outputs and runtime resources are also disjoint",
        "A task claim is no file or resource lock",
        "Verify the prior writer process and every descendant have stopped",
        "A returned agent turn, interrupted session or closed terminal alone proves no process termination",
        "unknown descendant liveness is unresolved ownership",
        "Observe the scoped files and generated/shared resources are stable after those processes stop",
        "Preserve surviving edits and compare them with the existing progress journal, bound issue and checkpoint",
        "Create no journal or locking system for this check",
        "Only then assign the remaining overlapping writes to the replacement",
        "do not replay it or reset the diff",
        "If liveness, stability or ownership remains ambiguous, block only overlapping writes and shared-resource use",
        "Continue independently owned disjoint work",
        "Compaction does not transfer a living writer's ownership",
        "recover the same actor and reconcile its active process before continuing",
        EXECUTION, CLASSIFICATION,
    ),
    "continuity": ("Shared-file ownership and stopped-writer recovery", "compaction preserves living ownership"),
})

# Only complete normative clauses identify duplicate policy. Requirement
# fragments, topic names, status headings and citations remain legal pointers.
NORMATIVE_DUPLICATES = MappingProxyType({
    "execution": (
        "Runtime orchestrators own role authority, observer independence, allocation and phase/review scheduling",
        "required gates, exact commands and scoped inputs, cwd, timeout, environment/resource limits, expected cases, declared case dependencies, aggregate-to-child coverage and eligible citations",
        "Record each command's machine-readable reporter when available and retain its output",
        "Record the tested content snapshot, relevant untracked inputs and tool versions",
        "Keep check inputs stable during the pass",
        "For a new or changed test command, or one with a recorded harness failure, confirm selection before citing its result",
        "otherwise compare the first run's selected cases with the recorded expected cases",
        "Preserve selected and executed counts, case identities and skip/setup reasons, including every covered child of an aggregate",
        "Non-test lint/type/build/render commands need no case selection check",
        "Inspect aggregate execution: a name proves no coverage",
        "Count underlying checks once and run uncovered gates separately",
        "One failure never cancels independent remaining checks",
        "Record each command's exit/result and each unrun check's blocker",
        "A dependent case whose precondition failed is skipped with that precondition named",
        "use its supported keep-going mode or exact uncovered child commands while preserving failure exits",
        "A clear owner or cheap fix does not bypass collection",
        "Only an obstruction blocking all or most remaining checks permits minimal early repair",
        "record the cause and blocked checks, repair only that obstruction, then resume the full collection, including previously blocked checks",
        "Review waits for checks required before it",
        "Acceptance waits for all required checks and retests",
        "Rerun failed or invalidated checks on the frozen repaired snapshot, including invalidated citations",
        "Run any remaining checks whose preconditions are now satisfied",
        "Cite valid passing evidence unless fresh proof is required",
        "Repeat the whole list only when all its evidence is invalidated or the governing gate requires a fresh whole-list run",
        "Collect new failures within the existing budget",
        "Preserve the original result, repair and retest separately",
        "Never weaken assertions, suppress findings, lower thresholds, widen tolerances, add assertion retries or alter fixtures to conceal failure",
        "Environment recovery changes require their own authority and evidence",
        "Unresolved required checks block acceptance",
    ),
    "resources": (
        "Tool/runtime concurrency (`GOMAXPROCS`, package parallelism, test workers, browser workers)",
        "Lower priority does not limit parallelism. Configure both",
        "Use `Idle` only for explicitly background-grade benchmark/fuzz/full-profile work",
        "Use repository scripts exactly",
        "Do not run package installation merely because a command is missing",
        "Preserve explicit `--browser chromium`",
        "Preserve configured user-data/profile paths",
        "Do not kill unrelated services, dev servers, containers, or processes",
        "Do not start duplicate services when a reusable declared service already exists",
        "Limit browser workers through the repository-supported mechanism only",
        "Do not kill or reuse another worktree's server without explicit ownership",
        "Declare one allowed artifact directory in the execution record",
        "Write run artifacts only there plus unavoidable tool temp directories allowed by the sandbox",
        "Unexpected tracked file changes contaminate the run",
        "Run only one CPU-heavy verification or profiling command at a time per host in this workflow",
        "A gate's supported internal parallel mode counts as that one command",
        "Priority alone is not a CPU limit",
        "including container/VM/cgroup quotas, affinity restrictions and reserved capacity",
        "Their simultaneous allocations must fit effective host capacity with the declared reserve",
        "Set container `--cpus` limits below the host logical CPU count and within that effective budget",
        "Record dependency-container allocations as well as the test-container allocation",
        "Defer work when a safe concurrent budget cannot be established",
        "read-only source mount, complete copy into the container filesystem (including required Git metadata)",
        "The container CPU limit replaces the host low-priority wrapper for that run",
        "make one host fallback under the low-priority wrapper when repository policy and authority permit",
        "Under Codex, invoke /alaa-codex-runtime-ops for Docker-access permission failures within its declared runtime scope before fallback",
        "Installation, pulling an undeclared image, permission changes or starting an unowned service require separate authority",
        "Never substitute another image",
        "A before/after performance claim requires an idle host: no unrelated CPU-heavy work and no overlapping validation",
        "Verify and record host load before and during samples",
        "discard or label contaminated samples rather than presenting them as improvement",
        "Loaded or slower-host runs remain valid flake diagnosis under `50-flake.md`; they do not support a speed comparison",
        "Keep CPU allocation/affinity, worker counts, workload/case selection, dependency state, tool versions, image, setup and cache state identical between candidates",
        "Declare warmup, warm/cold cache policy, sample count and interleaved before/after order before measurement",
        "Record timer identity, timer resolution, raw samples, units, spread/dispersion and deviations/outliers with their causes",
        "Retain machine-readable timing output when the tool supports it",
        "The canonical implementation is `scripts/run-low-priority.sh` in this skill",
        "preserve arguments, child stdout/stderr and exit status from any cwd, including paths with spaces",
        "The runner uses Bash and `nice`, with optional `taskset`",
    ),
    "classification": (
        "Use one primary classification per command and record secondary factors separately",
        "whose selection is empty or differs from the expected cases recorded for it is `TEST-INFRA-FAILURE`, never `PASS`",
        "inside a container run, an incomplete copy or mount is instead `ENVIRONMENT-BLOCKED`",
        "A list or collect selection check executes no case by design: it is `PASS` when it lists exactly the expected cases",
        "A scoped lint, type-check or build command whose scope matches no file is `TEST-INFRA-FAILURE`",
        "Do not disguise this as a product failure or install/change the environment without authority",
        "Preserve partial logs and process/resource evidence",
        "Do not revert automatically",
        "Unexecuted checks are never implied passes",
        "A container runtime is not running, an image is absent, a mount failed, or the daemon refused the socket",
        "A file, directory, port, or device was refused, locked, or held open by another process",
        "A required executable, service, credential, browser, or platform capability is absent",
        "A build, dependency, module, or test cache served an artifact from before the change",
        "The harness, fixture, factory, seed, or generated setup broke independently of the behaviour under test",
        "Never repair the product in response to any row above",
        "Clearing a cache, installing a tool, changing a permission, or starting a service is a declared and reported action, never a silent retry step",
        "Identify the first causal error, not the last stack trace",
        "Confirm command/cwd/environment/resource limits",
        "Compare initial/final git status and concurrent changes",
        "Inspect the owning code/test/config path",
        "Classify owner: product, test infrastructure, environment, or unresolved ownership",
        "Route the smallest grounded next action",
    ),
    "doctrine": (
        "**Focused** | the smallest test/path/scenario distinguishing the subtask's changed behavior",
        "**Task acceptance** | bounded acceptance selectors combining that task's subtasks",
        "**Exhaustive** | the whole suite and only the race, end-to-end and higher-level proofs the claims require",
        "Labels never narrow an actual command's scope",
        "When one of them changes, say which one, and re-run every result downstream of it",
        "A failed, flaky, contaminated, timed-out or environment-blocked result cannot discharge a required check",
        "a check outside the list runs only when the repair changes shared behaviour or proves a new reachable surface",
        "A phase transition, new agent or compaction alone invalidates nothing",
        "A case failing never stops an independent case from running",
        "Classify first, then act",
        "A tier is never made to pass by deleting an assertion, widening a tolerance, adding a retry, skipping a case, or lowering a threshold",
    ),
})

# Frozen preservation baseline over every NORMATIVE_DUPLICATES clause.
EXPECTED_NORMATIVE_INVENTORY_SHA256 = "f08d218a8dfd09fdf073ac68f72d08aa2efb6150552c18ca6175db020215da24"

# These are contradictory positive instructions, not mere absent keywords.
# Append them with all required clauses intact to prove contradiction detection.
CONTRADICTIONS = (
    "Stop collection after the first failed command",
    "Start one repair lane for each failed test",
    "Any failed check permits an early repair",
    "Review immediately after the minimal early repair",
    "A fail-fast aggregate proves all required checks ran",
    "Skip previously blocked checks after early repair",
    "Collection resets the retry budget",
    "rerun the whole recorded check list on the frozen repaired snapshot, including checks previously discharged by citation",
    "the exhaustive tier has run once on the final candidate tree",
    "A command whose selector executed zero cases",
    "invoke /alaa-codex-runtime-ops for a Docker named-pipe permission failure before fallback",
    "Priority alone caps CPU usage",
    "Only the test container needs a CPU budget",
    "Measure all baseline samples before all candidate samples",
    "A selected test command that executed zero cases is PASS",
    "A pass after a failure is a clean PASS",
    "Compaction transfers live writer ownership",
    "Unknown ownership blocks all disjoint work",
    "Create a new worktree automatically on resume",
)


def pointer_clause(clause: str) -> bool:
    return re.fullmatch(r"[\w./-]+\.(?:md|py)", clause) is not None


def contains(clause: str, normalized: str) -> bool:
    clause = " ".join(clause.split()).casefold()
    if pointer_clause(clause):
        # A path prefix is not a valid pointer: x.md.missing and missing/x.md
        # must fail even though the old filename survives as a substring.
        return re.search(r"(?<![\w./-])" + re.escape(clause) + r"(?![\w./-])", normalized) is not None
    return clause in normalized


def source_paths(root: Path = ROOT) -> dict[str, Path]:
    paths = {
        "body": root / "SKILL.md", "doctrine": root / "SKILL.md", "router": root / "references/00-topic-map.md",
        "execution": root / EXECUTION, "resources": root / RESOURCES,
        "classification": root / CLASSIFICATION, "flake": root / "references/50-flake.md",
        "economy": root / "references/90-test-economy.md",
        "workspace": root.parent / "alaa-workflow/references/workspace-and-integration.md",
        "continuity": root.parent / "alaa-workflow/references/context-continuity.md",
    }
    workflow = root.parent / "alaa-workflow"
    for name, relative in (
        ("workflow_body", "SKILL.md"),
        ("planning", "references/artifact-lifecycle.md"),
        ("plan_template", "assets/plan-template.md"),
        ("phase_template", "assets/phase-template.md"),
        ("prompt_routing", "references/phase-prompts.md"),
        ("prompt_template", "assets/phase-prompts-template.md"),
    ):
        paths[name] = workflow / relative
    for runtime in ("cc", "codex"):
        other = root.parent / f"alaa-{runtime}-orchestrator"
        for name, relative in (("body", "SKILL.md"), ("gates", "references/verification-and-gates.md"),
                               ("resources", "references/resource-policy.md"),
                               ("taxonomy", "references/failure-taxonomy.md"),
                               ("routing", "references/routing-matrix.md"),
                               ("verifier", "references/delegation-prompts/40-verification.md"),
                               ("repair", "references/delegation-prompts/30-implementation.md")):
            paths[f"{runtime}_{name}"] = other / relative
    return paths


def load_sources(root: Path = ROOT) -> Mapping[str, str]:
    return MappingProxyType({name: path.read_text(encoding="utf-8")
                             for name, path in source_paths(root).items()})


def requirements() -> dict[str, tuple[str, ...]]:
    result = dict(REQUIREMENTS)
    for runtime in ("cc", "codex"):
        for name in ("body", "gates"):
            result[f"{runtime}_{name}"] = ("/alaa-testing-strategy", EXECUTION, RESOURCES, CLASSIFICATION)
        result[f"{runtime}_resources"] = ("/alaa-testing-strategy", RESOURCES)
        result[f"{runtime}_taxonomy"] = ("/alaa-testing-strategy", CLASSIFICATION)
    return result


def normative_inventory_failures(inventory: Mapping[str, tuple[str, ...]]) -> list[str]:
    # Sorting and normalization ignore presentation, while preserving every
    # owner/clause entry. No runtime length heuristic chooses protected rules.
    entries = sorted(f"{owner}\t{' '.join(clause.split()).casefold()}"
                     for owner, clauses in inventory.items() for clause in clauses)
    digest = hashlib.sha256(("\n".join(entries) + "\n").encode("utf-8")).hexdigest()
    if digest != EXPECTED_NORMATIVE_INVENTORY_SHA256:
        return ["normative duplicate inventory differs from frozen preservation baseline: " + digest]
    return []


def failures(sources: Mapping[str, str]) -> list[str]:
    errors = normative_inventory_failures(NORMATIVE_DUPLICATES)
    normalized = {name: " ".join(text.split()).casefold() for name, text in sources.items()}
    for name, clauses in requirements().items():
        for clause in clauses:
            if not contains(clause, normalized[name]):
                errors.append(f"{name}: missing execution contract: {clause}")
    for name, text in sources.items():
        for clause in CONTRADICTIONS:
            if " ".join(clause.split()).casefold() in normalized[name]:
                errors.append(f"{name}: contradictory execution contract: {clause}")
        if name.startswith(("cc_", "codex_")):
            # Only canonical owners state generic policy. A pointer cannot mask
            # a surviving, conflicting or duplicate old paragraph.
            for owner, clauses in NORMATIVE_DUPLICATES.items():
                for clause in clauses:
                    if " ".join(clause.split()).casefold() in normalized[name]:
                        errors.append(f"{name}: duplicate {owner} policy: {clause}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    try:
        sources = load_sources()
        errors = failures(sources)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("EXECUTION CONTRACTS OK: canonical ownership, standalone/runtime routes and recovery")
        return 0
    except (OSError, UnicodeError, KeyError, ValueError) as exc:
        print(f"execution contract check unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

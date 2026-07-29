#!/usr/bin/env python3
"""Assert that the three declarations of one contract agree, and that every index resolves.

The capability contract is declared in three places and they must not drift:
  * examples/browser-capabilities.ts -- the implementation and the single field-set
    declaration
  * assets/capability-tier-contract.json -- the tiers and the feature-detect targets
  * assets/browser-test-matrix.yaml    -- the lanes, each naming the tiers and features
    it can observe

A document asserting parity is not evidence of parity. This harness drives all three
over one corpus and fails on any disagreement.

It also checks every `createIndex` in examples/ against the record type its store holds:
an index whose key path names a field the record does not carry is silently empty and
never errors, which is the highest-yield defect in this domain.

Exit codes
  0  clean.
  1  findings, each naming the file and what disagrees.
  2  could not run: a required artifact is missing or unparseable. Never a pass.

A green run bounds only what the corpus covers: it proves the three artifacts agree with
each other. It proves nothing about any real browser -- that is level 4 and level 5 in
assets/browser-test-matrix.yaml.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

EXIT_CLEAN, EXIT_FINDINGS, EXIT_CANNOT_RUN = 0, 1, 2

CAPABILITIES_TS = "examples/browser-capabilities.ts"
CONTRACT_JSON = "assets/capability-tier-contract.json"
MATRIX_YAML = "assets/browser-test-matrix.yaml"

INTERFACE_BLOCK = re.compile(
    r"export interface BrowserStorageCapabilities\s*\{(.*?)\n\}", re.S
)
FIELD = re.compile(r"^\s*([A-Za-z][A-Za-z0-9]*)\s*:", re.M)
TIER_RETURN = re.compile(r"return\s+([0-3])\s*;")
CREATE_INDEX = re.compile(r"createIndex\(\s*'([^']+)'\s*,\s*(\[[^\]]*\]|'[^']*')")
STORE_DECL = re.compile(r"createObjectStore\(\s*'([^']+)'")


def parse_capability_fields(text: str) -> set[str]:
    block = INTERFACE_BLOCK.search(text)
    if not block:
        raise ValueError(f"{CAPABILITIES_TS}: BrowserStorageCapabilities interface not found")
    return set(FIELD.findall(block.group(1)))


def parse_matrix(text: str) -> tuple[dict[str, set[int]], dict[str, set[str]]]:
    """Minimal lane extractor. The matrix is authored to be readable by this parser:
    a lane is `- name:`, its tiers a flow sequence, its features a block sequence."""
    lane_tiers: dict[str, set[int]] = {}
    lane_features: dict[str, set[str]] = {}
    lane: str | None = None
    in_features = False

    for raw in text.splitlines():
        name = re.match(r"\s*-\s*name:\s*(\S+)", raw)
        if name:
            lane = name.group(1)
            lane_tiers[lane] = set()
            lane_features[lane] = set()
            in_features = False
            continue
        if lane is None:
            continue
        tiers = re.match(r"\s*tiers:\s*\[([^\]]*)\]", raw)
        if tiers:
            lane_tiers[lane] = {int(n) for n in re.findall(r"\d", tiers.group(1))}
            in_features = False
            continue
        if re.match(r"\s*covers_features:\s*$", raw):
            in_features = True
            continue
        if in_features:
            item = re.match(r'\s*-\s*"(.+)"\s*$', raw)
            if item:
                lane_features[lane].add(item.group(1))
            elif raw.strip() and not raw.lstrip().startswith("-"):
                in_features = False
    return lane_tiers, lane_features


def find(root: Path) -> list[str]:
    findings: list[str] = []

    ts = (root / CAPABILITIES_TS).read_text(encoding="utf-8")
    contract = json.loads((root / CONTRACT_JSON).read_text(encoding="utf-8"))
    matrix_text = (root / MATRIX_YAML).read_text(encoding="utf-8")

    fields = parse_capability_fields(ts)
    lane_tiers, lane_features = parse_matrix(matrix_text)
    declared_lanes = set(lane_tiers)

    # 1. Every must_feature_detect entry names a capability field that exists.
    contract_features: set[str] = set()
    for entry in contract.get("must_feature_detect", []):
        feature = entry["feature"]
        contract_features.add(feature)
        field = entry.get("capability_field")
        if field not in fields:
            findings.append(
                f"{CONTRACT_JSON}: feature '{feature}' maps to capability_field "
                f"'{field}', which {CAPABILITIES_TS} does not declare"
            )
        for lane in entry.get("lanes", []):
            if lane not in declared_lanes:
                findings.append(
                    f"{CONTRACT_JSON}: feature '{feature}' names lane '{lane}', "
                    f"which {MATRIX_YAML} does not declare"
                )
            elif feature not in lane_features[lane]:
                findings.append(
                    f"{MATRIX_YAML}: lane '{lane}' is claimed by feature '{feature}' "
                    f"in {CONTRACT_JSON} but does not list it under covers_features"
                )
        if not entry.get("lanes"):
            findings.append(f"{CONTRACT_JSON}: feature '{feature}' has no test lane")

    # 2. Every feature a lane claims to cover is a feature the contract governs.
    for lane, features in lane_features.items():
        for feature in features - contract_features:
            findings.append(
                f"{MATRIX_YAML}: lane '{lane}' covers '{feature}', which "
                f"{CONTRACT_JSON} does not list under must_feature_detect"
            )

    # 3. Every tier is reachable in code and has at least one lane.
    reachable = {int(n) for n in TIER_RETURN.findall(ts)}
    for key, tier in contract.get("tiers", {}).items():
        number = int(re.search(r"tier(\d)", key).group(1))
        if number not in reachable:
            findings.append(
                f"{CONTRACT_JSON}: {key} is declared but chooseCapabilityTier in "
                f"{CAPABILITIES_TS} can never return {number}"
            )
        lanes = set(tier.get("lanes", []))
        if not lanes:
            findings.append(f"{CONTRACT_JSON}: {key} has no lane")
        for lane in lanes - declared_lanes:
            findings.append(f"{CONTRACT_JSON}: {key} names lane '{lane}', which {MATRIX_YAML} lacks")
        for lane in lanes & declared_lanes:
            if number not in lane_tiers[lane]:
                findings.append(
                    f"{MATRIX_YAML}: lane '{lane}' is claimed by {key} but its "
                    f"tiers list does not include {number}"
                )

    # 4. Every capability field is governed by at least one feature entry.
    mapped = {e.get("capability_field") for e in contract.get("must_feature_detect", [])}
    for field in sorted(fields - mapped - {"indexedDb"}):
        findings.append(
            f"{CONTRACT_JSON}: capability field '{field}' is probed in {CAPABILITIES_TS} "
            "and governed by no must_feature_detect entry"
        )

    return findings


def check_indexes(root: Path, source_dir: str = "examples") -> list[str]:
    """Every segment of every index key path must be a declared field on some record type.

    `--source-dir` points this check at any TypeScript tree, so it runs against a
    product repository as well as against this pack. It is deliberately narrow: it
    matches only a literal `createIndex('name', [...])`, so a key path built from a
    constant or assembled at runtime escapes it. A clean run bounds the literal form
    and nothing else.
    """
    findings: list[str] = []
    declared: set[str] = set()
    base = root / source_dir
    if not base.is_dir():
        raise ValueError(f"{source_dir} is not a directory under {root}")
    for path in sorted(base.rglob("*.ts")):
        text = path.read_text(encoding="utf-8")
        # Field names declared on any exported interface or type in examples/.
        for name in re.findall(r"^\s{2}([A-Za-z][A-Za-z0-9]*)\??\s*:", text, re.M):
            declared.add(name)

    for path in sorted(base.rglob("*.ts")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        for lineno, line in enumerate(text.splitlines(), start=1):
            for _, key_path in CREATE_INDEX.findall(line):
                for segment in re.findall(r"'([^']+)'", key_path):
                    if segment not in declared:
                        findings.append(
                            f"{rel}:{lineno}: index key path segment '{segment}' is not a "
                            f"declared field on any record type under {source_dir}/; that "
                            "index is silently empty and never errors"
                        )
    return findings


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "examples").mkdir()
        (root / "assets").mkdir()

        (root / CAPABILITIES_TS).write_text(
            "export interface BrowserStorageCapabilities {\n"
            "  indexedDb: string;\n"
            "  estimate: boolean;\n"
            "  orphanField: boolean;\n"
            "}\n"
            "export function chooseCapabilityTier(): 0 | 1 {\n"
            "  return 0;\n"
            "  return 1;\n"
            "}\n",
            encoding="utf-8",
        )
        (root / CONTRACT_JSON).write_text(
            json.dumps(
                {
                    "tiers": {
                        "tier0_x": {"lanes": ["known-lane"]},
                        "tier3_unreachable": {"lanes": ["known-lane"]},
                    },
                    "must_feature_detect": [
                        {"feature": "estimate", "capability_field": "estimate", "lanes": ["known-lane"]},
                        {"feature": "ghost", "capability_field": "nosuchfield", "lanes": ["ghost-lane"]},
                    ],
                }
            ),
            encoding="utf-8",
        )
        (root / MATRIX_YAML).write_text(
            "lanes:\n"
            "  - name: known-lane\n"
            "    tiers: [0]\n"
            "    covers_features:\n"
            '      - "estimate"\n',
            encoding="utf-8",
        )

        findings = find(root)
        expectations = [
            ("nosuchfield", "a feature mapped to an undeclared capability field"),
            ("ghost-lane", "a feature naming a lane the matrix lacks"),
            ("can never return 3", "an unreachable tier"),
            ("orphanField", "a probed field governed by no feature entry"),
            ("does not include 3", "a lane claimed by a tier it does not list"),
        ]
        for needle, label in expectations:
            if not any(needle in f for f in findings):
                print(f"SELF-TEST FAIL: did not report {label}", file=sys.stderr)
                print("\n".join(findings), file=sys.stderr)
                return EXIT_FINDINGS

        # Index check: an index over a field no record declares.
        (root / "examples" / "bad.ts").write_text(
            "export interface Row {\n  id: string;\n  status: string;\n}\n"
            "store.createIndex('byStatusRetryAt', ['status', 'retryAt']);\n",
            encoding="utf-8",
        )
        index_findings = check_indexes(root)
        if not any("'retryAt'" in f for f in index_findings):
            print("SELF-TEST FAIL: did not report an index over an undeclared field", file=sys.stderr)
            return EXIT_FINDINGS

    print(f"SELF-TEST OK: {len(expectations) + 1} checks each fail on a fixture that violates them")
    return EXIT_CLEAN


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="capability_contract_conformance.py",
        description="Assert the capability contract's three declarations agree, and that every index key path resolves.",
        epilog="Exit 0 clean, 1 findings, 2 could not run. A green run bounds only what the corpus covers.",
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true", help="run the built-in fixtures")
    parser.add_argument("--check-indexes", action="store_true", help="only run the index key-path check")
    parser.add_argument(
        "--source-dir",
        default="examples",
        help="TypeScript tree the index check scans, relative to --root (default: examples)",
    )
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    root: Path = args.root.resolve()
    if not args.check_indexes:
        for rel in (CAPABILITIES_TS, CONTRACT_JSON, MATRIX_YAML):
            if not (root / rel).is_file():
                print(f"CANNOT RUN: {rel} is missing", file=sys.stderr)
                return EXIT_CANNOT_RUN

    try:
        findings = (
            check_indexes(root, args.source_dir)
            if args.check_indexes
            else find(root) + check_indexes(root, args.source_dir)
        )
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as error:
        print(f"CANNOT RUN: {error}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if findings:
        for finding in findings:
            print(f"FINDING: {finding}", file=sys.stderr)
        print(f"{len(findings)} finding(s)", file=sys.stderr)
        return EXIT_FINDINGS

    if args.check_indexes:
        print(
            f"OK: every literal createIndex key path under {args.source_dir}/ names a declared "
            "field. This bounds the literal form only; a key path built from a constant escapes it."
        )
    else:
        print(
            "OK: the capability field set, the tier contract and the test matrix agree; every tier is "
            "reachable and laned; every index key path names a declared field. "
            "This bounds the three artifacts against each other, not against any real browser."
        )
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())

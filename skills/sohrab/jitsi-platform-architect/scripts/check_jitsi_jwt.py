#!/usr/bin/env python3
"""Assert the Jitsi join-token claim contract and the room-name rules.

The room-name rules are capacity and predictability checks, not an entropy
measurement. Alphabet and length prove only what a name COULD carry if it were
drawn uniformly at random; no check on a single value can prove that the
generator actually supplied that unpredictability. The contract remains a
CSPRNG mapped uniformly onto the room alphabet, and the assurance for it is
generator-level design evidence, never this script's output.

This checks the shape of a token, not its authenticity. It never verifies a
signature, and it must not be used as an admission control. Signature
verification of a platform access token belongs to the Ala gateway; signature
verification of a Jitsi join token belongs to the Prosody verifier inside the
Jitsi deployment. Both hold key material this script deliberately does not.
What this script owns is the claim-shape breach class: a wildcard room, an
over-long lifetime, a shared signing key, a top-level moderator claim, or a
guessable room name will each pass a signature check and still open a
classroom to a stranger.

Standard library only, so it runs from a fresh checkout with no install step.

Run `--self-test` after changing this file. Every rule below has a fixture.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import contextlib
import io
import json
import math
import re
import sys
from pathlib import Path

# Lowercase Crockford Base32: the digits plus the lowercase letters, with i, l,
# o and u removed so that no rendering is confusable with a digit.
CROCKFORD_LOWER = "0123456789abcdefghjkmnpqrstvwxyz"

DEFAULT_PROFILE = {
    "allowed_algs": ["RS256"],
    "max_lifetime_seconds": 120,
    "platform_access_token_kids": [],
    "room_min_entropy_bits": 128,
    "room_alphabet": CROCKFORD_LOWER,
}

# Claims that carry privilege. None of them belongs at the top level of the
# token: the verifier is configured to read privilege out of `context`, so a
# top-level copy is read by nothing and denies nobody.
PRIVILEGE_CLAIMS = ("role", "roles", "moderator", "is_moderator", "affiliation", "isModerator")

# Substrings that betray a room name derived from something a stranger can
# guess or enumerate. Kept as whole words rather than fragments to hold the
# false-positive rate down; see the note in the epilog.
MEANINGFUL_TOKENS = (
    "class", "course", "room", "lesson", "teacher", "student", "session",
    "meeting", "tenant", "school", "grade", "term", "math", "exam", "period",
    "lecture", "webinar", "standup", "daily",
)

DATE_PATTERNS = (
    re.compile(r"^(?:19|20)\d{2}"),
    re.compile(r"(?:19|20)\d{2}$"),
    re.compile(r"^\d{8}"),
    re.compile(r"\d{8}$"),
    re.compile(r"\d{4}-\d{2}-\d{2}"),
)


class BadInput(Exception):
    """The input was not a token, not a room name, or not a usable profile."""


def b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    try:
        return base64.urlsafe_b64decode(segment + padding)
    except (binascii.Error, ValueError) as exc:
        raise BadInput(f"segment is not base64url: {exc}") from exc


def decode_json_segment(segment: str, label: str) -> dict:
    raw = b64url_decode(segment)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BadInput(f"{label} is not JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise BadInput(f"{label} is not a JSON object")
    return value


def split_compact_jwt(token: str) -> tuple[str, str]:
    token = token.strip()
    if not token:
        raise BadInput("token is empty")
    parts = token.split(".")
    if len(parts) == 5:
        raise BadInput("token has five segments: this is an encrypted JWE and its claims cannot be inspected")
    if len(parts) != 3:
        raise BadInput(f"token has {len(parts)} dot-separated segments; a compact JWS has 3")
    if not parts[0] or not parts[1]:
        raise BadInput("token has an empty header or payload segment")
    return parts[0], parts[1]


def load_profile(path: str | None) -> dict:
    profile = dict(DEFAULT_PROFILE)
    if path is None:
        return profile
    file_path = Path(path)
    if not file_path.is_file():
        raise BadInput(f"profile is not a readable regular file: {path}")
    try:
        loaded = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BadInput(f"profile is not readable JSON: {exc}") from exc
    if not isinstance(loaded, dict):
        raise BadInput("profile must be a JSON object")
    profile.update(loaded)
    return profile


def smallest_period(name: str) -> int:
    """The length of the shortest pattern whose repetition writes the name.

    Computed with the Knuth-Morris-Pratt border array, so `abababa` has period
    2 even though 7 is not a multiple of 2. A uniformly generated name has a
    period equal to its own length except with negligible probability, so a
    short period is decisive evidence against uniform generation.
    """
    if not name:
        return 0
    border = [0] * len(name)
    k = 0
    for i in range(1, len(name)):
        while k and name[i] != name[k]:
            k = border[k - 1]
        if name[i] == name[k]:
            k += 1
        border[i] = k
    return len(name) - border[-1]


def required_room_length(profile: dict) -> int:
    alphabet = profile.get("room_alphabet") or CROCKFORD_LOWER
    bits = profile.get("room_min_entropy_bits", 128)
    if not isinstance(bits, int) or bits <= 0:
        raise BadInput("room_min_entropy_bits must be a positive integer")
    if len(alphabet) < 2:
        raise BadInput("room_alphabet must contain at least two characters")
    return math.ceil(bits / math.log2(len(alphabet)))


def check_room_name(name, profile: dict) -> list[tuple[str, str]]:
    """Return (code, message) for every room-name rule the name breaks."""
    findings: list[tuple[str, str]] = []
    if not isinstance(name, str):
        return [("ROOM_NAME_NOT_STRING", "room name is not a string")]
    if name == "":
        return [("ROOM_NAME_EMPTY", "room name is empty")]
    if "*" in name:
        findings.append(("ROOM_NAME_WILDCARD", "room name contains a wildcard"))

    if "-" in name or "_" in name:
        findings.append((
            "ROOM_NAME_SEPARATOR",
            "room name contains a separator; an opaque generated identifier is one unseparated token",
        ))

    alphabet = set(profile.get("room_alphabet") or CROCKFORD_LOWER)
    outside = sorted({c for c in name if c not in alphabet})
    if outside:
        findings.append((
            "ROOM_NAME_ALPHABET",
            "room name uses characters outside the configured alphabet: " + "".join(outside),
        ))

    needed = required_room_length(profile)
    if len(name) < needed:
        findings.append((
            "ROOM_NAME_TOO_SHORT",
            f"room name is {len(name)} characters, below the {needed} a uniformly "
            f"generated name in this alphabet needs to reach a capacity of "
            f"{profile.get('room_min_entropy_bits', 128)} bits; length bounds capacity "
            f"only and proves nothing about the generator",
        ))

    # Pathological-value checks. Each rejects only values that a uniform
    # generator produces with negligible probability (far below 1e-20 at the
    # required length), so no plausible random identifier is rejected merely
    # for containing repeated characters.
    period = smallest_period(name)
    if len(name) >= 2 and period <= len(name) // 2:
        findings.append((
            "ROOM_NAME_REPEATED",
            f"room name is a repetition of the {period}-character pattern "
            f"{name[:period]!r}; no uniform generator plausibly produced it",
        ))
    # The diversity floor is meaningful only against a large alphabet: with a
    # configured 2- or 4-symbol alphabet, a perfectly uniform value has few
    # distinct characters by construction, so the check would reject every
    # correct name. The period check above stays active for every alphabet.
    if len(alphabet) >= 8 and len(name) >= 8 and len(set(name)) <= 3:
        findings.append((
            "ROOM_NAME_LOW_DIVERSITY",
            f"room name uses only {len(set(name))} distinct characters across "
            f"{len(name)} positions; no uniform generator over this "
            f"{len(alphabet)}-symbol alphabet plausibly produced it",
        ))

    if name.isdigit():
        findings.append(("ROOM_NAME_SEQUENTIAL", "room name is entirely digits, which reads as a sequential id"))

    for pattern in DATE_PATTERNS:
        if pattern.search(name):
            findings.append(("ROOM_NAME_DATE", "room name carries a date, which a published timetable supplies"))
            break

    flat = name.replace("-", "")
    if len(flat) == 32 and all(c in "0123456789abcdef" for c in flat) and flat[12] == "7":
        findings.append((
            "ROOM_NAME_UUIDV7",
            "room name is a UUIDv7; its leading 48 bits are a timestamp and a class start time is published",
        ))

    lowered = name.lower()
    hits = sorted({word for word in MEANINGFUL_TOKENS if word in lowered})
    if hits:
        findings.append((
            "ROOM_NAME_MEANINGFUL",
            "room name contains a meaningful token: " + ", ".join(hits),
        ))

    return findings


def check_token(token: str, profile: dict) -> list[tuple[str, str]]:
    """Return (code, message) for every claim rule the token breaks."""
    header_segment, payload_segment = split_compact_jwt(token)
    header = decode_json_segment(header_segment, "header")
    payload = decode_json_segment(payload_segment, "payload")

    findings: list[tuple[str, str]] = []

    alg = header.get("alg")
    allowed = profile.get("allowed_algs") or []
    if not isinstance(alg, str) or alg == "":
        findings.append(("ALG_MISSING", "header has no alg"))
    elif alg.lower() == "none":
        findings.append(("ALG_NONE", "header declares alg none, which is an unsigned token"))
    elif alg not in allowed:
        findings.append(("ALG_NOT_ALLOWED", f"alg {alg} is not in the profile allow-list {allowed}"))

    kid = header.get("kid")
    if not isinstance(kid, str) or kid == "":
        findings.append(("KID_MISSING", "header has no kid, so the signing key cannot be identified or rotated"))
    elif kid in (profile.get("platform_access_token_kids") or []):
        findings.append((
            "KID_IS_PLATFORM_KEY",
            f"kid {kid} signs platform access tokens; the Jitsi key must be a separate key",
        ))

    room = payload.get("room")
    if "room" not in payload:
        findings.append(("ROOM_MISSING", "payload has no room claim"))
    elif not isinstance(room, str):
        findings.append(("ROOM_NOT_STRING", "room claim is not a string"))
    elif room == "":
        findings.append(("ROOM_EMPTY", "room claim is empty"))
    elif "*" in room:
        findings.append((
            "ROOM_WILDCARD",
            "room claim contains a wildcard; it admits its holder to every room it matches",
        ))
    else:
        findings.extend(check_room_name(room, profile))

    for claim in ("iss", "aud", "sub"):
        if claim not in profile:
            continue
        expected = profile[claim]
        actual = payload.get(claim)
        if claim == "aud" and isinstance(actual, list):
            matched = isinstance(expected, str) and expected in actual
        elif isinstance(expected, list):
            matched = actual in expected
        else:
            matched = actual == expected
        if not matched:
            findings.append((f"{claim.upper()}_MISMATCH", f"{claim} is {actual!r}, profile expects {expected!r}"))

    iat = payload.get("iat")
    exp = payload.get("exp")
    nbf = payload.get("nbf")
    iat_ok = isinstance(iat, int) and not isinstance(iat, bool)
    exp_ok = isinstance(exp, int) and not isinstance(exp, bool)
    if "iat" not in payload:
        findings.append(("IAT_MISSING", "payload has no iat, so the lifetime cannot be measured"))
    elif not iat_ok:
        findings.append(("IAT_NOT_INT", "iat is not an integer number of seconds"))
    if "exp" not in payload:
        findings.append(("EXP_MISSING", "payload has no exp, so the token never expires"))
    elif not exp_ok:
        findings.append(("EXP_NOT_INT", "exp is not an integer number of seconds"))

    if iat_ok and exp_ok:
        lifetime = exp - iat
        maximum = profile.get("max_lifetime_seconds", 120)
        if lifetime <= 0:
            findings.append(("LIFETIME_NOT_POSITIVE", f"exp - iat is {lifetime} seconds"))
        elif lifetime > maximum:
            findings.append((
                "LIFETIME_TOO_LONG",
                f"exp - iat is {lifetime} seconds, over the profile maximum of {maximum}",
            ))

    if isinstance(nbf, int) and not isinstance(nbf, bool) and exp_ok and nbf > exp:
        findings.append(("NBF_AFTER_EXP", "nbf is after exp, so the token is never valid"))

    outside = sorted({claim for claim in PRIVILEGE_CLAIMS if claim in payload})
    if outside:
        findings.append((
            "ROLE_CLAIM_OUTSIDE_CONTEXT",
            "privilege claim outside context: " + ", ".join(outside),
        ))

    return findings


def read_token(args: argparse.Namespace) -> str:
    if args.token is not None:
        return args.token
    if args.token_file == "-":
        return sys.stdin.read()
    path = Path(args.token_file)
    if not path.is_file():
        raise BadInput(f"token file not found: {args.token_file}")
    return path.read_text(encoding="utf-8")


def report(findings: list[tuple[str, str]], subject: str, pass_note: str | None = None) -> int:
    if not findings:
        print(f"PASS {subject}" + (f": {pass_note}" if pass_note else ""))
        return 0
    for code, message in findings:
        print(f"FAIL {code} {message}")
    print(f"FAIL {subject}: {len(findings)} violation(s)")
    return 1


# A pass on one value proves the format and the predictability heuristics, and
# nothing about the generator. Say so in the output, so a green run is never
# quoted as evidence of entropy.
ROOM_PASS_NOTE = (
    "format and predictability heuristics passed for this value; a single sample "
    "cannot establish generator entropy - the CSPRNG/uniform-generation contract "
    "must be shown with generator-level design evidence"
)

TOKEN_PASS_NOTE = (
    "claim shape and room-name heuristics passed; signature authenticity and "
    "generator entropy are out of this script's scope"
)


def run(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    if args.room_name is not None:
        return report(check_room_name(args.room_name, profile), "room-name", ROOM_PASS_NOTE)
    token = read_token(args)
    for claim in ("iss", "aud", "sub"):
        if claim not in profile:
            raise BadInput(
                f"profile does not declare {claim}; a profile that declares no {claim} cannot assert one. "
                "Add it, or state in the deliverable why this deployment does not bind it."
            )
    return report(check_token(token, profile), "token", TOKEN_PASS_NOTE)


SELF_TEST_PROFILE = {
    "iss": "alaa-platform",
    "aud": "jitsi-classes",
    "sub": "meet.example.test",
    "allowed_algs": ["RS256"],
    "max_lifetime_seconds": 120,
    "platform_access_token_kids": ["platform-access-2026-01"],
    "room_min_entropy_bits": 128,
    "room_alphabet": CROCKFORD_LOWER,
}

GOOD_ROOM = "3k9wq2mtb7xz4np8vfhc5rjd6s"


def encode_token(header: dict, payload: dict) -> str:
    def seg(value: dict) -> str:
        raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    return f"{seg(header)}.{seg(payload)}.c2lnbmF0dXJl"


def good_header() -> dict:
    return {"alg": "RS256", "typ": "JWT", "kid": "jitsi-join-2026-07"}


def good_payload() -> dict:
    return {
        "iss": "alaa-platform",
        "aud": "jitsi-classes",
        "sub": "meet.example.test",
        "room": GOOD_ROOM,
        "iat": 1_800_000_000,
        "exp": 1_800_000_100,
        "context": {"user": {"id": "u-42", "name": "A Teacher", "moderator": True}},
    }


def self_test() -> int:
    failures: list[str] = []

    def expect_codes(label: str, findings: list[tuple[str, str]], expected: str | None) -> None:
        codes = [code for code, _ in findings]
        if expected is None:
            if codes:
                failures.append(f"{label}: expected no violation, got {codes}")
            return
        if expected not in codes:
            failures.append(f"{label}: expected {expected}, got {codes or 'none'}")

    def expect_bad_input(label: str, token: str) -> None:
        try:
            check_token(token, SELF_TEST_PROFILE)
        except BadInput:
            return
        failures.append(f"{label}: expected BadInput, got none")

    def token_with(header_patch: dict | None = None, payload_patch: dict | None = None,
                   drop: tuple[str, ...] = ()) -> str:
        header = good_header()
        payload = good_payload()
        header.update(header_patch or {})
        payload.update(payload_patch or {})
        for key in drop:
            header.pop(key, None)
            payload.pop(key, None)
        return encode_token(header, payload)

    expect_codes("valid token", check_token(token_with(), SELF_TEST_PROFILE), None)
    expect_codes("alg none", check_token(token_with({"alg": "none"}), SELF_TEST_PROFILE), "ALG_NONE")
    expect_codes("alg not allowed", check_token(token_with({"alg": "HS256"}), SELF_TEST_PROFILE), "ALG_NOT_ALLOWED")
    expect_codes("alg missing", check_token(token_with(drop=("alg",)), SELF_TEST_PROFILE), "ALG_MISSING")
    expect_codes("kid missing", check_token(token_with(drop=("kid",)), SELF_TEST_PROFILE), "KID_MISSING")
    expect_codes(
        "kid is platform key",
        check_token(token_with({"kid": "platform-access-2026-01"}), SELF_TEST_PROFILE),
        "KID_IS_PLATFORM_KEY",
    )
    expect_codes("room missing", check_token(token_with(drop=("room",)), SELF_TEST_PROFILE), "ROOM_MISSING")
    expect_codes("room not string", check_token(token_with(payload_patch={"room": 7}), SELF_TEST_PROFILE), "ROOM_NOT_STRING")
    expect_codes("room empty", check_token(token_with(payload_patch={"room": ""}), SELF_TEST_PROFILE), "ROOM_EMPTY")
    expect_codes("room star", check_token(token_with(payload_patch={"room": "*"}), SELF_TEST_PROFILE), "ROOM_WILDCARD")
    expect_codes(
        "room prefix wildcard",
        check_token(token_with(payload_patch={"room": "grade9*"}), SELF_TEST_PROFILE),
        "ROOM_WILDCARD",
    )
    expect_codes("iss mismatch", check_token(token_with(payload_patch={"iss": "other"}), SELF_TEST_PROFILE), "ISS_MISMATCH")
    expect_codes("aud mismatch", check_token(token_with(payload_patch={"aud": "other"}), SELF_TEST_PROFILE), "AUD_MISMATCH")
    expect_codes("sub mismatch", check_token(token_with(payload_patch={"sub": "other"}), SELF_TEST_PROFILE), "SUB_MISMATCH")
    expect_codes("aud list match", check_token(token_with(payload_patch={"aud": ["jitsi-classes", "x"]}), SELF_TEST_PROFILE), None)
    expect_codes("iat missing", check_token(token_with(drop=("iat",)), SELF_TEST_PROFILE), "IAT_MISSING")
    expect_codes("exp missing", check_token(token_with(drop=("exp",)), SELF_TEST_PROFILE), "EXP_MISSING")
    expect_codes("exp not int", check_token(token_with(payload_patch={"exp": "soon"}), SELF_TEST_PROFILE), "EXP_NOT_INT")
    expect_codes(
        "lifetime too long",
        check_token(token_with(payload_patch={"exp": 1_800_003_600}), SELF_TEST_PROFILE),
        "LIFETIME_TOO_LONG",
    )
    expect_codes(
        "lifetime not positive",
        check_token(token_with(payload_patch={"exp": 1_799_999_000}), SELF_TEST_PROFILE),
        "LIFETIME_NOT_POSITIVE",
    )
    expect_codes(
        "nbf after exp",
        check_token(token_with(payload_patch={"nbf": 1_800_009_999}), SELF_TEST_PROFILE),
        "NBF_AFTER_EXP",
    )
    expect_codes(
        "top-level moderator",
        check_token(token_with(payload_patch={"moderator": True}), SELF_TEST_PROFILE),
        "ROLE_CLAIM_OUTSIDE_CONTEXT",
    )
    expect_codes(
        "top-level role",
        check_token(token_with(payload_patch={"role": "moderator"}), SELF_TEST_PROFILE),
        "ROLE_CLAIM_OUTSIDE_CONTEXT",
    )
    expect_codes(
        "weak room claim",
        check_token(token_with(payload_patch={"room": "3k9wq2mt"}), SELF_TEST_PROFILE),
        "ROOM_NAME_TOO_SHORT",
    )

    expect_bad_input("two segments", "aaa.bbb")
    expect_bad_input("five segments", "a.b.c.d.e")
    expect_bad_input("empty token", "   ")
    expect_bad_input("header not base64", "!!!.e30.sig")
    expect_bad_input("payload not json", "eyJhbGciOiJSUzI1NiJ9.bm90LWpzb24.sig")
    # "WzFd" is base64url for the JSON array [1]: a syntactically valid segment that is not an object.
    expect_bad_input("header not object", "WzFd." + encode_token({}, good_payload()).split(".")[1] + ".sig")

    expect_codes("good room name", check_room_name(GOOD_ROOM, SELF_TEST_PROFILE), None)
    expect_codes(
        "repeated single character",
        check_room_name("a" * 26, SELF_TEST_PROFILE),
        "ROOM_NAME_REPEATED",
    )
    expect_codes(
        "short repeated pattern",
        check_room_name("ab" * 13, SELF_TEST_PROFILE),
        "ROOM_NAME_REPEATED",
    )
    expect_codes(
        "odd-length repeated pattern",
        check_room_name("ab" * 13 + "a", SELF_TEST_PROFILE),
        "ROOM_NAME_REPEATED",
    )
    expect_codes(
        "two-block low diversity",
        check_room_name("a" * 12 + "b" * 14, SELF_TEST_PROFILE),
        "ROOM_NAME_LOW_DIVERSITY",
    )

    # With a configured small alphabet, low diversity is the correct shape of a
    # uniform value and must not be rejected. The Thue-Morse prefix is
    # overlap-free, so it is also immune to the period check.
    small_alphabet_profile = dict(SELF_TEST_PROFILE)
    small_alphabet_profile["room_alphabet"] = "ab"
    thue_morse = "".join("ab"[bin(i).count("1") % 2] for i in range(128))
    expect_codes(
        "binary alphabet, non-periodic full-length name",
        check_room_name(thue_morse, small_alphabet_profile),
        None,
    )
    expect_codes(
        "binary alphabet still rejects a constant name",
        check_room_name("a" * 128, small_alphabet_profile),
        "ROOM_NAME_REPEATED",
    )
    expect_codes("empty room name", check_room_name("", SELF_TEST_PROFILE), "ROOM_NAME_EMPTY")
    expect_codes("non-string room name", check_room_name(5, SELF_TEST_PROFILE), "ROOM_NAME_NOT_STRING")
    expect_codes("wildcard room name", check_room_name("*", SELF_TEST_PROFILE), "ROOM_NAME_WILDCARD")
    expect_codes("uppercase room name", check_room_name(GOOD_ROOM.upper(), SELF_TEST_PROFILE), "ROOM_NAME_ALPHABET")
    expect_codes("hyphenated room name", check_room_name("3k9wq2mtb7xz-4np8vfhc5rjd6s", SELF_TEST_PROFILE), "ROOM_NAME_SEPARATOR")
    expect_codes("short room name", check_room_name("3k9wq2mt", SELF_TEST_PROFILE), "ROOM_NAME_TOO_SHORT")
    expect_codes("numeric room name", check_room_name("40219", SELF_TEST_PROFILE), "ROOM_NAME_SEQUENTIAL")
    expect_codes("year-prefixed room name", check_room_name("2026zqwmtb7xz4np8vfhc5rjd6s", SELF_TEST_PROFILE), "ROOM_NAME_DATE")
    expect_codes("date-suffixed room name", check_room_name("zqwmtb7xz4np8vfhc5rjd20260901", SELF_TEST_PROFILE), "ROOM_NAME_DATE")
    expect_codes("uuidv7 room name", check_room_name("0192f4a1b2c37abc8def0123456789ab", SELF_TEST_PROFILE), "ROOM_NAME_UUIDV7")
    expect_codes("meaningful room name", check_room_name("3k9wq2mtermb7xz4np8vfhc5rjd6s", SELF_TEST_PROFILE), "ROOM_NAME_MEANINGFUL")

    # Exercise the exit-code mapping itself, with the report output swallowed so the
    # self-test's own result is the only thing on stdout.
    parser = build_parser()
    with contextlib.redirect_stdout(io.StringIO()):
        clean = run(parser.parse_args(["--room-name", GOOD_ROOM]))
        dirty = run(parser.parse_args(["--room-name", "grade9"]))
    if clean != 0:
        failures.append("exit mapping: a clean room name did not return 0")
    if dirty != 1:
        failures.append("exit mapping: a violating room name did not return 1")

    if failures:
        print("SELF-TEST FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 3
    print("SELF-TEST PASSED")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_jitsi_jwt.py",
        description=(
            "Assert the Jitsi join-token claim contract and the room-name entropy rules. "
            "This does not verify signatures and is not an admission control."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exit codes and what each obliges you to do:\n"
            "  0  every rule held. Record the check and its date in the deliverable.\n"
            "  1  a claim or room-name rule was broken. Do not ship the mint path or the room-name\n"
            "     generator. Fix the producer, not the token, and run again.\n"
            "  2  the input was not a token, not a room name, or not a usable profile. Fix the\n"
            "     invocation. A 2 is never evidence that anything passed.\n"
            "  3  the self-test failed, so this script is broken on this runtime. Do not trust a 0\n"
            "     from it. Report the failure and stop.\n"
            "\n"
            "Why no signature check: signature verification of a platform access token belongs to the\n"
            "Ala gateway, and of a Jitsi join token to the Prosody verifier in the Jitsi deployment.\n"
            "Both hold key material this script deliberately does not have. A token can carry a valid\n"
            "signature and still open every classroom, which is the class of defect checked here.\n"
            "\n"
            "Use --token-file, or --token-file - for standard input, rather than --token: a token\n"
            "on a command line lands in the shell history and in the process list of every user\n"
            "on the host.\n"
            "\n"
            "The room-name pattern rules are heuristics. On a 26-character Crockford Base32 name they\n"
            "flag a random name well under once in a thousand. The correct response to a coincidental\n"
            "match is to regenerate the name, which costs nothing; never widen the rule to admit it.\n"
            "\n"
            "Alphabet and length prove only capacity: what a name of this shape could carry if it were\n"
            "drawn uniformly at random. No check on a single value proves the generator's entropy. The\n"
            "contract stays what it is - a CSPRNG mapped uniformly onto the room alphabet - and the\n"
            "assurance for it is generator-level design evidence and review, never a PASS from here.\n"
            "\n"
            "Profile keys (JSON): iss, aud, sub (required for token mode), allowed_algs,\n"
            "max_lifetime_seconds, platform_access_token_kids, room_min_entropy_bits, room_alphabet.\n"
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--token", help="the compact JWT to check, as a literal argument")
    mode.add_argument("--token-file", help="a file holding the compact JWT, or - for standard input")
    mode.add_argument("--room-name", help="a room name to check against the entropy and derivation rules")
    mode.add_argument("--self-test", action="store_true", help="run the built-in fixtures and exit")
    parser.add_argument("--profile", help="path to the deployment profile JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    try:
        return run(args)
    except BadInput as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

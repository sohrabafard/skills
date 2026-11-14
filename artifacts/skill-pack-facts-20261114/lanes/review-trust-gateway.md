# Independent instruction review, trust-gateway lane and the parallel session's commits: VERDICT: CHANGES-REQUESTED
Reviewer: alaa-instruction-reviewer, read-only, requested opus/high, self-reported claude-opus-5-5, effort unknown. Paths are under `skills/sohrab/alaa-trust-gateway-auth/` unless another skill is named; line numbers are those of the reviewed tree.

## Part A: decisions on the lane's work
A1. The lane's edit of the case 6 test sentence (an empty `X-Access` denies with `AUTH_ACCESS_HEADER_MISSING`) is correct: `references/50-deny-codes.md` owns which code applies and gives HEADER_MISSING for a value that is "missing or blank" and BITMAP_INVALID for a value that is present but unusable. The script must agree. In `scripts/trust_boundary_check.py`, the handler that reports a bitmap the decoder rejected (about lines 95-99) becomes:
    except BitmapError as exc:
        code = "AUTH_ACCESS_HEADER_MISSING" if value.strip() == "" else "AUTH_ACCESS_BITMAP_INVALID"
        findings.append(f"bitmap: {value!r} is not a usable bitmap ({exc}); the trusted-context normalizer rejects it with {code}")
   Keep the decoder's own guard as it is. If `scripts/test_trust_boundary_check.py` asserts the old message for an empty or whitespace-only value, update that expected text to match; change no other test.
A2. nit. `SKILL.md` about line 70 names only BITMAP_INVALID for case 6. Append to that row: "; an absent or blank `X-Access` denies with `AUTH_ACCESS_HEADER_MISSING`".
A3. nit. `references/30-fail-closed-cases.md` about lines 203-204: "both name the bitmap" does not hold for HEADER_MISSING. Replace "both name the bitmap" with "both name the failure".
A4. `references/10-verification-and-ingress.md` about lines 486-487, the "four layers" sentence against a three-row table. Replace the sentence with: "`tenant_id`, `tenant_public_id`, `project_id`, the compact claim `pid` and the header `X-Project-Id` name one concept; `tenant_id` and `tenant_public_id` are legacy aliases. The canonical form per layer is fixed:" (keep the table and the text after it).
A5. `references/60-auth-service-v3-contract.md` about line 181. Replace "**Do not freeze that positive-integer parser into the shared public contract.**" with "**Do not freeze a numeric parse of `X-User-Id` into the shared public contract.**" Leave the two lines after it unchanged.

## Part B: findings in the parallel session's commits (already on main)
B1. major, fail-open reading. `references/40-downstream-normalization.md` about lines 76-78: the clause "except the WA guest-ingest rule" reads as if a body field may override trusted tenant context. Replace so the sentence ends: "...including in anonymous and analytics flows. The WA guest-ingest rule in `references/10-verification-and-ingress.md` applies only when no trusted `X-Project-Id` arrived, so it is no exception to this rule."
B2. major, fail-open reading. Same file about lines 106-108: the exception covers "missing or malformed", so a malformed trusted header reads as if it may fall back to the client envelope. Replace with: "A later transform that finds `X-Project-Id` missing or malformed drops the data: the transport was accepted and the business result is a denial. On WA ingest a batch with no `X-Project-Id` takes its tenant from the envelope under the WA guest-ingest rule in `references/10-verification-and-ingress.md`. A present but malformed `X-Project-Id` never falls back to the envelope."
B3. minor. `SKILL.md` about line 69: replace the row text with: "a required claim or trusted header absent, including `rol` | 3 and 4 — deny; an absent role never means "no restrictions apply"; an absent `X-Project-Id` on a route with a guest rule is the guest shape (case 3 Scope), not a deny". Keep the table's cell structure.
B4. minor. `references/30-fail-closed-cases.md` about lines 344-346: replace "a step-up header" in the deny condition with "any of the three step-up headers", so the sentence reads "Deny when any of the three step-up headers arrives on a request the gateway did not authenticate".
B6. minor. `references/10-verification-and-ingress.md` about line 142: point the shipping status at one home: "Read its shipping status in `alaa-services-contract references/95-fleet-conformance.md`".
B7. minor. `SKILL.md` about lines 32-33: replace "The header itself is still forwarded to the backend" (and its parenthesis if it is one) with "(... not trusted; the gateway currently forwards its `Authorization` header to the backend, `references/10-verification-and-ingress.md`)" fitted to the sentence so that it keeps its meaning and carries the pointer.
B9. nit. `references/70-review-and-anti-patterns.md` about line 32: add to the reason cell "; the advisory header is a message hint, never a decision input".

## Not to be changed by the lane (reported to the owner)
B5. `alaa-services-contract/references/00-topic-map.md` about line 37 states a who-may-set rule ("A backend never sets it on a public route") that trust-gateway owns.
B8. `alaa-services-contract/references/25-end-to-end-flow-and-boundaries.md` and `32-...` restate the optional-bearer rule that trust-gateway owns; they agree today.

## Accepted by the reviewer
The services-contract "Trusted context rule" reduced to a pointer; the drop table and the case 2 amendment; the WA route family row; the marker header shape; the SDK reaction; the deny-code preamble; the new source-map and conformance rows. The description has no angle bracket and counts about 971 characters by hand.

## Not assessed
The contract values against the gateway, wa or client repositories; validators.

## Dispositions
The lane applied A1 to A5 and B1, B2, B3, B4, B6, B7 and B9 in four commits on the lane branch; the script's unit test passed (8 tests) and the script now reports `AUTH_ACCESS_HEADER_MISSING` for an empty or whitespace-only value. The confirmation pass returned APPROVED-WITH-NITS: every item accepted, and one clause the reviewer's own B3 text had dropped (a missing or failing bearer on a public path is dropped, not denied) was added by the lead before the merge. B5 and B8 were not applied: they sit in `alaa-services-contract` and go to the owner. The marker's shipping status still has a second home in `references/90-source-map.md`; the reviewer said it may stay.

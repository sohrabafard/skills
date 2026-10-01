# Independent gate evidence

## Failure analysis

Read-only `alaa-failure-analyst`, configured gpt-6.1-sol/high; observed identity unknown.
No reruns performed after the package's repair/retry budget was exhausted.

- Parser retry attempted 22 targets: 20 clean, example 10 and the Kubernetes
  ConfigMap fatal on `no option httplog`. Pinned configuration lines 6142/6255
  confirm this option does not support negation. Proposed correction: move
  `option httplog` from shared defaults to traffic frontends and remove negations.
- Runtime first failed on HTTP503, then failed its fallback deadline after the
  repair tolerated only that transitional response. No persistent raw log survived.
  The exact failing stage is unobserved, not a proven health-timing problem.
- Source-backed cause: the fixture adds `/live -> be_live` while unpublished;
  map's default applies only to absent keys (`configuration.txt:22500`), and
  unpublished selection falls through (`15295-15304`). The fixture has no
  `default_backend`, so 503 is expected. Proposed correction: add an explicit
  `default_backend be_fallback` and label each assertion stage.
- These are package example/fixture defects; no HAProxy product regression was established.

## Instruction review

Initial verdict: CHANGES-REQUESTED. Read-only `alaa-instruction-reviewer`,
configured gpt-6-astra/high; observed identity unknown. No gates executed.

| Finding | Initial severity | Resolution submitted for readback |
|---|---|---|
| Dynamic runtime script unreachable from package Markdown | major | HAProxy body/router/gate register now route exact command and proof limits |
| Network wall-time compared with pure Lua service execution timeout | major | Lua reference separates overall deadline from execution budget |
| Mandatory rejection conflicts with advisory sentinel exception | minor | Rejection requirement scoped to rejection-contract call sites |
| Five-argument/string-only prototypes conflict with verified API | minor | Twelve optional arguments and sample-compatible results documented |

Compression was reviewed against HEAD and the intended corrected contracts; a
separately retained draft was unavailable. Implementers report draft/compression
passes; independent review does not claim a draft replay or live-agent evaluation.
Instruction-only closure returned APPROVED: all four findings closed against
current files. No gates were executed, no retained draft was replayed, and this
does not close the separately failed parser/lifecycle operations.

## Correctness review

Initial verdict: CHANGES-REQUESTED. Read-only `alaa-reviewer`, configured
gpt-6.1-sol/high; observed identity unknown. No gates executed.

- Major: invalid logging negation in example 10 and the Kubernetes ConfigMap.
- Major: missing fallback backend in the dynamic lifecycle fixture.
- Minor: qualify rate-limit multiplication by peer isolation, measurement window
  and penalty assumptions; allow Runtime API wait replies enough transport time
  and prove active-stream drain; ensure failed container creation and parser
  timeouts clean up with confirmed results; match the exact 3.4.6 patch boundary;
  classify absurd decimal Content-Length values rather than raising ValueError.
- The parser and lifecycle repair/retry budgets are exhausted. Additional edits
  and retries for those operations await explicit user authority.

## Release review

Initial verdict: NOT-READY. Read-only `alaa-release-guardian`, configured
gpt-6.1-sol/medium; observed identity unknown. No gates executed.

- Parser/lifecycle failures and the absent integrated frozen-snapshot receipt
  prevent readiness.
- Lua runtime timeout cleanup must report nonzero `docker rm -f` results. This
  separate first correction is assigned to the Lua owner; runtime verification
  remains deferred to the final frozen verifier.
- Cached Alpine proof does not establish Debian, other architectures, registry
  digest resolution, admission, UID/mount behavior or consumer rollout/drain.

## Security review

Verdict: PASS-WITH-HARDENING. Read-only `alaa-security-reviewer`, configured
gpt-6-astra/high; observed identity unknown. No gates executed.

- Low-severity hardening: parser Docker adapter forwards every inherited
  `HAPROXY_*` variable into command arguments. Restrict this to explicit fixture
  variables and add an unrelated synthetic sentinel regression. No real
  credential exposure was established.
- Examined Lua/token, library, identity, cryptographic and control-plane guidance
  has no newly identified fail-open or identity regression. Unrun subrequest,
  timeout and cryptographic negative-vector adoption evidence remains explicit.
- Overall readiness remains blocked by parser/lifecycle and final verification.

## Lua cleanup correction

Original Lua owner corrected nonzero removal handling in `check_runtime.py` and
added `test/test_runtime_runner.py`, routed from the testing reference.
`python -B test/test_runtime_runner.py` returned 4/4 passing synthetic cases:
successful removal, nonzero removal, OS error and timeout. Scoped diff check
returned 0. No Docker runtime operation was repeated.

## Final Lua runner and documentation closure

Independent verifier observed 4/4 synthetic tests and the final runner's 34/34
embedded-unit assertions plus library/parser/sample/token probes, exit 0 for
both. The before/after 38-file manifest matched; receipt and raw streams are in
`verification/verification-report.md`. Three termination messages occur in
stderr after fixture cleanup with overall exit 0; stdout retains the probe results.

The Lua owner subsequently split five references into retained entrypoints and
20 focused children, with no executable/configuration/fixture changes. Native
links/line-budget checks measured all 25 affected docs GREEN. Instruction reviewer
returned APPROVED for the split: original findings stay closed, all children are
reachable, and restrictions, exceptions, obligations and proof limits survive.
No exact pre-compression draft replay or new runtime recertification was claimed.

## Additional bounded correction authority

The user explicitly approved one additional HAProxy correction/test cycle after
the failed parser/lifecycle repair-and-retry. Original package owner is correcting
the eight concrete review findings; read-only closures and final documentation
precede one verifier attempt. Further retries are not authorized by this decision.

## HAProxy correction and bounded closure

The original owner corrected all eight findings. Twelve synthetic runner tests,
eight byte fixtures, 21 structure/defaults configurations and scoped diff checks
returned exit 0. These are focused author observations, not parser/lifecycle
execution. Six retained reference routers now reach 28 focused children.

- Security closure: PASS. Explicit fixture variables and the sentinel regression
  close the inherited-environment finding; no real credential exposure was seen.
- Instruction closure: APPROVED-WITH-NITS. Boundaries, prerequisites and historical
  proof survive the split. Three overpromising cache routing descriptions were
  subsequently narrowed to the actual child contents; the parent readback
  confirmed the descriptions. No obligation was removed.
- Correctness closure: APPROVED. All seven original findings are statically
  closed. The new minor warning finding in the Lua streaming fixture is also
  closed: explicit `normal` precedes Lua loading, fatal/warning outputs are
  classified at a named stage and the regression discriminates both streams.
- Docker parser/lifecycle execution remains pending the final documenter and
  frozen verifier; no result here predicts its outcome. No gate was run by a
  read-only reviewer, and no new major finding remains open.

## Release prerequisite readback

Original implementation findings are closed. The release guardian returned
NOT-READY solely pending corrected HAProxy parsing, active-stream lifecycle and
final frozen-snapshot receipts; no further package correction was required.
Local prerequisites are the cached 3.4.6 Alpine build with Lua, authorized Docker,
host Python/OpenSSL and image-provided shell/nc/wget. Successful observed final
receipts can close this local prerequisite without changing package inputs.
Consumer build/digest/admission/drain/rollback and deployment remain unproven;
the user did not request release, installation or deployment.

## Final attempted runtime and acceptance disposition

The verifier observed all 22 parser targets passing on the frozen 477-file
snapshot. The dynamic lifecycle runner exited 1 at `active stream prevents
deletion: lifecycle assertion`. Its actual Runtime API reply was not retained;
this is a candidate gate failure, not an established HAProxy regression.
Subsequent stream completion, drained deletion and reload reconstruction were
not reached. The user-authorized extra correction/test cycle is exhausted.

Final release-guardian readback: NOT-READY for lifecycle adoption; prior static
findings remain closed. Independent instruction/correctness/security approvals
do not override the failed executable gate. The objective permits an explicitly
partially validated result, which is the final disposition. Further correction
and runtime execution require new authority. No package changes or Docker
reruns follow this result.

Read-only failure analysis localized the assertion to
`check_runtime_3_4.py:179`. The piped `printf | nc` CLI transport may close its
input during the asynchronous wait: pinned source `src/cli.c:2382-2384`
interrupts waits on peer shutdown, and lines 2399-2402 distinguish expired,
interrupted, failed and done replies. Stream completion before the assertion
or an ineffective maintenance transition are other unconfirmed possibilities.
The timeout wording itself is source-correct. A future authorized diagnostic
must capture the raw reply, phase timing and contemporaneous server/stream state
before choosing a correction. No runtime rerun or package edit was performed.

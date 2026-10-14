# Independent correctness review - initial

Reviewer: /root/correctness, alaa-reviewer, requested gpt-6.1-sol/medium, observed identity unknown. Verdict: CHANGES-REQUESTED. Read-only source inspection and bounded error injection; no source edits.

| Severity | Location | Finding / required correction |
|---|---|---|
| Major | memory-os/scripts/alaa_memory_staleness.ps1:84 | Suppressed partial enumeration returned clean exit 0; terminating enumeration/read errors and unavailable exit 2 required |
| Major | memory-os/scripts/alaa_obsidian_linkcheck.ps1:65 | Same incomplete-scan false pass; add partial scan regression |
| Minor | memory-os/scripts/alaa_memory_staleness.ps1:103 | Unreadable-note null binding returns exit 1, must distinguish unavailable from readable empty |
| Minor | memory-os/scripts/alaa_obsidian_linkcheck.ps1:96 | Same unavailable read violation |
| Minor | scripts/check_capability_recall.py:24 | Null scenario row raises AttributeError; malformed input must exit 2 |
| Minor | scripts/check_capability_recall.py:92 | IO.File.ReadAllLines direct-read mutant survives claimed guard |
| Minor | memory-os/scripts/session_start_context.ps1:36 | Readable empty Markdown may be confused with unavailable; add boundary test |

All findings assigned verbatim to T3 fix cycle 1. No acceptance weakened. Further unrelated findings not inferred.

Baseline decision grade: 34 records, 75 oracle checks, 74 pass, 1 fail. Gateway check 2 requires ci-image and gateway pin owner as leads; baseline record names generic current owner files instead. Strict failure retained. All other checks independently judged supported. Actual scenario effects none. This is proposed-decision behavior, not live tool execution.

Baseline provenance checked: 31 source texts match baseline HEAD after newline normalization; six policy texts in before-probe match baseline; packet scenarios match scenario-inputs. After comparison, final measurements, fix verification, installed runtimes, Claude and live Hindsight not assessed yet.

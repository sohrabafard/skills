# Follow-up decisions

User request: investigate `alaa-147` and `alaa-x05`, correct confirmed defects, otherwise
close with reasons. Both existing `repo:skills` spikes were claimed. Their original
`discovered-from` edges identify provenance, not membership in the completed epic.
This is bounded follow-up work; the completed optimization plan remains historical.

## Draft decisions before compression

- Arvan: official per-operation pages retrieved on 2026-10-18 document CORS put and
  delete, multipart upload and part listing, object tagging, object listing and deletion,
  and bucket/object ACL get and put. Replace the affected absence claims with documented
  capability, exact operation names, source URLs and read dates. Correct every repeated
  absence claim in cost and migration guidance. Keep the existing matrix status meaning:
  Supported is documentation evidence, never a successful call to a live endpoint.
  No provider calls, credential use, bucket mutation or inferred full AWS parity.
- Octane: `refreshApplication()` assigns a newly created application; this removes
  singleton instances too and therefore cannot distinguish singleton from scoped
  registration. Shape A must keep the same application, resolve the real registration,
  establish tenant A state, invoke `forgetScopedInstances()`, resolve again and assert
  both an empty value and a different object. Do not rebind the production service in
  the adopter test. Require a deliberately broken singleton and a removed-reset control
  to fail, then restore and pass. This proves binding lifetime only. Actual listener
  registration, flush configuration, captured objects, static state and server lifecycle
  require the one-worker Shape B test; it must verify both requests reached the same
  surviving worker and the trusted first-tenant fixture was exercised.
- Proportional checks: official source comparison; real installed framework container
  experiment in an existing network-disabled image; skill structure and reference
  validators; Arvan checker self-test; final scoped diff/encoding inspection. No test of
  live Arvan or a deployed Octane service is claimed.

## Compression decisions

Use the matrix as the single operation inventory; migration guidance points to it instead
of maintaining a second whitelist. Restrict Shape A to its actual proof and route the
remaining cases to Shape B. Preserve both assertions, observed negative controls, the
same-worker condition and all existing authority boundaries. References retain dates
and exact versions. No router is moved or removed.

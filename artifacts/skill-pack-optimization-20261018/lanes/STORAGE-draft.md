# STORAGE wording draft

This is pass one, before behavior-preserving compression. The proposal decision record owns rationale and evidence. Product edits await parent ratification.

## Hooks

The hook table must distinguish the failure of an optional hint's own computation from the failure of the upstream hook invocation. An optional hint never decides whether a caller may act, so when the hint's dependency fails, catch that error, log it, increment the appropriate counter, and return a successful response without the hint. For an HTTP hook this is a successful JSON hook response. For an embedded callback it is an empty HTTPResponse with nil error. Do not pretend the upstream transport itself fails open: an unreachable pre-finish endpoint or a returned callback error still fails the completion response after storage has finished. If even the hint endpoint's outage must not affect completion, do not enable that optional blocking hook. Keep the real hint data available through the control plane rather than only in the completion response.

For post-receive, split recording from a decision about whether the caller's right still holds. Recording failure continues and records the loss. If a revocation decision denies or cannot be obtained, the hook must return a successful StopUpload response, not return an error to the hook transport. Upstream does not interpret a hook transport failure as a stop; it logs and continues. Per-method authorization must still run in front of the handler, using the verified trust boundary and without adding a backend bearer-token fallback. An active-stream deadline for revocation requires a design that proves the deadline even if the hook endpoint is unavailable. Do not approve the deadline based only on progress hooks. A stop can arrive after the transfer finishes, and termination requires backend support and can fail; deny later requests according to the durable ownership state and reconcile cleanup rather than asserting that StopUpload proves deletion.

## Part sizing

The application client owns STORAGE_PART_SIZE_BYTES. Its 16 MiB default remains an estimate. The standalone tusd deployment asset owns TUSD_S3_PART_SIZE, which the Compose command passes to -s3-part-size and which configures PreferredPartSize. A library consumer must configure PreferredPartSize explicitly; setting the deployment asset's env variable does nothing by itself in an embedded service. Neither setting is the browser's tus PATCH chunk size, which comes from the upload plan and is bounded by ingress caps.

For Arvan, a preference at or below the provider ceiling is necessary but insufficient. The store may increase effective parts for large declared uploads to stay within MaxMultipartParts. Require the actual MaxPartSize and resulting effective part size to fit the resolved provider bounds, together with the upload/object-size cap. Verify which controls the pinned binary exposes; use library configuration where applicable and do not invent a CLI flag or automatic STORAGE_* mapping. Test an upload size that would force growth past the provider ceiling, not only the default 50 MiB setting.

## Endpoint and missing variable

Endpoint, bucket and credentials must be chosen explicitly. A provider-profile endpoint shape never becomes a startup default. The Arvan delta table must label endpoint values as examples, with the operator selecting the bucket's own region and paired endpoint. Existing resolution precedence remains unchanged for optional settings. No implemented client-abort boolean exists in the shared owner; the hypothetical extension procedure must not assert that one exists, invent its name/default or make mandatory Arvan abort optional.

## Keys and reports

Generic object-key namespace and tenant-prefix rules stay with the MinIO owner. The tusd reference owns the tus/application layout, random upload identity and reserved sidecars. Keep the historical observation that Ala keys lack tenant scope, the isolation dependency on Postgres, its operational consequences and the migration warning for existing keys. Keep external routers and distinguish generic from tusd part sizing in their matching conditions.

Retain the dated MinIO fleet observation in its body and correct the repository source name throughout that skill. Retain the historical unsafe mc command with a DO NOT COPY comment inside the code fence; require version/schema verification before a hand-written scoped mc config rather than assert release-independent compatibility. Keep every existing safety boundary and explicit alternative.

For full upload-plane design reports, keep every existing output dimension. For a partial review, include the applicable dimensions and cross-boundary consequences only; identify the register and include tests and risks. A hook-only review includes posture, lifecycle and observability, so making the report smaller does not erase the failure consequences.

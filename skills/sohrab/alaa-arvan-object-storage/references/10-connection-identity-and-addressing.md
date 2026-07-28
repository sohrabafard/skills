# Connection, Identity and Addressing

Read this when pointing a client at ArvanCloud, choosing a region, deciding an addressing style or a signature
version, or issuing and rotating an access key. Client-library selection, credential hygiene and rotation doctrine are
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`) `references/70-client-libraries.md` and
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`) `references/30-identity-credentials-and-access.md`; only
the Arvan deltas are here.

## Regions and endpoints

Two regions are documented, and each is a separate namespace.

| Region name | Region identifier | Endpoint |
|---|---|---|
| Simin (Tehran) | `ir-thr-at1` | `https://s3.ir-thr-at1.arvanstorage.ir` |
| Shahriar (Tabriz) | `ir-tbz-sh1` | `https://s3.ir-tbz-sh1.arvanstorage.ir` |

`[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/, read: 2026-07-27]`, corroborated with the
same two hostnames and the Simin/Shahriar names by rclone's provider list
`[source: https://rclone.org/s3/, read: 2026-07-27]`, which is a third-party source and is recorded here only because
it agrees with the vendor page.

**Set the client's endpoint from `STORAGE_ENDPOINT` and its region from `STORAGE_REGION` in every environment, and
fail startup when either is unset.** `references/15-environment-contract-deltas.md` carries the Arvan defaults for
both, and `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) `references/05-environment-contract.md` owns
the family. A bucket is reachable only in the data centre that created it
`[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`, so a default-region fallback sends
production traffic to a namespace where the bucket does not exist and the error is a not-found, not a misconfiguration
error.

**Treat the region identifier as part of the bucket's identity in every record that names the bucket** — configuration,
runbook, migration script and incident note — because the bucket name alone does not locate the object.

## Addressing style

**Use virtual-hosted-style addressing, `<bucket>.s3.<region>.arvanstorage.ir`.** Arvan states the virtual host format
is required for CDN caching `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]` and its
custom-domain guide addresses objects that way, for example
`arvan-test.s3.ir-thr-at1.arvanstorage.ir/arvan.png`
`[source: https://docs.arvancloud.ir/en/object-storage/buckets/custom-domain, read: 2026-07-27]`.

**Set `STORAGE_USE_PATH_STYLE` to `false` on an Arvan client, and record the reason beside the value when a
specific failure forces it to `true`.** Path-style loses edge caching without returning an error, so the cost
appears as a traffic bill rather than as a broken request, and a value changed without a written reason gets copied
forward by the next service.

**Arvan recommends and uses virtual-hosted addressing; whether it accepts path-style at all is unestablished.** Its
limits page gives the Virtual Host format and states it is required for CDN caching, its custom-domain guide
addresses objects that way, and its SDK examples set no path-style flag and so take the SDK's virtual-hosted
default. No page says what happens to a path-style request. That is open question 2.

**Name every Arvan bucket so it is valid as a DNS label**: 3 to 63 characters, lowercase letters, digits, hyphens and
periods, starting and ending with a letter or digit, no consecutive periods, no underscores, no uppercase, not
IP-address shaped `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-27]`. A name that is
legal in MinIO but contains an underscore cannot be addressed virtual-hosted at all, and a name containing a period
breaks TLS certificate matching on the wildcard host.

## Signature version

**Set `STORAGE_SIGNATURE_VERSION` to `s3v4` on every Arvan endpoint, and set it explicitly rather than leaving it
to an SDK default.** An explicit value survives a dependency upgrade that changes the default; a default does not,
and the resulting failure looks like a revoked credential rather than a changed library.

The evidence for `s3v4` is indirect, and it is worth knowing exactly how indirect. **Arvan publishes no statement
that Version 4 is required or that Version 2 is accepted.** What its material shows is that every reachable Arvan
SDK example constructs the client from credentials and `ServiceURL` alone, with no signature option of any kind
`[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/, read: 2026-07-28]`
`[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/multipart-upload/, read: 2026-07-28]`
`[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/upload-presigned/, read: 2026-07-28]`,
and an unmodified AWS SDK signs Version 4. rclone ships ArvanCloud as a named provider with both endpoints and
documents no signature override for it, so its Version 4 default applies too `[source: https://rclone.org/s3/,
read: 2026-07-28]`. **The s3cmd and S3Browser guides that would print the setting verbatim are on
`www.arvancloud.ir/help/`, a host that refuses retrieval entirely**, so no Arvan page states the value in words.

**Record `s3v4` as this skill's default rather than as a provider guarantee**, because the difference decides
whether a future failure is a bug in our configuration or a fact nobody had checked. Open question 1 in
`references/SOURCES.md` holds what is still unanswered.

**When an Arvan request fails with `SignatureDoesNotMatch` and the secret is known good, check the signature
version and the addressing style before reissuing the key.** A mismatch and a wrong secret produce the same error
code, and reissuing a key that was never wrong costs a rotation and leaves the cause in place.

## Credentials

**Obtain the Access Key and Secret Key from the Object Storage dashboard**; Arvan describes them as belonging to the
user account and pairs them with the endpoint URL
`[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/credentials/, read: 2026-07-27]`
`[source: https://docs.arvancloud.ir/en/object-storage/dashboard, read: 2026-07-27]`.

**Assume an Arvan key reaches every bucket in its account until Arvan documents otherwise.** No scoped machine user,
per-bucket key or attachable key policy appears in the documentation read for this skill, so the blast radius of a leak
is the account. Two compensating controls apply, and at least one is required on every Arvan bucket holding
user-supplied bytes:

1. **Give a service that must be isolated its own Arvan account**, because the account is the only boundary the
   credential model demonstrably provides.
2. **Attach a bucket policy that names the exact prefixes a caller may read**, using the documented IAM-shaped policy
   `[source: https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/put-bucket-policy/, read: 2026-07-27]`.
   This restricts anonymous and cross-service reads; it does not restrict the account's own key.

**Rotation procedure is unverified** — open question 4. Until it is confirmed, **plan any Arvan key rotation as a
change with a possible interruption**, and do not promise a zero-downtime rotation to an operator. Whether a second
concurrent key can exist during a cutover is exactly what open question 4 asks.

Credential storage, log redaction and the rule that a credential never appears in a URL or a metric label are
`/alaa-minio-object-storage` (`$alaa-minio-object-storage`) constraints 4 and 5 and apply here unchanged.

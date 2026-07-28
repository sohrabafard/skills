# Client libraries

This file owns which object-storage client a service uses and how it is configured. Read it before adding,
replacing or reconfiguring a client in any language.

## One client per process

**A process talks to the object store through exactly one client.** Two clients in one process diverge in timeout,
retry policy, credential handling, checksum behaviour and signing, so every rule proven on one path is unproven on
the other, and a fix applied to one leaves the other broken in a way no test covers.

The fleet's only object-storage consumer runs two: `aws-sdk-go-v2/service/s3` v1.101.0 feeding the upload library,
and a hand-rolled SigV4 client for bucket checks, object reads and writes, the finalization copy and cleanup. The
hand-rolled client uses `http.DefaultClient`, which has **no timeout at all**, performs no retries, and sets no
`x-amz-security-token`, so it cannot use temporary credentials `[source: tusd-upload-platform repository,
internal/storage/s3_http_client.go, internal/httpapi/official_tusd_creation.go and go.mod, read: 2026-07-27]`.
Name that shape when you meet it; do not reproduce it.

## Never hand-roll SigV4

**Use a maintained SDK for request signing.** A correct signer has to handle the session-token header, canonical
header and query ordering, payload hashing including the unsigned and chunked variants, checksum algorithms,
clock-skew correction on retry, and endpoint resolution for path-style and virtual-host addressing. Each of those
is a separate defect class, none of them fails visibly in a happy-path test, and several fail only against a
different store implementation than the one used in development.

The one legitimate exception is a build constraint that forbids the dependency. Where that applies, write it down
with its owner, and treat the resulting client as a component needing its own conformance tests against a real
store.

## Choosing the library

| Runtime | Client | Notes |
|---|---|---|
| Go | `github.com/aws/aws-sdk-go-v2/service/s3` | Works against MinIO with `BaseEndpoint` and `UsePathStyle` set. The fleet already depends on it. |
| Go, S3-only workloads | `github.com/minio/minio-go/v7` | Smaller surface; choose it only when the service has no other AWS dependency. |
| PHP and Laravel | `league/flysystem-aws-s3-v3` behind the framework's `s3` filesystem disk | Configure `endpoint` and `use_path_style_endpoint` for a self-hosted store. |
| Node and TypeScript | `@aws-sdk/client-s3` | Presigning lives in a separate `@aws-sdk/s3-request-presigner` package. |
| Python | `boto3` | Set `endpoint_url` and the `s3.addressing_style` config for a self-hosted store. |

Package names are recorded as unverified for version and current-maintenance status
`[source: package registries were not reachable this session, read: unverified as of 2026-07-27]`. Confirm the
version installed in the service before writing an API call against it, and take the dependency decision itself to
the owning language skill — `/alaa-golang` (`$alaa-golang`) for Go, `/alaa-php-clean-code`
(`$alaa-php-clean-code`) for PHP.

## Configuration every client needs

1. **An explicit request timeout on the underlying HTTP client.** A default client with no timeout turns a stalled
   store into an exhausted worker pool: every request waits forever and the process stops serving everything else,
   not just storage calls. Take the value from `/alaa-services-contract` (`$alaa-services-contract`) and the
   doctrine from `/alaa-reliability-sla` (`$alaa-reliability-sla`).
2. **An explicit retry policy, distinct from the SDK default.** SDK defaults are tuned for a public cloud's error
   profile, not for a single-node store on the same network.
3. **An addressing style set explicitly from `STORAGE_USE_PATH_STYLE`, and an endpoint override** when the store
   is self-hosted — see "The addressing style" below, which owns the choice, and
   `40-encryption-tls-and-durability.md` for the TLS consequence of the virtual-hosted form.
4. **A credential provider rather than a captured pair**, where the runtime offers one, so rotation does not
   require a rebuild — see `30-identity-credentials-and-access.md`.
5. **A checksum choice made deliberately.** Newer SDK releases changed default request checksum behaviour, and a
   store that does not implement the newer algorithm rejects requests that worked with an older SDK
   `[source: https://docs.aws.amazon.com/sdkref/latest/guide/feature-dataintegrity.html, read: unverified as of
   2026-07-27]`. Pin the behaviour explicitly when talking to a self-hosted store.
6. **An explicitly set S3 signature version** — see the next section, which owns the rule.

## The addressing style

Every S3 request names a bucket, and there are two places to put that name. **Read `STORAGE_USE_PATH_STYLE` and set
the client's addressing style from it, in every client, in every language.** The right style is a property of the
endpoint rather than of the code, which is why it is an environment value with a default per provider in
`05-environment-contract.md`.

**Path-style** puts the bucket in the first path segment and leaves the host fixed:

```
https://s3.example.com/media-assets/uploads/2026/07/report.pdf
```

The host is `s3.example.com` and one certificate covers every bucket, the bucket is `media-assets` in the first path
segment, and the key is `uploads/2026/07/report.pdf`.

**Virtual-hosted style** puts the bucket in the leftmost DNS label and leaves the whole path to the key:

```
https://media-assets.s3.ir-thr-at1.arvanstorage.ir/uploads/2026/07/report.pdf
```

The bucket is `media-assets` in the leftmost label, the host the certificate must match is therefore
`media-assets.s3.ir-thr-at1.arvanstorage.ir` and differs per bucket, and the key is `uploads/2026/07/report.pdf`.

**Set the addressing style explicitly in every client, and leave it to no library default.** The default differs by
library and by version: some libraries build a virtual host unless told otherwise, some infer the style from whether
an endpoint override was supplied, and some changed that inference between major versions. A style left unset is
therefore decided by the next dependency upgrade rather than by the endpoint, and what it produces is a
`NoSuchBucket` or a TLS hostname mismatch on a deployment where the bucket, the credential and the policy all stayed
the same.

### What breaks under each style

Under virtual-hosted style:

- **A bucket name that is not a valid DNS label cannot be addressed at all**, because the name becomes a hostname.
  An underscore, an uppercase letter or a 64-character name is legal in a path segment and illegal in a label.
- **A bucket name containing a dot cannot be served under a wildcard TLS certificate.** `media.assets.s3.example.com`
  carries one label more than `*.s3.example.com` matches, so the handshake fails for that bucket and only that
  bucket, while every neighbouring bucket keeps working. That is the practical reason
  `10-buckets-and-object-keys.md` rule 2 forbids a dot in a bucket name, and the reason
  `05-environment-contract.md` validates `STORAGE_BUCKET` as a DNS label whenever `STORAGE_USE_PATH_STYLE` is
  `false`.
- **A self-hosted store needs wildcard DNS and a wildcard certificate covering every bucket**, which a single-node
  MinIO deployment usually has neither of.

Under path-style:

- **CDN fronting generally stops working**, because a CDN's origin and cache key are the host and every bucket
  collapses onto one host under path style. ArvanCloud states the Virtual Host format is required for CDN caching
  `[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]`. The cost arrives as a traffic
  bill rather than as a failed request, so nothing in the request path reports it.
- **A provider narrowing path-style support breaks the client on a date this fleet does not set.** AWS is recorded
  here as narrowing path-style support, unverified as of 2026-07-28. Confirm it against AWS's own documentation
  before choosing path style on an AWS endpoint, because the failure arrives with no deploy of ours attached to it.
- **A proxy or gateway that rewrites paths in front of the store can corrupt the bucket segment**, because under
  path style the bucket sits in the path a rewrite rule is allowed to touch.

### Why this is a knob and not a rule

**ArvanCloud documents virtual-hosted addressing and states nothing about whether path-style works at all**
`[source: https://docs.arvancloud.ir/en/object-storage/limits/, read: 2026-07-28]`; that is open question 2 in
`/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) `references/SOURCES.md`. **MinIO is normally addressed
path-style**, because virtual-hosted addressing needs wildcard DNS and a wildcard certificate that a single-node
deployment usually lacks. Neither statement is a property of S3; each is a property of one provider's deployment,
and a third provider may agree with neither. **That is why the value is `STORAGE_USE_PATH_STYLE` with a default per
provider profile rather than a rule in code**, because a rule in code would need editing on the day the fleet adopts
a provider nobody has met yet, and an env value would not.

### How each client selects it

| Client | Setting for path-style | Status |
|---|---|---|
| `mc` | derived from the alias endpoint; no addressing-style flag was read this session | *needs verification* |
| Go, `aws-sdk-go-v2/service/s3` | `UsePathStyle` on `s3.Options`, set in the options function passed to `NewFromConfig`, beside `BaseEndpoint` | *needs verification* |
| Go, `minio-go/v7` | a bucket-lookup option on `minio.Options` selecting path lookup rather than DNS lookup | *needs verification* |
| PHP, `aws/aws-sdk-php` under Flysystem | `use_path_style_endpoint`, a client option taking a boolean | *needs verification* |
| Node, `@aws-sdk/client-s3` | `forcePathStyle`, a client-constructor option taking a boolean | *needs verification* |
| Python, `boto3` | `botocore.config.Config(s3={"addressing_style": ...})`, taking `path`, `virtual` or `auto` | *needs verification* |

Every row is recorded as needing verification, because no SDK or MinIO documentation was reachable in the session
that wrote it `[source: package registries and vendor documentation were not reachable this session, read:
unverified as of 2026-07-28]`. **Confirm the option name against the installed version before writing it into a
configuration file, and take its value from `STORAGE_USE_PATH_STYLE` rather than writing a literal**, because a
literal is the compiled-in value the environment contract exists to remove.

**Set the addressing style and the signature version at the same point in the client's construction.** Both are
properties of the endpoint, both fail in a shape that reads as something else — a not-found or an authentication
error — and `90-failure-classes.md` class 2 already lists addressing style beside signature version among the causes
to check before anyone rotates a credential that was never wrong. Arvan's own stance on both is
`/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) `references/10-connection-identity-and-addressing.md`.

## The signature version

This is one of two unrelated things people call "the version API". This one selects how a request is signed. The
other is bucket versioning, which decides whether the store keeps superseded objects, and it is
`40-encryption-tls-and-durability.md`. They share a word and nothing else: setting the wrong signature version
produces a client that cannot authenticate, and setting bucket versioning wrongly produces a bucket whose bill
grows forever. Read the right file for the one you mean.

**Set the signature version explicitly in every client's configuration from `STORAGE_SIGNATURE_VERSION`, whose
stated default is `s3v4`, and record which one the store requires beside the endpoint it belongs to.** The right
value is a property of the endpoint rather than of the code, and it is one this fleet has not confirmed for every
provider it uses, so it is an environment value — see `05-environment-contract.md`. Signature v4 is what current S3-compatible stores expect; v2 is legacy, some
providers reject it outright, and a few older or non-AWS implementations still require it. Leaving the choice to a
library default means an unrelated dependency upgrade can change how requests are signed, which turns a working
deployment into an authentication failure with no change to the credential, the endpoint or the policy.

**Never switch the signature version to make an authentication error go away.** Establish which version the
endpoint requires — from the store's own documentation, or from a client already reaching that endpoint
successfully — and then set that one, because flipping the setting can turn a signing failure into a different
failure that is harder to attribute and leaves the real cause in place.

How each client the skill names expresses it:

| Client | Setting | Status |
|---|---|---|
| `mc` | `--api S3v4` on `mc alias set`, or `S3v2` for the legacy version | `S3v4` **repo-verified**; `S3v2` *needs verification* |
| Go, `aws-sdk-go-v2/service/s3` | signs SigV4 and offers no v2 signer, so a store requiring v2 cannot be reached with it at all | *needs verification* |
| Go, `minio-go/v7` | chosen by the credentials provider — a v4 static-credentials constructor rather than a v2 one | *needs verification* |
| PHP, `aws/aws-sdk-php` under Flysystem | a `signature_version` client option taking `v4` or `v2` | *needs verification* |
| Node, `@aws-sdk/client-s3` | signs SigV4; the `signatureVersion` option from the previous major version is not honoured | *needs verification* |
| Python, `boto3` | `botocore.config.Config(signature_version=...)`, `s3v4` or `s3` for the legacy one | *needs verification* |

Every row except the `mc` flag is recorded as needing verification, because no SDK or MinIO documentation was
reachable in the session that wrote it `[source: package registries and vendor documentation were not reachable
this session, read: unverified as of 2026-07-27]`. Confirm the option name against the installed version before
writing it into a configuration file.

A signature-version mismatch surfaces as an authentication error that looks exactly like a wrong secret key, which
is why `90-failure-classes.md` class 2 lists it among the causes to check before anyone rotates a credential that
was never wrong.

## Client lifetime

**Construct the client once per process and share it.** SDK clients hold a connection pool; constructing one per
request discards the pool and leaks file descriptors under load.

**Hold no per-request state on the client.** In a long-lived worker — an Octane worker, a Go server, a queue
consumer — the client outlives every request, so a tenant, an actor or a bucket override stored on it leaks across
requests. Route long-lived-worker state safety to `/alaa-octane-performance` (`$alaa-octane-performance`).

## Testing a client

Prove the client against a real store, not a mock of the interface it implements. A mock proves that the calling
code calls the method; it proves nothing about signing, path style, checksum negotiation, or how the store answers
a delete of an object that is not there. Proof levels and which layer each behaviour is tested at belong to
`/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md`.

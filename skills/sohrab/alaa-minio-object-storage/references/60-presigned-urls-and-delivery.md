# Presigned URLs and delivery

This file owns how bytes leave the bucket. Read it before issuing a presigned URL, before letting a browser talk to
the store directly, and before putting a CDN in front of a bucket.

## What a presigned URL is

A presigned URL is a complete, signed S3 request encoded into a link. Anyone holding it can perform that one
operation on that one key, as the signing identity, until it expires
`[source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html, read: unverified as of
2026-07-27]`. It is a bearer credential with a short life, and every rule below follows from that one fact.

## The user download path

**Serve a user's download of a file that user is entitled to through a presigned `GET` URL with a bounded
lifetime, or by streaming the object through the application, and never by making the bucket publicly readable.**
The object store is not internal-only on this fleet: a file that lands in it has to reach the client again so a
user can download it, and this section names the path that carries it. Choosing between the two carriers is
"Downloading through the application instead" below. Choosing neither, and reaching for public read instead, is
the defect this section exists to prevent.

**Take the presigned lifetime from `STORAGE_PRESIGN_MAX_SECONDS`, whose stated default is 900 seconds**, per
`references/05-environment-contract.md`. The lifetime is a value that differs between a test stack and production
and between one download size and another, so it is an environment value with a default rather than a number in
code.

**Re-run the authorization check at the moment of signing, and return the URL only in an authenticated response to
the caller who passed that check.** The signature proves the store should honour the request and proves nothing
about whether this user should have asked, so an authorization decision cached from an earlier request signs a
link for someone who has since lost access.

**Sign a download URL with an identity whose policy grants `s3:GetObject` on that user's prefix and nothing
else.** A presigned URL carries the signer's permissions for that one request, so a URL signed by a broad identity
is a broad credential sitting in a link.

**Set a `Content-Disposition` and a content type the store returns with the object, and derive both server-side.**
A download served with a client-declared content type executes in the browser origin when the client declared one
that does, which turns a file store into a script host.

## Rules

1. **Set the shortest lifetime that covers one download or upload attempt on the slowest supported connection.**
   The link cannot be revoked before it expires, so the lifetime is the entire blast radius. Where the fleet
   registers a maximum, take it from `/alaa-services-contract` (`$alaa-services-contract`); where it does not,
   choose the shortest workable value and request registration rather than inventing a second number.
2. **Sign with an identity scoped to the one operation and the one prefix.** A presigned URL inherits the signer's
   permissions for that request, so a URL signed by a broad identity is a broad credential in a link.
3. **Never log a presigned URL, never put one in an error message, and never let one reach a page that a third
   party can read.** It appears in browser history, in the `Referer` header sent to whatever the page loads next,
   and in any proxy or analytics log on the path. This is the same rule as `SKILL.md` rule 4 and it is the one most
   often broken by a debug log added during an incident.
4. **Revocation means rotating the signing credential.** There is no per-URL revocation, so an accidental
   disclosure forces a rotation that invalidates every outstanding URL signed by that identity. Say that out loud
   when choosing the lifetime.
5. **Deliver the URL over an authenticated response to the caller who is entitled to the object**, and re-run the
   authorization check at signing time rather than reusing an earlier decision. The signature proves the store
   should honour the request; it proves nothing about whether the user should have asked.

## Presigned uploads

A presigned `PUT` places no constraint on what the client sends unless the constraint was part of the signature.
The client controls the body length and the content type, so a presigned `PUT` issued for a 2 MiB avatar accepts a
2 GiB file.

**Use a signed POST policy with explicit conditions when a browser uploads directly**, so content-length range,
content type and key prefix are enforced by the store
`[source: https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-HTTPPOSTConstructPolicy.html, read: unverified as
of 2026-07-27]`. Where the client uploads through a resumable protocol instead, that protocol's own size chain is
`/tusd-upload-platform` (`$tusd-upload-platform`).

**Never trust the content type the client declared.** Store it as a claim, determine the real type server-side
before serving the object back, and serve user-supplied bytes with a content type and a `Content-Disposition` that
cannot execute in the browser origin.

## Downloading through the application instead

Proxying the download through the service gives per-request authorization, an audit line, and no bearer link in the
wild; it costs the service's own bandwidth, a held connection per download, and egress paid twice. **Proxy when the
object is small, the audit requirement is explicit, or the authorization decision depends on request-time state.
Presign when the object is large or the download is long**, because a large object streamed through an application
process is a stalled worker for the duration.

## Public read

**Make no bucket holding user-supplied bytes publicly readable, and carry those downloads by the path in "The user
download path" above instead.** Public read is an unbounded, unauthenticated and unrevocable read grant over every
object in the bucket, and each of those three words names a difference from a presigned URL. It is unbounded
because it covers every key in the bucket, the ones added next year included, where a presigned URL names one
object. It is unauthenticated because the object key becomes the only credential, and keys leak through logs,
`Referer` headers and browser history exactly the way presigned URLs leak, where a presigned URL carries a
signature the store verifies. It is unrevocable in the way that matters operationally: withdrawing it is a policy
change affecting every reader at once, and nothing records who copied a key while the bucket was open, where a
presigned URL expires on its own without anyone acting.

**Put genuinely public content — a logo, a published document, a static asset — in a different bucket whose entire
contents are intended to be public.** A single bucket serving both kinds of object makes one policy mistake widen
the private half, and there is no signal when it happens.

## CDN in front of a bucket

1. **Give the CDN an origin identity and keep the bucket private.** A CDN that reads a public bucket means the
   bucket is public, and every control the CDN adds can be bypassed by addressing the store directly.
2. **Do not put a presigned URL behind a shared cache.** The signature is part of the URL, so either the cache key
   includes it and nothing is ever a hit, or it does not and the cache serves one user's signed response to
   another.
3. **Keep the cache lifetime shorter than the object's mutability, or make the key immutable.** An object store has
   no way to purge a CDN, so a cached copy of a deleted object outlives the deletion by the whole cache lifetime —
   which matters when the deletion was a retention obligation.
4. **Route the CDN or proxy configuration itself to its owner**: HAProxy directives are `/alaa-haproxy`
   (`$alaa-haproxy`), and Kubernetes ingress is `/alaa-k8s-helm` (`$alaa-k8s-helm`).

## What the fleet does today

No presigned URL is issued anywhere in the fleet's only object-storage consumer, and no CDN origin is configured.
`presigned_url` and `object_key` are already on that service's forbidden-log-field list, so the logging rule above
is met before the feature exists `[source: tusd-upload-platform repository,
internal/observability/contracts.go, read: 2026-07-27]`. No bucket policy is set, so whether the bucket is publicly
readable is decided by the store's own default rather than by an explicit decision.

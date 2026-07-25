# Outbound Fetching And File Handling

Read when the change makes an outbound request whose destination is influenced by request data, or accepts, stores, or serves a file.

# Part 1 - Outbound fetching (SSRF)

**An outbound request whose destination is influenced by request data goes only to a destination on a configured allowlist, connects to the address the guard checked, and follows no redirects.** "Influenced by request data" includes the host, the port, the scheme, the path, and any part of a URL assembled from a request field, a database value a client wrote, a webhook registration, or a document a client uploaded.

## One egress component

Every request-influenced outbound fetch goes through one named component that owns the allowlist, the address pin, the redirect policy, and the response bounds. No other code path opens an outbound connection to a request-influenced destination. This is the only structure in which the rules below can be reviewed at all: six call sites with six partial guards is six vulnerabilities waiting for one to be edited.

## The allowlist

- A set of exact hosts, or registrable-domain suffixes, together with an allowed scheme set and an allowed port set, held in configuration and validated at process start.
- Nothing is fetched until the allowlist is loaded. An egress client that starts, or keeps serving, with no allowlist in hand is the outbound instance of stop-the-line item 22; `60-deep-review-and-hardening.md` owns the general default-safety rule for configured allowlists.
- Matching is on the parsed host after normalisation - lowercased, IDNA-resolved, trailing dot removed - never on a substring, a prefix, or a suffix of the raw URL string. `https://evil.com/?x=api.internal` contains the allowed host as a substring and is not it. `https://api.internal.evil.com` has it as a prefix.
- Scheme allowlist is `https`, plus `http` only for a named in-cluster destination. `file:`, `gopher:`, `ftp:`, `data:`, `dict:`, `ldap:`, `jar:`, and `netdoc:` are excluded by the allowlist rather than by a blocklist.
- **One parser.** The URL is parsed once, by the same library the HTTP client will use, and the guard inspects the parsed result rather than re-parsing the string. Two parsers disagreeing on where the host ends - on embedded credentials, a backslash, a tab, a fragment, or a second `@` - is the classic bypass.

## Resolve, check, then connect to the checked address

Resolve the hostname yourself. Check **every** returned address, A and AAAA, against the deny set. Then connect to a checked address - not to the hostname again.

Re-resolving the hostname for the connection is the DNS-rebinding hole: the guard resolved a public address and the connection resolved a private one, with a TTL of zero making the window reliable rather than lucky. In Go this means a `DialContext` or `Control` hook that inspects the resolved address at connect time; in other stacks it means resolving first and connecting to the literal address with the `Host` header set, or using the client's equivalent connect-time hook. A guard that only inspects the URL string is reported as not implementing the control.

Deny set, by address and not by name:

- loopback `127.0.0.0/8`, `::1`
- link-local `169.254.0.0/16`, `fe80::/10`
- private `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- carrier-grade NAT `100.64.0.0/10`
- `0.0.0.0/8`, broadcast, multicast `224.0.0.0/4`, `ff00::/8`
- IPv6 unique-local `fc00::/7`
- IPv4-mapped and IPv4-compatible IPv6 `::ffff:0:0/96`, `::/96` - a mapped address that decodes to a private IPv4 passes an IPv6-only check
- the environment's own pod, service, and node CIDRs

**Cloud and orchestrator metadata endpoints are denied by address**, because any resolver an attacker influences bypasses a name check: `169.254.169.254`, `fd00:ec2::254`, `169.254.170.2` (ECS task metadata), `100.100.100.200` (Alibaba), `192.0.0.192` (Oracle), the Kubernetes API service address, and the kubelet read-only and authenticated ports. Denying names such as `metadata.google.internal` is a supplement and never the control.

## Redirects, bounds, and the response

- The client is configured with a redirect limit of zero. Where a flow legitimately needs a hop, each hop's URL passes the same allowlist and the same address check as the first, and the hop count is bounded in configuration.
- The response is bounded on three axes, all from configuration: a byte ceiling enforced while streaming, a total-time ceiling, and a content-type allowlist. An unbounded read from an attacker-chosen URL is memory exhaustion on a shared fleet as well as an SSRF.
- **Nothing from the response is returned verbatim.** A failed or rejected fetch returns one fixed error. Echoing the upstream status, headers, body, or elapsed time turns a blind SSRF into a full one and makes the service an internal port scanner.
- No credential is attached implicitly. The egress client uses no ambient cloud or instance credentials, no proxy that injects authorization, and no cookie jar shared with any other client. Where the destination needs a credential, it is looked up per allowlisted destination.

## Where this applies even when it does not look like a fetch

Flag when a request-derived URL, host, port, path, or scheme reaches: an HTTP client; a webhook dispatcher; an image, PDF, HTML, or office-document renderer that loads remote references; an XML, YAML, or SVG parser with external references enabled (`20-untrusted-input.md` owns the parser flags); a `git clone`, `curl`, or `wget` subprocess; a database facility that opens a connection or reads a file (`COPY FROM PROGRAM`, `dblink`, `file()`, `LOAD DATA INFILE`); a mail client's SMTP or MX target; a monitoring or health-check probe target; an OIDC discovery or key-set URL; or an SDK call that accepts an endpoint override.

The product features that make this mandatory rather than theoretical: tenant-configured webhooks, avatar-by-URL, RSS or feed import, link previews and unfurling, HTML-to-PDF export, remote-file import, and any "test connection" button.

# Part 2 - File upload, storage, and serving

## Accepting an upload

- **Type is decided from the bytes.** Detect the media type by inspecting content with a maintained detection library, then confirm the client-declared content type and the filename extension agree with the detected type. A mismatch is a rejection, not a correction. The declared type and the extension are never the deciding input.
- The accepted set is a configured allowlist of detected media types. An empty allowlist accepts nothing.
- **The stored name is server-generated** - a random identifier or a content digest. The client's filename is stored as a separate display-only metadata field, never used to build a path or a storage key, and rendered escaped (`25-browser-trust-and-output.md`).
- **Two size ceilings, both configured**: a per-file byte ceiling enforced *while streaming*, so the connection aborts at the ceiling rather than after the whole body is buffered; and a per-actor and per-tenant quota over a time window.
- **Bounds on anything the service expands or decodes.** For an archive: a maximum entry count, a maximum total decompressed size, and a maximum compression ratio, plus per-entry destination validation (`20-untrusted-input.md`, path construction). For an image: a maximum pixel dimension and total pixel count, because a compressed-size bound does not bound what the decoder allocates. For a document converted or thumbnailed: a wall-clock and memory ceiling on the converting process, which runs with no network access.
- Where the repository already runs a content or malware scan, an added upload path uses it. Where none exists, that absence is a P2 finding naming the mechanism the stack already has - never a proposal to adopt a new product.

## Storing it

- Uploads are written outside every directory any web server, application router, or static-file handler can serve, on a store with no execute permission, and never to a path reachable by a template resolver, an autoloader, or an include path. An upload under a document root is a remote-code-execution path in any stack that maps an extension to an interpreter.
- The storage key contains the tenant identifier, derived server-side. The key containing the tenant is a convention; the control is that **every read re-derives the tenant from verified context and confirms the stored object's tenant matches** (`40-authorization-and-tenancy.md`).
- The bytes that were validated are the bytes that get stored and served. Validate the stream you persist, or re-validate after the move; validating one copy and serving another is the file-handling form of the check-then-act defect in `40-`.

## Serving it

- Every download performs an authorization decision on every request. Where the object store must serve directly, a signed URL is acceptable when the signature covers the object key, the expiry, the method, and the tenant, and the expiry is short. **A URL whose only secret is an unguessable key is not an authorization control** - it is a bearer credential with no expiry, no revocation, and a habit of appearing in referrers, logs, and shared chat messages.
- A download endpoint takes an **identifier**, resolved through a tenant-scoped query. It never takes a path, a storage key, or an absolute URL.
- Response headers on any served user-supplied bytes: `Content-Type` set from the server-detected type and never echoed from the upload; `X-Content-Type-Options: nosniff`; `Content-Disposition: attachment` with a sanitised filename for everything outside a small, named inline-render allowlist; and a CSP on the serving response.
- **Serve user-supplied bytes from a hostname that holds no cookies and shares no same-origin trust with the application.** An HTML, SVG, or XML file served from the application origin is stored XSS with full session access no matter what the sanitiser did, because the browser executes it in the application's origin.
- SVG is active content. Serve it as `attachment` only, or sanitise it through the platform's sanitiser **and** serve it from the separate origin.
- A missing object and an unauthorized object return the same response.

## Flag list for files

A filename, extension, or declared content type from a request used in a path, a storage key, a response `Content-Type`, or a type decision; a body fully buffered before its size is checked; an upload directory inside a served root; a download endpoint accepting a path, key, or URL; an archive expanded without entry-count and decompressed-size ceilings; an image decoded without dimension bounds; a signed URL with a long or absent expiry, or one whose signature does not cover the tenant; user-supplied HTML or SVG served inline from the application origin.

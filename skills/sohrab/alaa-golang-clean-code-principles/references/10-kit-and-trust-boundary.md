# P1–P3 · Kit Boundary and Trust Boundary

These three principles guard the two boundaries where a wrong line of code becomes a platform problem: the
boundary between service code and the kit, and the boundary between the request edge and everything behind it.

## P1 — The Kit Writes It Once

If a concern is kit-owned — error envelope, middleware chain, readiness, trusted headers, outbox, jobs, seeding,
envelope codec, UUIDv7, audience predicate — service code **calls** the kit. It never re-implements the shape,
never wraps-and-renames it, and never copies it "temporarily". A hand-rolled copy is how dual behavior is born,
and dual behavior is the bug class the kit exists to kill: two services disagreeing about what a 422 looks like
at 2 a.m.

```go
// WRONG — hand-rolled error response; drifts from the canonical envelope on day one
func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    if err := h.uc.Create(r.Context(), in); err != nil {
        w.WriteHeader(422)
        json.NewEncoder(w).Encode(map[string]any{"code": "VALIDATION", "msg": err.Error()})
    }
}

// RIGHT — errkit domain error, one kit mapper renders {error:{status,code,message,meta}}
func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
    in, err := httpkit.Bind[CreateNewsRequest](r)
    if err != nil { httpkit.RespondError(w, r, err); return }
    out, err := h.uc.Create(r.Context(), in)
    if err != nil { httpkit.RespondError(w, r, err); return }
    httpkit.Respond(w, r, http.StatusCreated, out)
}
```

**Proof.** Check the shape against the kit-owned surface inventory before you write it. That inventory is the
kit repository's `CONTRACTS.md` (every code-enforced shape), `docs/INDEX.md` (every documented package), and the
capability map in `/alaa-go-chi-development` (`$alaa-go-chi-development`) `references/12-kit-capability-map.md`.
Name the kit package that would own your shape; if you can name one, you are re-implementing. Three narrow
automated gates exist — `make lint-structtags`, `make lint-metricnames`, `make contracttest` — and each catches
one specific re-implementation. **There is no general "did you re-implement a kit surface" analyzer**; this
check is a human reading the inventory, and a review that skips it has not tested P1.

**When the kit's shape does not fit**, the answer is never a local fork. File one timestamped change request in
the kit repository's `docs/change-requests/YYYY-MM-DD-<slug>.md` through `/alaa-go-chi-development`
(`$alaa-go-chi-development`) — that skill owns the channel and the template. The only sanctioned interim form is
a thin wrapper marked `KIT-WRAP` with the request already filed and a maximum lifetime of two kit releases.
Review question for every diff: *does anything in this change re-state a shape the kit already owns?*

## P2 — Route Posture Is Declared, Never Implied

Every route is registered under exactly one family — `Trusted`, `Anonymous`, `ProviderFacing`, `Operational` —
in the router builder. A route whose trust posture must be inferred from its handler body is a security review
failure, not a style issue: the reviewer, the pen-tester, and the next agent must all be able to read a route's
authentication and authorization story from the routing table alone.

```go
// WRONG — posture invisible; is this authenticated? project-scoped? nobody can tell from here
r.Post("/api/v1/news", h.Create)

// RIGHT — posture, permission, and step-up requirements read like a sentence
routes.Trusted(r, func(t chi.Router) {
    t.With(
        trustkit.RequirePermission(perm.NewsUserCanSendToHisShobe /* …evaluated by grant rules */),
        trustkit.RequireTOTP("news.insert"),
    ).Post("/api/v1/news", h.Create)
})
```

Family meanings, exactly: `Trusted` = full gateway context required; `Anonymous` = project context only (the
gateway injects `X-Project-Id` on every proxied request, authenticated or not) and never branches on user
identity; `ProviderFacing` = no trusted headers at all, the route owns its own verification (webhooks);
`Operational` = health, readiness, and metrics with their exact platform envelopes.

**Proof.** The router fails closed. `httpkit`'s route inventory returns `ErrUnlabeledRoute` — *"httpkit: route
is not registered through a route family"* (`httpkit/route_inventory.go`) — for any route that reached the mux
without a declared family, and a nil posture is a refusal rather than a default. `contracttest`'s route-inventory
conformance asserts the registered inventory as black-box HTTP behavior. Run `make contracttest`
(`go test ./contracttest/...`) in the service; a route you forgot to label cannot pass it.

## P3 — TrustCtx or Nothing: No Raw Headers Past the Edge

Identity, project, permissions, location, and TOTP metadata are parsed **once** by `trustkit` into an immutable
`TrustCtx`. Handlers, use cases, and repositories never touch `r.Header`, never re-parse `X-Access`, and never
accept identity from body or query on trusted routes (root's explicit `project_id` parameter is authorized by
the root permission *first*). The identity types are settled platform truth: `X-Project-Id` is a **UUIDv7
string**, `X-User-Id` is a **positive int64** (`users.id`). Code that parses either differently is wrong even
when it appears to work.

```go
// WRONG — re-parsing trusted headers deep in a use case; type drift and spoofing bugs live here
func (uc *CreateNews) Handle(r *http.Request) error {
    projectID, _ := strconv.Atoi(r.Header.Get("X-Project-Id")) // int?! it's a UUIDv7
    ...
}

// RIGHT — one typed context, injected; the use case never sees HTTP
func (uc *CreateNews) Handle(ctx context.Context, tc trustkit.TrustCtx, in CreateNewsInput) error {
    if !tc.Can(perm.NewsUserCanSendPublic) && in.Visibility == VisibilityPublic {
        return errkit.Denied("NEWS_AUDIENCE_SCOPE_DENIED")
    }
    ...
}
```

**Proof, two halves.** Inward, run this from the service repository root — every hit is a P3 violation, and the
inward layers are the only place the pattern is forbidden outright:

```sh
grep -rn --include='*.go' -e 'Header\.Get(' -e '"X-Access"' -e '"X-Project-Id"' -e '"X-User-Id"' \
  internal/domain internal/application
```

At the edge, `contracttest.AssertTrustBoundary` proves the boundary as black-box HTTP conformance: a malformed
trusted request renders the canonical 401 envelope, a denied permission the 403 envelope, a missing step-up the
TOTP challenge. Run `make totp-contract` in the kit, or the service's own `contracttest` suite. No analyzer
enforces the grep — wire it into the service's CI lint job yourself, or it runs only when someone remembers.

Why this is a principle and not a preference: every place that re-parses a trusted header is a place where a
type change, a header rename, or a spoofing-defense update must be found and fixed — and the one place nobody
finds is the vulnerability. Header semantics themselves (which claim feeds which header, bitmap packing) are
owned by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`); read it rather than encoding assumptions.

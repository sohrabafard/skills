# Contract Before Implementation

`SKILL.md` owns the rule that the contract is decided in the record and committed before the code that
satisfies it. This file says how to enumerate the interfaces, what a data shape must fix, how to derive an
error surface, and where the contract is committed. Read it during step 3.

`/alaa-services-contract` (`$alaa-services-contract`) owns the platform invariants: response envelopes,
correlation and trusted gateway headers, the public identifier boundary, the trust boundary, event and code
names, and the deprecation procedure. Satisfy and cite them. Nothing in this file restates one, because a
restated envelope is a second envelope the moment the contract changes.

## Enumerate every interface, in and out

Work from the journeys, not from the code you intend to write. A design that lists only synchronous routes
has left its asynchronous surfaces to be discovered by the first consumer.

Eight kinds, each enumerated or explicitly marked none:

1. synchronous routes this subsystem serves;
2. synchronous calls this subsystem makes;
3. events it emits;
4. events it consumes;
5. jobs or commands it enqueues, and the queue that carries them;
6. jobs or commands it consumes;
7. scheduled triggers it owns;
8. anything else that reads or writes its state — an operator action, an admin panel, a migration, a report
   query, another component reading its datastore directly.

The eighth kind exists to make one specific defect visible: **another component reading this subsystem's
datastore directly is an interface with no contract.** Record it as an interface, then decide in step 4
whether it becomes a contract or is removed; leaving it unlisted means the next schema change breaks a
consumer nobody knew existed.

For each interface record: the caller, the direction, whether it crosses the trust boundary, whether it is
synchronous or asynchronous, and whether repeating it is safe. The last one is not a detail — it decides in
step 5 whether a retry is legal at all, and `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns what
that requires.

## Fix the data shape

For every field crossing an interface, fix: name, type, whether it may be absent, whether it may be null,
its unit or precision where it carries a quantity, and its identifier kind where it identifies something.

Three field-level rules, each of which resolves a defect that is expensive to fix after release:

- **Absent and null mean the same thing, or they are two different fields.** When absence means "unknown"
  and null means "known to be empty", say so; when they mean the same, permit exactly one of them. A
  consumer that guesses will guess differently from the next consumer.
- **A quantity carries its unit in the design, not in the field name alone.** State the unit and the
  precision. A number with an assumed unit is the defect class that survives every test written by the
  person who assumed it.
- **An enumeration is closed or open, and the design says which.** Closed means a consumer may reject an
  unknown value; open means a consumer must tolerate one, and the design states what it does with it.
  Adding a value to a closed enumeration is a breaking change and goes through deprecation.

Identifier kinds at the boundary — which identifier is public, which is internal, and what may cross —
are `/alaa-services-contract`'s. Cite the rule and apply it; a design that invents an identifier shape has
created a second boundary.

## Derive the error surface

The error surface is the set of outcomes a caller must be able to distinguish, and what each obliges the
caller to do. Derive it rather than listing plausible errors:

1. Take every dependency from step 5 and every validation the interface performs.
2. Map each failure onto exactly one caller-visible outcome. **A dependency failure with no mapped outcome
   will be mapped by whichever exception escapes first**, which is how one dependency's timeout becomes a
   generic 500 that the caller retries into an outage.
3. For each outcome state: is it retryable by the caller, is it permanent, does it carry a correlation
   identifier, and does it distinguish "this will never work" from "try later". The doctrine for retry
   legality belongs to `/alaa-reliability-sla`; this step only ensures the caller can tell the two apart.
4. Collapse outcomes a caller would treat identically. An error surface with more outcomes than the caller
   has behaviours is noise that consumers will map back down inconsistently.

A design that documents the success shape and stops has not specified the interface, because the failure
outcomes are the half a caller writes the most code against.

## Compatibility

For every interface the design changes, state per consumer whether the consumer must change, and when.
Classify each change as additive — new optional field, new outcome in an open enumeration, new interface —
or breaking — removed or renamed field, narrowed type, new required field, new value in a closed
enumeration, changed meaning of an existing field.

**A changed meaning with an unchanged shape is a breaking change and the most dangerous one**, because no
schema check catches it and every consumer keeps compiling. When the design changes what a field means,
rename the field.

The deprecation window, the parallel-run rules, and the removal procedure are
`/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md`. Cite it; do not invent
a window.

## Where the contract is committed

Where the repository holds a machine-readable contract — an API description, an event schema, a generated
client, a shared DTO package — the first implementation lane changes it, and the record points at the file
rather than repeating the fields. Where no machine-readable contract exists, the record carries the shapes
in full, and the design says whether creating one is in scope.

Either way the ordering is the same and is checkable in history: the commit that first states the shape
precedes the commit that adds the handler, the consumer, or the route.

## Anti-patterns

- writing the handler and generating the contract from what it returns, which documents an implementation
  accident as a promise;
- an error surface listing HTTP status codes with no statement of what the caller does with each;
- a new required field added to an existing interface and called additive;
- a shared DTO package changed for one consumer's convenience, which turns one team's convenience into
  every consumer's release;
- an interface enumerated as "internal only" that a second service already calls — internal describes the
  network, not the contract.

# Untrusted Input: Validation And Injection

Read when the inventory shows request-derived data reaching a query, a shell, a template, a deserializer, a document parser, a path, a response header, or a redirect target.

**A value is trusted because a control verified it, not because of where it arrived from.** A queue payload, a cache entry, a cookie, a webhook body, a value read back from your own database after a client wrote it, and an expired-but-signed token are all untrusted input.

## Validation

**Every entry point validates its input against a declared schema before any business logic reads it, and the schema is the only place that shape is defined.**

- **Reject, never repair.** A value outside the schema produces a rejection with a stable error code. A validator that trims, truncates, or coerces a non-conforming value approved a value the sink never receives.
- **Order: decode once, canonicalise, validate, use.** A validator that runs before transport decoding is bypassed by encoding the payload. A validator that runs before Unicode normalisation is bypassed by a homoglyph or a combining sequence. A value decoded twice - once at the boundary, once at the sink - was validated in a form the sink never sees.
- **Allowlist per constrained field**: an enum, a numeric range bounded at both ends, a length bound, or a regular expression anchored at both ends. A blocklist of dangerous substrings is reported as a finding, never accepted as the control.
- **Unknown fields**: the decoder's behaviour on a field the schema does not declare is chosen explicitly in code - reject or ignore. Silent ignoring is how mass assignment survives review.
- **Mass assignment**: no request body is passed whole to a model constructor, an update, a merge, or a patch. Writable fields are an explicit per-endpoint allowlist, and no field carrying authorization meaning is in it - tenant or project id, owner id, role, permission, status, price, balance, quota, or any verified flag.
- **Bound every number** that reaches a limit, offset, page size, quantity, retry count, or allocation. An unbounded integer from a request is a resource-exhaustion path on a shared fleet.
- **Bound every body.** Each entry point has a maximum request-body size enforced by the framework or the reverse proxy; the review names the file where the ceiling is set.

### Per stack

The rule above is universal; the mechanism is not. Use the mechanism the repository already has - introducing a second validation library is a finding, not a fix.

- **Laravel / PHP**: a Form Request, or an explicit `validate()` call, on every write endpoint. `$fillable` is enumerated; `$guarded = []` and `Model::unguard()` are findings. `request()->all()` never reaches `create`, `update`, or `fill`.
- **Go**: decode into a declared struct, never into `map[string]any` that is then indexed. `json.Decoder.DisallowUnknownFields()` when the chosen behaviour is reject. Validate through the repository's existing validator before use.
- **Node / TypeScript**: parse at the boundary with the repository's schema validator and carry the parsed type downstream. A TypeScript interface is a compile-time claim and validates nothing at runtime; an `as` cast on a request body is an unvalidated input.

## Injection: the general rule

**For every place the service builds a string another interpreter will parse, the untrusted parts travel as data through that interpreter's own parameter mechanism, and never as text spliced into the string.** Each interpreter below names its mechanism and what to flag.

## SQL

Bound parameters. No concatenation, no interpolation, no driver option that renders parameters client-side into a statement string.

The parts of a statement that cannot be parameterised - table names, column names, `ORDER BY` targets, sort direction, and the arity of an `IN` list - come from a server-side map from a client-supplied token to a fixed identifier. They never come from client text, and never from a quoting or escaping helper: escaping an identifier is not the same problem as escaping a value, and the helpers that exist for it are per-dialect and routinely wrong on edge cases.

Flag when:

- any SQL fragment is built with string concatenation, interpolation, `sprintf`, or a template
- a raw-SQL escape hatch receives a value derived from a request: `DB::raw`, `whereRaw`, `havingRaw`, `orderByRaw`, `selectRaw`, `DB::statement`, `db.Exec(fmt.Sprintf(...))`, `.Raw(`, `queryRawUnsafe`, `$queryRaw`
- `ORDER BY`, a column list, a table name, or a `LIMIT` is assembled from a request field
- a search or filter parameter is passed through to a query builder as an operator, a comparison, or an expression
- a stored procedure or database function concatenates its arguments internally - parameterising the call does not parameterise what the procedure does with it
- a migration or seeder interpolates a value that originated outside the repository

## Document stores and NoSQL

Coerce every untrusted value to its expected scalar type before it reaches a query, so a JSON object cannot arrive where a scalar was expected and be interpreted as an operator. No decoded request body, and no sub-object of one, is passed into a filter, projection, sort, or update position.

Flag when:

- a filter, projection, sort, or update document is assembled from request data without per-field type coercion
- a request field typed `any`, `interface{}`, `mixed`, or `object` reaches a filter position
- `$where`, `$expr`, `$function`, `mapReduce`, or an aggregation stage contains request-derived text
- a key in a filter document comes from request data, rather than a value in a filter whose key is fixed

## Shell and subprocess

Execute the program by path with an argument vector. Never hand a command line to a shell.

No untrusted value becomes an argument the target program interprets as an option: place request-derived arguments after `--` where the program supports it, and reject or prefix with `./` any value that could begin with `-`. Where the operation exists as a library call in the language, the library call replaces the subprocess.

Flag when:

- `shell=True`, `sh -c`, `bash -c`, backticks, `system()`, `exec()`, `popen()`, `passthru()`, `proc_open` with an interpolated string, or `os/exec` with a shell as the program
- a request-derived value becomes an argument to `tar`, `zip`, `unzip`, `ffmpeg`, `convert` / ImageMagick, `curl`, `wget`, `git`, `ssh`, `rsync`, `find -exec`, `xargs`, `pandoc`, or a PDF or document renderer, without an allowlist on the value
- an environment variable for a child process is set from request data - `PATH`, `IFS`, `LD_PRELOAD`, `LD_LIBRARY_PATH`, `GIT_SSH_COMMAND`, `BASH_ENV`, `PERL5OPT`, `PYTHONPATH`, `NODE_OPTIONS` are each a code-execution path
- a filename from a request reaches a subprocess argument at all: see the storage-key rules in `30-outbound-fetch-and-files.md`

## Template engines

A template is a server-controlled artifact selected from a fixed set. Request data is passed as template **variables**. It is never concatenated into template source, and never used to select a template path outside an explicit allowlist map.

Flag when:

- a template is compiled or rendered from a string built at request time: `Blade::render`, `twig->createTemplate`, `template.New(...).Parse(userText)`, Jinja `from_string`, `Handlebars.compile(userText)`, `new Function`
- a template name or path comes from a request field without an allowlist map
- an email, notification, or export body is produced by rendering user-supplied text as a template
- a product feature offers tenant-supplied templates. If the product requires it, the engine is a logic-free interpolation engine over a fixed variable set, not a general template engine, and the review names which one is in use and what it can reach.

## Deserialization

**Untrusted bytes are parsed only by a parser that cannot instantiate types named in the input and cannot invoke code.** The positive form: decode into a declared struct or schema, with unknown-field behaviour chosen explicitly.

Flag when:

- **PHP**: `unserialize()` on request, cookie, cache, session, or queue data. Where a plain structure must be recovered, `unserialize($x, ['allowed_classes' => false])` is the only acceptable form; a populated `allowed_classes` list still admits every gadget those classes reach.
- **Python**: `pickle`, `marshal`, `dill`, `shelve`, `jsonpickle`, `yaml.load` without `SafeLoader`, `numpy.load` with `allow_pickle=True`
- **Java**: `ObjectInputStream`, Jackson `enableDefaultTyping` or `@JsonTypeInfo` over a broad base type, SnakeYAML's default constructor, XStream without a type allowlist
- **.NET**: `BinaryFormatter`, `NetDataContractSerializer`, `LosFormatter`, `SoapFormatter`, `TypeNameHandling` other than `None`
- **Node**: `node-serialize`, an `eval`-based JSON reviver, `vm` without a locked context, and any recursive merge or path-set that accepts `__proto__`, `constructor`, or `prototype` as a key - prototype pollution turns a config merge into an application-wide behaviour change
- **Ruby**: `Marshal.load`, `YAML.load` outside `safe_load`
- **Any stack**: a signed payload deserialized *before* its signature is verified. Verification comes first, always; a gadget chain does not need the signature to be valid if the parse happens first.

## Document parsers that resolve external references

DTD processing and external entity resolution are disabled explicitly at every parser construction site, and entity expansion is bounded. A process-global toggle set once during boot is not the control, because any library that constructs its own parser resets it.

Flag when: a parser is constructed without the flags; `LIBXML_NOENT` or `LIBXML_DTDLOAD` appears; `XmlReaderSettings.DtdProcessing` is not `Prohibit`; a YAML loader resolves custom tags; a document-conversion, thumbnailing, or office-format library is invoked on untrusted files without disabling its external-fetch and macro options. An external reference resolved by a parser is also an outbound request - `30-outbound-fetch-and-files.md` owns where it may go.

## Path construction

No component of a filesystem path or an object-store key comes from request data. Where a client identifier must select a stored object, it selects a row through a tenant-scoped query and the path is built from server-held columns.

Where the design genuinely requires a client-supplied path component, it is validated against an anchored allowlist pattern **and** the resolved absolute path is confirmed to be inside the intended root **after** resolution. Checking before resolution is defeated by `..`, by percent-encoded and double-encoded traversal, by Unicode normalisation, by a Windows short name, and by a symlink.

Flag when: a path is checked for `..` by substring before resolution; a path is joined with a request value; an archive is expanded without validating each entry's resolved destination (`zip-slip`); a symlink in an untrusted tree is followed by a copy, move, or read.

## Header, redirect, log, and email injection

- No request-derived value reaches a response header, a `Location` value, a `Set-Cookie` attribute, or an email header without validation against a pattern that excludes CR, LF, and NUL.
- A redirect target from request data is resolved against a server-side allowlist of paths or hosts. A relative path is validated to begin with exactly one `/` and not with `//` or `/\`, both of which are protocol-relative in browsers.
- Values that appear in logs are passed as **structured fields**, never concatenated into the message text, so a newline or a fabricated key in user input cannot forge a log record. The audit trail is a security control, and a forgeable record is not evidence.

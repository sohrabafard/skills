// The fleet safety-control variable register, in machine-readable form.
//
// The prose form of this register, with the argument for every entry, is
// `alaa-docker-production references/25-fail-closed-interpolation.md`. This file and that file
// state the same register; when they disagree, that file is the specification and this file is the
// defect. Keep the `id` values identical in both so a finding can be traced to its paragraph.
//
// Two classes, because "a default would silently disable a safety control" has two shapes.
//
//   class A — "no default is ever correct". The value cannot be invented by the file that uses
//   it: it is a credential, a key, a token or a signing input. Any `:-` form is a violation,
//   including `:-` with an empty default, because an empty password is a password the process
//   will try to authenticate with and a broker or database configured to trust it will accept it.
//
//   class B — "the default is the disabling value". The variable names a control that may
//   legitimately carry a default, and the defect is the specific default that turns the control
//   off: an empty or zero cap (which most servers read as unlimited), a permissive value for an
//   authentication or verification toggle, or a wildcard for an allowlist. A class-B variable
//   with a real restrictive default in the file is not a finding.
//
// To extend the register: add an entry here and the matching paragraph in `references/25-…`, or
// pass `--register <file.json>` holding `{"entries":[{id,class,pattern,why,disabling?}]}`, or
// declare it in the Compose file itself with a comment
// `# safety-control: VAR_NAME — why it is a safety control`.

export const REGISTER = [
  {
    id: 'sc-password',
    class: 'A',
    pattern: '(^|_)(PASSWORD|PASSWD|PASS)$',
    why: 'A database, broker, cache or admin password. A default makes the file itself a credential source, so a service that forgot to set the variable authenticates with whatever the file says instead of failing to start. An empty default is the worst case: PostgreSQL with trust or md5 auth and RabbitMQ both accept an empty password from a client that offers one, so the deployment comes up looking healthy with no credential in play.',
  },
  {
    id: 'sc-secret',
    class: 'A',
    pattern: '(^|_)SECRET($|_)',
    why: 'A shared secret used to sign, encrypt or authenticate. A default value is published in the repository the moment the file is committed, so every environment that forgets to override it shares one attacker-known secret.',
  },
  {
    id: 'sc-token',
    class: 'A',
    pattern: '(^|_)TOKEN$',
    why: 'A bearer credential presented to another system. A default is either an invalid token that fails at first call in production, or a real token committed to the repository.',
  },
  {
    id: 'sc-key',
    class: 'A',
    pattern: '(^|_)(KEY|PRIVATE_KEY|PUBLIC_KEY|API_KEY|ACCESS_KEY|SECRET_KEY|SIGNING_KEY|ENCRYPTION_KEY|KEYFILE|KEY_PATH)$',
    why: 'Application, signing and encryption key material. Laravel APP_KEY is the canonical case: with a defaulted APP_KEY every environment can decrypt every other environment\'s cookies and encrypted columns, and rotating it is a data-loss event rather than a config change.',
  },
  {
    id: 'sc-credentials',
    class: 'A',
    pattern: '(^|_)(CREDENTIALS|DSN|CONNECTION_STRING)$',
    why: 'A compound value that carries a credential inside it. Defaulting it hides the credential from every grep that looks for PASSWORD or SECRET.',
  },
  {
    id: 'sc-admin-password',
    class: 'A',
    pattern: '^(DB_PROVISION_ADMIN_PASSWORD|POSTGRES_PASSWORD|MYSQL_ROOT_PASSWORD|RABBITMQ_DEFAULT_PASS|REDIS_PASSWORD)$',
    why: 'A superuser credential for shared infrastructure. It is named explicitly because these are the variables whose vendor images accept a well-known default, so the failure is silent: the container starts, the port answers, and the account has the password the whole internet already knows.',
  },
  {
    id: 'sc-tls-verification',
    class: 'B',
    pattern: '(VERIFY_PEER|VERIFY_HOST|TLS_VERIFY|SSL_VERIFY|VERIFY_SSL|VERIFY_TLS|CERT_VERIFY)',
    why: 'Certificate verification. Turning it off converts every TLS connection into an unauthenticated encrypted channel, which no probe and no dashboard will report as broken.',
    disabling: ['false', '0', 'off', 'no', 'none', 'disabled', ''],
  },
  {
    id: 'sc-insecure-flag',
    class: 'B',
    pattern: '(INSECURE|SKIP_VERIFY|ALLOW_INSECURE|DISABLE_AUTH|DISABLE_SSL|DISABLE_TLS|NO_VERIFY)',
    why: 'A negatively worded control. The disabling value is the true one, so the usual "default false is safe" instinct is inverted and reviewers miss it.',
    disabling: ['true', '1', 'on', 'yes', 'enabled'],
  },
  {
    id: 'sc-auth-toggle',
    class: 'B',
    pattern: '(^|_)(AUTH_ENABLED|AUTH_REQUIRED|REQUIRE_AUTH|AUTHENTICATION_ENABLED|SIGNATURE_REQUIRED|AUTHORIZATION_ENABLED)$',
    why: 'The switch that decides whether requests are authenticated at all. A false default produces a service that answers every caller and emits no error, which looks identical to a healthy service in every metric this fleet collects.',
    disabling: ['false', '0', 'off', 'no', 'none', ''],
  },
  {
    id: 'sc-size-cap',
    class: 'B',
    pattern: '(MAX_UPLOAD|UPLOAD_MAX|MAX_BODY|BODY_LIMIT|MAX_REQUEST_SIZE|MAX_FILE_SIZE|CLIENT_MAX_BODY)',
    why: 'An upload or request-body cap. Nginx, HAProxy, PHP and most brokers read 0 or an empty value as "no limit", so the default that looks like the safest number is the one that removes the control.',
    disabling: ['0', '', '0b', '0k', '0m', '-1', 'unlimited', 'none'],
  },
  {
    id: 'sc-rate-limit',
    class: 'B',
    pattern: '(RATE_LIMIT|THROTTLE|MAX_ATTEMPTS|MAX_CONCURRENC|MAX_CONNECTIONS|PIDS_LIMIT)',
    why: 'A rate, concurrency or process cap that exists to stop one caller or one bug from consuming the node. Zero and empty mean unlimited in every implementation this fleet uses.',
    disabling: ['0', '', '-1', 'unlimited', 'none', 'false'],
  },
  {
    id: 'sc-allowlist',
    class: 'B',
    pattern: '(ALLOWED_ORIGINS|ALLOWED_HOSTS|CORS_ALLOWED|TRUSTED_PROXIES|TRUSTED_HOSTS|ALLOWED_IPS)',
    why: 'An allowlist. The wildcard default accepts everything, and for TRUSTED_PROXIES specifically a wildcard makes every client-supplied X-Forwarded-For header authoritative, which turns an IP allowlist elsewhere in the system into an attacker-controlled value.',
    disabling: ['*', '**', '0.0.0.0/0', '', 'all', 'any'],
  },
  {
    id: 'sc-debug',
    class: 'B',
    pattern: '^(APP_DEBUG|DEBUG|DEBUGBAR_ENABLED|TELESCOPE_ENABLED)$',
    why: 'Debug output. In Laravel a true APP_DEBUG renders the stack trace, the environment and the connection parameters into the HTTP 500 body, so the defect is an information-disclosure endpoint that is only reachable when something is already going wrong.',
    disabling: ['true', '1', 'on', 'yes'],
  },
];

const RE_CACHE = new Map();

function compiled(pattern) {
  if (!RE_CACHE.has(pattern)) RE_CACHE.set(pattern, new RegExp(pattern));
  return RE_CACHE.get(pattern);
}

/**
 * Classify a variable name against the register.
 * Returns null, or {id, class, why, disabling}.
 */
export function classify(name, extraEntries = []) {
  for (const entry of [...extraEntries, ...REGISTER]) {
    if (compiled(entry.pattern).test(name)) return entry;
  }
  return null;
}

/** True when `defaultValue` is one of the values that disables a class-B control. */
export function isDisablingDefault(entry, defaultValue) {
  const normalised = String(defaultValue).trim().toLowerCase();
  return (entry.disabling || []).some((d) => String(d).toLowerCase() === normalised);
}

export function validateExtraEntries(parsed, source) {
  if (!parsed || !Array.isArray(parsed.entries)) {
    throw new Error(`${source}: expected an object with an "entries" array`);
  }
  for (const entry of parsed.entries) {
    if (!entry.id || !entry.pattern || !entry.why) {
      throw new Error(`${source}: every entry needs id, pattern and why`);
    }
    if (entry.class !== 'A' && entry.class !== 'B') {
      throw new Error(`${source}: entry ${entry.id} needs class "A" or "B"`);
    }
    if (entry.class === 'B' && !Array.isArray(entry.disabling)) {
      throw new Error(`${source}: class-B entry ${entry.id} needs a "disabling" array`);
    }
    try {
      new RegExp(entry.pattern);
    } catch (err) {
      throw new Error(`${source}: entry ${entry.id} has an invalid pattern: ${err.message}`);
    }
  }
  return parsed.entries;
}

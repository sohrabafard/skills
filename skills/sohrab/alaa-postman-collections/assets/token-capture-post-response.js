// Post-response script template: capture an access token and everything the next
// request needs, so no value is ever copied by hand.
//
// Where this goes: the token-issuing request item's own `event` array, with
// `listen: "test"`, `script.exec` as an array of one string per line.
// Never `request.event`; Postman v2.1 does not execute scripts there.
//
// Fill in the four marked places. Keep every other line as written: each one
// carries a rule from references/42-scripts-and-state-capture.md.

// 1. EDIT: the response fields this route actually returns, proven from the
//    serializer or a saved example. Left side is the variable name the next
//    request references; right side is the JSON path.
const CAPTURE_MAP = {
  access_token: 'data.token.access_token',
  session_id: 'data.token.session_id',
};

// 2. EDIT: the success status this route returns on a token issue (200 or 201).
const SUCCESS_CODE = 200;

// --- nothing below needs editing for the common case ---

const readPath = (root, path) =>
  path.split('.').reduce((node, key) => (node == null ? undefined : node[key]), root);

// Writes to the environment, not to collection variables: the collection file is
// committed, and `pm.collectionVariables.set` mutates it in place, so a captured
// token would reach git on the next export. The environment file is committed with
// placeholders only.
const setEnv = (name, value) => {
  if (value === undefined || value === null || String(value) === '') {
    return false;
  }
  pm.environment.set(name, String(value));
  return true;
};

const body = (() => {
  try {
    return pm.response.json();
  } catch (error) {
    return null;
  }
})();

// The capture is guarded on an explicit success status. An error response must
// never overwrite a working token, and must never leave a half-written session.
const captured = [];
const missing = [];

if (pm.response.code === SUCCESS_CODE && body) {
  Object.keys(CAPTURE_MAP).forEach((name) => {
    const value = readPath(body, CAPTURE_MAP[name]);
    if (setEnv(name, value)) {
      captured.push(name);
    } else {
      missing.push(name + ' (' + CAPTURE_MAP[name] + ')');
    }
  });

  // 3. EDIT or DELETE: only when the route sets a refresh cookie. Reads the raw
  //    Set-Cookie header because a cookie jar is not replayed identically by every
  //    client. Replace `auth_refresh_token` with this service's cookie name.
  pm.response.headers
    .all()
    .filter((header) => String(header.key).toLowerCase() === 'set-cookie')
    .forEach((header) => {
      const match = String(header.value).match(/(?:^|;\s*)auth_refresh_token=([^;]*)/);
      if (match && match[1]) {
        setEnv('refresh_token', match[1]);
      }
    });
}

// Extraction failure is reported as a failing test, not swallowed. A silent failure
// leaves the previous token in place and the next request fails somewhere else with
// a misleading 401.
pm.test('Token capture wrote every variable the next request needs', function () {
  pm.expect(pm.response.code, 'token request did not succeed').to.eql(SUCCESS_CODE);
  pm.expect(missing, 'missing response fields: ' + missing.join(', ')).to.be.an('array').that.is.empty;
});

// 4. EDIT: assert the contract this request exists to satisfy, beyond the capture.
//    Add the envelope, content-type, and correlation-header assertions from
//    assets/response-tests-post-response.js. Never assert on the token's value.
pm.test('Issued token is a usable bearer credential', function () {
  const token = pm.environment.get('access_token');
  pm.expect(token, 'access_token variable is empty after capture').to.be.a('string').and.not.empty;
  pm.expect(token).to.not.include('replace-me');
});

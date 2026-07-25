// Post-response test template: the five assertions every request carries, plus the
// one assertion that is specific to the request.
//
// Where this goes: the request item's own `event` array, `listen: "test"`,
// `script.exec` as an array of one string per line. Never `request.event`.
//
// The rule this template exists to satisfy: a test that still passes against a
// plausible broken implementation is not a test. Asserting only `status === 200`
// passes against a handler that returns an empty body, the wrong resource, or
// another tenant's row. Every block below closes one of those holes.

// 1. EDIT: the success status this route returns.
const EXPECTED_CODE = 200;

// 2. EDIT: the one field this request exists to produce, as a JSON path, plus the
//    check that proves it is the right value and not merely present.
const SUBJECT_PATH = 'data.id';

const readPath = (root, path) =>
  path.split('.').reduce((node, key) => (node == null ? undefined : node[key]), root);

const body = (() => {
  try {
    return pm.response.json();
  } catch (error) {
    return null;
  }
})();

pm.test('Status is ' + EXPECTED_CODE, function () {
  pm.expect(pm.response.code).to.eql(EXPECTED_CODE);
});

pm.test('Response is JSON with the platform success envelope', function () {
  pm.expect(pm.response.headers.get('Content-Type') || '').to.include('application/json');
  pm.expect(body, 'response body is not parseable JSON').to.not.equal(null);
  // 3. EDIT only if this route is a documented exception to the platform envelope.
  //    The envelope itself is owned by `alaa-services-contract`; assert the shape
  //    that skill declares, and report drift rather than asserting the drift.
  pm.expect(body).to.have.property('data');
});

pm.test('Correlation header is returned', function () {
  pm.expect(pm.response.headers.has('X-Request-Id'), 'X-Request-Id missing').to.be.true;
});

pm.test('Response carries the value this request exists to produce', function () {
  const subject = readPath(body, SUBJECT_PATH);
  pm.expect(subject, SUBJECT_PATH + ' is absent').to.not.equal(undefined);
  // 4. EDIT: replace this with the check that would fail against a wrong value.
  //    A type check alone passes against a handler that returns a placeholder.
  pm.expect(subject).to.be.a('string').and.not.empty;
});

// 5. EDIT or DELETE: keep only the assertions this route's contract actually
//    defines. Delete a block rather than leave it asserting a value the route does
//    not return, because a test asserting an absent field fails for the wrong reason.
pm.test('Pagination envelope is coherent', function () {
  pm.expect(body.meta).to.be.an('object');
  pm.expect(body.meta).to.have.property('total');
});

# Security checklist: Transport Verification

## S7. Transport is encrypted and verified

**Predicate.** No `get_url` or `uri` task uses an `http://` URL, and none sets
`validate_certs: false`.

**Evaluate.**

```bash
bash scripts/validate_playbook_security.sh <target>
# CKV_ANSIBLE_1  uri disabling certificate validation
# CKV_ANSIBLE_2  get_url disabling certificate validation
# CKV2_ANSIBLE_1 uri over HTTP
# CKV2_ANSIBLE_2 get_url over HTTP
```

A task that sets `validate_certs: false` carries a comment naming the internal
certificate authority it is working around and a linked issue for installing
that authority on the target. "Only disable for testing" is not a rule, because
nothing distinguishes testing from production in the file.

A `get_url` that fetches an artifact states a `checksum`. Transport encryption
proves who served the bytes, not which bytes they served.

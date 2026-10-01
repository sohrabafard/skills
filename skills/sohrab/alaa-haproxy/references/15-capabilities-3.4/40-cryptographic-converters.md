# JWE and cryptographic converters

3.4 introduces `jwt_decrypt_jwk`, `jwt_decrypt_cert`, `jwt_decrypt_secret` and
`aes_cbc_enc`/`aes_cbc_dec`; JWT verification and AES-GCM already existed.
The decrypt converters require OpenSSL support, take a compact JWE and yield
raw plaintext; parsing/authentication/decryption errors return an empty string.
Configure `jwt.decrypt_alg_list` and `jwt.decrypt_enc_list` to the protocol's
allowlist; defaults retain supported
algorithms except RSA1_5, which is disabled. AWS-LC lacks the documented A128KW/
A192KW variants. Certificate decryption requires a loaded certificate with `jwt on`.
Treat unsupported algorithms, incorrect keys, malformed tokens and authentication-tag
failures as explicit authorization failure, never an empty authenticated identity.
3.4.4 fixed JWE secret-length validation and full-length AES-GCM tag enforcement.
Positive and negative vectors must validate those paths on 3.4.6.

Decryption does not validate issuer, audience, expiry, replay or application claims;
`/alaa-trust-gateway-auth` owns their meaning. AES-CBC alone is not authenticated
encryption. Do not log keys or plaintext, and bound token/input size and CPU cost.
Key distribution, authorization and acceptable algorithms require their security
owner before introducing a cryptographic example. `jwt_verify_cert` is a 3.3
addition, not new in 3.4.

# QUIC and HTTP/3

Read build requirements before configuring any HTTP/3 mode. Use the selected mode guide only after the binary/build gate is established.

## The build requirement, which comes before everything else

When selecting a TLS stack or deciding whether this binary can serve QUIC, read [build requirements and binary choices](./30-quic-http3/10-build-requirements.md).

## What to do when `haproxy -vv` reports no QUIC

When the binary reports no QUIC, read [build requirements and binary choices](./30-quic-http3/10-build-requirements.md).

## Frontend HTTP/3

Before advertising HTTP/3 to clients, read [build requirements and binary choices](./30-quic-http3/10-build-requirements.md), then read [frontend HTTP/3](./30-quic-http3/20-frontend-http3.md).

## Backend HTTP/3

Before configuring HTTP/3 to an origin, read [build requirements and binary choices](./30-quic-http3/10-build-requirements.md), then read [backend HTTP/3](./30-quic-http3/30-backend-http3.md).

## Tuning and naming

Before changing QUIC tuning directives, read [build requirements and binary choices](./30-quic-http3/10-build-requirements.md), then read [QUIC tuning and names](./30-quic-http3/40-quic-tuning.md).

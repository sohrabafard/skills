# Sources

Use this file when HAProxy branch, release, directive, container, chart, security, or observability behavior must be current.

## Freshness triggers

Re-check official sources when the user asks for latest/current behavior, branch status, a security-sensitive directive, TLS/QUIC/HTTP3 behavior, container or Kubernetes delivery, chart behavior, deprecations, or an upgrade across `3.2` and `3.3`.

## First-check official sources

- https://docs.haproxy.org/
- https://docs.haproxy.org/3.2/configuration.html
- https://docs.haproxy.org/3.2/management.html
- https://docs.haproxy.org/3.3/configuration.html
- https://docs.haproxy.org/3.3/management.html
- https://www.haproxy.org/download/3.2/src/
- https://www.haproxy.org/download/3.3/src/
- https://www.haproxy.org/download/3.2/doc/configuration.txt

## Official ecosystem sources

- https://hub.docker.com/_/haproxy/
- https://github.com/haproxytech/helm-charts
- https://www.haproxy.com/documentation/kubernetes-ingress/

## Useful official background

- https://www.haproxy.com/blog/announcing-haproxy-3-2
- https://www.haproxy.com/blog/announcing-haproxy-3-3
- https://www.haproxy.com/blog/state-of-ssl-stacks
- https://www.haproxy.com/user-spotlight-series/tls-and-haproxy-3-2-from-stunnel-to-native-tls-support

## Notes

- For version-sensitive work, prefer the docs index and release directories over older blog posts.
- Confirm the running build with `haproxy -vv` before relying on QUIC, TLS, tracing, or experimental directives.
- Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting after official manuals, release notes, `haproxy -vv`, and `haproxy -c -f ...` are checked.

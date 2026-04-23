# Official-first source map

Use this map before validating version-sensitive GitHub Actions content. GitHub Docs, action maintainer repositories, and tool docs outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- GitHub Actions docs home: https://docs.github.com/en/actions
- Workflow syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- Contexts: https://docs.github.com/en/actions/learn-github-actions/contexts
- Expressions: https://docs.github.com/en/actions/learn-github-actions/expressions
- Security hardening: https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- Runner images: https://github.com/actions/runner-images
- actionlint: https://github.com/rhysd/actionlint
- act: https://github.com/nektos/act
- GitHub Marketplace actions: https://github.com/marketplace?type=actions

## Freshness triggers

Fetch current official docs when validation depends on new events, runner labels, permission defaults, public action versions, OIDC behavior, cache/artifact major versions, actionlint diagnostics, act runtime behavior, or any security/current-version claim.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, discussions, and community blogs only to troubleshoot observed failures. Confirm workflow syntax, security findings, and action inputs against GitHub Docs, the action maintainer source, or tool docs.

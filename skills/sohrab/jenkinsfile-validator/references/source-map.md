# Official-first source map

Use this map before validating version-sensitive Jenkins pipeline content. Jenkins docs, plugin docs, and the target controller's actual plugin inventory outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- Jenkins Pipeline book: https://www.jenkins.io/doc/book/pipeline/
- Pipeline syntax reference: https://www.jenkins.io/doc/book/pipeline/syntax/
- Pipeline steps reference: https://www.jenkins.io/doc/pipeline/steps/
- Shared Libraries: https://www.jenkins.io/doc/book/pipeline/shared-libraries/
- Credentials handling: https://www.jenkins.io/doc/book/using/using-credentials/
- Jenkins security: https://www.jenkins.io/doc/book/security/
- Plugin site: https://plugins.jenkins.io/
- LTS upgrade guides: https://www.jenkins.io/doc/upgrade-guide/

## Freshness triggers

Fetch current Jenkins/plugin docs when validation depends on controller LTS version, plugin versions, deprecated steps, CPS behavior, credential masking, security advisories, or syntax/step parameters missing from local references.

## Troubleshooting-only sources

Use Stack Overflow, Jenkins issue threads, mailing lists, and community blogs only to troubleshoot symptoms. Confirm validation findings against Jenkins docs, plugin docs, or live controller metadata when available.

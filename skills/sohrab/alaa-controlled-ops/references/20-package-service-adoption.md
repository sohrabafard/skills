# Package And Service Adoption

## Adoption source

Normal service adoption should use a tagged `alaa/controlled-ops` package release from the Ala Satis Composer repository.

Use a sibling checkout only while developing the package itself. Do not commit a service dependency model that requires `../alaa-controlled-ops` unless the user explicitly asks for that temporary state.

## Package release checklist

Before asking a service to consume a new package tag:

- run package metadata validation
- run the package verifier
- run package PHPUnit tests when dependencies are installed
- run Composer audit when the advisory endpoint is reachable
- tag the verified package commit with the intended semantic version
- publish or refresh that tag in Satis

## Service adoption checklist

In the consuming service:

- require the approved package constraint
- run `composer update alaa/controlled-ops --with-dependencies`
- confirm `composer show alaa/controlled-ops --locked` reports the intended tag and a Satis dist URL
- reject lock files that record a path repository unless the task explicitly asked for local package development
- bind only the package contracts the service actually adopts
- keep public API shape and docs under the service repo

## Public surface rule

Do not introduce new service route families, Postman folders, queue jobs, or lifecycle actions just because the package has a helper. Add them only when the service implementation, tests, docs, and public artifact sync are part of the task.

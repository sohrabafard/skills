
# Validation and testing

## Validate config
Use:
- `vector --version`
- `vector validate /etc/vector/vector.yaml`
- or multiple files together if the topology is split

## Unit test transforms
Use:
- `vector test /etc/vector/vector.yaml`
- or separate pipeline/test files together

## Why it matters
- catches required-field/type issues early
- proves VRL behavior on real examples
- prevents rollout of fragile transformations
- makes large topologies maintainable
- verifies the runtime version used in CI/CD really matches the intended release

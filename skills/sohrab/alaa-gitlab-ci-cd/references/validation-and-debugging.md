# Validation and debugging

## Table of contents

- Validation ladder
- The bundled checkers: what they assert and what they cannot see
- Gate-eligible versus advisory, and who chooses
- Live GitLab validation
- The five failure classes
- Symptom map
- Debugging across multiple files

## Validation ladder

When selecting local validation steps, use [Static validation and checker limits](./validation-and-debugging/10-static-validation-and-checkers.md).

## The bundled checkers: what they assert and what they cannot see

When using bundled static checkers, use [Static validation and checker limits](./validation-and-debugging/10-static-validation-and-checkers.md).

### `validate_gitlab_ci.py`
For this detail, use [Static validation and checker limits](./validation-and-debugging/10-static-validation-and-checkers.md).

### `validate_runner_config.py`
For this detail, use [Static validation and checker limits](./validation-and-debugging/10-static-validation-and-checkers.md).

## Gate-eligible versus advisory, and who chooses

When deciding whether findings block a pipeline, use [Gate eligibility](./validation-and-debugging/40-gate-eligibility.md).

## Live GitLab validation

When validating merged configuration in GitLab, use [Live GitLab validation](./validation-and-debugging/20-live-validation.md).

## The five failure classes

Classify before editing anything. Editing a script when the pipeline was never
created wastes a full cycle.

For the class-based triage procedure, use [Failure-class triage](./validation-and-debugging/30-failure-class-triage.md); for literal symptoms or multi-file investigation, use [symptom lookup](./validation-and-debugging/50-symptoms-and-cross-file.md).

### 1. YAML or schema failure
For this detail, use [configuration failure triage](./validation-and-debugging/30-configuration-and-rule-failures.md#1-yaml-or-schema-failure).

### 2. Pipeline creation or rule evaluation failure
For this detail, use [configuration failure triage](./validation-and-debugging/30-configuration-and-rule-failures.md#2-pipeline-creation-or-rule-evaluation-failure).

### 3. Runner matching failure
For this detail, use [runner and runtime triage](./validation-and-debugging/40-runner-and-runtime-failures.md#3-runner-matching-failure).

### 4. Executor startup failure
For this detail, use [runner and runtime triage](./validation-and-debugging/40-runner-and-runtime-failures.md#4-executor-startup-failure).

### 5. Runtime failure
For this detail, use [runner and runtime triage](./validation-and-debugging/40-runner-and-runtime-failures.md#5-runtime-failure).

## Symptom map

When matching a literal failure message, use [Symptoms and cross-file debugging](./validation-and-debugging/50-symptoms-and-cross-file.md).

## Debugging across multiple files

When tracing includes or cross-file configuration, use [Symptoms and cross-file debugging](./validation-and-debugging/50-symptoms-and-cross-file.md).

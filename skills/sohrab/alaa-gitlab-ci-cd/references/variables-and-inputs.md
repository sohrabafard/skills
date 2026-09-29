# Variables and inputs

## Table of contents

- Choose the right mechanism
- What GitLab's expansion does and does not do
- Variable precedence
- Masked, protected and file variables
- `id_tokens:`, `secrets:` and secure files
- Inputs and components
- Rules and variable limitations
- Downstream pipelines and forwarding
- Debugging an unexpected value
- Variable inventory template

## Choose the right mechanism

When choosing between inputs, variables, file variables and dotenv, use [Mechanisms and expansion](./variables-and-inputs/10-mechanism-and-expansion.md).

## What GitLab's expansion does and does not do

When checking GitLab variable expansion rules, use [Mechanisms and expansion](./variables-and-inputs/10-mechanism-and-expansion.md).

## Variable precedence

When resolving which variable source wins, use [Variable precedence](./variables-and-inputs/20-variable-precedence.md).

## Masked, protected and file variables

When checking masking, protection or file-variable paths, use [Protected and file variables](./variables-and-inputs/30-protected-and-file-variables.md).

## `id_tokens:`, `secrets:` and secure files

When using job identity tokens, fetched secrets or secure files, use [Tokens and secure files](./variables-and-inputs/40-tokens-and-secure-files.md).

## Inputs and components

When designing typed inputs or reusable components, use [Inputs and components](./variables-and-inputs/50-inputs-and-components.md).

## Rules and variable limitations

When checking variable availability during rule evaluation, use [Rules and value availability](./variables-and-inputs/60-rules-and-value-availability.md).

## Downstream pipelines and forwarding

When controlling variables passed to downstream pipelines, use [Downstream forwarding](./variables-and-inputs/70-downstream-forwarding.md).

## Debugging an unexpected value

When diagnosing an unexpected variable value, use [Variable debugging and inventory](./variables-and-inputs/80-variable-debugging-and-inventory.md).

## Variable inventory template

When recording the source of custom values, use [Variable debugging and inventory](./variables-and-inputs/80-variable-debugging-and-inventory.md).

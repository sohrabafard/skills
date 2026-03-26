# Bash Script Validator Topic Map

Use this file to choose the smallest relevant section in `./full-guide.md`.

## Covered sections

- `# Bash Script Validator`
- `## Overview`
- `## When to Use This Skill`
- `## Validation Capabilities`
- `### 1. Syntax Validation`
- `### 2. ShellCheck Integration`
- `### 3. Security Checks`
- `### 4. Performance Optimizations`
- `### 5. Portability Checks (for sh scripts)`
- `### 6. Best Practices`
- `## Quick Start`
- `### Basic Validation`
- `# Validate a script`
- `# The validator will:`
- `# 1. Detect shell type from shebang`
- `# 2. Run syntax validation`
- `# 3. Run ShellCheck (if installed)`
- `# 4. Run custom security/optimization checks`
- `# 5. Generate detailed report`
- `### Example Output`
- `## Usage in Claude Code`
- `### Required Workflow`
- `### Example Response Format`
- `## Validation Results`
- `### Issue 1: Unquoted Variable (Line 25)`
- `### Issue 2: ...`
- `## Comprehensive Documentation`
- `### Core References`
- `#### bash-reference.md`
- `#### shell-reference.md`
- `#### shellcheck-reference.md`
- `### Tool References`
- `#### grep-reference.md`
- `#### awk-reference.md`
- `#### sed-reference.md`
- `#### regex-reference.md`
- `#### common-mistakes.md`
- `## Example Scripts`
- `## Validation Script Features`
- `### Automatic Shell Detection`
- `### Multi-Layer Validation`
- `### Exit Codes`
- `## Installation Requirements`
- `### Required`
- `### ShellCheck Installation Options`
- `# macOS`
- `# Ubuntu/Debian`
- `# Fedora`
- `# The wrapper automatically installs shellcheck-py in a venv`
- `# Requires: python3 and pip3`
- `# Cache location: ~/.cache/bash-script-validator/shellcheck-venv`
- `# Clear cache: ./scripts/shellcheck_wrapper.sh --clear-cache`
- `## Common Validation Scenarios`
- `### Scenario 1: Converting Bash Script to POSIX sh`
- `# 1. Validate current bash script`
- `# 2. Change shebang to #!/bin/sh`
- `# 3. Re-validate - catches bashisms`
- `# 4. Reference shell-reference.md for POSIX alternatives`
- `# 5. Fix bashisms (arrays → set --, [[ ]] → [ ], etc.)`
- `# 6. Re-validate until clean`
- `### Scenario 2: Security Audit`
- `### Scenario 3: Performance Optimization`
- `## Integration with Development Workflow`
- `### Pre-commit Hook`
- `#!/bin/bash`
- `### CI/CD Integration`
- `# Example for GitHub Actions`
- `## Learning Resources`
- `## Best Practices`
- `### For Script Authors`
- `### For Reviewers`
- `## Technical Details`
- `### Directory Structure`
- `### Validation Logic`
- `## Resources`
- `### Official Documentation`
- `### Internal References`

## Working rule

- Read only the sections you need from `./full-guide.md`.
- Keep this topic map small and update it when major sections are added or renamed.

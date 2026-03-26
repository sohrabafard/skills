# Fluent Bit Config Validator Topic Map

Use this file to choose the smallest relevant section in `./full-guide.md`.

## Covered sections

- `# Fluent Bit Config Validator`
- `## Overview`
- `## When to Use This Skill`
- `## Validation Workflow`
- `### Stage 1: Configuration File Structure`
- `### Stage 2: Section Validation`
- `#### SERVICE Section Checks`
- `#### INPUT Section Checks`
- `#### FILTER Section Checks`
- `#### OUTPUT Section Checks`
- `#### PARSER Section Checks`
- `### Stage 3: Tag Consistency Check`
- `### Stage 4: Security Audit`
- `# Before (insecure)`
- `# After (secure)`
- `### Stage 5: Performance Analysis`
- `# Good configuration`
- `### Stage 6: Best Practice Validation`
- `### Stage 7: Dry-Run Testing`
- `### Stage 8: Documentation Lookup (if needed)`
- `### Stage 9: Report and Fix Issues`
- `# Fix 1: Add missing Host parameter`
- `# Fix 2: Add Mem_Buf_Limit to prevent OOM`
- `# Fix 3: Use environment variable for password`
- `## Common Issues and Solutions`
- `### Configuration Errors`
- `### Tag Routing Issues`
- `# Logs are generated but don't appear in output`
- `### Memory Issues`
- `# Container or process killed due to memory`
- `### Security Issues`
- `## Integration with fluentbit-generator`
- `## Resources`
- `### scripts/`
- `### tests/`
- `# Test on valid config`
- `# Test on invalid config (should report errors)`
- `# Test all configs`
- `### Documentation Sources`

## Working rule

- Read only the sections you need from `./full-guide.md`.
- Keep this topic map small and update it when major sections are added or renamed.

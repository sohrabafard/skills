# Fluent Bit Config Generator Topic Map

Use this file to choose the smallest relevant section in `./full-guide.md`.

## Covered sections

- `# Fluent Bit Config Generator`
- `## Overview`
- `## When to Use This Skill`
- `## Configuration Generation Workflow`
- `### Stage 1: Understand Requirements`
- `### Script vs Manual Generation`
- `# REQUIRED: Run --help to check if your use case is supported`
- `# Generate configuration for a supported use case`
- `### Consulting Examples Before Manual Generation`
- `### Stage 2: Plugin Documentation Lookup (if applicable)`
- `### Stage 3: SERVICE Section Configuration`
- `### Stage 4: INPUT Section Configuration`
- `#### Kubernetes Pod Logs (DaemonSet)`
- `### Stage 5: FILTER Section Configuration`
- `#### Kubernetes Metadata Enrichment`
- `### Stage 6: OUTPUT Section Configuration`
- `#### Elasticsearch`
- `#### Grafana Loki`
- `#### AWS S3`
- `#### Kafka`
- `#### AWS CloudWatch Logs`
- `#### OpenTelemetry (OTLP)`
- `#### Prometheus Remote Write`
- `#### HTTP Endpoint`
- `#### stdout (debugging)`
- `### Stage 7: PARSER Section Configuration`
- `# Read the examples/parsers.conf file to see available parsers`
- `# parsers.conf - Add custom parsers alongside existing ones`
- `### Stage 8: Complete Configuration Structure`
- `# fluent-bit.conf`
- `### Stage 9: Best Practices and Optimization`
- `#### Performance Optimization`
- `#### Reliability`
- `#### Security`
- `#### Resource Limits`
- `#### Logging Best Practices`
- `### Stage 10: Validate Generated Configuration`
- `## Error Handling`
- `### Common Issues and Solutions`
- `## Communication Guidelines`
- `## Integration with $fluentbit-validator`
- `## Resources`
- `### scripts/`
- `### examples/`
- `## Documentation Sources`

## Working rule

- Read only the sections you need from `./full-guide.md`.
- Keep this topic map small and update it when major sections are added or renamed.

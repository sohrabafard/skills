# Dashboard Dataset Workflow

Use these files with OpenAI Datasets and Prompt Optimizer:

1. Upload one or more `datasets/*.jsonl` files into Datasets.
2. Mark high-risk skills first: `alaa-trust-gateway-auth`, `alaa-data-layer`, `alaa-php-clean-code`, `caas-arvan-kuber`, `bash-script-generator`, `dockerfile-generator`, `gitlab-ci-generator`, and `promql-validator`.
3. Add human annotations for Good/Bad and specific routing critiques.
4. Add graders for:
   - correct skill activation
   - correct companion-skill selection
   - suppression of over-triggering
   - concise routing quality
   - domain-safe guidance
5. Use Prompt Optimizer only on top-level descriptions and routing blocks, never on long reference files.
6. Manually review optimized prompts before adoption.

# Install the OpenFGA vendor

Run commands from the repository root.

First add the vendor skill:

```bash
git remote add openfga-upstream https://github.com/openfga/agent-skills.git
git subtree add --prefix vendor/openfga-agent-skills openfga-upstream main --squash
```

Update later with:

```bash
git fetch openfga-upstream
git subtree pull --prefix vendor/openfga-agent-skills openfga-upstream main --squash
node vendor/openfga-agent-skills/scripts/build-agents-md.js
```

The installer links its skills through the generated [`Source roots` block](../../install-skills.md#source-roots).

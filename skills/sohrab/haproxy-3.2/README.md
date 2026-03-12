# HAProxy 3.2 LTS Skill Pack

This pack contains:
- SKILL.md: the main operator skillbook
- examples/haproxy/: ready-to-adapt HAProxy configuration examples
- examples/kubernetes/: Kubernetes manifests for running HAProxy as a Deployment
- examples/helm/: Helm values patterns and notes
- examples/gitlab-ci/: pipeline validation snippet
- references/: links + notes

You should:
1) Read SKILL.md
2) Pick the closest example config
3) Validate: haproxy -c -f <cfg>
4) Deploy using your preferred method (systemd / container / Helm)

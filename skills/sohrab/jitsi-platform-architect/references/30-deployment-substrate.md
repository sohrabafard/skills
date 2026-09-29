# Deployment Substrate

Read this when choosing or defending a substrate for Jitsi, when exposing JVB or TURN, or when handing a
requirement to a cluster team.

This file owns what the media plane demands of a substrate. It does not own substrate mechanics: chart values,
manifests, rollout strategy and namespace policy belong to `/alaa-k8s-helm` and, on Arvan, to
`/caas-arvan-kuber`; image hardening, Compose and Swarm delivery belong to
`/alaa-docker-production`; edge termination, TLS and websocket proxying belong to
`/alaa-haproxy`. Every upstream packaging and support-tier claim below has a row in
`references/90-source-map.md`.

Before writing any Jitsi manifest, read [Substrate selection and platform matrix](./30-deployment-substrate/10-selection-and-platform-matrix.md#the-selection-rule), answer the four substrate questions there, and record the answers in the deliverable. This prerequisite applies to every manifest, whatever component or substrate it describes.

## The selection rule
When choosing or defending a Jitsi deployment substrate, read [Substrate selection and platform matrix](./30-deployment-substrate/10-selection-and-platform-matrix.md) for substrate selection and platform matrix.

## Platform matrix
When comparing substrate fit and cautions, read [Substrate selection and platform matrix](./30-deployment-substrate/10-selection-and-platform-matrix.md) for substrate selection and platform matrix.

## Debian or VM installs
When deploying on a virtual machine or host, read [VM and container substrates](./30-deployment-substrate/20-vm-and-container-substrates.md) for vm and container substrates.

## Docker Compose
When deploying with Docker Compose, read [VM and container substrates](./30-deployment-substrate/20-vm-and-container-substrates.md) for vm and container substrates.

## Docker Swarm
When deploying with Docker Swarm, read [VM and container substrates](./30-deployment-substrate/20-vm-and-container-substrates.md) for vm and container substrates.

## Kubernetes with Helm
When deploying Jitsi on Kubernetes, read [Kubernetes substrate](./30-deployment-substrate/30-kubernetes-substrate.md) for kubernetes substrate.

## OpenShift under restricted access
When deploying into a restricted OpenShift namespace, read [OpenShift substrate](./30-deployment-substrate/40-openshift-substrate.md) for openshift substrate.

## Rootless and single-namespace constraints
When evaluating rootless, namespace, or cluster-team constraints, read [Deployment boundaries and handoff](./30-deployment-substrate/50-boundaries-and-handoff.md) for deployment boundaries and handoff.

## Cluster-team handoff checklist
When preparing a Kubernetes or OpenShift handoff, read [Deployment boundaries and handoff](./30-deployment-substrate/50-boundaries-and-handoff.md) for deployment boundaries and handoff.

## What a school timetable adds
When planning capacity for a scheduled class peak, read [Deployment boundaries and handoff](./30-deployment-substrate/50-boundaries-and-handoff.md) for deployment boundaries and handoff.

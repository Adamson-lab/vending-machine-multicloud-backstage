# ADR 0003: Compile requests to tfvars JSON and drive Terraform with for_each

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

Terraform has to turn many requests into many containers. Options include one module instance per request, generated per-request configurations, orchestration with Terragrunt, or a Kubernetes control plane such as Crossplane.

## Decision drivers

- Reviewable diffs per request
- Small, understandable Terraform
- No new runtime to operate

## Options considered

| Option | Assessment |
|---|---|
| Hand-written module block per request | Readable but easy to get wrong; no validation before commit |
| Terragrunt per request | Powerful orchestration, an extra tool and state-per-request overhead |
| Crossplane control plane | Strong model, but requires running and securing a cluster for a low-volume workflow |
| Compile to tfvars JSON and for_each over a map (chosen) | One state per cloud; plan time grows with request count |

## Decision

`vendingctl compile` writes deterministic tfvars files; each cloud stack loads them with `-var-file` and uses `for_each`. AWS is the exception (ADR 0005).

## Consequences

- The generated files are committed and a CI check proves they match the requests
- Adding a request is a one-file change with a small, reviewable diff
- Sharding is needed if plan time becomes a problem (ADR 0004)

## Reversibility

Two-way door.

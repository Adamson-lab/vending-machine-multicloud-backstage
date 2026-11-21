# ADR 0007: Approval routing is policy as code in Rego

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

Which roles must approve a request depends on data classification, ingress, budget and scope. CODEOWNERS cannot express conditions on file content; manual triage is inconsistent.

## Decision drivers

- Consistent, explainable routing
- Testable policy
- Changes to the routing rules are themselves reviewed

## Options considered

| Option | Assessment |
|---|---|
| CODEOWNERS only | Static per path, cannot react to content |
| Manual triage by the platform team | Inconsistent, undocumented, a bottleneck |
| Rego policy producing required roles with reasons (chosen) | Another policy language; mitigated by 14 unit tests |

## Decision

`policies/rego/approvals.rego` computes required roles and reasons from the request. A workflow labels the pull request; a gate requires an approval from a member of the mapped team. The author's approval never counts, and an unknown role has no team so it can never be satisfied.

## Consequences

- Thresholds live in configuration, not code
- The gate depends on team membership data and a read:org token
- Decommissioning requests are intentionally light (platform review only)

## Reversibility

Two-way door.

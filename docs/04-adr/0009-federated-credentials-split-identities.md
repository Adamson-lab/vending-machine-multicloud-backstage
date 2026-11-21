# ADR 0009: Federated credentials with separate plan and apply identities

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

The pipeline can create organization-level objects, so its credentials are among the most valuable in the estate.

## Decision drivers

- No static cloud credentials
- Pull requests must never receive write access
- Apply requires an approved environment

## Options considered

| Option | Assessment |
|---|---|
| Long-lived service principal keys in secrets | Easy, high theft impact |
| A single identity for plan and apply | Simple, but a pull request run holds write power |
| OIDC federation with a read-only plan identity and a write apply identity bound to main and a protected environment (chosen) | More configuration per cloud |

## Decision

GitHub OIDC tokens are exchanged for short-lived access. The apply identity trusts only the main branch and the `vending-apply` environment. Workflow permissions are least-privilege and `pull_request` (not `pull_request_target`) is used for untrusted code.

## Consequences

- Trust conditions are part of the security design and must be tested in a sandbox
- A compromise of the AFT repository token remains a separate risk

## Reversibility

Two-way door.

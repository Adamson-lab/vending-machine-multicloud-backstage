# ADR 0005: Provision AWS accounts through Account Factory for Terraform

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

The landing zone (project 1, ADR 0004) uses Control Tower. Accounts created directly through the Organizations API are not enrolled in Control Tower and miss its baseline controls and drift management.

## Decision drivers

- Every account must be enrolled in Control Tower
- Reuse the supported mechanism
- Keep a Terraform-based workflow for review

## Options considered

| Option | Assessment |
|---|---|
| aws_organizations_account resources | Simple, but creates accounts outside Control Tower governance |
| Control Tower Account Factory through the console or Service Catalog | Supported, but not request-file driven or reviewable as code |
| AFT account requests generated from requests (chosen) | Depends on AFT; an extra repository and pipeline |

## Decision

`vendingctl` generates AFT account request modules (`generated/aft/vending-*.tf`) which a workflow delivers to the AFT account-request repository. Baseline configuration runs as AFT account customizations.

## Consequences

- AWS is the one cloud where creation is not performed by this repository's stack
- A token to the AFT repository is a sensitive credential (threat T-06)
- Only files matching vending-*.tf are ever managed by the delivery job

## Reversibility

Two-way door; leaving Control Tower would also change this decision.

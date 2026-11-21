# ADR 0006: Quarantine first; deletion is manual, with prevent_destroy on containers

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

Removing a request file would, in a naive design, destroy an account, subscription or project and its data. Cloud containers are among the most destructive things Terraform can delete.

## Decision drivers

- No data loss from a merged pull request
- Sandbox sprawl still needs an end of life
- Deletion must be a deliberate, attributable act

## Options considered

| Option | Assessment |
|---|---|
| Delete on removal of the request file | Simple lifecycle, catastrophic if a file is removed by mistake |
| Delete automatically at expiry | Cleans up quickly, unacceptable data-loss risk |
| Quarantine on expiry, manual deletion after retention (chosen) | Quarantined containers linger and cost something until deleted |

## Decision

Expiry or an owner request sets `lifecycle: decommissioning`, which moves the container to a quarantine location. `prevent_destroy` and provider deletion protections stop Terraform deleting containers. Deletion follows runbook RB-05 with a named approver.

## Consequences

- Costs continue during retention; quarantine placement should also cap spend
- Removing a request file does not delete anything and the plan will fail loudly on prevent_destroy
- A stale-quarantine report keeps the backlog visible

## Reversibility

Two-way door.

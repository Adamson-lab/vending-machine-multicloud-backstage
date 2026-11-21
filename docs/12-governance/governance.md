# Governance

## Charter
Govern how cloud containers are requested, approved, created, expire and are deleted. Decisions are fast, recorded and reviewable.

## Forums and cadence
| Forum | Members | Cadence | Decides |
|---|---|---|---|
| Platform stand-up | Platform team | Weekly | Delivery priorities |
| Request review | Platform plus routed approvers | Per request | Individual requests |
| Policy review | Security, finance, compliance, platform | Monthly | Changes to thresholds and routing |
| Architecture review board | Architecture, security, platform | Monthly | Changes to request contract, approval policy, credential model |
| Quarterly assurance | Platform, security, audit liaison | Quarterly | RB-10 outcomes, risk register |

## Decision rights
| Decision | Decides | Consulted | Recorded in |
|---|---|---|---|
| Approve a request | Routed approver roles | Requester | Pull request |
| Change approval rules or thresholds | ARB | Security, finance, compliance | ADR and pull request |
| Change the request schema | ARB | Platform, workload reps | ADR |
| Grant an exception | Risk acceptance role | Security | Request `exception_ref` and register |
| Delete a container | Owner, platform lead, data owner | Compliance | Pull request (RB-05) |
| Add a cloud | ARB | Sponsor | ADR |

## Change classes
| Class | Example | Review |
|---|---|---|
| Standard | Add a request | Routed approvals |
| Normal | Change generator or module | CODEOWNERS |
| Major | Change approval policy, credential model, or schema | ARB, sandbox rehearsal |
| Emergency | Disable apply | Platform lead, review within two working days |

## Rules of the road
- No container is created outside the pipeline, other than in documented break-glass cases.
- The approval policy and team map are never changed in the same pull request as a request they would affect.
- Exceptions have an expiry (maximum 90 days) and a named owner.
- Administrators follow the same rules; rulesets apply to them too.

## Metrics reported
Request-to-ready time, containers created outside the pipeline, approvals overridden, sandboxes past expiry, quarantine backlog, plan duration per stack.

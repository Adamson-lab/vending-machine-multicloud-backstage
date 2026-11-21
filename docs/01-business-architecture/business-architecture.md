# Business architecture

## Strategic alignment
| Enterprise goal (assumed) | How this project serves it | Measure |
|---|---|---|
| Reduce audit and regulatory risk | Every container creation is a reviewed, attributable change | Share of containers created through the pipeline |
| Increase delivery speed | Self-service request with automated checks | Request-to-ready time |
| Control cloud spend | Mandatory budget and cost center on creation; sandbox expiry | Share of spend with an owner; sandbox lifetime |
| Preserve strategic options | One request format across clouds | Time to add a fourth cloud |

## Stakeholders and concerns
| Stakeholder | Concern | Influence | Interest |
|---|---|---|---|
| Workload teams | Speed and clarity | Medium | High |
| Platform team | Maintainability, fewer manual requests | Medium | High |
| Security | No unreviewed creation, least privilege | High | High |
| Finance / FinOps | Budgets, ownership, sandbox spend | High | Medium |
| Compliance | Evidence, restricted data handling | High | Medium |
| Architecture board | Standards, multi-cloud scope | High | Medium |
| Auditors | Traceability | Medium | Medium |

## Capability map
View D15: Request, Provision, Lifecycle and Govern. Priority for the pilot: validation, approval routing, creation with baseline, expiry and quarantine. Deferred: automated deletion (deliberately manual), owner directory validation, cost anomaly handling.

## Value stream: request to governed container
| Stage | Today (assumed) | Target | Pain removed |
|---|---|---|---|
| Intake | Ticket with free text | Form producing a validated file | Missing information |
| Validation | Manual review | Automated rules R1 to R10 | Review delay |
| Approval | Email chains | Policy-routed pull request approvals | Lost or unclear approvals |
| Creation | Console work per cloud | Pipeline with baseline and budget | Inconsistent setup |
| Onboarding | Ad hoc | Catalog entry and standard guide | Rework |
| End of life | Forgotten | Expiry and quarantine | Sprawl |

## Operating model
- **Platform team:** owns the engine, modules, pipelines and runbooks.
- **Approvers:** security, finance, compliance, architecture and risk acceptance, as decided by policy.
- **Workload owners:** responsible for what runs inside their containers and for the accuracy of their request.
- **Governance:** the architecture review board approves changes to approval policy and the request contract.

## RACI
| Activity | Platform | Requester | Security | Finance | Compliance | ARB |
|---|---|---|---|---|---|---|
| Submit request | C | R/A | I | I | I | I |
| Operate pipeline | R/A | I | C | I | I | I |
| Approve restricted data | C | I | R | I | R | I |
| Approve high budget | C | I | I | R | I | I |
| Approve three-cloud request | C | I | C | I | I | R/A |
| Change approval policy | R | I | C | C | C | A |
| Delete a container | R | C | C | I | C | I |

## KPIs and targets (proposed, not achieved results)
| KPI | Baseline | Proposed target | Source |
|---|---|---|---|
| Request-to-ready time (median) | Measured at pilot start | Agreed with workload teams | Pipeline timestamps |
| Containers created outside the pipeline | Measured at pilot start | Trend to zero | Cloud audit logs |
| Containers with all four tags and a budget | Measured at pilot start | 100% of new containers | `docs/container-inventory.md`, billing exports |
| Sandboxes past expiry still active | Measured at pilot start | 0 | Expiry workflow |
| Approvals bypassed or overridden | 0 allowed | 0 | Repository audit log |

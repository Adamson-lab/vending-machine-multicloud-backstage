# Data architecture

The vending machine handles **request data** (who asked for what) and **derived data** (generated Terraform inputs, catalog entities, state). It does not hold workload business data.

## Classification
| Data | Classification | Why |
|---|---|---|
| Request files | internal | Owner emails, cost centers, data classification of workloads |
| Approval policy, thresholds, team map | internal | Reveals control design |
| Generated files | internal | Derived from requests |
| Terraform state | confidential | Identifiers; may contain sensitive attributes |
| Pull request history | internal | Audit evidence |
| Billing scope identifiers | confidential | Identify commercial arrangements |

A public portfolio copy uses synthetic names and no real identifiers.

## Conceptual model
View D13: a request compiles to one placement per cloud, requires approvals, may reference an exception, and each placement may be published as a catalog resource.

## Logical entities
| Entity | Key attributes | Owner | Store |
|---|---|---|---|
| Request | workload_name, environment, owner, cost_center, data_classification, jurisdiction, clouds, requested_on, lifecycle | Requester | `requests/*.yaml` |
| Placement | cloud, container kind, parent key | Pipeline output | `generated/`, cloud APIs |
| Approval | role, reason, approving team members | Policy output and reviewers | Pull request |
| Exception | reference, scope, expiry | Governance | Exception register |
| Catalog resource | name, owner, annotations | Pipeline output | `generated/catalog/` |

## Identity of a request
`<workload_name>-<environment>`; the file must be named `<key>.yaml`. This makes uniqueness a property of the file system and keeps names stable across clouds.

## Data flow
Request file -> validation -> compile -> generated files -> stacks and AFT -> clouds; generated catalog entities -> Backstage. See D02.

## Retention
Request files and pull request history are retained as long as the repository exists; they are the audit trail. State backups follow platform backup policy. Retention periods are set by legal and compliance.

## Data quality controls
Schema and rules on every request; controlled vocabularies for environment, classification, jurisdiction; a tag value standard that every cloud accepts; generated outputs verified against sources.

# Executive brief: governed self-service for cloud containers

**Decision requested:** approve a sandbox pilot of the vending machine across AWS, Azure and GCP, and name an accountable owner.

## Situation
Cloud accounts, subscriptions and projects are created through tickets and console work. Ownership, budgets and approvals are inconsistent, and sandboxes accumulate.

## Options
| Option | What it means | Advantages | Disadvantages | Risk |
|---|---|---|---|---|
| A. Do nothing | Keep tickets and manual setup | No spend | Inconsistency, sprawl, weak audit trail | Rising |
| B. Minimal | Checklist and a shared form | Cheap | No enforcement, no end of life | Medium |
| C. **Recommended** | Request-as-code, policy-routed approvals, reviewed pipeline, expiry and quarantine | Auditable, consistent, safe by default | Needs a small platform investment | Managed |
| D. Ambitious | Fully automated, including deletion, with a custom portal | Maximum speed | Data-loss risk, large build, new product to secure | High |

## Why C
It delivers control and evidence without automating the most dangerous action (deletion) and without building a bespoke portal. The reasoning is in ADR 0001, 0002 and 0006.

## What success looks like at the pilot gate
- Sandbox containers created on all three clouds through the pipeline, with budgets and tags.
- An expired sandbox moved to quarantine, and a removed request file proven not to delete anything.
- OIDC trust verified: a feature branch cannot apply.
- A measured baseline of current request volume and effort, so the business case uses data.

## Stop criteria
Stop or re-scope if measured volume is far below break-even and no control or audit benefit is accepted as sufficient; if approver teams cannot be staffed; or if billing-scope permissions cannot be limited safely.

## Cost
See the business case. Inputs are placeholders; the effort case only holds above a break-even volume (about 40 requests a month with the placeholder inputs).

## Top risks
Over-privileged apply identities, weakened approval policy, AFT token compromise, low volume.

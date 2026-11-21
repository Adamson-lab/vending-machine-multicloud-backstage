# Executive summary

## The problem
Creating a cloud account, subscription or project is usually a ticket, followed by hand work in a console. The result is slow, inconsistent and hard to audit: missing owners, missing budgets, forgotten sandboxes, and no single record of who approved what.

## The decision needed
Approve a pilot of a **vending machine**: one request format for AWS, Azure and GCP; approvals decided by policy and recorded in pull requests; creation by a reviewed pipeline with federated credentials; sandboxes that expire into quarantine instead of living forever.

## The approach
1. Requesters use a Backstage form (or a pull request) to describe a workload, its data classification, clouds and budget.
2. Automated checks validate the request against schema and business rules and decide which roles must approve.
3. After approval and merge, a pipeline creates the container: AWS through Account Factory for Terraform so Control Tower governs it, Azure and GCP through Terraform stacks.
4. Every container carries the same four metadata tags and a budget with alerts.
5. Sandboxes expire into quarantine. Deletion is always a deliberate manual act.

## What leadership gets
- A single, auditable record of every container request and approval.
- Consistent ownership, classification and spend controls from day one.
- Faster provisioning for workload teams, with a clear route for exceptions.
- Sandbox sprawl brought under control without risking data loss.

## What this does not promise
- It does not pay back on effort alone at low volume. With placeholder inputs, break-even is around 40 requests a month; below that the case rests on control, consistency and auditability.
- It does not secure what runs inside a container; the landing zone guardrails and workload controls do that.
- The cost and effort figures in this repository are model structure with placeholder inputs. They must be replaced with measured data.

## Honest status
Engine, policies, Backstage template and Terraform logic are tested (see test strategy). The Terraform modules have not been applied against real billing scopes, organizations or AFT, and the Azure and GCP provider schemas have not been validated in the authoring environment. A sandbox pilot is the first gate.

## Top risks
1. Over-privileged apply identities (the pipeline can create organization-level objects).
2. Approval policy weakened through a pull request.
3. Low volume making the effort case weak.
4. AFT delivery token compromise.
5. Over-engineering relative to the size of the estate.

## Ask
Approve a sandbox pilot on all three clouds, name an accountable owner for the request contract and approval policy, and nominate approvers from security, finance and compliance.

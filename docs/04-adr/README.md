# Architecture decision records

| ID | Title | Status |
|---|---|---|
| 0001 | Pull requests in Git are the system of record for requests | Accepted |
| 0002 | Backstage is a thin front door; no custom scaffolder action | Accepted |
| 0003 | Compile requests to tfvars JSON and drive Terraform with for_each | Accepted |
| 0004 | One Terraform state per cloud, with a defined sharding trigger | Accepted |
| 0005 | Provision AWS accounts through Account Factory for Terraform | Accepted |
| 0006 | Quarantine first; deletion is manual, with prevent_destroy on containers | Accepted |
| 0007 | Approval routing is policy as code in Rego | Accepted |
| 0008 | Business rules live in one place; the portal mirrors only the schema | Accepted |
| 0009 | Federated credentials with separate plan and apply identities | Accepted |
| 0010 | Generated artefacts are committed and verified in CI | Accepted |

Format: MADR-style. Supersede rather than edit accepted ADRs. Add an ADR for any change to the request contract, a module interface, the approval policy or the credential model.

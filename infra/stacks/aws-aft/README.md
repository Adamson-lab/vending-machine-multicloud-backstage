# AWS stack: Account Factory for Terraform (AFT)

AWS accounts are not created by Terraform resources in this repository. Because the landing zone
uses Control Tower (landing-zone ADR 0004), new accounts must be enrolled through Account Factory
or AFT; creating them with the Organizations API directly would leave them outside Control Tower
governance. See ADR 0005 in this repository.

`vendingctl compile` writes one AFT account request per AWS request to `generated/aft/vending-<key>.tf`.
Deliver those files (only ever files matching `vending-*.tf`, so hand-written requests in that repository are never touched) to the `terraform/` directory of your AFT *account-request* repository (it already
contains `modules/aft-account-request`). Choose a delivery mechanism:

1. Pull request from this repo's apply workflow into the AFT account-request repo (recommended; needs a
   token with write access to that repo, stored as an environment secret or, better, a GitHub App).
2. Manual copy during the pilot.

Account customizations `baseline-standard` and `baseline-restricted` live in the AFT
account-customizations repository and call `infra/modules/aws-account-baseline`.

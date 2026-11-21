# Test strategy and validation status

## Layers
| Level | What it proves | Tooling | Status |
|---|---|---|---|
| Unit: rules and model | Schema, rules R1 to R10, ID generation, tag validity | pytest | Passing |
| Unit: compiler | Output content, determinism, stale and orphan detection | pytest | Passing |
| Security regression | Injection payloads rejected and neutralised | pytest | Passing |
| Unit: policy | Approval routing | `opa test` | 14 passing |
| End to end: policy | Real example requests route as expected | pytest plus OPA | Passing |
| Provider-free Terraform logic | Azure and GCP module locals and variable validation with real generated inputs | `tofu apply` on `variables.tf` and `locals.tf` only | Passing (positive and negative cases) |
| Static: Terraform | Formatting of modules, stacks and generated files | `tofu fmt -check` | Passing |
| Template drift | Portal form equals schema; rendered skeleton passes the rules | pytest with Jinja | Passing |
| Backstage schemas | Template and catalog entities valid; names, tags and annotations valid | `@backstage/catalog-model`, `@backstage/plugin-scaffolder-common` | Passing, and a negative test proves it rejects bad input |
| Workflows | Syntax and expressions | `actionlint` | Clean |
| Diagrams | Mermaid parses | `mermaid.parse` | All parse |
| Provider schemas | Azure and GCP resources valid for their providers | `tofu validate` with providers | **Not run here** |
| Live sandbox | Creation works with real billing scopes, AFT and OIDC trust | Sandbox organization | **Not run** |
| Negative cloud tests | Unauthorised creation is refused | Scripted | **Not run** |

## What the passing tests do and do not prove
They prove the logic you control: request semantics, deterministic generation, injection resistance, approval routing, template consistency and Backstage conformance. They do **not** prove provider behaviour, billing-scope permissions, AFT behaviour or OIDC trust configuration. Those need the sandbox.

## Planned live tests
| ID | Scenario | Expected |
|---|---|---|
| LT-01 | Create an Azure subscription with a budget in a sandbox billing scope | Subscription in the expected management group with tags and budget |
| LT-02 | Create a GCP project with APIs and budget | Project in the expected folder, no default network, budget attached |
| LT-03 | Submit an AFT account request | Account enrolled in Control Tower in the registered OU; customization applied |
| LT-04 | Run a plan from a pull request | Uses read-only identity; cannot apply |
| LT-05 | Attempt apply from a feature branch | Refused by OIDC trust conditions |
| LT-06 | Remove a request file | Plan fails on `prevent_destroy`; nothing deleted |
| LT-07 | Expire a sandbox | Container moves to quarantine location |
| LT-08 | Restricted-data request without a security approval | Approval gate fails |
| LT-09 | Author approves own request | Does not satisfy the gate |
| LT-10 | Backstage template end to end | Pull request opened with a valid file |

## Acceptance for moving from Tier 2 to Tier 3
1. Modules validate against provider schemas in CI.
2. LT-01 to LT-10 pass in a sandbox or deviations are documented.
3. Rollback and quarantine drills completed.
4. Security review of OIDC trust and the AFT delivery token.

## Reproduce
```
make test
make diagrams-check
```

# Requirements

## Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Accept requests in one cloud-neutral format validated against a schema | Must |
| FR-02 | Enforce business rules R1 to R10 | Must |
| FR-03 | Compile requests into deterministic per-cloud Terraform inputs and AFT account requests | Must |
| FR-04 | Create Azure subscriptions and GCP projects with tags, budgets and management group or folder placement | Must |
| FR-05 | Create AWS accounts through Account Factory for Terraform with baseline customizations | Must |
| FR-06 | Decide required approver roles by policy, with explanations | Must |
| FR-07 | Gate merging on approvals from members of the mapped teams | Must |
| FR-08 | Provide a Backstage template that produces a valid request pull request | Must |
| FR-09 | Publish one catalog resource per container | Should |
| FR-10 | Expire sandboxes into quarantine; never delete automatically | Must |
| FR-11 | Generate documentation and inventory from sources | Should |
| FR-12 | Provide a business-case model with explicit placeholders | Should |

## Non-functional requirements
| ID | Quality | Scenario | Measure |
|---|---|---|---|
| NFR-01 | Security | A malicious value in a request tries to inject Terraform expressions | Rejected by schema and neutralised by escaping |
| NFR-02 | Safety | A request file is removed by mistake | No container is deleted; apply fails closed |
| NFR-03 | Auditability | An auditor asks who approved a production container | Answered from the pull request |
| NFR-04 | Maintainability | A new cloud or rule is added | Change confined to config, schema, rules and one module with tests |
| NFR-05 | Determinism | Compile is run twice on the same input | Byte-identical output |
| NFR-06 | Least privilege | A pull request workflow runs | It never holds write credentials |
| NFR-07 | Resilience | Backstage or the portal is down | Requests can still be made as pull requests |
| NFR-08 | Consistency | The portal form and the schema differ | A test fails |
| NFR-09 | Cost | Volume is low | The model shows break-even and the case does not rely on effort alone |

## Regulatory and compliance
Data classification drives approval routing (restricted data requires security and compliance). Jurisdiction is a mandatory field enabled by configuration. Legal and compliance confirm adequacy; this project provides the control and the record.

## Traceability
| Requirement | Design | Implementation | Test or evidence |
|---|---|---|---|
| FR-01, FR-02 | Schema and rules | `schema/`, `src/vendingctl/rules.py` | `tests/test_rules.py` |
| FR-03, NFR-05 | Compiler | `src/vendingctl/compile.py` | `tests/test_compile.py` |
| FR-04 | Azure and GCP modules and stacks | `infra/modules/`, `infra/stacks/` | `tests/test_tf_logic.py`, `tofu fmt` |
| FR-05 | AFT delivery (ADR 0005) | `generated/aft/`, `aws-account-baseline` | `tests/test_compile.py`, format check |
| FR-06 | Approval policy (ADR 0007) | `policies/rego/approvals.rego` | 14 Rego tests, `tests/test_approvals_integration.py` |
| FR-07 | Approval gate | `src/vendingctl/approvals.py`, `approval-gate.yml` | `tests/test_approvals_and_cli.py`, `actionlint` |
| FR-08, NFR-08 | Template (ADR 0002, 0008) | `backstage/templates/` | `tests/test_backstage_template.py`, `scripts/validate_backstage.mjs` |
| FR-09 | Catalog entities | `generated/catalog/` | `scripts/validate_backstage.mjs` |
| FR-10, NFR-02 | Quarantine (ADR 0006) | `src/vendingctl/expire.py`, modules | `tests/test_expire.py`, module `prevent_destroy` |
| FR-11 | Doc generator | `scripts/build_docs.py` | CI sync check |
| FR-12, NFR-09 | Effort model | `scripts/effort_model.py` | `tests/test_effort_model.py` |
| NFR-01 | Threat T-02 | schema patterns, `_q` | injection tests in `tests/test_compile.py` |
| NFR-06 | ADR 0009 | workflows | `actionlint`, sandbox test (planned) |

# Control mapping

Mapping aid, not a certification claim. Confirm applicability with compliance.

| Reference | Intent | Where this project contributes | Evidence |
|---|---|---|---|
| NIST 800-53 AC-2 Account management | Governed creation of accounts and containers | Request, approval and apply flow | Pull request history |
| NIST 800-53 AC-3 / AC-6 Least privilege | Separate plan and apply identities | ADR 0009, workflows | Workflow files, cloud trust policies |
| NIST 800-53 AU-2 / AU-12 Audit events | Who requested, approved and applied | Git history, review events, workflow logs | Repository audit log |
| NIST 800-53 CM-2 / CM-3 Baseline and change control | Containers created with the baseline; changes reviewed | Generated baselines, AFT customizations | `generated/`, CI results |
| NIST 800-53 CM-5 Access restrictions for change | Only the pipeline creates containers | Branch protection, environments | Repository settings |
| NIST 800-53 CM-8 Component inventory | Every container has owner and cost metadata | Mandatory tags, catalog resources | `docs/container-inventory.md` |
| NIST 800-53 SA-2 Allocation of resources | Budgets at creation | Budget resources per cloud | Budget outputs |
| NIST 800-53 SI-10 Information input validation | Requests validated before use | Schema, rules, injection hardening | `tests/test_rules.py`, `tests/test_compile.py` |
| ISO 27001 A.5.9 Inventory of assets | Owner and classification recorded | Tags and catalog | Tag compliance report |
| ISO 27001 A.8.32 Change management | Reviewed, approved changes | Approval routing | Required status checks |
| ISO 27001 A.8.28 Secure coding | Defensive generation of code | HCL escaping, tests | Test results |
| SOC 2 CC6.1 / CC8.1 | Logical access and change management | Same as above | Same as above |

The landing zone project provides the preventive guardrails that apply once a container exists. This project provides controlled creation.

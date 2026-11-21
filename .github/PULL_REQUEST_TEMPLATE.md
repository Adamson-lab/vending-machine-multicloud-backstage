## What changed and why

## Type
- [ ] Request (new, changed or decommissioning)
- [ ] Engine, schema or rules
- [ ] Approval policy, thresholds or team map (major change: ARB)
- [ ] Terraform module or stack
- [ ] Workflow or credentials
- [ ] Documentation

## Risk
Which clouds are affected? Could this create, move or expose a container? Does it touch approvals, credentials or generated code?

## Evidence
- [ ] `vendingctl validate` and `vendingctl compile --check` pass
- [ ] `python -m pytest -q` and `opa test policies/rego` pass
- [ ] Generated files and docs regenerated
- [ ] ADR added or updated for contract, policy, credential or module-interface changes
- [ ] No secrets, real tenant, account, billing or project identifiers

# Security policy

## Reporting
Report suspected vulnerabilities privately to the maintainers (favouradamson803@gmail.com). Do not open a public issue.

## Repository hygiene
- No credentials or real identifiers. Cloud access uses federated, short-lived credentials only.
- Pin GitHub Actions to full commit SHAs before production use; review dependency updates.
- Enforce rulesets for administrators, require reviews and the `validate-requests`, `ci` and `approval-gate` checks.
- Keep the `vending-apply` environment restricted to the main branch with required reviewers.

## Scope
Reference infrastructure and governance material. Applying it is the adopter's responsibility; test in a sandbox first. See `docs/06-security/threat-model.md`.

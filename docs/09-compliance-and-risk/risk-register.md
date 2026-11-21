# Risk register

L/M/H for likelihood and impact. Residual is after the listed mitigation. Owners are roles.

| ID | Risk | L | I | Mitigation | Residual | Owner |
|---|---|---|---|---|---|---|
| R-01 | Apply identity over-privileged or abusable | L | H | Federation, split plan/apply, environment and branch restriction, billing role limited to one scope | M | Security lead |
| R-02 | Approval policy or team map weakened via pull request | L | H | CODEOWNERS on policy and config, tests, ARB for policy changes | M | ARB chair |
| R-03 | AFT repository token compromised | L | H | Fine-grained token or GitHub App, delivery by pull request, branch protection on AFT repo | M | Platform lead |
| R-04 | Volume too low for the effort case | M | M | State the case on control and audit; measure baseline; stop criteria | L | Sponsor |
| R-05 | Request injection into generated code | L | H | Schema patterns, HCL escaping, regression tests | L | Platform lead |
| R-06 | Approval gate bypass by administrators | L | H | Rulesets enforced for administrators; audit log monitoring | M | Security lead |
| R-07 | Quarantined containers linger and cost money | M | M | Spend cap on quarantine, stale-quarantine report, deletion runbook | L | FinOps lead |
| R-08 | Sandbox users resist the TTL | M | L | Clear extension route; communicate early | L | Platform lead |
| R-09 | Landing zone outputs missing (folder or management group keys) | M | M | Preconditions fail loudly; documented dependency, including a `decommissioned` folder | L | Platform lead |
| R-10 | Plan time grows with request count | M | L | Track duration; shard by cost center or region (ADR 0004) | L | Platform lead |
| R-11 | Provider changes break modules (Azure and GCP provider schemas not yet validated here) | M | M | Add provider-schema validation to CI; pin provider ranges; sandbox rehearsal | M | Platform lead |
| R-12 | Over-engineering relative to estate size | M | M | Pilot scope, decision gates, honest break-even | L | Sponsor |
| R-13 | Owner field not tied to a real identity | M | M | Platform review; roadmap: validate against directory | M | Platform lead |
| R-14 | Key-person dependency on the engine | M | M | Tests, documentation, second maintainer | M | Platform lead |

See view D10 for the dependency failure responses.

## Risk acceptance
Residual risk above medium requires CISO acceptance with an expiry date.

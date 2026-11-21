# Threat model (STRIDE)

## Why this system is a high-value target
The vending machine can create organization-level objects (AWS accounts, Azure subscriptions, GCP projects), attach them to the enterprise hierarchy and spend money. Whoever controls its pipeline or its approvals controls the shape of the estate.

## Assets
| Asset | Why it matters |
|---|---|
| Apply identities (one per cloud) | Create containers and billing objects |
| Request repository and branch protection | Source of truth for what gets created and approved |
| Approval policy, thresholds and team map | Decide who must approve what |
| AFT repository token | Can inject account requests into the AWS pipeline |
| Backstage GitHub integration token | Can push branches and open pull requests |
| Terraform state | Contains identifiers and may contain sensitive attributes |
| Billing scope permissions | Allow creating subscriptions that cost money |

## Trust boundaries
1. Requester to the request repository (identity and review boundary).
2. Pull request code to privileged workflows (the fork and `pull_request_target` boundary).
3. GitHub to each cloud (OIDC federation boundary).
4. Vending repository to the AFT repository (token boundary).
5. Backstage to GitHub (integration token boundary).

Diagrams: D01, D03, D07, D08 in the architecture views.

## Threats
| ID | STRIDE | Threat | Mitigation | Verified by | Residual |
|---|---|---|---|---|---|
| T-01 | Spoofing | A compromised GitHub account opens or approves a request | Branch protection, required reviews, signed commits, SSO on the organization, author approvals never count | Gate logic tests; repository settings review | Medium |
| T-02 | Tampering | Request fields are injected into generated Terraform, for example an email containing `${file("/etc/passwd")}`, to run expressions in the AFT pipeline | Strict schema patterns; HCL string escaping that neutralises `${` and `%{`; only schema-constrained values reach HCL; generated files reviewed and format-checked | `tests/test_compile.py` injection tests (6 payloads, escaping unit tests, scan of all generated HCL) | Low |
| T-03 | Tampering | Approval rules, thresholds or the team map are weakened through a pull request | CODEOWNERS require security and architecture reviewers on `policies/` and `config/`; policy unit tests; change class "major" in governance | 14 Rego tests; CODEOWNERS | Medium |
| T-04 | Elevation of privilege | Untrusted pull request code obtains apply credentials | `pull_request` not `pull_request_target`; plan identity read-only; apply identity trusts only main and the protected environment; least-privilege workflow permissions | `actionlint`; sandbox test of OIDC trust conditions | Medium until sandbox-tested |
| T-05 | Elevation of privilege | Approval gate bypassed: stale approval after new commits, label removed, author approves own request | Gate recomputes required roles from policy (labels are informational); author excluded; latest review per user; dismiss stale reviews on push; gate is a required status check | `tests/test_approvals_and_cli.py` (reviewer and gate tests) | Medium (organization admins can bypass) |
| T-06 | Elevation of privilege | AFT repository token compromised | Fine-grained token or GitHub App limited to one repository; delivery by pull request not direct push; branch protection and review on the AFT repository; delivery job only touches `vending-*.tf`; rotation | Workflow review | Medium |
| T-07 | Tampering | Generated files edited by hand to differ from requests | `compile --check` is a required check and detects stale, missing and orphaned files; CODEOWNERS on `generated/` | `test_committed_generated_dir_is_in_sync`, CI | Low |
| T-08 | Denial of service | Request flood or quota exhaustion | Review gate, concurrency group on apply, quotas monitored, budgets on every container | Runbook RB-08 | Low |
| T-09 | Repudiation | An approval or change is disputed | Git history, review events and workflow logs; signed commits; log retention | Repository settings | Low |
| T-10 | Information disclosure | State files leak identifiers or secrets | Encrypted, versioned, access-restricted remote state; no secrets in tfvars; state read access limited to pipeline identities | Backend configuration review | Medium |
| T-11 | Elevation of privilege | Backstage integration token abused to push branches | GitHub App with permission only to create branches and pull requests on the requests repository; pull requests still need review | Integration review | Low to medium |
| T-12 | Tampering / data loss | Removing a request file destroys a container and its data | `prevent_destroy`, provider deletion protections, quarantine before deletion, manual deletion runbook | Terraform source; ADR 0006 | Low |
| T-13 | Tampering | Supply chain compromise (actions, providers, npm packages) | Pin versions; pin actions to commit SHAs before production use; lock files; dependency updates reviewed | Dependabot configuration | Medium |
| T-14 | Spoofing | `owner_email` is free text and may not belong to a real person | Platform review checks the owner; AFT requires a real identity for SSO provisioning; roadmap: validate owners against the identity directory | Roadmap item | Medium |
| T-15 | Elevation of privilege | Azure apply identity with broad billing rights creates subscriptions at will | Limit the billing role to the specific invoice section; budgets and alerts on every subscription; alert on subscription creation outside the pipeline | Runbook RB-01 | Medium |

## Finding recorded during build (T-02)
During the build, a test payload showed that the original owner email pattern allowed `$`, `{` and `}`, and that JSON string escaping alone does not stop HCL from evaluating `${...}`. A request passed validation and produced Terraform containing a live expression. The pattern was tightened and escaping added; both layers are covered by regression tests so neither can regress silently.

## Inherent limits
- Organization owners and repository administrators can bypass branch protection unless rulesets are enforced for administrators.
- OIDC trust conditions are configured in each cloud and are only as strong as their subject claims; they must be tested in a sandbox.
- The approval gate relies on team membership data from GitHub.

## Review triggers
Revisit after any change to the request schema, the generator, the approval policy, the workflow permissions or the credential model, and after any incident.

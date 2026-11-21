# Migration and rollout plan

## Principles
Sandbox first, smallest blast radius, no deletion automation, every phase reversible.

| Phase | Scope | Entry | Exit | Rollback |
|---|---|---|---|---|
| 0 Preparation | Sandbox billing scopes, OIDC trust, AFT access, landing zone outputs | Sponsor approval | RB-01 complete per cloud; baselines for request time and volume captured | None needed |
| 1 Sandbox pilot | Sandbox requests on all three clouds through the pipeline | Phase 0 exit | LT-01 to LT-10 pass; expiry and quarantine work | Disable apply variable |
| 2 Template pilot | Backstage template for a few teams | Phase 1 exit | Pull requests valid; feedback gathered | Use pull requests directly |
| 3 Non-production | New non-prod containers only through the pipeline | Phase 2 exit; approvers staffed | Median request time agreed; no unreviewed creation | Re-open manual route with approval |
| 4 Production | New production containers | Phase 3 exit; ARB approval | Stable for one business cycle | Re-open manual route |
| 5 Brownfield | Adopt existing containers | Inventory complete | Containers adopted or recorded as exceptions | Per container |

## Brownfield adoption
1. Inventory containers per cloud (owner, cost center, data class, region).
2. Create request files that describe existing containers (`lifecycle: active`) without creating anything: import into state where appropriate, never recreate.
3. Resolve gaps (missing owner, tags, budget); record exceptions with expiry.
4. Close the manual route on an announced date.

## Coexistence
During phases 1 to 4 some containers are created manually. The inventory and the audit-log monitor (RB-09) show which, so coverage is never overstated.

## Communication and training
Announce each phase two weeks ahead. Provide a one-page guide to the template, rules, approvals and expiry. Rehearse RB-05 and RB-07 with the platform team.

## Rollout risks
Approver availability (R-02 policy depends on named teams), low volume (R-04), provider differences found in the sandbox (R-11).

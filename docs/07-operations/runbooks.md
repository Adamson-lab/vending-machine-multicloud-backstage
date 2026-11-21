# Operational runbooks

Every change goes through a pull request. Commands illustrate the native tooling; confirm flags for your CLI versions. Never paste credentials into tickets or chat.

## RB-01 First-time setup per cloud
**AWS**
1. Confirm Control Tower and AFT are deployed (landing zone ADR 0004). Register the OU names used in `config/vending.yaml` (Workloads-Prod, Workloads-NonProd, Sandbox, Suspended).
2. Create account customizations `baseline-standard` and `baseline-restricted` that call `infra/modules/aws-account-baseline`.
3. Set repository variables `AFT_REPO` and secret `AFT_REPO_TOKEN` (fine-grained token or GitHub App limited to that repository).

**Azure**
1. Obtain a billing scope the apply identity may create subscriptions under (EA enrollment account, MCA invoice section or MPA customer). Grant only the subscription-creator role on that scope.
2. Create a federated credential for the apply identity: subject restricted to this repository's `vending-apply` environment. Create a separate read-only identity for plans.
3. Provide the `management_group_ids` map from the landing zone output.

**GCP**
1. Create a workload identity pool and provider trusting this repository and environment. Create separate plan (read-only) and apply service accounts.
2. Grant the apply account project creation on the target folders and billing user on the billing account.
3. Enable Cloud Billing Budget and Cloud Resource Manager APIs on the quota project.
4. Provide `folder_ids` including a `decommissioned` folder.

**All clouds:** create the `vending-apply` GitHub environment with required reviewers, restricted to main. Set `ENABLE_APPLY=true` only after a successful sandbox dry run.

## RB-02 Handle a request
1. Requester uses the Backstage template (or edits a file directly).
2. `validate-requests` runs, labels the pull request with required roles.
3. Approvers review; the approval gate checks every required role has a team member approval.
4. Merge. The apply workflow waits for environment approval, then applies.
5. Verify: container exists in the expected location; tags and budget present; catalog resource appears; owner notified.

## RB-03 Change a request (for example budget or clouds)
Edit the request file in a pull request. Compile output changes in the same pull request. Removing a cloud from `clouds` removes it from generated inputs but never deletes the container (ADR 0006); handle that as decommissioning.

## RB-04 Sandbox expiry
The daily workflow opens a pull request moving expired sandboxes to `decommissioning`. Review and merge. Owners can ask for an extension before expiry by editing `sandbox_ttl_days` (within the limit) with a reason.

## RB-05 Delete a container (manual, after retention)
1. Confirm the container is in quarantine and the retention window has passed.
2. Owner and platform lead sign off in the pull request; data owner confirms nothing needs to be kept.
3. Take a final export of anything required (billing, audit logs).
4. Remove protection deliberately: for Azure and GCP set the specific resource's lifecycle protection off in a reviewed change; for AWS follow Control Tower and AFT account closure procedure.
5. Apply, verify, then remove the request file in a final pull request.

## RB-06 Approval gate failures
Missing approvals: the gate lists missing roles. If a role has no eligible approvers, escalate to the ARB; never bypass the gate by editing the team map in the same pull request.

## RB-07 State lock or corruption
1. Identify the stack (Azure or GCP) and who holds the lock.
2. If the holder is a dead run, force-unlock using the backend's documented command after confirming no apply is running.
3. For corruption, restore the latest versioned state backup and run a plan; expect no changes.
4. Record the incident and review the cause.

## RB-08 Quota or billing failures
Apply fails on creation: check account, subscription or project quotas and billing permissions. Raise the quota or fix the role, then rerun the apply. Requests wait; nothing is lost.

## RB-09 Drift or manual creation
Alert on containers created outside the pipeline (cloud audit logs). Triage: adopt into a request, or quarantine. Report the count monthly.

## RB-10 Quarterly assurance
Re-test OIDC trust conditions, review CODEOWNERS and team membership, re-run the effort model with measured data, and review the stale-quarantine list.

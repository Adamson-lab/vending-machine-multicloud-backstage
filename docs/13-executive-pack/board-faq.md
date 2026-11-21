# Executive FAQ

**1. Is anything deleted automatically?** No. Expiry moves a container to quarantine. Deletion is manual, approved and recorded.

**2. Who approves what?** A policy decides by data classification, internet ingress, budget, scope and exceptions. The platform team reviews everything; other roles are added as needed.

**3. Can the requester approve their own request?** No. The author's approval never counts.

**4. Why Git instead of a database or ticketing system?** The request, review, approval and change history become one auditable object, and it keeps working when the portal is down (ADR 0001).

**5. Why Backstage?** It gives requesters a form without a new application to build, using built-in actions. It can be replaced without changing the contract (ADR 0002).

**6. Why do AWS accounts go through AFT?** The landing zone uses Control Tower. Accounts created directly would sit outside its governance (ADR 0005).

**7. What is the biggest security risk?** The apply identities and the approval policy, because they control what gets created. Mitigations are federation, split identities, restricted triggers and protected policy files (threat model T-03, T-04).

**8. Did the build find any security problem?** Yes: request values could have injected Terraform expressions. It was fixed in two layers and is covered by regression tests (T-02).

**9. Does it pay for itself?** Only above a break-even volume; with placeholder inputs that is about 40 requests a month. Below that, the case rests on control and auditability. Measure the baseline first.

**10. What is actually tested?** Request rules, the compiler, injection resistance, approval policy, Terraform module logic without providers, template consistency, Backstage schema conformance, workflow syntax and diagrams. Provider behaviour and live billing permissions are not yet tested.

**11. What happens if GitHub or Backstage is down?** Existing containers are unaffected. Requests can wait or use a pull request directly.

**12. How is spend controlled?** Every container has a budget and alerts at creation; sandboxes have caps and expiry.

**13. How hard is it to add a fourth cloud?** Add configuration, a compile target and a module; the request format stays the same.

**14. What do we need from the business?** Named approvers, a measured baseline of requests and effort, and acceptance of a sandbox pilot first.

**15. What is the first step?** RB-01 setup in sandbox billing scopes, then the sandbox pilot.

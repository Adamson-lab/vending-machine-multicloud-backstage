# Architecture principles

**P1. Requests are code.** Rationale: reviewable, attributable, revertible. Implications: Git is the record; no side channels.

**P2. Approval is policy.** Rationale: consistency and explainability. Implications: roles are computed, reasons recorded, rules tested.

**P3. Never delete automatically.** Rationale: containers hold data. Implications: quarantine, protection flags, manual deletion runbook.

**P4. One source of truth for rules.** Rationale: duplicates drift. Implications: the portal mirrors only the schema, and a test enforces it.

**P5. Least privilege, short-lived.** Rationale: the pipeline reaches the whole estate. Implications: federation, split plan and apply, protected environment.

**P6. Generated means checked.** Rationale: reviewers must see what is applied. Implications: deterministic output committed and verified.

**P7. Treat input as hostile.** Rationale: request fields reach code generators. Implications: strict patterns, output escaping, regression tests.

**P8. Native first for creation.** Rationale: supported mechanisms keep governance intact. Implications: AFT for AWS, provider resources for Azure and GCP.

**P9. Fail closed.** Rationale: ambiguity must not grant access. Implications: unknown approval roles are never satisfied; missing inputs stop the apply.

**P10. Measure the claim.** Rationale: credibility. Implications: placeholders are labelled; the business case shows break-even.

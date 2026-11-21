# Evidence

Captured on 2026-11-21 (Python 3.12, OPA 0.68.0, OpenTofu 1.8.5, Node 22, actionlint 1.7.1). Regenerate with the commands in `docs/10-testing/test-strategy.md`.

| File | What it shows |
|---|---|
| `verification.log` | Full run: validate, compile and docs sync, pytest, OPA, format, actionlint, Backstage entities, diagrams |
| `security-and-approvals-demo.txt` | An injection attempt rejected by the schema and, if validation were bypassed, neutralised by escaping; approval routing with reasons for the example requests |
| `backstage-negative-test.txt` | The Backstage validator rejecting an invalid name, a missing owner and an invalid tag (proves it is not a no-op) |
| `effort-model-output.txt` | Business-case model output, labelled ILLUSTRATIVE (placeholder inputs) |

Not evidenced here: provider-schema validation of the Azure and GCP modules, and any live-tenant behaviour (billing scopes, AFT, OIDC trust). See the test strategy.

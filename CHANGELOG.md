# Changelog

Format follows Keep a Changelog; versions follow Semantic Versioning.

## [0.1.0] - 2026-11-21
### Added
- Request schema v2, configuration schema and business rules R1 to R10
- `vendingctl` engine: validate, compile, expire, approval input, gate and reviewer helpers
- Azure subscription and GCP project vending modules, AWS account baseline customization, stacks
- AFT account request generation (`vending-*.tf`)
- Rego approval routing with explanations
- Backstage template, skeleton, catalog entities and validation against Backstage schemas
- Workflows: ci, validate-requests, approval-gate, expire-sandboxes, apply (disabled by default)
- 15 architecture views, 10 ADRs, threat model, runbooks, business-case model, governance and executive documents

### Security
- Fixed request-to-HCL injection (`${...}` and `%{...}`) with strict patterns and output escaping; regression tests added

### Known limitations
- Azure and GCP provider schemas not validated in the authoring environment
- No live-tenant testing yet
- Business-case inputs are placeholders

# ADR 0010: Generated artefacts are committed and verified in CI

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

Terraform inputs, AFT requests and catalog entities are derived from requests. They can be generated at apply time or committed.

## Decision drivers

- Reviewers should see exactly what will be applied
- Generator changes must be visible
- No hidden state at apply time

## Options considered

| Option | Assessment |
|---|---|
| Generate at apply time only | Nothing to commit, but reviewers cannot see the effect and generator changes are invisible |
| Commit generated files without verification | Visible but can drift |
| Commit and verify with `compile --check` (chosen) | Noisy diffs for generator changes, which is the point |

## Decision

`generated/` is committed. CI fails if it does not match what the compiler would produce, including orphaned files. Output is deterministic (sorted keys, no timestamps) and HCL is emitted in `tofu fmt` canonical form.

## Consequences

- A generator change shows up as a diff across all generated files
- Contributors must run `vendingctl compile` before committing

## Reversibility

Two-way door.

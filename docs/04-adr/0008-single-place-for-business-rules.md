# ADR 0008: Business rules live in one place; the portal mirrors only the schema

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

Validation can exist at form time, at pull request time, and in the apply pipeline. Duplicated rules inevitably drift.

## Decision drivers

- One source of truth
- Fast feedback where possible
- Defence in depth without duplication

## Options considered

| Option | Assessment |
|---|---|
| Re-implement rules in the portal | Fast feedback, two implementations to maintain |
| Only schema checks, no business rules | Cheap, lets semantically invalid requests through |
| Schema shared; business rules in `vendingctl`; template constraints tested against the schema (chosen) | Some invalid combinations are caught only at PR time |

## Decision

The JSON Schema is the shared contract. A test compares the template's constraints with the schema, and another renders the skeleton and runs the full rules on the result.

## Consequences

- The portal cannot silently accept something the engine rejects at the schema level
- Rule changes ship with tests in one repository

## Reversibility

Two-way door.

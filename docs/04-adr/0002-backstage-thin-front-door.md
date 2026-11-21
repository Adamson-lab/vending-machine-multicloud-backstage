# ADR 0002: Backstage is a thin front door; no custom scaffolder action

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

Requesters need a form, not a Git workflow. A portal can either be a thin template over Git or carry its own logic, for example a custom scaffolder action that validates requests.

## Decision drivers

- One place for business rules, not two
- Use Backstage built-in actions to stay upgradeable
- Keep the portal replaceable

## Options considered

| Option | Assessment |
|---|---|
| Custom portal application | Maximum control, a product to build and secure |
| Backstage with a custom validation action in TypeScript | Early feedback, but duplicates rules from the Python engine; two implementations drift |
| ITSM service catalogue front end | Familiar to many organizations, but adds an integration to reach Git and weaker developer experience |
| Backstage template using built-in actions, rules enforced at pull request time (chosen) | Feedback arrives at PR time not form time |

## Decision

The template renders a request file and opens a pull request using `fetch:template` and `publish:github:pull-request`. JSON Schema constraints in the form mirror the schema, and a test fails if they diverge. All business rules run in `vendingctl`.

## Consequences

- Single implementation of business rules
- Form-level validation is limited to what JSON Schema can express
- Replacing Backstage later only means replacing the form

## Reversibility

Two-way door.

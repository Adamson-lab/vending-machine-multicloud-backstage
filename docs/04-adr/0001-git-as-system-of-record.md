# ADR 0001: Pull requests in Git are the system of record for requests

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

A vending machine needs durable, reviewable, attributable records of who asked for what and who approved it. Candidates are a ticketing system, a database behind a portal, or Git.

## Decision drivers

- Every request and approval must be attributable and auditable
- The record must survive portal outages
- Changes must be reviewable and revertible

## Options considered

| Option | Assessment |
|---|---|
| ITSM ticket as the record | Good workflow tools, but the ticket and the infrastructure change are separate records that drift apart |
| Database behind a custom portal | Fast UI, but a new system to secure, back up and audit; approvals live outside code review |
| Git pull requests (chosen) | Intent, review, approval and change history are one object; weaker UX, mitigated by the Backstage front door |

## Decision

Each request is a YAML file in `requests/`; the pull request is the approval and audit record. ITSM tickets may link to it but are not authoritative.

## Consequences

- Git history becomes the audit trail; branch protection becomes a control
- Backstage and GitHub outages do not lose requests
- Requesters without Git skills need the Backstage template

## Reversibility

Two-way door while the file format stays stable.

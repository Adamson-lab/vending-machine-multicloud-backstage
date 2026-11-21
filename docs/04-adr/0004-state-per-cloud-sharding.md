# ADR 0004: One Terraform state per cloud, with a defined sharding trigger

- **Status:** Accepted
- **Date:** 2026-11-21
- **Deciders:** Architecture Review Board (proposed)

## Context

State layout trades blast radius against operational overhead. One state per request isolates failures but multiplies backends and pipelines. One shared state couples clouds.

## Decision drivers

- Failure in one cloud must not block the others
- Locking contention must be tolerable
- Few moving parts for a small platform team

## Options considered

| Option | Assessment |
|---|---|
| Single state for all clouds | Simplest, but one provider outage or lock blocks everything |
| State per request | Smallest blast radius, heavy overhead and slow cross-request changes |
| State per cloud (chosen) | Plan time grows with the number of containers |

## Decision

Azure and GCP each have their own stack and state. AWS accounts are delivered through AFT's own pipeline. Shard a stack by cost centre or region when plan time exceeds an agreed threshold.

## Consequences

- A lock or corruption affects one cloud only (runbook RB-07)
- A sharding decision is measured, not guessed: track plan duration per stack
- State is encrypted, versioned and access-restricted

## Reversibility

Two-way door, but moving resources between states needs careful state surgery.

"""Approval routing support. Policy lives in Rego (policies/rego/approvals.rego); this module
prepares the input for OPA and evaluates whether collected approvals satisfy the result."""
from __future__ import annotations

from .model import Request, owner_alias


def opa_input(req: Request, config: dict) -> dict:
    d = dict(req.data)
    d.setdefault("lifecycle", "active")
    d["key"] = req.key
    d["owner_alias"] = owner_alias(d["owner_email"])
    return {"request": d, "config": {"approvals": config["approvals"]}}


def evaluate_gate(required: set, approvals: list, team_for: dict) -> tuple:
    """Decide whether approvals satisfy required approver roles.

    approvals: [{"reviewer": "alice", "teams": ["security"]}, ...]  (only APPROVED reviews)
    team_for:  role -> team slug that may approve that role, e.g. {"security": "security-architecture"}
    The requester cannot satisfy a role by approving their own request: callers must exclude the
    author's review before calling (see gate CLI).
    Returns (ok, missing_roles).
    """
    approved_teams = {t for a in approvals for t in a.get("teams", [])}
    missing = sorted(role for role in required if team_for.get(role) not in approved_teams)
    return (not missing, missing)


def approved_reviewers(reviews: list, author: str) -> list:
    """Users whose most recent review is an approval, excluding the pull request author.

    reviews: GitHub review objects, oldest first: {"user": {"login": ...}, "state": "APPROVED"|...}.
    Only the latest review per user counts: a later CHANGES_REQUESTED or DISMISSED cancels an
    earlier approval. COMMENTED reviews do not change a user's standing.
    """
    latest = {}
    for r in reviews:
        user = (r.get("user") or {}).get("login")
        state = r.get("state")
        if not user or state == "COMMENTED" or state == "PENDING":
            continue
        latest[user] = state
    return sorted(u for u, s in latest.items() if s == "APPROVED" and u.lower() != author.lower())

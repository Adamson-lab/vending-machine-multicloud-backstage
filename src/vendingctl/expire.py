"""Sandbox expiry: find expired sandbox requests and move them to decommissioning.

Nothing here deletes a cloud container. Expiry only changes the request to
`lifecycle: decommissioning`, which re-places the container in the quarantine
location (Suspended OU, decommissioned management group or folder). Deletion is a
separate, manual, reviewed action (runbook RB-05).
"""
from __future__ import annotations

import datetime as dt
import re

from .model import Request, parse_date


def expiry_date(req: Request) -> dt.date | None:
    ttl = req.data.get("sandbox_ttl_days")
    if req.data.get("environment") != "sandbox" or ttl is None:
        return None
    return parse_date(req.data["requested_on"]) + dt.timedelta(days=ttl)


def expired(requests: list, today: dt.date) -> list:
    out = []
    for r in requests:
        exp = expiry_date(r)
        if exp is not None and r.lifecycle == "active" and today > exp:
            out.append((r, exp))
    return out


def mark_decommissioning(req: Request, exp: dt.date) -> str:
    """Return new file text with lifecycle and reason set (text edit keeps comments and order)."""
    text = req.path.read_text(encoding="utf-8")
    reason = f"sandbox TTL expired on {exp.isoformat()}"
    if re.search(r"^lifecycle:.*$", text, flags=re.M):
        text = re.sub(r"^lifecycle:.*$", "lifecycle: decommissioning", text, flags=re.M)
    else:
        text = text.rstrip("\n") + "\nlifecycle: decommissioning\n"
    if re.search(r"^decommission_reason:.*$", text, flags=re.M):
        text = re.sub(r"^decommission_reason:.*$", f"decommission_reason: {reason}", text, flags=re.M)
    else:
        text = text.rstrip("\n") + f"\ndecommission_reason: {reason}\n"
    return text

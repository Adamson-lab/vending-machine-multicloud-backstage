"""Business rules for requests. The JSON schema covers shape; these cover meaning.

R1  sandbox: ttl required (<= limit), budget required (<= limit), no confidential/restricted data
R2  sandbox_ttl_days only valid for sandbox
R3  prod or restricted data require monthly_budget_usd
R4  restricted data with internet ingress requires exception_ref
R5  azure placement needs azure_landing_zone unless sandbox
R6  aws requires owner_first_name and owner_last_name (Account Factory needs them)
R7  jurisdiction must be enabled in config
R8  requested_on must be a real calendar date
R9  decommissioning requires decommission_reason; active must not carry one
R10 file name must equal <workload_name>-<environment>.yaml (identity and uniqueness)
"""
from __future__ import annotations

from dataclasses import dataclass

from .model import Request, parse_date, schema_errors, ROOT


@dataclass(frozen=True)
class Violation:
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def check(req: Request, config: dict) -> list:
    errs = schema_errors(req.data, ROOT / "schema/request.schema.json")
    if errs:
        return [Violation("SCHEMA", e) for e in errs]
    d, lim, out = req.data, config["limits"], []
    env, cls, budget = d["environment"], d["data_classification"], d.get("monthly_budget_usd")

    if req.path.name != f"{req.key}.yaml":
        out.append(Violation("R10", f"file must be named {req.key}.yaml, found {req.path.name}"))
    try:
        parse_date(d["requested_on"])
    except ValueError:
        out.append(Violation("R8", f"requested_on {d['requested_on']!r} is not a valid date"))

    if env == "sandbox":
        ttl = d.get("sandbox_ttl_days")
        if ttl is None:
            out.append(Violation("R1", "sandbox requests require sandbox_ttl_days"))
        elif ttl > lim["sandbox_max_ttl_days"]:
            out.append(Violation("R1", f"sandbox_ttl_days {ttl} exceeds limit {lim['sandbox_max_ttl_days']}"))
        if budget is None or budget > lim["sandbox_max_budget_usd"]:
            out.append(Violation("R1", f"sandbox budget must be set and <= {lim['sandbox_max_budget_usd']}"))
        if cls in ("confidential", "restricted"):
            out.append(Violation("R1", "confidential/restricted data is not allowed in sandbox"))
    elif "sandbox_ttl_days" in d:
        out.append(Violation("R2", "sandbox_ttl_days is only valid for sandbox requests"))

    if (env == "prod" or cls == "restricted") and budget is None:
        out.append(Violation("R3", "prod or restricted workloads require monthly_budget_usd"))
    if cls == "restricted" and d.get("internet_ingress") and "exception_ref" not in d:
        out.append(Violation("R4", "restricted data with internet ingress requires exception_ref"))
    if "azure" in d["clouds"] and env != "sandbox" and "azure_landing_zone" not in d:
        out.append(Violation("R5", "azure placement needs azure_landing_zone (corp|online)"))
    if "aws" in d["clouds"] and not (d.get("owner_first_name") and d.get("owner_last_name")):
        out.append(Violation("R6", "aws requires owner_first_name and owner_last_name"))
    if d["jurisdiction"] not in config["organization"]["jurisdictions"]:
        out.append(Violation("R7", f"jurisdiction {d['jurisdiction']} is not enabled in config"))

    life = req.lifecycle
    if life == "decommissioning" and not d.get("decommission_reason"):
        out.append(Violation("R9", "decommissioning requires decommission_reason"))
    if life == "active" and "decommission_reason" in d:
        out.append(Violation("R9", "decommission_reason is only valid when lifecycle is decommissioning"))
    return out


def check_all(requests: list, config: dict) -> dict:
    """Return {path: [violations]} for requests that have any."""
    result = {}
    for r in requests:
        v = check(r, config)
        if v:
            result[str(r.path)] = v
    return result

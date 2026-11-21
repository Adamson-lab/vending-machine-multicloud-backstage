"""Loading, schema validation and shared helpers."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent.parent
GCP_LABEL_VALUE = re.compile(r"^[a-z0-9_-]{0,63}$")


@dataclass(frozen=True)
class Request:
    """A parsed request file plus its path (the file name is part of the contract)."""
    path: Path
    data: dict

    @property
    def key(self) -> str:
        return f"{self.data['workload_name']}-{self.data['environment']}"

    @property
    def lifecycle(self) -> str:
        return self.data.get("lifecycle", "active")

    @property
    def clouds(self) -> list:
        return list(self.data["clouds"])


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def schema_errors(instance: dict, schema_path: Path) -> list:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
            for e in sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.absolute_path))]


def load_config(path: Path | None = None) -> dict:
    path = path or ROOT / "config/vending.yaml"
    cfg = load_yaml(path)
    errs = schema_errors(cfg, ROOT / "schema/config.schema.json")
    if errs:
        raise ValueError("invalid config: " + "; ".join(errs))
    return cfg


def load_requests(directory: Path) -> list:
    files = sorted(p for p in directory.glob("*.yaml") if p.is_file())
    return [Request(p, load_yaml(p)) for p in files]


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def label_safe(value: str) -> str:
    """Valid for every cloud (GCP label rules are the strictest): [a-z0-9_-], max 63."""
    return re.sub(r"[^a-z0-9_-]", "-", value.lower())[:63]


def owner_alias(email: str) -> str:
    return label_safe(email.split("@", 1)[0])


def tags_for(req: Request) -> dict:
    """Mandatory four tags plus bookkeeping tags. All values are GCP-label-safe."""
    d = req.data
    return {
        "cost-center": d["cost_center"],
        "data-classification": d["data_classification"],
        "environment": d["environment"],
        "lifecycle": req.lifecycle,
        "managed-by": "vending-machine",
        "owner": owner_alias(d["owner_email"]),
    }


def gcp_project_id(key: str, org_name: str) -> str:
    """Deterministic, globally-unlikely-to-collide ID that always fits 6-30 chars.

    base (max 24, no trailing hyphen) + '-' + 5 hex chars of sha1(org:key) = at most 30.
    """
    base = key[:24].rstrip("-")
    suffix = hashlib.sha1(f"{org_name}:{key}".encode()).hexdigest()[:5]
    return f"{base}-{suffix}"


def first_of_month_utc(date_str: str) -> str:
    d = parse_date(date_str)
    return f"{d.year:04d}-{d.month:02d}-01T00:00:00Z"

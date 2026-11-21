import copy
import datetime as dt
from pathlib import Path

import pytest

from vendingctl.model import Request, load_config, ROOT


@pytest.fixture(scope="session")
def config():
    return load_config()


BASE = {
    "workload_name": "payments-api",
    "owner_email": "ada.owner@example.com",
    "owner_first_name": "Ada",
    "owner_last_name": "Owner",
    "cost_center": "cc-1042",
    "environment": "prod",
    "data_classification": "restricted",
    "jurisdiction": "eu",
    "clouds": ["aws", "azure"],
    "requested_on": "2027-01-11",
    "monthly_budget_usd": 12000,
    "azure_landing_zone": "corp",
}

SANDBOX = {
    "workload_name": "analytics-spike",
    "owner_email": "data.lead@example.com",
    "cost_center": "cc-2210",
    "environment": "sandbox",
    "data_classification": "internal",
    "jurisdiction": "eu",
    "clouds": ["gcp"],
    "requested_on": "2027-01-12",
    "monthly_budget_usd": 300,
    "sandbox_ttl_days": 14,
}


def make(base=None, name=None, **changes):
    """Build a Request with overrides; value None removes a field. File name follows the contract."""
    data = copy.deepcopy(base or BASE)
    for k, v in changes.items():
        if v is None:
            data.pop(k, None)
        else:
            data[k] = v
    key = f"{data['workload_name']}-{data['environment']}"
    return Request(Path(name or f"{key}.yaml"), data)


@pytest.fixture
def prod():
    return make()


@pytest.fixture
def sandbox():
    return make(SANDBOX)

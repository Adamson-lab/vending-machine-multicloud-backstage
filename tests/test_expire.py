import datetime as dt

from conftest import SANDBOX, make
from vendingctl import expire, rules
from vendingctl.model import Request, load_yaml


def test_expiry_date_only_for_sandbox_with_ttl(prod, sandbox):
    assert expire.expiry_date(prod) is None
    assert expire.expiry_date(sandbox) == dt.date(2027, 1, 26)


def test_expired_boundaries(sandbox):
    assert expire.expired([sandbox], dt.date(2027, 1, 26)) == []        # on expiry day: still valid
    assert len(expire.expired([sandbox], dt.date(2027, 1, 27))) == 1    # day after


def test_already_decommissioning_not_listed_again():
    r = make(SANDBOX, lifecycle="decommissioning", decommission_reason="sandbox TTL expired")
    assert expire.expired([r], dt.date(2030, 1, 1)) == []


def test_mark_decommissioning_edits_file_and_result_validates(tmp_path, config):
    p = tmp_path / "analytics-spike-sandbox.yaml"
    p.write_text("# keep this comment\nworkload_name: analytics-spike\nowner_email: data.lead@example.com\ncost_center: cc-2210\n"
                 "environment: sandbox\ndata_classification: internal\njurisdiction: eu\nclouds: [gcp]\n"
                 "requested_on: '2027-01-12'\nmonthly_budget_usd: 300\nsandbox_ttl_days: 14\n")
    req = Request(p, load_yaml(p))
    (r, exp_date), = expire.expired([req], dt.date(2027, 2, 1))
    new_text = expire.mark_decommissioning(r, exp_date)
    assert "# keep this comment" in new_text
    assert "lifecycle: decommissioning" in new_text and "decommission_reason: sandbox TTL expired on 2027-01-26" in new_text
    p.write_text(new_text)
    updated = Request(p, load_yaml(p))
    assert rules.check(updated, config) == []
    assert updated.lifecycle == "decommissioning"


def test_mark_is_idempotent(tmp_path):
    p = tmp_path / "analytics-spike-sandbox.yaml"
    p.write_text("workload_name: analytics-spike\nlifecycle: active\n")
    req = Request(p, {"workload_name": "analytics-spike", "environment": "sandbox", "requested_on": "2027-01-12", "sandbox_ttl_days": 14})
    once = expire.mark_decommissioning(req, dt.date(2027, 1, 26))
    p.write_text(once)
    twice = expire.mark_decommissioning(req, dt.date(2027, 1, 26))
    assert once == twice and once.count("lifecycle:") == 1

import pytest

from conftest import BASE, SANDBOX, make
from vendingctl import rules


def codes(req, config):
    return {v.code for v in rules.check(req, config)}


def test_valid_prod_and_sandbox(config):
    assert rules.check(make(), config) == []
    assert rules.check(make(SANDBOX), config) == []


def test_schema_errors_short_circuit(config):
    v = rules.check(make(workload_name="Bad Name"), config)
    assert v and all(x.code == "SCHEMA" for x in v)


def test_unknown_field_rejected(config):
    assert "SCHEMA" in codes(make(surprise=1), config)


@pytest.mark.parametrize("changes,expected", [
    ({"sandbox_ttl_days": None}, "R1"),
    ({"sandbox_ttl_days": 45}, "R1"),
    ({"monthly_budget_usd": 5000}, "R1"),
    ({"monthly_budget_usd": None}, "R1"),
    ({"data_classification": "restricted"}, "R1"),
])
def test_sandbox_rule_r1(config, changes, expected):
    assert expected in codes(make(SANDBOX, **changes), config)


def test_ttl_only_in_sandbox_r2(config):
    assert "R2" in codes(make(sandbox_ttl_days=7), config)


def test_budget_required_for_prod_and_restricted_r3(config):
    assert "R3" in codes(make(monthly_budget_usd=None), config)
    assert "R3" in codes(make(environment="nonprod", data_classification="restricted", monthly_budget_usd=None), config)
    assert "R3" not in codes(make(environment="nonprod", data_classification="internal", monthly_budget_usd=None), config)


def test_restricted_ingress_needs_exception_r4(config):
    assert "R4" in codes(make(internet_ingress=True), config)
    assert "R4" not in codes(make(internet_ingress=True, exception_ref="EXC-123"), config)
    assert "R4" not in codes(make(internet_ingress=False), config)


def test_azure_needs_landing_zone_r5(config):
    assert "R5" in codes(make(azure_landing_zone=None), config)
    assert "R5" not in codes(make(SANDBOX, clouds=["azure"]), config)


def test_aws_needs_owner_names_r6(config):
    assert "R6" in codes(make(owner_first_name=None), config)
    assert "R6" in codes(make(owner_last_name=None), config)
    assert "R6" not in codes(make(clouds=["azure"], owner_first_name=None), config)


def test_jurisdiction_must_be_enabled_r7(config):
    cfg = {**config, "organization": {**config["organization"], "jurisdictions": ["eu"]}}
    assert "R7" in codes(make(jurisdiction="us"), cfg)


def test_invalid_calendar_date_r8(config):
    assert "R8" in codes(make(requested_on="2027-02-30"), config)


def test_decommission_reason_pairing_r9(config):
    assert "R9" in codes(make(lifecycle="decommissioning"), config)
    assert "R9" in codes(make(decommission_reason="no longer needed"), config)
    assert "R9" not in codes(make(lifecycle="decommissioning", decommission_reason="project cancelled"), config)


def test_file_name_must_match_identity_r10(config):
    assert "R10" in codes(make(name="wrong-name.yaml"), config)


def test_check_all_reports_per_file(config):
    reqs = [make(), make(SANDBOX, sandbox_ttl_days=None)]
    problems = rules.check_all(reqs, config)
    assert list(problems) == ["analytics-spike-sandbox.yaml"]

import re

from vendingctl import model


def test_gcp_project_id_always_valid_and_deterministic():
    pat = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")
    for name in ["abc", "a" * 24, "payments-api", "x-" + "y" * 22, "ab-" + "c" * 21]:
        for env in ["prod", "nonprod", "dev", "sandbox"]:
            pid = model.gcp_project_id(f"{name}-{env}", "example-corp")
            assert 6 <= len(pid) <= 30, pid
            assert pat.match(pid), pid
            assert pid == model.gcp_project_id(f"{name}-{env}", "example-corp")


def test_gcp_project_id_differs_by_org():
    assert model.gcp_project_id("a-prod", "org1") != model.gcp_project_id("a-prod", "org2")


def test_gcp_project_id_never_ends_with_double_hyphen():
    pid = model.gcp_project_id("abcdefghijklmnopqrstuvw-prod", "o")
    assert "--" not in pid


def test_label_safe_and_owner_alias():
    assert model.label_safe("A B/C") == "a-b-c"
    assert model.owner_alias("Jane.Doe+ops@Example.com") == "jane-doe-ops"
    assert len(model.label_safe("x" * 100)) == 63


def test_tags_are_valid_gcp_labels(prod, sandbox):
    for req in (prod, sandbox):
        for k, v in model.tags_for(req).items():
            assert model.GCP_LABEL_VALUE.match(k) and model.GCP_LABEL_VALUE.match(v), (k, v)


def test_first_of_month():
    assert model.first_of_month_utc("2027-01-31") == "2027-01-01T00:00:00Z"

import json
import shutil
import subprocess

import pytest
import yaml

from conftest import SANDBOX, make
from vendingctl import compile as comp
from vendingctl.model import load_requests, ROOT


def test_azure_entry_shape(prod, config):
    e = comp.azure_entry(prod, config)
    assert e["management_group_key"] == "corp" and e["workload"] == "Production"
    assert e["budget_start_date"] == "2027-01-01T00:00:00Z" and e["budget_alert_emails"] == ["ada.owner@example.com"]
    assert e["tags"]["owner"] == "ada-owner"


def test_azure_sandbox_goes_to_sandbox_group(config):
    r = make(SANDBOX, clouds=["azure"])
    e = comp.azure_entry(r, config)
    assert e["management_group_key"] == "sandbox" and e["workload"] == "DevTest"


def test_gcp_entry_merges_and_sorts_apis(sandbox, config):
    sandbox.data["gcp_apis"] = ["bigquery.googleapis.com", "logging.googleapis.com"]
    e = comp.gcp_entry(sandbox, config)
    assert e["activate_apis"] == ["bigquery.googleapis.com", "logging.googleapis.com", "monitoring.googleapis.com"]
    assert e["folder_key"] == "sandbox" and e["labels"]["managed-by"] == "vending-machine"


def test_decommissioning_replaces_placement_on_all_clouds(config):
    r = make(clouds=["aws", "azure", "gcp"], lifecycle="decommissioning", decommission_reason="project cancelled")
    assert comp.azure_entry(r, config)["management_group_key"] == "decommissioned"
    assert comp.gcp_entry(r, config)["folder_key"] == "decommissioned"
    assert 'ManagedOrganizationalUnit = "Suspended"' in comp.aws_aft_module(r, config)
    assert comp.azure_entry(r, config)["tags"]["lifecycle"] == "decommissioning"


def test_aft_module_content(prod, config):
    text = comp.aws_aft_module(prod, config)
    assert 'module "acct_payments_api_prod"' in text
    assert 'AccountEmail              = "aws+payments-api-prod@example.com"' in text
    assert 'ManagedOrganizationalUnit = "Workloads-Prod"' in text
    assert 'account_customizations_name = "baseline-restricted"' in text
    assert "GENERATED" in text


def test_aft_customization_follows_classification(config):
    std = make(data_classification="internal")
    assert 'baseline-standard' in comp.aws_aft_module(std, config)


def test_aws_email_fits_account_email_limit(config):
    longest = make(workload_name="a" * 24, environment="nonprod", data_classification="internal")
    email = f"aws+{longest.key}@{config['organization']['email_domain']}"
    assert len(email) <= 64


def test_catalog_entity_fields(prod):
    doc = yaml.safe_load(comp.catalog_entity(prod, "azure"))
    assert doc["kind"] == "Resource" and doc["metadata"]["name"] == "payments-api-prod-azure"
    assert doc["spec"] == {"type": "azure-subscription", "owner": "user:default/ada-owner"}
    assert doc["metadata"]["annotations"]["vending.example.com/request-file"] == "requests/payments-api-prod.yaml"


def test_compile_all_is_deterministic(prod, sandbox, config):
    a = comp.compile_all([prod, sandbox], config)
    b = comp.compile_all([sandbox, prod], config)
    assert a == b


def test_compile_all_file_set(prod, sandbox, config):
    files = comp.compile_all([prod, sandbox], config)
    assert set(files) == {"azure.tfvars.json", "gcp.tfvars.json", "aft/vending-payments-api-prod.tf",
                          "catalog/payments-api-prod-aws.yaml", "catalog/payments-api-prod-azure.yaml",
                          "catalog/analytics-spike-sandbox-gcp.yaml"}
    assert json.loads(files["azure.tfvars.json"])["subscriptions"].keys() == {"payments-api-prod"}
    assert json.loads(files["gcp.tfvars.json"])["projects"].keys() == {"analytics-spike-sandbox"}


def test_empty_input_yields_empty_maps(config):
    files = comp.compile_all([], config)
    assert json.loads(files["azure.tfvars.json"]) == {"subscriptions": {}}
    assert json.loads(files["gcp.tfvars.json"]) == {"projects": {}}


def test_write_removes_stale_and_check_detects_drift(tmp_path, prod, sandbox, config):
    files = comp.compile_all([prod, sandbox], config)
    comp.write_outputs(tmp_path, files)
    assert comp.diff_outputs(tmp_path, files) == []
    smaller = comp.compile_all([sandbox], config)
    assert comp.diff_outputs(tmp_path, smaller)            # orphans detected
    removed = comp.write_outputs(tmp_path, smaller)
    assert "aft/vending-payments-api-prod.tf" in removed and comp.diff_outputs(tmp_path, smaller) == []
    (tmp_path / "gcp.tfvars.json").write_text("{}")
    assert any(p.startswith("stale") for p in comp.diff_outputs(tmp_path, smaller))


def test_committed_generated_dir_is_in_sync(config):
    reqs = load_requests(ROOT / "requests")
    assert comp.diff_outputs(ROOT / "generated", comp.compile_all(reqs, config)) == []


@pytest.mark.skipif(shutil.which("tofu") is None and shutil.which("terraform") is None, reason="no tofu/terraform")
def test_generated_hcl_is_canonically_formatted():
    tf = shutil.which("tofu") or shutil.which("terraform")
    r = subprocess.run([tf, "fmt", "-check", "-recursive", str(ROOT / "generated")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


# ---------------------------------------------------------------- injection hardening
EVIL_EMAILS = ['a${file("/etc/passwd")}@example.com', "a%{ if true }x%{ endif }@example.com",
               'a"b@example.com', "a b@example.com", "a$@example.com", "a{b}@example.com"]


@pytest.mark.parametrize("email", EVIL_EMAILS)
def test_schema_rejects_injection_shaped_emails(email, config):
    from vendingctl import rules
    v = rules.check(make(owner_email=email), config)
    assert v and v[0].code == "SCHEMA", email


def test_hcl_quoting_neutralises_interpolation_even_if_validation_is_bypassed():
    assert comp._q("a${b}") == '"a$${b}"'
    assert comp._q("a%{ if x }") == '"a%%{ if x }"'
    assert comp._q('he said "hi"') == '"he said \\"hi\\""'
    assert comp._q("back\\slash") == '"back\\\\slash"'


def test_generated_module_has_no_live_interpolation_when_validation_bypassed(config):
    r = make(owner_email='a${file("/etc/passwd")}@example.com', clouds=["aws"], owner_first_name="x${y}")
    text = comp.aws_aft_module(r, config)
    import re
    assert not re.search(r"(?<!\$)\$\{", text), text   # no un-doubled ${
    assert not re.search(r"(?<!%)%\{", text), text


def test_every_hcl_string_in_generated_files_is_safe(config):
    import re
    from vendingctl.model import load_requests, ROOT
    for rel, text in comp.compile_all(load_requests(ROOT / "requests"), config).items():
        if rel.endswith(".tf"):
            assert not re.search(r"(?<!\$)\$\{", text) and not re.search(r"(?<!%)%\{", text), rel

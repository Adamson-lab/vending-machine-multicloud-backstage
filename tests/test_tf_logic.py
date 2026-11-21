"""Provider-free tests of the Terraform modules' logic (variables.tf + locals.tf).

Skipped automatically when neither tofu nor terraform is installed.
"""
import copy
import json
import shutil
import subprocess

import pytest

from vendingctl.model import ROOT

TF = shutil.which("tofu") or shutil.which("terraform")
pytestmark = pytest.mark.skipif(TF is None, reason="tofu/terraform not installed")

HARNESS = ROOT / "scripts/eval_tf_logic.sh"
AZ_MOD = ROOT / "infra/modules/azure-subscription-vending"
GCP_MOD = ROOT / "infra/modules/gcp-project-vending"

MG = {k: f"/providers/Microsoft.Management/managementGroups/ex-{k}" for k in ("corp", "online", "sandbox", "decommissioned")}
FOLDERS = {"workloads-prod": "folders/111", "workloads-nonprod": "folders/222", "sandbox": "folders/333", "decommissioned": "folders/444"}


def run(module, tmp_path, variables, *names):
    f = tmp_path / "vars.json"
    f.write_text(json.dumps(variables))
    r = subprocess.run([str(HARNESS), str(module), str(f), *names], capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr
    return {k: v["value"] for k, v in json.loads(r.stdout).items()}, ""


def azure_vars():
    d = json.loads((ROOT / "generated/azure.tfvars.json").read_text())
    d.update(management_group_ids=MG, billing_scope_id="/providers/Microsoft.Billing/billingAccounts/0/enrollmentAccounts/0")
    return d


def gcp_vars():
    d = json.loads((ROOT / "generated/gcp.tfvars.json").read_text())
    d.update(folder_ids=FOLDERS, billing_account="ABCDEF-123456-ABCDEF")
    return d


def test_azure_management_group_resolution(tmp_path):
    out, err = run(AZ_MOD, tmp_path, azure_vars(), "management_group_id", "missing_management_groups", "budgeted")
    assert out, err
    assert out["management_group_id"]["payments-api-prod"].endswith("ex-corp")
    assert out["management_group_id"]["orders-web-nonprod"].endswith("ex-online")
    assert out["missing_management_groups"] == []
    assert set(out["budgeted"]) == {"payments-api-prod", "orders-web-nonprod"}


def test_azure_missing_management_group_is_reported(tmp_path):
    v = azure_vars()
    v["management_group_ids"] = {"corp": MG["corp"]}
    out, err = run(AZ_MOD, tmp_path, v, "missing_management_groups")
    assert out["missing_management_groups"] == ["online"]


def test_azure_null_budget_is_not_budgeted(tmp_path):
    v = azure_vars()
    v["subscriptions"]["orders-web-nonprod"]["budget_amount"] = None
    out, _ = run(AZ_MOD, tmp_path, v, "budgeted")
    assert set(out["budgeted"]) == {"payments-api-prod"}


def test_azure_rejects_bad_workload_value(tmp_path):
    v = azure_vars()
    v["subscriptions"]["payments-api-prod"]["workload"] = "Prod"
    out, err = run(AZ_MOD, tmp_path, v, "budgeted")
    assert out is None and "workload must be Production or DevTest" in err


def test_azure_rejects_more_than_five_thresholds(tmp_path):
    v = azure_vars()
    v["subscriptions"]["payments-api-prod"]["budget_thresholds"] = [10, 20, 30, 40, 50, 60]
    out, err = run(AZ_MOD, tmp_path, v, "budgeted")
    assert out is None and "at most 5" in err


def test_gcp_folder_ids_are_numeric(tmp_path):
    out, err = run(GCP_MOD, tmp_path, gcp_vars(), "folder_numeric_id", "missing_folders")
    assert out, err
    assert out["folder_numeric_id"] == {"workloads-prod": "111", "workloads-nonprod": "222", "sandbox": "333", "decommissioned": "444"}
    assert out["missing_folders"] == []


def test_gcp_missing_folder_reported(tmp_path):
    v = gcp_vars()
    del v["folder_ids"]["sandbox"]
    out, _ = run(GCP_MOD, tmp_path, v, "missing_folders")
    assert out["missing_folders"] == ["sandbox"]


def test_gcp_api_flattening_counts(tmp_path):
    v = gcp_vars()
    out, _ = run(GCP_MOD, tmp_path, v, "project_apis")
    expected = sum(len(p["activate_apis"]) for p in v["projects"].values())
    assert len(out["project_apis"]) == expected
    assert "analytics-spike-sandbox/bigquery.googleapis.com" in out["project_apis"]


def test_gcp_threshold_fractions_and_viewers(tmp_path):
    out, _ = run(GCP_MOD, tmp_path, gcp_vars(), "threshold_fractions", "viewers", "budgeted")
    assert out["threshold_fractions"]["orders-web-nonprod"] == [0.5, 0.8, 1]
    assert out["viewers"] == {"analytics-spike-sandbox": "data-team@example.com"}
    assert set(out["budgeted"]) == {"analytics-spike-sandbox", "orders-web-nonprod"}


def test_gcp_rejects_invalid_project_id(tmp_path):
    for bad in ("Bad_ID-12345", "ab", "x" * 31, "ends-with-hyphen-"):
        v = copy.deepcopy(gcp_vars())
        v["projects"]["orders-web-nonprod"]["project_id"] = bad
        out, err = run(GCP_MOD, tmp_path, v, "budgeted")
        assert out is None and "project_id must be 6-30" in err, bad


def test_gcp_rejects_bad_billing_account(tmp_path):
    v = gcp_vars()
    v["billing_account"] = "not-a-billing-account"
    out, err = run(GCP_MOD, tmp_path, v, "budgeted")
    assert out is None and "billing_account must look like" in err


def test_every_generated_project_id_passes_module_validation(tmp_path):
    out, err = run(GCP_MOD, tmp_path, gcp_vars(), "budgeted")
    assert out, err

"""End to end: request file -> vendingctl input -> OPA -> required roles.

Skipped when opa is not installed. CI installs it.
"""
import json
import shutil
import subprocess
import sys

import pytest

from vendingctl.model import ROOT

OPA = shutil.which("opa")
pytestmark = pytest.mark.skipif(OPA is None, reason="opa not installed")


def required_roles(request_file):
    inp = subprocess.run([sys.executable, "-m", "vendingctl", "input", str(request_file)], capture_output=True, text=True, check=True).stdout
    out = subprocess.run([OPA, "eval", "-f", "json", "-d", str(ROOT / "policies/rego/approvals.rego"), "--stdin-input",
                          "data.vending.approvals.required"], input=inp, capture_output=True, text=True, check=True).stdout
    return set(json.loads(out)["result"][0]["expressions"][0]["value"])


def test_example_requests_route_as_expected():
    r = ROOT / "requests"
    assert required_roles(r / "payments-api-prod.yaml") == {"platform", "security", "compliance", "finance"}
    assert required_roles(r / "orders-web-nonprod.yaml") == {"platform", "architecture"}
    assert required_roles(r / "analytics-spike-sandbox.yaml") == {"platform"}


def test_every_role_the_policy_can_emit_has_a_team():
    teams = json.loads((ROOT / "policies/data/approval-teams.json").read_text())
    text = (ROOT / "policies/rego/approvals.rego").read_text()
    import re
    roles = set(re.findall(r'"role": "([a-z-]+)"', text))
    assert roles and roles <= set(teams), roles - set(teams)

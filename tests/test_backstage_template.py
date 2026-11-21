"""The Backstage template must not drift from the request schema, and what it renders
must pass the same validation the pull request checks apply."""
import json
from pathlib import Path

import jinja2
import pytest
import yaml

from vendingctl import rules
from vendingctl.model import Request, ROOT

TEMPLATE_DIR = ROOT / "backstage/templates/request-cloud-container"
TEMPLATE = yaml.safe_load((TEMPLATE_DIR / "template.yaml").read_text())
SCHEMA = json.loads((ROOT / "schema/request.schema.json").read_text())


def portal_properties():
    props, required = {}, set()
    for page in TEMPLATE["spec"]["parameters"]:
        props.update(page["properties"])
        required |= set(page.get("required", []))
    return props, required


def test_template_covers_the_schema_fields_it_exposes():
    props, _ = portal_properties()
    unknown = set(props) - set(SCHEMA["properties"])
    assert not unknown, f"template fields not in schema: {unknown}"


def test_template_requires_everything_the_schema_requires():
    _, required = portal_properties()
    assert set(SCHEMA["required"]) <= required


@pytest.mark.parametrize("constraint", ["enum", "pattern", "minimum", "maximum", "minLength", "maxLength", "exclusiveMinimum", "uniqueItems"])
def test_shared_constraints_are_identical(constraint):
    props, _ = portal_properties()
    for name, p in props.items():
        s = SCHEMA["properties"][name]
        if constraint in p or constraint in s:
            assert p.get(constraint) == s.get(constraint), f"{name}.{constraint}: portal={p.get(constraint)!r} schema={s.get(constraint)!r}"


def test_array_item_enums_match():
    props, _ = portal_properties()
    assert props["clouds"]["items"]["enum"] == SCHEMA["properties"]["clouds"]["items"]["enum"]


def test_every_template_value_feeds_the_skeleton():
    step = next(s for s in TEMPLATE["spec"]["steps"] if s["id"] == "render")
    skeleton = "".join(p.read_text() + p.name for p in (TEMPLATE_DIR / "skeleton").rglob("*.yaml"))
    for key in step["input"]["values"]:
        assert f"values.{key}" in skeleton, f"{key} is passed but unused by the skeleton"


def test_every_portal_field_is_passed_to_the_skeleton():
    props, _ = portal_properties()
    step = next(s for s in TEMPLATE["spec"]["steps"] if s["id"] == "render")
    assert set(props) == set(step["input"]["values"])


ENV = jinja2.Environment(variable_start_string="${{", variable_end_string="}}", undefined=jinja2.Undefined)


def render(values):
    out = {}
    for p in (TEMPLATE_DIR / "skeleton").rglob("*.yaml"):
        rel = str(p.relative_to(TEMPLATE_DIR / "skeleton"))
        out[ENV.from_string(rel).render(values=values)] = ENV.from_string(p.read_text()).render(values=values)
    return out


PROD = dict(workload_name="payments-api", owner_email="ada.owner@example.com", owner_first_name="Ada", owner_last_name="Owner",
            cost_center="cc-1042", environment="prod", data_classification="restricted", jurisdiction="eu",
            clouds=["aws", "azure"], azure_landing_zone="corp", internet_ingress=False, requested_on="2027-01-11",
            monthly_budget_usd=12000)
SANDBOX = dict(workload_name="spike", owner_email="d.lead@example.com", owner_first_name="Dee", owner_last_name="Lead",
               cost_center="cc-2210", environment="sandbox", data_classification="internal", jurisdiction="eu",
               clouds=["gcp"], requested_on="2027-01-12", monthly_budget_usd=300, sandbox_ttl_days=14,
               gcp_viewer_group="team@example.com")


@pytest.mark.parametrize("values", [PROD, SANDBOX, {**PROD, "owner_last_name": "O'Brien", "clouds": ["aws", "azure", "gcp"]},
                                    {**PROD, "internet_ingress": True, "exception_ref": "EXC-123"}])
def test_rendered_request_passes_validation(values, config):
    files = render(values)
    assert len(files) == 1
    (rel, text), = files.items()
    assert rel.startswith("requests/")
    data = yaml.safe_load(text)
    req = Request(Path(rel), data)
    assert rules.check(req, config) == [], text
    assert Path(rel).name == f"{values['workload_name']}-{values['environment']}.yaml"
    assert data["clouds"] == values["clouds"]


def test_optional_fields_are_omitted_when_empty():
    (_, text), = render(SANDBOX).items()
    data = yaml.safe_load(text)
    assert "azure_landing_zone" not in data and "exception_ref" not in data and "internet_ingress" not in data
    assert data["sandbox_ttl_days"] == 14 and data["gcp_viewer_group"] == "team@example.com"


def test_pull_request_step_targets_a_branch_per_workload_environment():
    step = next(s for s in TEMPLATE["spec"]["steps"] if s["id"] == "pull-request")
    assert "workload_name" in step["input"]["branchName"] and "environment" in step["input"]["branchName"]
    assert step["action"] == "publish:github:pull-request"

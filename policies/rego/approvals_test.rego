package vending.approvals_test

import rego.v1

import data.vending.approvals

cfg := {"approvals": {"finance_budget_threshold_usd": 10000}}

base := {
	"workload_name": "app",
	"environment": "nonprod",
	"data_classification": "internal",
	"clouds": ["aws"],
	"monthly_budget_usd": 1000,
	"jurisdiction": "eu",
}

mk(extra) := {"request": object.union(base, extra), "config": cfg}

test_plain_request_needs_platform_only if {
	approvals.required == {"platform"} with input as mk({})
}

test_confidential_needs_security if {
	approvals.required == {"platform", "security"} with input as mk({"data_classification": "confidential"})
}

test_restricted_needs_security_and_compliance if {
	approvals.required == {"platform", "security", "compliance"} with input as mk({"data_classification": "restricted"})
}

test_internet_ingress_needs_security if {
	approvals.required == {"platform", "security"} with input as mk({"internet_ingress": true})
}

test_ingress_false_does_not_trigger if {
	approvals.required == {"platform"} with input as mk({"internet_ingress": false})
}

test_budget_above_threshold_needs_finance if {
	approvals.required == {"platform", "finance"} with input as mk({"monthly_budget_usd": 10001})
}

test_budget_at_threshold_does_not if {
	approvals.required == {"platform"} with input as mk({"monthly_budget_usd": 10000})
}

test_missing_budget_does_not_crash_or_trigger if {
	req := {"request": {"workload_name": "app", "data_classification": "internal", "clouds": ["aws"]}, "config": cfg}
	approvals.required == {"platform"} with input as req
}

test_three_clouds_needs_architecture if {
	approvals.required == {"platform", "architecture"} with input as mk({"clouds": ["aws", "azure", "gcp"]})
}

test_two_clouds_does_not if {
	approvals.required == {"platform"} with input as mk({"clouds": ["aws", "azure"]})
}

test_exception_needs_risk_acceptance if {
	"risk-acceptance" in approvals.required with input as mk({"exception_ref": "EXC-123"})
}

test_decommissioning_only_needs_platform if {
	heavy := {"lifecycle": "decommissioning", "data_classification": "restricted", "clouds": ["aws", "azure", "gcp"], "monthly_budget_usd": 99999, "internet_ingress": true}
	approvals.required == {"platform"} with input as mk(heavy)
}

test_reasons_explain_each_role if {
	r := approvals.reasons with input as mk({"data_classification": "restricted", "internet_ingress": true})
	contains(r.security, "restricted")
	contains(r.security, "internet ingress")
	contains(r.compliance, "compliance review")
}

test_every_required_role_has_a_reason if {
	i := mk({"data_classification": "restricted", "internet_ingress": true, "clouds": ["aws", "azure", "gcp"], "monthly_budget_usd": 50000, "exception_ref": "EXC-9"})
	req := approvals.required with input as i
	r := approvals.reasons with input as i
	count(req) == count(object.keys(r))
}

# Approval routing for container requests.
#
# input.request : the request fields plus computed key/owner_alias (see `vendingctl input`)
# input.config  : { approvals: { finance_budget_threshold_usd } }
#
# Output: required (set of roles) and reasons (role -> explanation). Roles map to GitHub
# teams in policies/data/approval-teams.json. Fail-closed: an unknown role has no team and
# therefore can never be satisfied.
package vending.approvals

import rego.v1

# Every change needs a platform review.
triggers contains {"role": "platform", "reason": "all requests are reviewed by the platform team"}

# Decommissioning is deliberately light: it only moves a container into quarantine.
# Everything below applies to active containers only.
active if object.get(input.request, "lifecycle", "active") == "active"

triggers contains {
	"role": "security",
	"reason": sprintf("data classification is %s", [input.request.data_classification]),
} if {
	active
	input.request.data_classification in {"confidential", "restricted"}
}

triggers contains {"role": "security", "reason": "internet ingress requested"} if {
	active
	input.request.internet_ingress == true
}

triggers contains {
	"role": "finance",
	"reason": sprintf("monthly budget %v exceeds %v", [input.request.monthly_budget_usd, input.config.approvals.finance_budget_threshold_usd]),
} if {
	active
	input.request.monthly_budget_usd > input.config.approvals.finance_budget_threshold_usd
}

triggers contains {"role": "architecture", "reason": "request spans all three clouds"} if {
	active
	count(input.request.clouds) == 3
}

triggers contains {"role": "compliance", "reason": "restricted data requires compliance review"} if {
	active
	input.request.data_classification == "restricted"
}

triggers contains {
	"role": "risk-acceptance",
	"reason": sprintf("policy exception %s referenced", [input.request.exception_ref]),
} if {
	active
	input.request.exception_ref
}

required contains t.role if some t in triggers

reasons[role] := concat("; ", sort([t.reason | some t in triggers; t.role == role])) if {
	some role in required
}

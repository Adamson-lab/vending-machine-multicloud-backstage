# Pure logic lives here (no resources) so it can be evaluated without provider access.
locals {
  # Subscriptions that get a budget.
  budgeted = { for k, s in var.subscriptions : k => s if s.budget_amount != null }

  # Management group key -> ID lookups that fail loudly (see precondition in main.tf).
  missing_management_groups = sort(distinct([
    for s in values(var.subscriptions) : s.management_group_key
    if !contains(keys(var.management_group_ids), s.management_group_key)
  ]))

  management_group_id = {
    for k, s in var.subscriptions : k => lookup(var.management_group_ids, s.management_group_key, null)
  }
}

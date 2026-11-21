# Subscription creation requires a billing scope the identity can write to and
# `prevent_destroy` is deliberate: deleting a subscription is a reviewed manual
# action (runbook RB-05), never a side effect of removing a request file.

resource "azurerm_subscription" "this" {
  for_each = var.subscriptions

  alias             = each.key
  subscription_name = each.value.display_name
  billing_scope_id  = var.billing_scope_id
  workload          = each.value.workload
  tags              = each.value.tags

  lifecycle {
    prevent_destroy = true

    precondition {
      condition     = length(local.missing_management_groups) == 0
      error_message = "management_group_ids is missing keys: ${join(", ", local.missing_management_groups)}"
    }
  }
}

resource "azurerm_management_group_subscription_association" "this" {
  for_each = var.subscriptions

  management_group_id = local.management_group_id[each.key]
  subscription_id     = "/subscriptions/${azurerm_subscription.this[each.key].subscription_id}"
}

resource "azurerm_consumption_budget_subscription" "this" {
  for_each = local.budgeted

  name            = "budget-${each.key}"
  subscription_id = "/subscriptions/${azurerm_subscription.this[each.key].subscription_id}"
  amount          = each.value.budget_amount
  time_grain      = "Monthly"

  time_period {
    start_date = each.value.budget_start_date
  }

  dynamic "notification" {
    for_each = each.value.budget_thresholds

    content {
      enabled        = true
      threshold      = notification.value
      operator       = "GreaterThan"
      contact_emails = each.value.budget_alert_emails
    }
  }
}

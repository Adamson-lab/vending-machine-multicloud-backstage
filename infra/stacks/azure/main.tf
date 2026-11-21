provider "azurerm" {
  features {}
  subscription_id = var.management_subscription_id
}

module "subscriptions" {
  source = "../../modules/azure-subscription-vending"

  subscriptions        = var.subscriptions
  management_group_ids = var.management_group_ids
  billing_scope_id     = var.billing_scope_id
}

variable "management_subscription_id" {
  description = "Subscription the provider authenticates against for management operations."
  type        = string
}

variable "billing_scope_id" {
  type = string
}

variable "management_group_ids" {
  description = "Output `management_group_ids` of the landing zone azure-mg-baseline module."
  type        = map(string)
}

variable "subscriptions" {
  description = "Loaded from generated/azure.tfvars.json via -var-file."
  type        = any
}

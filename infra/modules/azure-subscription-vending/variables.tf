variable "subscriptions" {
  description = "Subscriptions to vend, keyed by <workload>-<environment>. Produced by `vendingctl compile`."
  type = map(object({
    display_name         = string
    management_group_key = string
    workload             = string
    tags                 = map(string)
    budget_amount        = optional(number)
    budget_alert_emails  = list(string)
    budget_thresholds    = list(number)
    budget_start_date    = string
  }))

  validation {
    condition     = alltrue([for s in values(var.subscriptions) : contains(["Production", "DevTest"], s.workload)])
    error_message = "workload must be Production or DevTest."
  }

  validation {
    condition     = alltrue([for s in values(var.subscriptions) : length(s.budget_thresholds) <= 5])
    error_message = "Azure budgets allow at most 5 notification thresholds."
  }
}

variable "management_group_ids" {
  description = "Management group IDs by logical key, from the landing zone module output."
  type        = map(string)
}

variable "billing_scope_id" {
  description = "Billing scope (EA enrollment account, MCA invoice section or MPA customer) that subscriptions are created under."
  type        = string
}

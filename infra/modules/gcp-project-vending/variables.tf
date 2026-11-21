variable "projects" {
  description = "Projects to vend, keyed by <workload>-<environment>. Produced by `vendingctl compile`."
  type = map(object({
    project_id        = string
    display_name      = string
    folder_key        = string
    labels            = map(string)
    activate_apis     = list(string)
    budget_amount     = optional(number)
    budget_thresholds = list(number)
    viewer_group      = optional(string)
  }))

  validation {
    condition     = alltrue([for p in values(var.projects) : can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", p.project_id))])
    error_message = "project_id must be 6-30 characters: lowercase letters, digits, hyphens; start with a letter; not end with a hyphen."
  }
}

variable "folder_ids" {
  description = "Folder resource names by logical key (for example folders/123), from the landing zone module output."
  type        = map(string)
}

variable "billing_account" {
  description = "Billing account ID in the form XXXXXX-XXXXXX-XXXXXX."
  type        = string

  validation {
    condition     = can(regex("^[A-Z0-9]{6}-[A-Z0-9]{6}-[A-Z0-9]{6}$", var.billing_account))
    error_message = "billing_account must look like XXXXXX-XXXXXX-XXXXXX."
  }
}

variable "currency_code" {
  description = "Currency of budget amounts."
  type        = string
  default     = "USD"
}

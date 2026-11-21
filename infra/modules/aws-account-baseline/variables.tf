variable "budget_amount" {
  description = "Monthly cost budget in USD. Null disables the budget."
  type        = number
  default     = null
}

variable "budget_thresholds" {
  description = "Actual-spend alert thresholds in percent."
  type        = list(number)
  default     = [50, 80, 100]
}

variable "alert_emails" {
  description = "Budget alert recipients."
  type        = list(string)
  default     = []

  validation {
    condition     = alltrue([for e in var.alert_emails : can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", e))])
    error_message = "alert_emails must be valid email addresses."
  }
}

variable "enable_ebs_default_encryption" {
  description = "Turn on EBS encryption by default in the provider's region (GR-007). Repeat per enabled region."
  type        = bool
  default     = true
}

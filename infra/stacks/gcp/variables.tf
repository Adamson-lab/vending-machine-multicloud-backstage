variable "billing_quota_project" {
  description = "Existing project used as quota project for billing APIs."
  type        = string
}

variable "billing_account" {
  type = string
}

variable "folder_ids" {
  description = "Output `folder_ids` of the landing zone gcp-org-baseline module (must include the decommissioned key)."
  type        = map(string)
}

variable "projects" {
  description = "Loaded from generated/gcp.tfvars.json via -var-file."
  type        = any
}

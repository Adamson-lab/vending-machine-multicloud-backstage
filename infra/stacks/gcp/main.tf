# The Billing Budget API needs a quota project, hence user_project_override.
provider "google" {
  user_project_override = true
  billing_project       = var.billing_quota_project
}

module "projects" {
  source = "../../modules/gcp-project-vending"

  projects        = var.projects
  folder_ids      = var.folder_ids
  billing_account = var.billing_account
}

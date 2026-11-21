# Projects are created with auto_create_network = false (GR-016) and deletion_policy
# PREVENT: removing a request never deletes a project (runbook RB-05).

resource "google_project" "this" {
  for_each = var.projects

  project_id          = each.value.project_id
  name                = each.value.display_name
  folder_id           = local.folder_numeric_id[each.value.folder_key]
  billing_account     = var.billing_account
  labels              = each.value.labels
  auto_create_network = false
  deletion_policy     = "PREVENT"

  lifecycle {
    precondition {
      condition     = length(local.missing_folders) == 0
      error_message = "folder_ids is missing keys: ${join(", ", local.missing_folders)}"
    }
  }
}

resource "google_project_service" "this" {
  for_each = local.project_apis

  project            = google_project.this[each.value.project].project_id
  service            = each.value.api
  disable_on_destroy = false
}

resource "google_project_iam_member" "viewer" {
  for_each = local.viewers

  project = google_project.this[each.key].project_id
  role    = "roles/viewer"
  member  = "group:${each.value}"
}

# Requires the Cloud Billing Budget API and billing account permissions for the
# identity running this stack (see docs/07-operations/runbooks.md RB-01).
resource "google_billing_budget" "this" {
  for_each = local.budgeted

  billing_account = var.billing_account
  display_name    = "budget-${each.key}"

  budget_filter {
    projects = ["projects/${google_project.this[each.key].number}"]
  }

  amount {
    specified_amount {
      currency_code = var.currency_code
      units         = tostring(each.value.budget_amount)
    }
  }

  dynamic "threshold_rules" {
    for_each = local.threshold_fractions[each.key]

    content {
      threshold_percent = threshold_rules.value
    }
  }
}

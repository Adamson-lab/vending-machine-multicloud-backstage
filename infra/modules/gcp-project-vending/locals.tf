# Pure logic lives here (no resources) so it can be evaluated without provider access.
locals {
  # google_project wants the numeric folder ID, not the "folders/123" resource name.
  folder_numeric_id = { for k, id in var.folder_ids : k => trimprefix(id, "folders/") }

  missing_folders = sort(distinct([
    for p in values(var.projects) : p.folder_key if !contains(keys(var.folder_ids), p.folder_key)
  ]))

  # One entry per project x API.
  project_apis = {
    for item in flatten([
      for k, p in var.projects : [
        for api in p.activate_apis : { key = "${k}/${api}", project = k, api = api }
      ]
    ]) : item.key => item
  }

  budgeted            = { for k, p in var.projects : k => p if p.budget_amount != null }
  threshold_fractions = { for k, p in local.budgeted : k => [for t in p.budget_thresholds : t / 100] }
  viewers             = { for k, p in var.projects : k => p.viewer_group if p.viewer_group != null }
}

output "project_numbers" {
  description = "Project numbers by request key."
  value       = { for k, p in google_project.this : k => p.number }
}

output "project_ids" {
  description = "Project IDs by request key."
  value       = { for k, p in google_project.this : k => p.project_id }
}

output "subscription_ids" {
  description = "Subscription GUIDs by request key."
  value       = { for k, s in azurerm_subscription.this : k => s.subscription_id }
}

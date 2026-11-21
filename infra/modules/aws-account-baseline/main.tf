# Account customization applied inside every vended account (use it as the body of an
# AFT account customization named baseline-standard / baseline-restricted).
# Region-scoped settings apply to the region of the configured provider; instantiate the
# module once per enabled region for those.

# GR-006: account-level S3 Block Public Access.
resource "aws_s3_account_public_access_block" "this" {
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# GR-007: encryption at rest by default for new EBS volumes.
resource "aws_ebs_encryption_by_default" "this" {
  count = var.enable_ebs_default_encryption ? 1 : 0

  enabled = true
}

# GR-014: budget with alerts.
resource "aws_budgets_budget" "monthly" {
  count = var.budget_amount == null ? 0 : 1

  name         = "monthly-account-budget"
  budget_type  = "COST"
  limit_amount = tostring(var.budget_amount)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  dynamic "notification" {
    for_each = var.budget_thresholds

    content {
      comparison_operator        = "GREATER_THAN"
      threshold                  = notification.value
      threshold_type             = "PERCENTAGE"
      notification_type          = "ACTUAL"
      subscriber_email_addresses = var.alert_emails
    }
  }
}

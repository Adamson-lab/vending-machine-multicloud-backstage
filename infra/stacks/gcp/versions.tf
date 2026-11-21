terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  # Configure remote state per environment, for example:
  #   tofu init -backend-config=backend.hcl
  # backend "gcs" {}
}

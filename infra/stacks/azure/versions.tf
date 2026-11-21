terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  # Configure remote state per environment, for example:
  #   tofu init -backend-config=backend.hcl
  # backend "azurerm" {}
}

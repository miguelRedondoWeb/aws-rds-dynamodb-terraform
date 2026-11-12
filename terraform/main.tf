
terraform {
  required_version = ">= 1.16.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.100"
    }
  }
}


provider "aws" {
  region  = "eu-south-2"
  profile = "terraform"
}

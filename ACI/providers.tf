terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aci = {
      source  = "CiscoDevNet/aci"
      version = ">= 2.19.0"
    }
  }
}

provider "aci" {
  username = "admin"
  password = "brandonstech"
  url      = "https://172.16.200.220"
  insecure = true   # lab APIC self-signed cert; set false in prod
}
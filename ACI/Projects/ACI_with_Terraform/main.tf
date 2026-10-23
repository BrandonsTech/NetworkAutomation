module "aci" {
  source  = "netascode/nac-aci/aci"
  version = "~> 0.9"

  yaml_directories = ["data"]

  # Start with ONE section on for your first import, then flip the rest
  # true once the workflow round-trips cleanly.
  manage_tenants            = false
  manage_access_policies    = false
  manage_fabric_policies    = false
  manage_pod_policies       = false
  manage_node_policies      = true
  manage_interface_policies = false
}
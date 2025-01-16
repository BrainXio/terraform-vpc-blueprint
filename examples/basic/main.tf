# main.tf

terraform {
  required_version = ">= 1.0.0"
}

module "default_vpc" {
  source         = "../../"
  ubiquity_unifi = true
  vpc_configurations = [
    {
      vpc_id      = 1
      vpc_cidr    = "192.168.0.0/16"
      vpc_name    = "Default"
      vpc_subnets = 256
      settings = {
        domain     = "lan"
        subdomains = ["default", "guest", "iot", "teleport", "camera", "voip", "staff"]
        vlan_range = "0-7"
      }
      template = {
        domain = "{settings_subdomains}.{settings_domain}"
        name   = "{vpc_name} {settings_subdomains} network"
      }
    }
  ]
}

output "default_vpc" {
  value = module.default_vpc
}
# main.tf

terraform {
  required_version = ">= 1.0.0"
}

module "multi_vpc" {
  source         = "../../"
  ubiquity_unifi = true # Assuming you want to leverage Unifi-specific features for all
  vpc_configurations = [
    {
      vpc_id      = 1
      vpc_cidr    = "10.10.0.0/16"
      vpc_name    = "OfficeNetwork"
      vpc_subnets = 10
      settings = {
        domain     = "local"
        subdomains = ["admin", "it", "hr", "marketing", "sales", "guest", "iot", "voip", "cameras", "teleport"]
        vlan_range = "10,20,30,40,50,60,70,80,90,100"
      }
      template = {
        domain = "{settings_subdomains}.{settings_domain}"
        name   = "{vpc_name} {settings_subdomains}"
      }
    },
    {
      vpc_id      = 2
      vpc_cidr    = "172.16.0.0/16" # Using Class B network for another part of the office
      vpc_name    = "Manufacturing"
      vpc_subnets = 5
      settings = {
        domain     = "factory"
        subdomains = ["production", "qa", "maintenance", "inventory", "security"]
        vlan_range = "150,155,160,165,170"
      }
      template = {
        domain = "{settings_subdomains}.{settings_domain}"
        name   = "{vpc_name} {settings_subdomains}"
      }
    },
    {
      vpc_id      = 3
      vpc_cidr    = "192.168.100.0/24" # Smaller network for a remote office or branch
      vpc_name    = "RemoteOffice"
      vpc_subnets = 3
      settings = {
        domain     = "remote"
        subdomains = ["general", "management", "development"]
        vlan_range = "200,201,202"
      }
      template = {
        domain = "{settings_subdomains}.{settings_domain}"
        name   = "{vpc_name} {settings_subdomains}"
      }
    }
  ]
}

output "multi_vpc_output" {
  value = module.multi_vpc.config
}
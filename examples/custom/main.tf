# main.tf

terraform {
  required_version = ">= 1.0.0"
}

module "custom_vpc" {
  source         = "../../"
  ubiquity_unifi = true # Assuming you want to leverage Unifi-specific features
  vpc_configurations = [
    {
      vpc_id      = 1
      vpc_cidr    = "10.0.0.0/16" # Changed to a Class A private network for more address space
      vpc_name    = "OfficeNetwork"
      vpc_subnets = 10 # Changed to a smaller number of subnets for this example
      settings = {
        domain     = "local"
        subdomains = ["admin", "it", "hr", "marketing", "sales", "guest", "iot", "voip", "cameras", "teleport"]
        vlan_range = "10,20,30,40,50,60,70,80,90,100" # Each VLAN for a specific department or service
      }
      template = {
        domain = "{settings_subdomains}.{settings_domain}"
        name   = "{vpc_name} {settings_subdomains}"
      }
    }
  ]
}

output "custom_vpc" {
  value = module.custom_vpc.config
}
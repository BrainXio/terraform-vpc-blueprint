variable "vpc_configurations" {
  type = list(object({
    vpc_id      = number
    vpc_cidr    = string
    vpc_name    = string
    vpc_subnets = number
    settings = object({
      domain     = string
      subdomains = list(string)
      vlan_range = string
    })
    template = object({
      domain = string
      name   = string
    })
  }))
  description = "List of VPC configurations to generate subnets for. Each entry defines a unique VPC setup with its subnets, domains, and VLANs."
  default     = []
  sensitive   = true

  validation {
    condition     = length(var.vpc_configurations) > 0
    error_message = "At least one VPC configuration must be specified."
  }

  validation {
    condition = alltrue([
      for config in var.vpc_configurations :
      can(cidrsubnet(config.vpc_cidr, 0, 0)) # Checks if the CIDR is valid
      && config.vpc_subnets > 0
      && length(config.settings.subdomains) > 0
      && try(regex("^\\d+(-\\d+)?(,\\d+(-\\d+)?)*$", config.settings.vlan_range), "") != "" # Ensures VLAN range is in correct format
    ])
    error_message = "Each VPC configuration must have a valid CIDR, positive number of subnets, at least one subdomain, and a properly formatted VLAN range (e.g., '1-5', '1,2,3', '1,5-7')."
  }
}

variable "ubiquity_unifi" {
  type        = bool
  default     = false
  description = "Flag to enable Unifi-specific configurations. When enabled, certain subnets are reserved or treated specially for Unifi network deployments."
  validation {
    condition     = var.ubiquity_unifi == true || var.ubiquity_unifi == false
    error_message = "The ubiquity_unifi variable must be a boolean value (true or false)."
  }
}
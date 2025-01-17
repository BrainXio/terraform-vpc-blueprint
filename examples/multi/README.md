<!-- BEGIN_TF_DOCS -->
# terraform-vpc-blueprint - multi

"Terraform module for designing and deploying customizable VPC architectures with subnet and VLAN management."

## Overview

This module facilitates the creation of complex VPC structures in Terraform by leveraging Python scripts to dynamically generate subnets, VLANs, and other network configurations. It's designed to be flexible, allowing you to specify multiple VPCs with different settings, subnets, and VLAN ranges.

## Usage

To use this module, you need to provide configurations for your VPCs via the `vpc_configurations` variable. Here's how you can integrate it into your Terraform setup:

### Example Usage

#### Multi-VPC Example

This example showcases how to configure multiple VPCs for different segments of an organization, each with its own network parameters:

- **File**: main.tf

- **Terraform Version**: Requires Terraform version >= 1.0.0.

- **Module Source**: Points to "../../" for the module location.

- **Unifi Flag**: `ubiquity_unifi` is set to `true` for all VPCs to leverage Unifi-specific features.

- **VPC Configurations**:
  - **OfficeNetwork (VPC ID 1)**:
    - **vpc\_cidr**: "10.10.0.0/16" for a Class A network.
    - **vpc\_subnets**: 10 subnets for various office departments.
    - **settings**: Domain "local", with subdomains for different office functions, each with a unique VLAN ID.
    - **template**: Dynamic naming for subnets based on department or service.

  - **Manufacturing (VPC ID 2)**:
    - **vpc\_cidr**: "172.16.0.0/16" for a Class B network, suitable for larger manufacturing setups.
    - **vpc\_subnets**: 5 subnets for distinct manufacturing operations.
    - **settings**: Domain "factory", with subdomains tailored to manufacturing processes, each on a specific VLAN.
    - **template**: Similar naming convention for clarity in network management.

  - **RemoteOffice (VPC ID 3)**:
    - **vpc\_cidr**: "192.168.100.0/24" for a smaller network, ideal for branch offices.
    - **vpc\_subnets**: 3 subnets for basic office functions in a remote setting.
    - **settings**: Domain "remote", with subdomains for general use, management, and development, each with dedicated VLANs.
    - **template**: Consistent naming to maintain organizational clarity.

- **Output**: `multi_vpc_output` provides the configurations for all VPCs created.

**What This Example Does:**

- **Multi-VPC Architecture**: Configures three separate VPCs to cater to different organizational needs:
  - An office network with segmented departments.
  - A manufacturing network for operational efficiency.
  - A small, remote office network for branch operations.

- **Scalability and Isolation**: Each VPC uses different IP ranges and VLANs to ensure scalability and network isolation where required.

- **Unifi Compatibility**: Ensures that all networks can work in harmony with Unifi network management devices, potentially leveraging features like reserved subnets for specific services.

This configuration is ideal for organizations with diverse operational needs across different locations or within the same facility, ensuring each segment has its tailored network environment.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_multi_vpc"></a> [multi\_vpc](#module\_multi\_vpc) | ../../ | n/a |

## Resources

No resources.

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_multi_vpc_output"></a> [multi\_vpc\_output](#output\_multi\_vpc\_output) | n/a |
<!-- END_TF_DOCS -->
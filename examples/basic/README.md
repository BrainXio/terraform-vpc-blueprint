<!-- BEGIN_TF_DOCS -->
# terraform-vpc-blueprint - basic

"Terraform module for designing and deploying customizable VPC architectures with subnet and VLAN management."

## Overview

This module facilitates the creation of complex VPC structures in Terraform by leveraging Python scripts to dynamically generate subnets, VLANs, and other network configurations. It's designed to be flexible, allowing you to specify multiple VPCs with different settings, subnets, and VLAN ranges.

## Usage

To use this module, you need to provide configurations for your VPCs via the `vpc_configurations` variable. Here's how you can integrate it into your Terraform setup:

### Example Usage

#### Basic Example

This example shows how to set up a basic VPC with tailored subnetting for different network segments:

- **File**: main.tf

- **Terraform Version**: Requires Terraform version >= 1.0.0.

- **Module Source**: Points to "../../" for the module location.

- **Unifi Flag**: `ubiquity_unifi` is set to `true` for Unifi-specific configurations.

- **VPC Configuration**:
  - **vpc\_id**: Set to 1, ensuring uniqueness.
  - **vpc\_cidr**: Defines the IP range as 192.168.0.0/16.
  - **vpc\_name**: Named "Default" for reference.
  - **vpc\_subnets**: Intends to generate 256 subnets, limited by VLAN range.
  - **settings**:
    - **domain**: Base domain set to "lan".
    - **subdomains**: Includes "default", "guest", "iot", "teleport", "camera", "voip", "staff".
    - **vlan\_range**: VLAN IDs from 0 to 7.
  - **template**:
    - **domain**: Template for dynamic domain names.
    - **name**: Template for naming networks/subnets.

- **Output**: The `default_vpc` output provides the module's structure.

**What This Example Does:**

- **Specifies a VPC**: With `vpc_id` of 1, named "Default", covering the IP range 192.168.0.0/16.
- **Generates Subnets**: Aims to create 256 subnets, though limited by VLAN range.
- **Defines Networks**: Sets up different network types with their own subdomains.
- **VLAN Configuration**: Uses VLAN IDs to separate network traffic.
- **Naming**: Uses templates for subnet and network naming.
- **Unifi Compatibility**: Ensures compatibility with Unifi network management systems.

This setup is ideal for environments needing distinct network segments, ensuring they are well-organized and secure.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_default_vpc"></a> [default\_vpc](#module\_default\_vpc) | ../../ | n/a |

## Resources

No resources.

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_default_vpc"></a> [default\_vpc](#output\_default\_vpc) | n/a |
<!-- END_TF_DOCS -->
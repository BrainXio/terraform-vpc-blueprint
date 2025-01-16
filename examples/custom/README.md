<!-- BEGIN_TF_DOCS -->
# terraform-vpc-blueprint

"Terraform module for designing and deploying customizable VPC architectures with subnet and VLAN management."

## Overview

This module facilitates the creation of complex VPC structures in Terraform by leveraging Python scripts to dynamically generate subnets, VLANs, and other network configurations. It's designed to be flexible, allowing you to specify multiple VPCs with different settings, subnets, and VLAN ranges.

## Usage

To use this module, you need to provide configurations for your VPCs via the `vpc_configurations` variable. Here's how you can integrate it into your Terraform setup:

### Example Usage

#### Custom Example

This example demonstrates how to set up a custom VPC tailored for an office environment with specific subnets for different departments or services:

- **File**: main.tf

- **Terraform Version**: Requires Terraform version >= 1.0.0.

- **Module Source**: Points to "../../" for the module location.

- **Unifi Flag**: `ubiquity_unifi` is set to `true` to leverage Unifi-specific features.

- **VPC Configuration**:
  - **vpc_id**: Set to 1, ensuring uniqueness.
  - **vpc_cidr**: Uses "10.0.0.0/16" for a Class A private network, providing more address space.
  - **vpc_name**: Named "OfficeNetwork" for reference.
  - **vpc_subnets**: Limited to 10 subnets, suitable for departmental segmentation.
  - **settings**: 
    - **domain**: Base domain set to "local".
    - **subdomains**: Customized for office departments and services like "admin", "it", "hr", "marketing", etc.
    - **vlan_range**: VLAN IDs are specifically chosen for each department or service, enhancing network isolation.
  - **template**: 
    - **domain**: Template for dynamic domain names, incorporating subdomains.
    - **name**: Names networks/subnets based on VPC name and subdomain.

- **Output**: The `custom_vpc` output returns the configuration of the custom VPC.

**What This Example Does:**

- **Custom VPC Setup**: Defines a VPC named "OfficeNetwork" with a wide IP range for scalability.
- **Departmental Subnets**: Creates subnets for different office functions, ensuring network policies can be applied per department.
- **VLANs for Isolation**: Each subnet corresponds to a specific VLAN, allowing for better network traffic management and security.
- **Unifi Compatibility**: Ensures compatibility with Unifi network devices, potentially reserving certain subnets for special services or devices like Teleport VPN.

This setup is perfect for an office environment where organizational structure dictates network configuration, offering both flexibility and security.

### Additional Information

Details on `vpc_configurations`, Unifi features, and how to use this module can be found in the [Overview](#overview) and 
<!-- END_TF_DOCS -->
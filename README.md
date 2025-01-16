<!-- BEGIN_TF_DOCS -->
# terraform-vpc-blueprint

"Terraform module for designing and deploying customizable VPC architectures with subnet and VLAN management."

## Overview

This module facilitates the creation of complex VPC structures in Terraform by leveraging Python scripts to dynamically generate subnets, VLANs, and other network configurations. It's designed to be flexible, allowing you to specify multiple VPCs with different settings, subnets, and VLAN ranges.

## Usage

To use this module, you need to provide configurations for your VPCs via the `vpc_configurations` variable. Here's how you can integrate it into your Terraform setup:

### Example Usage

```hcl
module "vpc_blueprint" {
  source         = "brainxio/terraform-vpc-blueprint"
  vpc_configurations = [
        {
        vpc_id      = 1
        vpc_cidr    = "192.168.0.0/16"
        vpc_name    = "Default"
        vpc_subnets = 256
        settings    = {
          domain       = "lan"
          subdomains   = ["default", "guest", "iot", "teleport", "camera", "voip", "staff"]
          vlan_range   = "0-7"
        }
        template    = {
          domain       = "{settings_subdomains}.{settings_domain}"
          name         = "{vpc_name} {settings_subdomains} network"
        }
      },
    # Add more VPC configurations as needed
  ]
  ubiquity_unifi = true # Set to true if using Unifi-specific configurations
}

output "vpc_config" {
  value = module.vpc_blueprint.config
}
```

### `vpc_configurations` Explanation

- **vpc\_id**: An identifier for the VPC. Must be unique across all configurations.
- **vpc\_cidr**: The CIDR block for this VPC. This defines the IP range for your network.
- **vpc\_name**: A name for the VPC, used in template processing for naming subnets or other resources.
- **vpc\_subnets**: The number of subnets to generate within this VPC.
- **settings**:
  - **domain**: The domain suffix for subnets (e.g., "local").
  - **subdomains**: A list of subdomain names that can be used to create distinct networks within your VPC.
  - **vlan\_range**: A string defining the VLAN IDs to use. Can be a range (e.g., "1-10"), a list (e.g., "1,2,3"), or a single VLAN ID. This determines how many subnets will be created or mapped to VLANs.
- **template**:
  - **domain**: A template string for the domain. Placeholders like `{settings_subdomains}` will be replaced with actual data from `settings`.
  - **name**: A template for naming subnets or networks. Placeholders here will also be replaced with actual data.

### Unifi-Specific Features

- **ubiquity\_unifi**: When set to `true`, the module will respect certain reserved subnets and VLANs specific to Unifi setups, like reserving the 192.168.4.0/24 subnet for Teleport VPN.

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_external"></a> [external](#provider\_external) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [external_external.config](https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ubiquity_unifi"></a> [ubiquity\_unifi](#input\_ubiquity\_unifi) | Flag to enable Unifi-specific configurations. When enabled, certain subnets are reserved or treated specially for Unifi network deployments. | `bool` | `false` | no |
| <a name="input_vpc_configurations"></a> [vpc\_configurations](#input\_vpc\_configurations) | List of VPC configurations to generate subnets for. Each entry defines a unique VPC setup with its subnets, domains, and VLANs. | <pre>list(object({<br/>    vpc_id      = number<br/>    vpc_cidr    = string<br/>    vpc_name    = string<br/>    vpc_subnets = number<br/>    settings = object({<br/>      domain     = string<br/>      subdomains = list(string)<br/>      vlan_range = string<br/>    })<br/>    template = object({<br/>      domain = string<br/>      name   = string<br/>    })<br/>  }))</pre> | `[]` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_config"></a> [config](#output\_config) | The generated VPC configurations. |
| <a name="output_source"></a> [source](#output\_source) | The source data used for configuration. |
| <a name="output_timestamp"></a> [timestamp](#output\_timestamp) | Timestamp of when the configuration was generated. |

## Development

### Installing Pre-Commit

**Linux:**

- Ensure you have git installed. Then, install pre-commit via pip:
  ```
  pip install pre-commit
  ```

- Navigate to your project root:

  ```
  cd /path/to/your/project
  ```

- Install the pre-commit hooks:

  ```
  pre-commit install
  ```

**Mac:**

- Similar to Linux, ensure git is installed. Use pip to install pre-commit:

  ```
  pip install pre-commit
  ```

- Change to your project directory:

  ```
  cd /path/to/your/project
  ```

- Install the hooks:

  ```
  pre-commit install
  ```

**Windows:**

- Install Python, which should include pip. Then install pre-commit:

  ```
  pip install pre-commit
  ```

- Open Command Prompt or Git Bash, navigate to your project directory:

  ```
  cd \path\to\your\project
  ```

- Install the hooks:

  ```
  pre-commit install
  ```

### Understanding lint\_patch.py

lint\_patch.py is a Python script designed to automate the formatting and import sorting of Python files before they are committed to the Git repository. Here's what it does:

- **Backup**: Creates a backup of each Python file before modifications are applied.
- **Sort Imports**: Uses isort to sort and organize import statements in Python files, ensuring consistency in how modules are imported across your codebase.
- **Format with Black**: Applies the Black code formatter to each Python file to standardize code style, improving readability and reducing style debates.

This script is particularly useful in maintaining a clean codebase where:

- All Python files conform to the same formatting standards.
- Import statements are consistently sorted, making it easier to manage dependencies.
- Changes can be reverted if necessary, thanks to the backups.

By integrating lint\_patch.py into your pre-commit hook, every commit will automatically be checked and formatted, ensuring that your code adheres to the project's coding standards before it enters the version control system.

### Using with Terraform Docs

After setting up pre-commit, you can use this setup in conjunction with terraform-docs to generate markdown documentation for your Terraform modules. terraform-docs will read the module's configuration and this footer.txt to compile complete documentation, including the development practices described here, into a markdown file for better project documentation and collaboration.
<!-- END_TF_DOCS -->
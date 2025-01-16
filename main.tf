# Use a more robust way to specify the path to the Python script
locals {
  script_path = "${path.module}/scripts/vpc_blueprint.py"
}

data "external" "config" {
  program = ["python3", local.script_path]
  query = {
    "vpcs"           = jsonencode(var.vpc_configurations)
    "ubiquity_unifi" = jsonencode(var.ubiquity_unifi)
  }
}

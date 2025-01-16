# Output the config
output "config" {
  value       = try(jsondecode(base64decode(data.external.config.result.output)).config, {})
  sensitive   = true
  description = "The generated VPC configurations."
}

# Output the source data
output "source" {
  value       = try(jsondecode(base64decode(data.external.config.result.output)).source, {})
  sensitive   = true
  description = "The source data used for configuration."
}

# Output the timestamp
output "timestamp" {
  value       = try(jsondecode(base64decode(data.external.config.result.output)).timestamp, "")
  description = "Timestamp of when the configuration was generated."
}
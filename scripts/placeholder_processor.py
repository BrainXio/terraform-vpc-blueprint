import re
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PlaceholderProcessor:
    def __init__(self, data):
        """
        Initialize the PlaceholderProcessor with VPC data.

        :param data: Dictionary containing VPC data. Must include 'vpcs' key.
        """
        if "vpcs" not in data:
            logger.warning(
                "Input data does not contain 'vpcs' key. Wrapping data in 'vpcs'."
            )
            self.data = {"vpcs": [data]}
        else:
            self.data = data

    def _create_context(self, vpc):
        """
        Creates a context dictionary for processing templates by flattening the VPC data.

        :param vpc: A single VPC configuration dictionary.
        :return: A context dictionary for template processing.
        """
        context = self._flatten(vpc)
        context["count_index"] = 0  # Initialize, will be overridden in process method
        return context

    def process(self):
        """
        Process all VPCs, applying templates to generate configurations.

        :return: JSON string of processed VPC configurations.
        """
        try:
            result = []
            for vpc in self.data["vpcs"]:
                context = self._create_context(vpc)
                for index in range(vpc["vpc_subnets"]):
                    context["count_index"] = (
                        index + 1
                    )  # Update count_index for each iteration
                    result.append(self._process_vpc(vpc, context, index))
            return json.dumps(result, indent=2)
        except KeyError as ke:
            logger.error(f"KeyError in processing VPC data: {ke}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in processing VPC data: {e}")
            raise

    def _process_vpc(self, vpc, context, index):
        """
        Process a single VPC configuration, resolving placeholders.

        :param vpc: VPC configuration dictionary.
        :param context: Context dictionary for placeholder resolution.
        :param index: Current subnet index for processing.
        :return: Processed VPC configuration.
        """
        processed_vpc = {}
        for key, value in vpc.items():
            if key == "template":
                processed_vpc.update(self._resolve_template(value, context, index))
            elif isinstance(value, dict):
                processed_vpc[key] = self._process_dict(value, context, index)
            elif isinstance(value, list):
                processed_vpc[key] = self._process_list(value, context, index)
            else:
                processed_vpc[key] = self._resolve_placeholders(
                    str(value), context, index
                )
        # Add dynamic vlan_id
        processed_vpc["vlan_id"] = index + 1
        return processed_vpc

    def _resolve_template(self, template, context, index):
        """
        Resolve placeholders in the template.

        :param template: Dictionary of template items to resolve.
        :param context: Context for placeholder resolution.
        :param index: Current index for processing.
        :return: Dictionary with resolved placeholders.
        """
        resolved = {}
        for key, value in template.items():
            try:
                resolved[key] = self._resolve_placeholders(value, context, index)
            except Exception as e:
                logger.error(f"Error resolving template for key '{key}': {e}")
                resolved[key] = (
                    value  # If resolution fails, keep the original template value
                )
        return resolved

    def _process_dict(self, data, context, index):
        """
        Recursively process a dictionary for placeholders.

        :param data: Dictionary to process.
        :param context: Context for placeholder resolution.
        :param index: Current index for processing.
        :return: Processed dictionary.
        """
        return {k: self._process_nested(v, context, index) for k, v in data.items()}

    def _process_list(self, lst, context, index):
        """
        Process list items for placeholders.

        :param lst: List to process.
        :param context: Context for placeholder resolution.
        :param index: Current index for processing.
        :return: Processed list.
        """
        return [self._process_nested(item, context, index) for item in lst]

    def _process_nested(self, item, context, index):
        """
        Recursively process nested data structures for placeholders.

        :param item: Item to process (can be dict, list, or other).
        :param context: Context for placeholder resolution.
        :param index: Current index for processing.
        :return: Processed item.
        """
        if isinstance(item, dict):
            return self._process_dict(item, context, index)
        elif isinstance(item, list):
            return self._process_list(item, context, index)
        else:
            return self._resolve_placeholders(str(item), context, index)

    def _resolve_placeholders(self, value, context, index):
        """
        Resolve placeholders within a string value.

        :param value: String value to resolve placeholders in.
        :param context: Context dictionary for placeholder values.
        :param index: Current index for cycling through list placeholders.
        :return: String with resolved placeholders.
        """
        if isinstance(value, str):
            placeholders = re.findall(r"{(\w+)}", value)
            for placeholder in placeholders:
                if placeholder in context:
                    if isinstance(context[placeholder], list):
                        value = value.replace(
                            f"{{{placeholder}}}",
                            str(
                                context[placeholder][index % len(context[placeholder])]
                            ),
                        )
                    else:
                        value = value.replace(
                            f"{{{placeholder}}}", str(context[placeholder])
                        )
                else:
                    logger.warning(
                        f"Placeholder {placeholder} not found in context. Keeping placeholder in output."
                    )
        return value

    def _flatten(self, d, parent_key="", sep="_"):
        """
        Flatten a nested dictionary into a single level dictionary.

        :param d: Dictionary to flatten.
        :param parent_key: Parent key in recursion.
        :param sep: Separator for key concatenation.
        :return: Flattened dictionary.
        """
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten(v, new_key, sep=sep))
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.update(self._flatten(item, f"{new_key}{sep}{i}", sep=sep))
                    else:
                        items[new_key] = v
                        break
            else:
                items[new_key] = v
        return items


if __name__ == "__main__":
    input_data = {
        "vpcs": [
            {
                "vpc_id": 1,
                "vpc_cidr": "192.168.0.0/24",
                "vpc_name": "Test VPC",
                "vpc_subnets": 4,
                "settings": {
                    "domain": "lan",
                    "prefix": "red",
                    "region_letters": ["a", "b", "c", "d"],
                    "vlan_range": "1-4",
                },
                "template": {
                    "domain": "{settings_prefix}-{vpc_id}{settings_region_letters}.{settings_domain}",
                    "base_name": "{settings_prefix}-{vpc_id}{settings_region_letters}",
                    "network": "{vpc_name}-{vpc_id}",
                },
            }
        ]
    }

    try:
        processor = PlaceholderProcessor(input_data)
        processed_vpcs = processor.process()
        print(processed_vpcs)
    except Exception as e:
        logger.error(f"An error occurred while processing VPCs: {e}")

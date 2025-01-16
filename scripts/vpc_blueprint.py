import json
import ipaddress
import uuid
import sys
import logging
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.terraform_data_external import TerraformDataExternal
from scripts.placeholder_processor import PlaceholderProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VpcGenerator:
    def __init__(self, vpc, ubiquity_unifi=False):
        self.vpc = vpc
        self.ubiquity_unifi = ubiquity_unifi

    def generate_subnets(self):
        try:
            network = ipaddress.ip_network(self.vpc['vpc_cidr'])
        except ValueError as e:
            raise ValueError(f"Invalid VPC CIDR: {self.vpc['vpc_cidr']}") from e

        num_subnets = self.vpc['vpc_subnets']
        if num_subnets <= 0:
            raise ValueError(f"Invalid number of subnets: {num_subnets}. Must be positive.")

        vlan_range = self.vpc['settings'].get('vlan_range', '1-1')
        vlan_ids = self._parse_vlan_range(vlan_range)

        name_prefix = network.prefixlen
        new_prefix = self._calculate_new_prefix(name_prefix, num_subnets)

        subnets = []
        processor = PlaceholderProcessor({'vpcs': [self.vpc]})
        vlan_counter = 0

        reserved_subnet = ipaddress.ip_network("192.168.4.0/24") if self.ubiquity_unifi else None

        for i, subnet in enumerate(network.subnets(new_prefix=new_prefix)):
            if vlan_counter >= len(vlan_ids):
                break

            current_vlan_id = vlan_ids[vlan_counter]
            
            if current_vlan_id == 0:
                vlan_counter += 1
                continue

            subnet_details = {
                "cidr": str(subnet),
                "device_count": subnet.num_addresses - 2,
                "uuid": str(uuid.uuid4()),
                "vlan_id": current_vlan_id,
            }

            if self.ubiquity_unifi and subnet.overlaps(reserved_subnet):
                subnet_details.update({
                    "name": "Teleport VPN server",
                    "dhcp_start": None,
                    "dhcp_stop": None,
                    "domain": None,
                    "gateway": None,
                    "description": "Reserved for Teleport VPN server",
                })
            else:
                try:
                    subnet_details.update(self._scale_dhcp(subnet))
                    if 'template' in self.vpc:
                        context = processor._create_context(self.vpc)
                        context['count_index'] = vlan_counter + 1  # 1-based index
                        processed_subnet = processor._process_vpc(self.vpc, context, vlan_counter)
                        subnet_details.update({
                            "domain": processed_subnet.get("domain", f"subdomain_{vlan_counter}.lan"),
                            "name": processed_subnet.get("name", f"{self.vpc['vpc_name']} Region {vlan_counter}"),
                        })
                    else:
                        subnet_details["name"] = f"{self.vpc['vpc_name']} Region {vlan_counter}"
                        subnet_details["domain"] = f"subdomain_{vlan_counter}.lan"
                    subnet_details["gateway"] = str(subnet.network_address + 1)
                    subnet_details["description"] = self._get_vlan_description(current_vlan_id)
                except Exception as e:
                    logger.error(f"Error processing subnet {str(subnet)}: {str(e)}")
                    continue  # Skip this subnet if there's an error

            subnets.append(subnet_details)
            vlan_counter += 1

        return subnets

    def _parse_vlan_range(self, vlan_range):
        if '-' in vlan_range:
            start, end = map(int, vlan_range.split('-'))
            return list(range(start, end + 1))
        elif ',' in vlan_range:
            return [int(v) for v in vlan_range.split(',')]
        else:
            return [int(vlan_range)]

    def _calculate_new_prefix(self, name_prefix, num_subnets):
        new_prefix = name_prefix
        while (1 << (new_prefix - name_prefix)) < num_subnets:
            new_prefix += 1
        if new_prefix > 32:  # For IPv4, adjust to 128 for IPv6
            raise ValueError("Cannot subdivide network further due to subnet limit.")
        return new_prefix

    def _scale_dhcp(self, subnet):
        total_hosts = subnet.num_addresses - 2
        static_count = int(0.1 * total_hosts)
        dhcp_start = subnet.network_address + 1 + static_count
        dhcp_end = subnet.broadcast_address - static_count - 1
        return {
            "dhcp_start": str(dhcp_start),
            "dhcp_stop": str(dhcp_end),
        }

    def _get_vlan_description(self, vlan_id):
        if vlan_id == 0:
            return "Reserved for priority-tagged frames"
        elif vlan_id == 1:
            return "Default VLAN, often used for management"
        elif vlan_id == 4095:
            return "Reserved for implementation use"
        elif 1002 <= vlan_id <= 1005:
            return "Reserved for Token Ring and FDDI VLANs in Cisco"
        return "Dynamic"

    def _get_subnet_purpose(self, cidr):
        reserved_subnets = {
            "192.168.4.0/24": "Reserved for Teleport VPN server",
            "10.255.253.0/24": "Reserved for Inter-VLAN routing (VLAN 4040)",
        }
        return reserved_subnets.get(cidr)


if __name__ == "__main__":
    try:
        input_data = json.load(sys.stdin)
        input_data['vpcs'] = json.loads(input_data['vpcs'])
        ubiquity_unifi = json.loads(input_data.get('ubiquity_unifi', 'false'))

        encoder = TerraformDataExternal()
        encoder.process_inputs(input_data)

        for vpc in encoder.source["vpcs"]:
            vpc_generator = VpcGenerator(vpc, ubiquity_unifi)
            vpc_subnets = vpc_generator.generate_subnets()
            if str(vpc["vpc_id"]) not in encoder.config:
                encoder.config[str(vpc["vpc_id"])] = {}
            encoder.config[str(vpc["vpc_id"])]["subnets"] = vpc_subnets

        encoded_result = encoder.encode_data()
        print(json.dumps({"output": encoded_result}))
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON input: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
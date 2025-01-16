import pytest
import json
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.vpc_blueprint import VpcGenerator
from scripts.placeholder_processor import PlaceholderProcessor

def test_vpc_generator_init():
    """Test initialization of VpcGenerator."""
    vpc_config = {
        "vpc_id": 1,
        "vpc_cidr": "192.168.0.0/24",
        "vpc_name": "Test VPC",
        "vpc_subnets": 2,
        "settings": {"vlan_range": "1-2"},
        "template": {}
    }
    generator = VpcGenerator(vpc_config)
    assert generator.vpc == vpc_config
    assert generator.ubiquity_unifi == False

def test_generate_subnets():
    """Test the generation of subnets."""
    vpc_config = {
        "vpc_id": 1,
        "vpc_cidr": "10.0.0.0/24",
        "vpc_name": "Test VPC",
        "vpc_subnets": 2,
        "settings": {"vlan_range": "1,2"},
        "template": {
            "domain": "{vpc_name}.lan",
            "name": "{vpc_name} {count_index}"
        }
    }
    generator = VpcGenerator(vpc_config)
    subnets = generator.generate_subnets()
    
    assert len(subnets) == 2  # Since we defined 2 VLANs
    for subnet in subnets:
        assert "cidr" in subnet
        assert "device_count" in subnet
        assert "uuid" in subnet
        assert "vlan_id" in subnet
        assert "name" in subnet
        assert "domain" in subnet
        assert "gateway" in subnet
        assert "dhcp_start" in subnet
        assert "dhcp_stop" in subnet
        assert "description" in subnet

def test_generate_subnets_with_unifi():
    """Test subnet generation with Unifi specific settings."""
    vpc_config = {
        "vpc_id": 1,
        "vpc_cidr": "192.168.0.0/16",
        "vpc_name": "Test VPC",
        "vpc_subnets": 4,  # Might need to be increased if 192.168.4.0/24 doesn't appear with this setting
        "settings": {"vlan_range": "1,2,3,4"},
        "template": {
            "domain": "{vpc_name}.lan",
            "name": "{vpc_name} {count_index}"
        }
    }
    generator = VpcGenerator(vpc_config, ubiquity_unifi=True)
    subnets = generator.generate_subnets()
    
    # Check if the reserved subnet for Teleport VPN is handled correctly by name
    teleport_subnet = next((s for s in subnets if s.get('name') == "Teleport VPN server"), None)
    assert teleport_subnet is not None
    assert teleport_subnet['dhcp_start'] is None
    assert teleport_subnet['dhcp_stop'] is None
    assert teleport_subnet['domain'] is None
    assert teleport_subnet['gateway'] is None
    assert teleport_subnet['description'] == "Reserved for Teleport VPN server"

    # Ensure other subnets are generated correctly
    other_subnets = [s for s in subnets if s.get('name') != "Teleport VPN server"]
    # Adjust expectation if necessary based on how many subnets are actually generated
    assert len(other_subnets) == 3  # 4 VLANs specified, one is reserved for Teleport VPN

def test_parse_vlan_range():
    """Test parsing of VLAN range strings."""
    generator = VpcGenerator({})
    assert generator._parse_vlan_range("1-3") == [1, 2, 3]
    assert generator._parse_vlan_range("1,2,3") == [1, 2, 3]
    assert generator._parse_vlan_range("1") == [1]

def test_calculate_new_prefix():
    """Test calculation of new prefix for subnet division."""
    generator = VpcGenerator({})
    assert generator._calculate_new_prefix(24, 2) == 25  # /24 to /25 for 2 subnets
    with pytest.raises(ValueError):
        generator._calculate_new_prefix(32, 2)  # Can't divide /32 further

if __name__ == "__main__":
    pytest.main([__file__])
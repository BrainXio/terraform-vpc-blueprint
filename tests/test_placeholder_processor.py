import pytest
import json
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.placeholder_processor import PlaceholderProcessor


def test_init_with_vpcs():
    """Test initialization with proper VPC data."""
    data = {
        "vpcs": [
            {
                "vpc_id": 1,
                "vpc_name": "Test VPC",
                "vpc_subnets": 2,
            }
        ]
    }
    processor = PlaceholderProcessor(data)
    assert 'vpcs' in processor.data


def test_init_without_vpcs():
    """Test initialization without 'vpcs' key."""
    data = {
        "vpc_id": 1,
        "vpc_name": "Test VPC",
        "vpc_subnets": 2,
    }
    processor = PlaceholderProcessor(data)
    assert 'vpcs' in processor.data
    assert len(processor.data['vpcs']) == 1


def test_create_context():
    """Test context creation with flattened data."""
    vpc = {
        "vpc_id": 1,
        "vpc_name": "Test VPC",
        "settings": {"domain": "lan"},
    }
    processor = PlaceholderProcessor({"vpcs": [vpc]})
    context = processor._create_context(vpc)
    assert 'vpc_id' in context
    assert 'vpc_name' in context
    assert 'settings_domain' in context  # Flattened key
    assert context['count_index'] == 0


def test_process():
    """Test processing of VPC configurations."""
    input_data = {
        "vpcs": [
            {
                "vpc_id": 1,
                "vpc_name": "Test VPC",
                "vpc_subnets": 2,
                "template": {
                    "domain": "{vpc_name}.lan",
                    "name": "{vpc_name}_{vpc_id}",
                },
            }
        ]
    }
    processor = PlaceholderProcessor(input_data)
    result = processor.process()
    parsed_result = json.loads(result)
    assert len(parsed_result) == 2  # 2 subnets for Test VPC
    for item in parsed_result:
        assert item['domain'] == "Test VPC.lan"
        assert item['name'] == "Test VPC_1"
        assert 'vlan_id' in item


def test_resolve_placeholders():
    """Test placeholder resolution in strings."""
    vpc = {
        "vpc_id": 1,
        "vpc_name": "Test VPC",
        "settings": {
            "domain": "lan",
            "subdomains": ["a", "b"],
        },
    }
    processor = PlaceholderProcessor({"vpcs": [vpc]})
    context = processor._create_context(vpc)

    # Test with a single placeholder
    assert processor._resolve_placeholders("{vpc_id}", context, 0) == "1"

    # Test with multiple placeholders and list cycling
    assert processor._resolve_placeholders("{vpc_name}_{settings_subdomains}.{settings_domain}", context, 1) == "Test VPC_b.lan"


def test_resolve_template():
    """Test template resolution."""
    vpc = {
        "vpc_id": 1,
        "vpc_name": "Test VPC",
        "template": {
            "domain": "{vpc_name}.lan",
            "name": "{vpc_name}_{vpc_id}",
        },
    }
    processor = PlaceholderProcessor({"vpcs": [vpc]})
    context = processor._create_context(vpc)

    resolved = processor._resolve_template(vpc['template'], context, 0)
    assert resolved['domain'] == "Test VPC.lan"
    assert resolved['name'] == "Test VPC_1"


if __name__ == "__main__":
    pytest.main([__file__])

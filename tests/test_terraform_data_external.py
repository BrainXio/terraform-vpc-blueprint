import pytest
import json
import base64
from datetime import datetime
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.terraform_data_external import TerraformDataExternal

def test_init():
    """Test initialization of TerraformDataExternal."""
    encoder = TerraformDataExternal()
    assert isinstance(encoder.config, dict)
    assert isinstance(encoder.source, dict)
    assert isinstance(encoder.timestamp, str)

def test_process_inputs_valid_json():
    """Test processing valid JSON string input."""
    encoder = TerraformDataExternal()
    test_input = json.dumps({"vpcs": [{"vpc_id": 1, "vpc_cidr": "192.168.0.0/24", "vpc_name": "Test VPC", "vpc_subnets": 2}]})
    
    encoder.process_inputs(test_input)
    assert encoder.source == json.loads(test_input)
    assert isinstance(encoder.timestamp, str)

def test_process_inputs_invalid_json():
    """Test processing invalid JSON string input."""
    encoder = TerraformDataExternal()
    test_input = '{"invalid": json}'
    
    with pytest.raises(ValueError, match="Input data is not valid JSON"):
        encoder.process_inputs(test_input)

def test_process_inputs_dict_input():
    """Test processing dictionary input."""
    encoder = TerraformDataExternal()
    test_input = {"vpcs": [{"vpc_id": 1, "vpc_cidr": "192.168.0.0/24", "vpc_name": "Test VPC", "vpc_subnets": 2}]}
    
    encoder.process_inputs(test_input)
    assert encoder.source == test_input
    assert isinstance(encoder.timestamp, str)

def test_process_inputs_non_dict():
    """Test processing non-dictionary input."""
    encoder = TerraformDataExternal()
    
    with pytest.raises(ValueError, match="Input data must be a dictionary"):
        encoder.process_inputs(["not", "a", "dict"])

def test_encode_data():
    """Test encoding data to base64."""
    encoder = TerraformDataExternal()
    encoder.config = {"test": "config"}
    encoder.source = {"test": "source"}
    encoder.timestamp = datetime.now().isoformat()

    encoded = encoder.encode_data()
    decoded = json.loads(base64.b64decode(encoded).decode())
    
    assert isinstance(encoded, str)
    assert decoded == {
        "config": {"test": "config"},
        "source": {"test": "source"},
        "timestamp": encoder.timestamp
    }

def test_encode_data_with_error():
    """Test handling of JSON encoding errors."""
    # This test is tricky because JSON encoding errors are rare unless you manually corrupt data types.
    # Here, we'll force an error by trying to encode something unserializable:

    class Unserializable:
        def __repr__(self):
            return "Unserializable object"

    encoder = TerraformDataExternal()
    encoder.config = Unserializable()
    
    with pytest.raises(TypeError):  # Changed to TypeError
        encoder.encode_data()

if __name__ == "__main__":
    pytest.main([__file__])
import base64
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TerraformDataExternal:
    def __init__(self):
        """
        Initialize the class with a simplified, flattened structure.
        """
        self.config = {}
        self.source = {}
        self.timestamp = datetime.now().isoformat()

    def process_inputs(self, input_data):
        """
        Processes input data, updating the 'source' field.

        :param input_data: Dictionary or JSON string of input data to process.
        :raises ValueError: If input data is not valid JSON or is not a dictionary.
        """
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON input: {e}")
                raise ValueError("Input data is not valid JSON") from e

        if not isinstance(input_data, dict):
            logger.error("Input data is not a dictionary")
            raise ValueError("Input data must be a dictionary")

        self.source = input_data
        self.timestamp = datetime.now().isoformat()  # Update timestamp
        logger.info("Input processed successfully")

    def encode_data(self):
        """
        Encodes the data into JSON, then Base64.

        :return: A base64 encoded string of the data.
        :raises TypeError: If encoding to JSON fails due to non-serializable objects.
        """
        try:
            data_to_encode = {
                "config": self.config,
                "source": self.source,
                "timestamp": self.timestamp,
            }
            json_data = json.dumps(data_to_encode)
            encoded = base64.b64encode(json_data.encode()).decode()
            logger.info("Data encoded to base64")
            return encoded
        except TypeError as e:
            logger.error(f"Error encoding data to JSON: {e}")
            raise


if __name__ == "__main__":
    # Example data for testing
    test_input = {
        "vpcs": [
            {
                "vpc_id": 1,
                "vpc_cidr": "192.168.0.0/24",
                "vpc_name": "Test VPC",
                "vpc_subnets": 2,
            }
        ]
    }

    try:
        # Create an instance of TerraformDataExternal
        encoder = TerraformDataExternal()

        # Process the test input
        encoder.process_inputs(test_input)

        # Test encode_data method
        encoded_result = encoder.encode_data()
        print(f"Encoded Data:\n{encoded_result}")

        # Decode and print the data
        decoded_data = json.loads(base64.b64decode(encoded_result).decode())
        print("\nDecoded Data:")
        print(json.dumps(decoded_data, indent=2))
    except ValueError as ve:
        logger.error(f"ValueError occurred: {ve}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# WLFI Name Service Python SDK

This SDK provides a convenient Python interface for interacting with the WLFI Name Service's smart contracts and metadata API.

## Installation

The SDK is not yet published to PyPI. To use it, you can install it directly from the local directory. It is highly recommended to use a virtual environment.

```bash
# Navigate to the SDK directory
cd python_sdk

# Install the SDK
pip install .

# For development, install in editable mode
pip install -e .
```

## Interacting with the Smart Contracts

The `ContractClient` class provides a high-level interface for interacting with the WLFI Name Service smart contracts.

### Example Usage:

```python
from wlfins_sdk.contracts import ContractClient

# Initialize the client (connects to a local Hardhat node by default)
# To connect to a different network, pass the provider URL:
# client = ContractClient(web3_provider_url="https://mainnet.infura.io/v3/YOUR_PROJECT_ID")
client = ContractClient()

# Get all contract instances
all_contracts = client.get_all_contracts()

# Access a specific contract
registrar = all_contracts.get("Registrar")

# You can now call functions on the contract
# For example (replace with a real function call):
# grace_period = registrar.functions.gracePeriod().call()
# print(f"Grace period: {grace_period}")
```

## Interacting with the Metadata API

The `WLFIApiClient` class allows you to fetch data from the WLFI Name Service metadata API.

### Example Usage:

```python
from wlfins_sdk.api_client import WLFIApiClient

# Initialize the client (connects to localhost:3001 by default)
api_client = WLFIApiClient()

# The token ID is the decimal representation of the namehash
example_token_id = "2727872353928655157841542879942343446921942823933093953431841122373210533342"

# Get the metadata for a token
metadata = api_client.get_metadata(example_token_id)
print(metadata)

# Get the SVG image for a token
svg_image = api_client.get_image(example_token_id)
# print(svg_image)

# Get the composite PNG image for a token
png_image = api_client.get_composite_image(example_token_id)
# You can save this to a file:
# with open("image.png", "wb") as f:
#     f.write(png_image)
```

## Utility Functions

The `utils.py` module provides helpful functions, such as `namehash` for computing ENS-compatible namehashes.

```python
from wlfins_sdk.utils import namehash

# Example: Compute the namehash for a domain
domain_name = "myname.wlfi"
hashed_node = namehash(domain_name)
print(f"Namehash of '{domain_name}': {hashed_node.hex()}")
```

## Contract Addresses (Mainnet)

When interacting with upgradeable contracts, always use the **Proxy** address.

*   **WLFIRegistryNFT:** `0x9E4730D0Cf58666BB8E4c39a20F58ebc3784A2F8`
*   **PublicResolver:** `0xA26ADBb653D0aA79e8b0cfF5B4637c3077856636`
*   **Registrar:** `0x545e3DC0Bd807df1Fa72Be095354F43C7eB5CCe9`
*   **ReverseRegistrar:** `0x4d9d06E47232848fffcd196D3Fb94244b20D1078`
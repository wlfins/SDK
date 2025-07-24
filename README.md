# WLFI Name Service Python SDK

This SDK provides convenient Python interfaces for interacting with the WLFI Name Service API and its smart contracts. It's designed to help developers easily integrate WLFI Name Service functionalities into their Python applications.

## Table of Contents
- [WLFI Name Service Python SDK](#wlfi-name-service-python-sdk)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Using pip](#using-pip)
    - [Development Installation](#development-installation)
  - [Usage](#usage)
    - [API Client](#api-client)
    - [Contract Client](#contract-client)
    - [Utility Functions](#utility-functions)
  - [Contract Addresses](#contract-addresses)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

### Prerequisites
- Python 3.7+
- `pip` (Python package installer)
- It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### Using pip

To install the SDK, navigate to the `python_sdk` directory and install it using pip:

```bash
cd C:/DEV/WLFIns/python_sdk
pip install .
```

Alternatively, if you are in the project root (`C:/DEV/WLFIns`), you can install directly:

```bash
pip install ./python_sdk
```

### Development Installation

If you are developing the SDK or want to make changes and see them reflected immediately without reinstalling, install it in editable mode:

```bash
cd C:/DEV/WLFIns/python_sdk
pip install -e .
```

This allows you to make changes to the source code, and they will be reflected without needing to reinstall the package.

## Usage

### API Client

The `WLFIApiClient` class allows you to interact with the WLFI Name Service metadata and image API endpoints.

```python
from wlfins_sdk.api_client import WLFIApiClient

# Initialize the API client.
# The default base_url is "http://localhost:3001".
# If your API is deployed, replace with your actual API URL.
api_client = WLFIApiClient(base_url="http://your-deployed-api-url.com")

# Example: Fetch metadata for a token ID
# Replace "123" with an actual token ID from your WLFI Name Service.
try:
    token_id = "123"
    metadata = api_client.get_metadata(token_id)
    print(f"Metadata for token {token_id}:\n{metadata}")
except requests.exceptions.RequestException as e:
    print(f"Error fetching metadata: {e}")

# Example: Fetch SVG image for a token ID
try:
    image_svg = api_client.get_image(token_id)
    print(f"SVG image for token {token_id} (first 200 chars):\n{image_svg[:200]}...")
except requests.exceptions.RequestException as e:
    print(f"Error fetching image: {e}")
```

### Contract Client

The `ContractClient` class enables interaction with the WLFI Name Service smart contracts on the Ethereum blockchain using `web3.py`.

```python
from wlfins_sdk.contracts import ContractClient
from web3 import Web3
from web3.middleware import geth_poa_middleware # Required for PoA networks like Ganache/Hardhat local node

# Initialize the contract client.
# The default web3_provider_url is "http://127.0.0.1:8545" (Hardhat/Ganache default).
# Replace with your actual blockchain node URL (e.g., Infura, Alchemy, local node).
contract_client = ContractClient(web3_provider_url="http://127.0.0.1:8545")

# If connecting to a Proof-of-Authority (PoA) network (like a local Hardhat node or Ganache),
# you might need to inject the Geth PoA middleware:
# contract_client.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Ensure connection
if not contract_client.w3.is_connected():
    print("Failed to connect to Web3 provider. Please ensure your node is running.")
    exit()

print("Connected to Web3 provider:", contract_client.w3.is_connected())

# Get contract instances using their proxy addresses
# These addresses are for the mainnet deployment. Adjust if using a different network.
REGISTRAR_ADDRESS = "0x545e3DC0Bd807df1Fa72Be095354F43C7eB5CCe9"
PUBLIC_RESOLVER_ADDRESS = "0xdBF2CC067580DDE08096ba280f8A631E069626c3"
REVERSE_REGISTRAR_ADDRESS = "0x4d9d06E47232848fffcd196D3Fb94244b20D1078"
WLFI_REGISTRY_NFT_ADDRESS = "0x9E4730D0Cf58666BB8E4c39a20F58ebc3784A2F8"

registrar_contract = contract_client.get_contract("Registrar", REGISTRAR_ADDRESS)
public_resolver_contract = contract_client.get_contract("PublicResolver", PUBLIC_RESOLVER_ADDRESS)
reverse_registrar_contract = contract_client.get_contract("ReverseRegistrar", REVERSE_REGISTRAR_ADDRESS)
wlfi_registry_nft_contract = contract_client.get_contract("WLFIRegistryNFT", WLFI_REGISTRY_NFT_ADDRESS)

print(f"Registrar contract functions: {dir(registrar_contract.functions)}")
print(f"PublicResolver contract functions: {dir(public_resolver_contract.functions)}")
print(f"ReverseRegistrar contract functions: {dir(reverse_registrar_contract.functions)}")
print(f"WLFIRegistryNFT contract functions: {dir(wlfi_registry_nft_contract.functions)}")

# Example: Call a view function on the Registrar contract (e.g., get grace period)
try:
    grace_period = registrar_contract.functions.gracePeriod().call()
    print(f"Registrar grace period: {grace_period} seconds")
except Exception as e:
    print(f"Error calling Registrar.gracePeriod(): {e}")

# Example: Call a view function on the WLFIRegistryNFT contract (e.g., get owner of a token)
# You'll need a valid tokenId.
# try:
#     token_id_to_check = 12345 # Replace with an actual token ID
#     owner_address = wlfi_registry_nft_contract.functions.ownerOf(token_id_to_check).call()
#     print(f"Owner of token {token_id_to_check}: {owner_address}")
# except Exception as e:
#     print(f"Error calling WLFIRegistryNFT.ownerOf(): {e}")

# Example: Sending a transaction (requires a connected wallet and unlocked account)
# IMPORTANT: For sending transactions, you need to manage your private keys securely.
# This example assumes you have an account managed by your Web3 provider (e.g., Hardhat node).
# For production, consider using libraries like `eth-account` for local signing or a wallet service.

# from web3.auto import w3 # For local signing with a private key
# from eth_account import Account
#
# # Configure your private key (NEVER hardcode in production!)
# private_key = "0x..." # Replace with your actual private key
# account = Account.from_key(private_key)
# contract_client.w3.eth.default_account = account.address
#
# # Example: Register a domain (requires sufficient ETH/payment token and approval if using ERC20)
# # Ensure the 'register' function parameters match your contract's ABI
# try:
#     domain_name_to_register = "testdomain"
#     duration_in_seconds = 31536000 # 1 year
#     payment_token_address = Web3.to_checksum_address("0x...") # Address of WLFI or USD1 token
#
#     # Get the fee for the name
#     fee_wei = registrar_contract.functions.getFeeForName(domain_name_to_register).call()
#     print(f"Fee for '{domain_name_to_register}': {Web3.from_wei(fee_wei, 'ether')} ETH (or equivalent)")
#
#     # Build the transaction
#     transaction = registrar_contract.functions.register(
#         domain_name_to_register,
#         payment_token_address,
#         duration_in_seconds
#     ).build_transaction({
#         'from': account.address,
#         'value': fee_wei, # Or the equivalent in payment token if using ERC20
#         'nonce': contract_client.w3.eth.get_transaction_count(account.address),
#         'gasPrice': contract_client.w3.eth.gas_price
#     })
#
#     # Sign the transaction
#     signed_txn = contract_client.w3.eth.account.sign_transaction(transaction, private_key)
#
#     # Send the transaction
#     tx_hash = contract_client.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#     print(f"Transaction sent. Hash: {tx_hash.hex()}")
#
#     # Wait for the transaction to be mined
#     receipt = contract_client.w3.eth.wait_for_transaction_receipt(tx_hash)
#     print("Transaction receipt:", receipt)
#
# except Exception as e:
#     print(f"Error sending transaction: {e}")
```

### Utility Functions

The `utils.py` module provides helpful functions, such as `namehash` for computing ENS-compatible namehashes.

```python
from wlfins_sdk.utils import namehash

# Example: Compute the namehash for a domain
domain_name = "myname.wlfi"
hashed_node = namehash(domain_name)
print(f"Namehash of '{domain_name}': {hashed_node.hex()}")

# Example: Namehash of an empty string (root node)
empty_name_hash = namehash("")
print(f"Namehash of empty string: {empty_name_hash.hex()}")
```

## Contract Addresses

These are the mainnet contract addresses for the WLFI Name Service. When interacting with upgradeable contracts, always use the **Proxy** address.

*   **WLFIRegistryNFT (Proxy):** `0x9E4730D0Cf58666BB8E4c39a20F58ebc3784A2F8`
    *   *Implementation:* `0x493fef71D67ec526aac73e383B7d3d5C841f9E19`
*   **PublicResolver:** `0xdBF2CC067580DDE08096ba280f8A631E069626c3`
*   **Registrar (Proxy):** `0x545e3DC0Bd807df1Fa72Be095354F43C7eB5CCe9`
    *   *Implementation:* `0xd0501aa8ab30acc3fa6878b31b3e4112c3ddae5f` (Note: This implementation is currently unverified on Etherscan.)
*   **ReverseRegistrar (Proxy):** `0x4d9d06E47232848fffcd196D3Fb94244b20D1078`
    *   *Implementation:* `0x9d4fcc02e0cac577359be9f6fb32624b2b6c29f7`

## Contributing

We welcome contributions to the WLFI Name Service Python SDK! If you have suggestions, bug reports, or want to contribute code, please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/wlfins/SDK).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


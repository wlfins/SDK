from web3 import Web3
import json
import os

class ContractClient:
    def __init__(self, web3_provider_url: str = "http://127.0.0.1:8545"):
        self.w3 = Web3(Web3.HTTPProvider(web3_provider_url))
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Web3 provider.")

        self.contracts = {}
        self.abi_paths = {
            "Registrar": "C:/DEV/WLFIns/artifacts/contracts/Registrar.sol/Registrar.json",
            "PublicResolver": "C:/DEV/WLFIns/artifacts/contracts/PublicResolver.sol/PublicResolver.json",
            "ReverseRegistrar": "C:/DEV/WLFIns/artifacts/contracts/ReverseRegistrar.sol/ReverseRegistrar.json",
            "WLFIRegistryNFT": "C:/DEV/WLFIns/artifacts/contracts/WLFIRegistryNFT.sol/WLFIRegistryNFT.json",
        }

    def _load_abi(self, contract_name: str):
        abi_path = self.abi_paths.get(contract_name)
        if not abi_path or not os.path.exists(abi_path):
            raise FileNotFoundError(f"ABI file not found for {contract_name} at {abi_path}")
        with open(abi_path, 'r') as f:
            return json.load(f)['abi']

    def get_contract(self, contract_name: str, contract_address: str):
        if contract_name not in self.contracts:
            abi = self._load_abi(contract_name)
            self.contracts[contract_name] = self.w3.eth.contract(address=contract_address, abi=abi)
        return self.contracts[contract_name]

# Example Usage (assuming contract addresses are known or deployed)
if __name__ == '__main__':
    try:
        client = ContractClient()
        print("Connected to Web3 provider:", client.w3.is_connected())

        # Replace with actual deployed contract addresses
        REGISTRAR_ADDRESS = "0x545e3DC0Bd807df1Fa72Be095354F43C7eB5CCe9"
<<<<<<< HEAD
        PUBLIC_RESOLVER_ADDRESS = "0xA26ADBb653D0aA79e8b0cfF5B4637c3077856636"
        REVERSE_REGISTRAR_ADDRESS = "0x4d9d06E47232848fffcd196D3Fb94244b20D1078"
        WLFI_REGISTRY_NFT_ADDRESS = "0x9E4730D0Cf58666BB8E4c39a20F58ebc3784A2F8"

        # Get contract instances
        registrar_contract = client.get_contract("Registrar", REGISTRAR_ADDRESS)
        public_resolver_contract = client.get_contract("PublicResolver", PUBLIC_RESOLVER_ADDRESS)
        reverse_registrar_contract = client.get_contract("ReverseRegistrar", REVERSE_REGISTRAR_ADDRESS)
        wlfi_registry_nft_contract = client.get_contract("WLFIRegistryNFT", WLFI_REGISTRY_NFT_ADDRESS)

        print(f"Registrar contract functions: {dir(registrar_contract.functions)}")
        print(f"PublicResolver contract functions: {dir(public_resolver_contract.functions)}")
        print(f"ReverseRegistrar contract functions: {dir(reverse_registrar_contract.functions)}")
        print(f"WLFIRegistryNFT contract functions: {dir(wlfi_registry_nft_contract.functions)}")

        # Example: Call a view function (replace with actual function and parameters)
        # try:
        #     grace_period = registrar_contract.functions.gracePeriod().call()
        #     print(f"Registrar grace period: {grace_period}")
        # except Exception as e:
        #     print(f"Error calling gracePeriod: {e}")

    except ConnectionError as e:
        print(f"Web3 connection error: {e}")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

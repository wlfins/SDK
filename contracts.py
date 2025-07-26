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
        self.contract_addresses = {
            "WLFIRegistryNFT": "0x9E4730D0Cf58666BB8E4c39a20F58ebc3784A2F8",
            "PublicResolver": "0xA26ADBb653D0aA79e8b0cfF5B4637c3077856636",
            "Registrar": "0x545e3DC0Bd807df1Fa72Be095354F43C7eB5CCe9",
            "ReverseRegistrar": "0x4d9d06E47232848fffcd196D3Fb94244b20D1078",
        }

    def _load_abi(self, contract_name: str):
        abi_path = self.abi_paths.get(contract_name)
        if not abi_path or not os.path.exists(abi_path):
            raise FileNotFoundError(f"ABI file not found for {contract_name} at {abi_path}")
        with open(abi_path, 'r') as f:
            return json.load(f)['abi']

    def get_contract(self, contract_name: str):
        if contract_name not in self.contracts:
            contract_address = self.contract_addresses.get(contract_name)
            if not contract_address:
                raise ValueError(f"Address not found for contract: {contract_name}")
            abi = self._load_abi(contract_name)
            self.contracts[contract_name] = self.w3.eth.contract(address=contract_address, abi=abi)
        return self.contracts[contract_name]

    def get_all_contracts(self):
        return {
            name: self.get_contract(name) for name in self.contract_addresses.keys()
        }

# Example Usage
if __name__ == '__main__':
    try:
        client = ContractClient()
        print("Connected to Web3 provider:", client.w3.is_connected())

        # Get all contract instances
        all_contracts = client.get_all_contracts()

        for name, contract in all_contracts.items():
            print(f"\n--- {name} ({contract.address}) ---")
            # Print the first 5 functions for brevity
            print("Functions:", list(contract.functions)[:5])

        # Example: Call a view function from the Registrar
        registrar = all_contracts.get("Registrar")
        if registrar:
            try:
                # This is an example, replace with a valid function if needed
                # grace_period = registrar.functions.gracePeriod().call()
                # print(f"\nRegistrar grace period: {grace_period}")
                pass
            except Exception as e:
                print(f"\nError calling view function on Registrar: {e}")

    except ConnectionError as e:
        print(f"Web3 connection error: {e}")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
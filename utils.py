from web3 import Web3

def namehash(name: str) -> bytes:
    """
    Computes the ENS namehash of a given name.
    """
    node = Web3.keccak(b'')
    if name:
        labels = name.split('.')
        for label in reversed(labels):
            node = Web3.keccak(node + Web3.keccak(text=label))
    return node

# Example Usage:
if __name__ == '__main__':
    domain = "example.wlfi"
    hashed_name = namehash(domain)
    print(f"Namehash of '{domain}': {hashed_name.hex()}")

    empty_name_hash = namehash("")
    print(f"Namehash of empty string: {empty_name_hash.hex()}")

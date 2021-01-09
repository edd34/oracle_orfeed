from web3 import Web3

minABI = [
    # balanceOf
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    # decimals
    {
        "constant": true,
        "inputs": [],
        "name":"decimals",
        "outputs":[{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

class ERC20:
    def __init__(self, web3, token_address):
        self.w3 = web3
        self.token_address = Web3.toChecksumAddress(token_address)
        self.erc20_contract = self.w3.eth.contract(address=self.token_address, abi=minABI)

    def decimals():
        return self.erc20_contract.functions.decimals()

    def balanceOf(owner_address):
        return self.erc20_contract.functions.balanceOf(owner_address)

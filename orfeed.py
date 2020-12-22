import web3
from web3 import Web3
import os
from smartcontracts import my_smartcontracts, aave_liquidity_provider

class Orfeed:
    def __init__(self, network, project_id, private_key=None):
        self.network = network
        self.project_id = project_id
        self.private_key = private_key
        self.orfeed_address = Web3.toChecksumAddress(my_smartcontracts["orfeed"]["address"])
        if private_key is not None:
            web3.eth.Account().from_key(private_key)
        self.w3 = Web3(Web3.HTTPProvider('https://'+self.network+'.infura.io/v3/'+project_id))
        self.orfeed_contract = self.w3.eth.contract(address=self.orfeed_address, abi=my_smartcontracts["orfeed"]["abi"])
    
    def getExchangeRate(self, _from, _to, _provider, _amount):
        if _from == _to or _amount <= 0:
            return 0

        try:
            res = self.orfeed_contract.functions.getExchangeRate(_from, _to, _provider, Web3.toWei(_amount, 'ether')).call()
            return Web3.fromWei(res, 'ether')
        except Exception:
            return 0

class Registry:
    def __init__(self, network, project_id, private_key=None):
        self.network = network
        self.project_id = project_id
        self.private_key = private_key
        self.registry_address = Web3.toChecksumAddress(my_smartcontracts["registry"]["address"])
        if private_key is not None:
            web3.eth.Account().from_key(private_key)
        self.w3 = Web3(Web3.HTTPProvider('https://'+self.network+'.infura.io/v3/'+project_id))
        self.registry_contract = self.w3.eth.contract(address=self.registry_address, abi=my_smartcontracts["registry"]["abi"])
    
    def getAllOracles(self):
        res = self.registry_contract.functions.getAllOracles().call()
        return res

    def getOracleInfo(self, name_reference=None):
        res = self.registry_contract.functions.getOracleInfo(name_reference).call()
        return res

from functions import getTokenToTokenPriceFeed, getEthToTokenPriceFeed
import pprint
from web3 import Web3, eth
import web3
import os
from orfeed import Orfeed
from data import init_dict_token_dex, orfeed_list_providers
import time

w3 = Web3(Web3.HTTPProvider('https://'+os.getenv("NETWORK")+'.infura.io/v3/'+os.getenv("INFURA_PROJECT_ID")))
orfeed_i = Orfeed(w3)
res = getEthToTokenPriceFeed(orfeed_i, verbose = True)
sorted_list = sorted(res.items(), key=lambda x: x[1]["res"]["%"], reverse=True)
top3 = [sorted_list[i] for i in range(3)]
pprint.pprint(top3)

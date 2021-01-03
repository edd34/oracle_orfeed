from functions import getTokenToTokenPriceFeed
import pprint
from web3 import Web3, eth
import web3
import os
from orfeed import Orfeed
from data import init_dict_token_dex, orfeed_list_providers
import time
from tqdm import tqdm

w3 = Web3(Web3.HTTPProvider('https://'+os.getenv("NETWORK")+'.infura.io/v3/'+os.getenv("INFURA_PROJECT_ID")))
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) # uncomment if you use ganache-cli
orfeed_i = Orfeed(w3)
while True:
    res = getTokenToTokenPriceFeed(orfeed_i, verbose=True)
    sorted_list = sorted(res.items(), key=lambda x: x[1]["%"], reverse=True)
    os.system('clear')
    pprint.pprint(sorted_list)
    cooldown = 20
    for i in tqdm(range(cooldown), desc="cooldown, waiting for new block"):
        time.sleep(1)

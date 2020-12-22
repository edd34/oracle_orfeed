import os
import time
import pprint
from data import init_dict_token_dex, orfeed_list_providers
from orfeed import Orfeed, Registry
from dotenv import load_dotenv
load_dotenv()
from web3 import Web3

orfeed_i = Orfeed(os.getenv("NETWORK"), os.getenv("INFURA_PROJECT_ID"))
registry_i = Registry(os.getenv("NETWORK"), os.getenv("INFURA_PROJECT_ID"))
dict_token_dex = init_dict_token_dex()

def getAllPriceFeed(threshold = 0):
    result = []
    
    for token in dict_token_dex:
        a = time.perf_counter()
        tmp = {
            token: {}
        }
        
        for provider in dict_token_dex[token]:
            res = orfeed_i.getExchangeRate("ETH", token, provider, 1)
            if res > 0:
                tmp[token][provider] = res
                # print(token + "("+ provider+")" + " = " + str(res))
        
        if not tmp[token]:
            continue

        key_max = max(tmp[token].keys(), key=(lambda k:tmp[token][k]))
        key_min = min(tmp[token].keys(), key=(lambda k:tmp[token][k]))
        
        if key_min == key_max:
            continue

        verdict = {
            "token" : token,
            "buy" : {
                "provider" : key_min,
                "price" : tmp[token][key_min]
            } ,
            "sell" : {
                "provider" : key_max,
                "price" : tmp[token][key_max]
            },
            "res" : {
                "%" : (tmp[token][key_max] - tmp[token][key_min]) * 100 /tmp[token][key_min] ,
                "spread" : tmp[token][key_max] - tmp[token][key_min]
            }
        }
        if float(verdict["res"]["%"]) > threshold:
            result.append(verdict)
    return result


def getPriceFeed(token):
    tmp = {
        token: {}
    }

    for provider in orfeed_list_providers:
        res = orfeed_i.getExchangeRate("ETH", token, provider, 1)
        if res > 0:
            tmp[token][provider] = res

    if not tmp[token]:
        return {}

    key_max = max(tmp[token].keys(), key=(lambda k:tmp[token][k]))
    key_min = min(tmp[token].keys(), key=(lambda k:tmp[token][k]))
    
    if key_min == key_max:
        return {}

    verdict = {
        token: {
            "buy" : {
                "provider" : key_min,
                "at" : tmp[token][key_min]
            } ,
            "sell" : {
                "provider" : key_max,
                "at" : tmp[token][key_max]
            },
            "res" : {
                "%" : (tmp[token][key_max] - tmp[token][key_min]) * 100 /tmp[token][key_min] ,
                "spread" : tmp[token][key_max] - tmp[token][key_min]
            }
        }
    }
    return verdict
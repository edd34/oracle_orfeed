import os
import time
import pprint
from data import init_dict_token_dex, orfeed_list_providers, init_dict_token_token_dex
from orfeed import Orfeed
from dotenv import load_dotenv
load_dotenv()
from web3 import Web3

def getEthToTokenPriceFeed(orfeed_i, threshold = 0, verbose = False):
    result = {}
    dict_token_dex = init_dict_token_dex()

    for token in dict_token_dex:
        tmp = {
            token: {}
        }
        for provider in dict_token_dex[token]:
            res = orfeed_i.getExchangeRateEthToToken(token, provider)
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
            # "token_address": orfeed_i.getTokenAddress(token),
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
            result[token] = verdict
            if verbose:
                pprint.pprint(verdict)

    return result

def getTokenToTokenPriceFeed(orfeed_i, threshold = 0):
    result = []
    dict_token_dex = init_dict_token_token_dex()
    for pair in dict_token_dex:
        tmp_res = {}
        for provider in ["UNISWAPBYSYMBOLV2", "KYBERBYSYMBOLV1"]:
            res = getTokenToTokenPrice(orfeed_i, pair["tokenSrc"], pair["tokenDst"], provider)

            if tmp_res.get(res["tokenPair"], None) == None:
                tmp_res[res["tokenPair"]] = {}
            tmp_res[res["tokenPair"]]["provider"] = provider
            tmp_res[res["tokenPair"]]["price"] = res["price"]
            pprint.pprint(tmp_res)


def getTokenToTokenPrice(orfeed_i, tokenSrc, tokenDst, provider):
    res = orfeed_i.getExchangeRateNormalized(tokenSrc, tokenDst, provider)

    return {
        "tokenSrc" : tokenSrc,
        "tokenDst" : tokenDst,
        "tokenPair" : tokenSrc + '-' + tokenDst,
        "provider" : provider,
        "price" : res
    }

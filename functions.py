import os
import time
import pprint
from data import init_dict_token_dex, orfeed_list_providers, init_dict_token_token_dex
from orfeed import Orfeed
from dotenv import load_dotenv
load_dotenv()
import web3
from web3 import Web3
from tqdm import tqdm

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

def getTokenToTokenPriceFeed(orfeed_i, threshold = 0, verbose = False):
    result = {}
    dict_token_dex = init_dict_token_dex()
    for token in tqdm(dict_token_dex, desc="finding arbitrage", total=len(dict_token_dex)):
        tmp_res = {}
        for provider in ["UNISWAPBYSYMBOLV2", "KYBERBYSYMBOLV1"]:
            buy = getTokenToTokenPrice(orfeed_i, "ETH", token, provider, amount=orfeed_i.w3.toWei('1', 'ether'))
            sell = getTokenToTokenPrice(orfeed_i, token, "ETH", provider, amount=buy["price"])
            if not(buy["price"] > 0 and sell["price"] > 0):
                continue

            tmp_res[provider] = {
                "buy_price_wei": buy["price"]/1e18,
                "sell_price_wei": sell["price"]*buy["price"]/(1e18*1e18),
            }

        if len(tmp_res.keys()) != 2:
            continue

        path = {
            "U->K": (tmp_res['KYBERBYSYMBOLV1']['sell_price_wei'] - tmp_res['UNISWAPBYSYMBOLV2']['buy_price_wei'])/tmp_res['UNISWAPBYSYMBOLV2']['buy_price_wei'] * 100,
            "K->U": (tmp_res['UNISWAPBYSYMBOLV2']['sell_price_wei'] - tmp_res['KYBERBYSYMBOLV1']['buy_price_wei'])/tmp_res['KYBERBYSYMBOLV1']['buy_price_wei'] * 100
        }
        if path["U->K"] > path["K->U"] and path["U->K"] > 0: # buy at uniswap and sell at kyber
            result[token] = {
                "buy_at": "UNISWAPBYSYMBOLV2",
                "buy_price": tmp_res["UNISWAPBYSYMBOLV2"]["buy_price_wei"],
                "sell_at": "KYBERBYSYMBOLV1",
                "sell_price": tmp_res["KYBERBYSYMBOLV1"]["sell_price_wei"],
                "%": path["U->K"]
            }
        elif path["K->U"] > path["U->K"] and path["K->U"] > 0: # buy at kyber and sell at uniswap
            result[token] = {
                "sell_at": "UNISWAPBYSYMBOLV2",
                "sell_price": tmp_res["UNISWAPBYSYMBOLV2"]["sell_price_wei"],
                "buy_at": "KYBERBYSYMBOLV1",
                "buy_price": tmp_res["KYBERBYSYMBOLV1"]["buy_price_wei"],
                "%": path["K->U"]
            }
        else:
            continue

        if verbose:
            print(""+ token + ' : ' + result[token]["buy_at"] + " -> " + result[token]["sell_at"] + ' : ' + str(result[token]["%"]))
            # pprint.pprint({token: result[token]})
            print("")
    return result


def getTokenToTokenPrice(orfeed_i, tokenSrc, tokenDst, provider, amount=1, normalized=False):
    if normalized == True:
        res = orfeed_i.getExchangeRateNormalized(tokenSrc, tokenDst, provider)
    else:
        res = orfeed_i.getExchangeRate(tokenSrc, tokenDst, provider, amount)

    return {
        "tokenSrc" : tokenSrc,
        "tokenDst" : tokenDst,
        "tokenPair" : tokenSrc + '-' + tokenDst,
        "provider" : provider,
        "price" : res
    }

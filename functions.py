import os
import time
import pprint
from data import init_dict_token_dex
from orfeed import Orfeed
from dotenv import load_dotenv
load_dotenv()
import web3
from web3 import Web3
from tqdm import tqdm

def getTokenToTokenPriceFeed(orfeed_i, threshold = 0, verbose = False):
    result = {}
    dict_token_dex = init_dict_token_dex()
    providers_list = ["UNISWAPBYSYMBOLV2", "KYBERBYSYMBOLV1"]
    for token in tqdm(dict_token_dex, desc="finding arbitrage", total=len(dict_token_dex)):
        tmp_res = {}
        for provider in providers_list:
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
            "one": (tmp_res[providers_list[1]]['sell_price_wei'] - tmp_res[providers_list[0]]['buy_price_wei'])/tmp_res[providers_list[0]]['buy_price_wei'] * 100,
            "two": (tmp_res[providers_list[0]]['sell_price_wei'] - tmp_res[providers_list[1]]['buy_price_wei'])/tmp_res[providers_list[1]]['buy_price_wei'] * 100
        }
        if path["one"] > path["two"] and path["one"] > 0: # buy at uniswap and sell at kyber
            result[token] = {
                "buy_at": providers_list[0],
                "buy_price": tmp_res[providers_list[0]]["buy_price_wei"],
                "sell_at": providers_list[1],
                "sell_price": tmp_res[providers_list[1]]["sell_price_wei"],
                "%": path["one"]
            }
        elif path["two"] > path["one"] and path["two"] > 0: # buy at kyber and sell at uniswap
            result[token] = {
                "sell_at": providers_list[0],
                "sell_price": tmp_res[providers_list[0]]["sell_price_wei"],
                "buy_at": providers_list[1],
                "buy_price": tmp_res[providers_list[1]]["buy_price_wei"],
                "%": path["two"]
            }
        else:
            continue

        if verbose:
            print(""+ token + ' : ' + result[token]["buy_at"] + " -> " + result[token]["sell_at"] + ' : ' + str(result[token]["%"]))
            pprint.pprint({token: result[token]})
            print("")
    return result

def simple_getTokenToTokenPrice(orfeed_i, token):
    result = {}
    providers_list = ["UNISWAPBYSYMBOLV2", "KYBERBYSYMBOLV1"]
    tmp_res = {}
    for provider in providers_list:
        buy = getTokenToTokenPrice(orfeed_i, "ETH", token, provider, amount=orfeed_i.w3.toWei('1', 'ether'))
        sell = getTokenToTokenPrice(orfeed_i, token, "ETH", provider, amount=buy["price"])
        if buy["price"] > 0 and sell["price"] > 0:
            tmp_res[provider] = {
                "buy_price_wei": buy["price"]/1e18,
                "sell_price_wei": sell["price"]*buy["price"]/(1e18*1e18),
            }
        else:
            return -1

    path = {
        "one": (tmp_res[providers_list[1]]['sell_price_wei'] - tmp_res[providers_list[0]]['buy_price_wei'])/tmp_res[providers_list[0]]['buy_price_wei'] * 100,
        "two": (tmp_res[providers_list[0]]['sell_price_wei'] - tmp_res[providers_list[1]]['buy_price_wei'])/tmp_res[providers_list[1]]['buy_price_wei'] * 100
    }

    if path["one"] > path["two"] and path["one"] > 0: # buy at uniswap and sell at kyber
        result = {
            "buy_at": providers_list[0],
            "buy_price": tmp_res[providers_list[0]]["buy_price_wei"],
            "sell_at": providers_list[1],
            "sell_price": tmp_res[providers_list[1]]["sell_price_wei"],
            "%": path["one"]
        }
    elif path["two"] > path["one"] and path["two"] > 0: # buy at kyber and sell at uniswap
        result = {
            "sell_at": providers_list[0],
            "sell_price": tmp_res[providers_list[0]]["sell_price_wei"],
            "buy_at": providers_list[1],
            "buy_price": tmp_res[providers_list[1]]["buy_price_wei"],
            "%": path["two"]
        }
    else:
        result = -1

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

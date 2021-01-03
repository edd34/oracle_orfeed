token_symbols = ["DAI", "USDC", "MKR", "LINK", "BAT", "WBTC", "BTC", "USDT",
                 "OMG", "ZRX", "TUSD", "LEND", "REP", "BNT", "PAX",  "SUSD", "KNC"]

orfeed_list_providers = ["UNISWAPBYSYMBOLV1", "UNISWAPBYSYMBOLV2", "KYBERBYSYMBOLV1"]

def init_dict_token_dex():
    token_dex = {}
    for token in token_symbols:
        token_dex[token] = {}
        for provider in orfeed_list_providers:
            token_dex[token][provider] = 0
    return token_dex

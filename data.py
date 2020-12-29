

token_symbols = ["SAI", "DAI", "USDC", "MKR", "LINK", "BAT", "WBTC", "BTC",
                       "OMG", "ZRX", "TUSD", "LEND", "ADAI", "REP", "ZIL", "AST",
                       "HOT", "KCS", "MXM", "CRO", "BNB", "BNT", "HT", "PAX", "CDAI",
                       "CSAI", "USDT", "SUSD", "SEUR", "SGBP", "SETH", "SJPY", "PAY"]

forex_rate_symbols = ['USD', 'EUR', 'CHF', 'JPY', 'GBP', 'sETH']

orfeed_list_providers = ["UNISWAPBYSYMBOLV1", "UNISWAPBYSYMBOLV2", "KYBERBYSYMBOLV1"]

def init_dict_token_dex():
    token_dex = {}
    for token in token_symbols:
        token_dex[token] = {}
        for provider in orfeed_list_providers:
            token_dex[token][provider] = 0
    return token_dex

def init_dict_token_token_dex():
    res = []
    path_resolved = []
    for tokenSrc in token_symbols:
        for tokenDst in token_symbols:
            for provider in orfeed_list_providers:
                pair_list = {tokenSrc, tokenDst}
                if tokenSrc != tokenDst and (pair_list not in path_resolved):
                    path_resolved.append(pair_list)
                    elem = {
                        "tokenSrc": tokenSrc,
                        "tokenDst": tokenDst
                    }
                    res.append(elem)
    return res

from .binance import Binance
from .bittrex import Bittrex
from .poloniex import Poloniex


def all_exchanges():
    return [Binance, Bittrex, Poloniex]


ALL_EXCHANGE_NAMES = ["binance", "bittrex", "poloniex"]
BID_ASK_ONLY = ["binance"]

from .binance import Binance
from .bittrex import Bittrex
from .poloniex import Poloniex


def all_exchanges():
    return [Binance, Bittrex, Poloniex]

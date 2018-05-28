from .bittrex import Bittrex
from .poloniex import Poloniex


def all_exchanges():
    return [Bittrex, Poloniex]

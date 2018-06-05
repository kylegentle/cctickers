import aiohttp
from datetime import datetime
from decimal import Decimal

from .base import Exchange


class Binance(Exchange):

    def __init__(self):
        Exchange.__init__(self, "binance")
        self.base_url = "https://api.binance.com"
        self.wait_time_sec = 0.06

    def has_pair(self, pair):
        return self._format_pair(pair) in self.markets

    async def _connect(self):
        endpoint = self.base_url + "/api/v1/exchangeInfo"
        session = aiohttp.ClientSession()
        async with session.get(endpoint) as resp:
            try:
                assert resp.status == 200
                resp_dict = await resp.json()
                self.markets = {
                    market["symbol"]: True for market in resp_dict["symbols"]
                }
                return session
            except AssertionError:
                raise Exception(f"Bad response code {resp.status} from {resp.url}")

    @Exchange.async_static_rate_limit
    async def _get_ticker(self, pair):
        endpoint = self.base_url + "/api/v3/ticker/bookTicker"
        pair = self._format_pair(pair)
        params = {"symbol": pair}

        async with self.session.get(endpoint, params=params) as resp:
            try:
                assert resp.status == 200
                resp_dict = await resp.json()
                ticker = {
                    "timestamp": datetime.now(),
                    "exchange": self.name,
                    "pair": pair,
                    "bid": Decimal(resp_dict["bidPrice"]),
                    "ask": Decimal(resp_dict["askPrice"]),
                    "last": None,
                }
                return ticker
            except AssertionError:
                raise Exception(f"Bad response code {resp.status} from {resp.url}")

    @staticmethod
    def _format_pair(pair):
        return "".join(pair.split("-")[::-1]).replace("-", "")

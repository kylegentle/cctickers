import aiohttp
from datetime import datetime
from decimal import Decimal

from .base import Exchange


class Bittrex(Exchange):

    def __init__(self):
        Exchange.__init__(self, "bittrex")
        self.base_url = "https://bittrex.com/api/v1.1/public"
        self.wait_time_sec = 1

    def has_pair(self, pair):
        return pair in self.markets

    async def _connect(self):
        endpoint = self.base_url + "/getmarkets"
        session = aiohttp.ClientSession()
        async with session.get(endpoint, timeout=10) as resp:
            try:
                assert resp.status == 200
                resp_dict = await resp.json()
                self.markets = {market["MarketName"] for market in resp_dict["result"]}
                return session
            except AssertionError:
                raise Exception(f"Bad response code {resp.status} from {resp.url}")

    @Exchange.async_static_rate_limit
    async def _get_ticker(self, pair):
        endpoint = self.base_url + "/getticker"
        params = {"market": pair}

        async with self.session.get(endpoint, params=params, timeout=10) as resp:
            try:
                resp_dict = await resp.json()
                assert resp_dict["success"] is True
                resp_ticker = resp_dict["result"]
                ticker = {
                    "timestamp": datetime.now(),
                    "exchange": self.name,
                    "pair": pair,
                    "bid": Decimal(str(resp_ticker["Bid"])),
                    "ask": Decimal(str(resp_ticker["Ask"])),
                    "last": Decimal(str(resp_ticker["Last"])),
                }
                return ticker
            except AssertionError:
                raise Exception(
                    f"Failed to retrieve ticker from {self.name}, "
                    f"endpoint={resp.url}, response={resp.status}"
                )

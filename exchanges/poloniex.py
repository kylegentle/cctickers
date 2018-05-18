import aiohttp
from datetime import datetime

from exchanges.base import Exchange


class Poloniex(Exchange):
    def __init__(self):
        Exchange.__init__(self, 'poloniex')
        self.endpoint = 'https://poloniex.com/public'
        self.wait_time_sec = 1

    async def _connect(self):
        params = {'command': 'returnTicker'}
        session = aiohttp.ClientSession()
        async with session.get(self.endpoint, params=params) as resp:
            try:
                assert resp.status == 200
                return session
            except AssertionError:
                raise Exception(f'Bad response code {resp.status} '
                                f'from {resp.url}')

    def _build_currency_dict(self, response_dict):
        currencies = dict()
        for coin, data in response_dict.items():
            coin_id = data['id']
            currencies[coin_id] = {'name': data['name'],
                                   'tx_fee': data['txFee'], }
        return currencies

    @Exchange.async_static_rate_limit
    async def _get_ticker(self, pair):
        pair = self._normalize_pair(pair)
        params = {'command': 'returnTicker'}

        async with self.session.get(self.endpoint, params=params) as resp:
            try:
                assert resp.status == 200
                resp_dict = await(resp.json())
                resp_ticker = resp_dict[pair]
                ticker = {'timestamp': datetime.now(),
                          'exchange': self.name,
                          'pair': pair,
                          'bid': resp_ticker['highestBid'],
                          'ask': resp_ticker['lowestAsk'],
                          'last': resp_ticker['last'], }
                return ticker
            except AssertionError:
                raise Exception(f'Bad response code {resp.status} '
                                f'from {resp.url}')

    @staticmethod
    def _normalize_pair(pair):
        return '_'.join(pair.split('-'))

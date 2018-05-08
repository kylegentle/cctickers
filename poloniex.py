import aiohttp
from datetime import datetime
import logging

from exchange import Exchange


class Poloniex(Exchange):
    def __init__(self):
        Exchange.__init__(self, 'poloniex')
        self.endpoint = 'https://poloniex.com/public'
        self.wait_time_sec = 1

    async def _connect(self):
        params = {'command': 'returnCurrencies'}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint, params=params) as resp:
                try:
                    assert resp.status == 200
                    response_dict = await resp.json()
                    self.currencies = self._read_currency_data(response_dict)
                except AssertionError:
                    raise Exception(f'Bad response code {resp.status} '
                                    f'from {resp.url}')

    def _read_currency_data(self, response_dict):
        currencies = dict()
        for coin, data in response_dict.items():
            currencies[data['id']] = {
                'name': data['name'],
                'tx_fee': data['txFee'],
            }
        return currencies

    @Exchange.async_static_rate_limit
    async def _get_ticker(self, pair):
        pair = self._normalize(pair)
        params = {'command': 'returnTicker'}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint, params=params) as resp:
                try:
                    assert resp.status == 200
                    resp_dict = await(resp.json())
                    resp_ticker = resp_dict[pair]
                    ticker = {
                        'timestamp': datetime.now(),
                        'exchange': self.name,
                        'pair': pair,
                        'bid': resp_ticker['highestBid'],
                        'ask': resp_ticker['lowestAsk'],
                        'last': resp_ticker['last'],
                    }
                    return ticker
                except AssertionError:
                    raise Exception(f'Bad response code {resp.status} '
                                    f'from {resp.url}')

    @staticmethod
    def _normalize(pair):
        return '_'.join(pair.split('-'))

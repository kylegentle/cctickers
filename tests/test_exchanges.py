import asyncio
from datetime import datetime
from decimal import Decimal

import aiohttp
import pytest
import uvloop

from tickerqueue.exchanges import all_exchanges, BID_ASK_ONLY

EXCHANGE_CLASSES = all_exchanges()


class TestExchange:

    @pytest.fixture(scope="class")
    def event_loop(self):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
        yield loop
        loop.close()

    @pytest.mark.asyncio
    @pytest.fixture(scope="class", params=EXCHANGE_CLASSES)
    async def exchange(self, request):
        exchange_cls = request.param
        exchange = await exchange_cls.create()
        yield exchange
        await exchange.session.close()

    @pytest.mark.asyncio
    @pytest.fixture(scope="class")
    async def ticker(self, exchange):
        pair = "BTC-ETH"
        ticker = await exchange._get_ticker(pair)
        return ticker

    def test_init(self, exchange):
        assert exchange.connected is True
        assert isinstance(exchange.session, aiohttp.ClientSession)

    @pytest.mark.parametrize(
        "key,key_type",
        [
            ("timestamp", datetime),
            ("exchange", str),
            ("bid", Decimal),
            ("ask", Decimal),
            ("last", Decimal),
        ],
    )
    def test_get_ticker(self, ticker, key, key_type):
        if key == "last" and ticker["exchange"] in BID_ASK_ONLY:
            pytest.skip("f{exchange} API does not report last price")
        assert isinstance(ticker[key], key_type)

    @pytest.mark.parametrize("pair", ["BTC-ETH", "BTC-XRP", "BTC-XMR", "BTC-LTC"])
    def test_has_pair(self, exchange, pair):
        assert exchange.has_pair(pair)

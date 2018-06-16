import asyncio
from datetime import datetime
from decimal import Decimal

import aiohttp
import pytest

from tickerqueue.exchanges import all_exchanges

EXCHANGE_CLASSES = all_exchanges()


# TODO: Refactor for pytest-asyncio?
class TestExchange:

    @pytest.fixture(scope="module")
    def loop(self):
        loop = asyncio.get_event_loop()
        yield loop
        loop.close()

    @pytest.fixture(scope="module", params=EXCHANGE_CLASSES)
    def exchange(self, loop, request):
        exchange_cls = request.param
        setup_task = asyncio.ensure_future(exchange_cls.create())
        exchange = loop.run_until_complete(setup_task)
        yield exchange
        teardown_task = asyncio.ensure_future(exchange.session.close())
        loop.run_until_complete(teardown_task)

    def test_init(self, exchange):
        assert exchange.connected is True
        assert isinstance(exchange.session, aiohttp.ClientSession)

    @pytest.fixture
    def ticker(self, exchange, loop):
        pair = "BTC-ETH"
        ticker_task = asyncio.ensure_future(exchange._get_ticker(pair))
        ticker = loop.run_until_complete(ticker_task)
        return ticker

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
        if key == "last":
            assert isinstance(ticker[key], key_type) or ticker[key] is None
        else:
            assert isinstance(ticker[key], key_type)

    @pytest.mark.parametrize("pair", ["BTC-ETH", "BTC-XRP", "BTC-XMR", "BTC-LTC"])
    def test_has_pair(self, exchange, pair):
        assert exchange.has_pair(pair)

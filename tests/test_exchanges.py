import asyncio
from datetime import datetime
from decimal import Decimal

import aiohttp
import pytest

from tickerqueue.exchanges import all_exchanges

EXCHANGE_CLASSES = all_exchanges()


class TestExchange:

    @pytest.fixture(scope="module")
    def loop(self):
        return asyncio.get_event_loop()

    @pytest.fixture(scope="module", params=EXCHANGE_CLASSES)
    def exchange(self, loop, request):
        setup_task = asyncio.ensure_future(request.param.create())
        exchange = loop.run_until_complete(setup_task)
        yield exchange
        teardown_task = asyncio.ensure_future(exchange.session.close())
        loop.run_until_complete(teardown_task)

    def test_init(self, exchange):
        assert exchange.connected is True
        assert isinstance(exchange.session, aiohttp.ClientSession)

    def test_get_ticker(self, loop, exchange):
        pair = "BTC-ETH"
        ticker_task = asyncio.ensure_future(exchange._get_ticker(pair))
        ticker = loop.run_until_complete(ticker_task)
        assert isinstance(ticker["timestamp"], datetime)
        assert ticker["exchange"] is not None
        assert isinstance(ticker["bid"], Decimal)
        assert isinstance(ticker["ask"], Decimal)
        assert isinstance(ticker["last"], Decimal) or ticker["last"] is None

    def test_has_pairs(self, exchange):
        assert exchange.has_pair("BTC-ETH")
        assert exchange.has_pair("BTC-XRP")
        assert exchange.has_pair("BTC-XMR")

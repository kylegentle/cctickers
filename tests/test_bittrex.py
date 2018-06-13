import asyncio
from datetime import datetime
from decimal import Decimal

import aiohttp
import pytest

from tickerqueue.exchanges import Bittrex


class TestBittrex:

    @pytest.fixture(scope="module")
    def loop(self):
        return asyncio.get_event_loop()

    @pytest.fixture(scope="module")
    def bittrex(self, loop):
        init_task = asyncio.ensure_future(Bittrex.create())
        bittrex = loop.run_until_complete(init_task)
        yield bittrex
        teardown_task = asyncio.ensure_future(bittrex.session.close())
        loop.run_until_complete(teardown_task)

    def test_init(self, bittrex):
        assert bittrex.connected is True
        assert isinstance(bittrex.session, aiohttp.ClientSession)

    def test_get_ticker(self, loop, bittrex):
        pair = "BTC-ETH"
        ticker_task = asyncio.ensure_future(bittrex._get_ticker(pair))
        ticker = loop.run_until_complete(ticker_task)
        assert isinstance(ticker["timestamp"], datetime)
        assert ticker["exchange"] is not None
        assert isinstance(ticker["bid"], Decimal)
        assert isinstance(ticker["ask"], Decimal)
        assert isinstance(ticker["last"], Decimal)

    def test_has_pair(self, bittrex):
        assert bittrex.has_pair("BTC-ETH")
        assert bittrex.has_pair("BTC-XMR")
        assert bittrex.has_pair("BTC-SC")

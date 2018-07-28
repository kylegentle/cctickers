import time

import pytest

from cctickers import tickerqueue, ALL_EXCHANGE_NAMES


class TestTickerQueue:

    @pytest.mark.parametrize("pair", ["BTC-ETH", "BTC-XRP", "BTC-XMR", "BTC-LTC"])
    def test_tickerqueue(self, pair):
        result = set()
        with tickerqueue(pair) as tq:
            start_time = time.time()

            while time.time() < start_time + 3:
                result.add(tq.get()["exchange"])

        assert result == set(ALL_EXCHANGE_NAMES)

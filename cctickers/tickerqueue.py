import asyncio
import logging
from multiprocessing import Process, Queue

import uvloop

from .exchanges import all_exchanges


def tickerqueue(pair, exchanges=all_exchanges()):
    logging.basicConfig(level=logging.INFO)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    q = Queue()
    streamer = Process(
        target=_enqueue_tickers_from_exchanges,
        args=(*exchanges,),
        kwargs={"queue": q, "pair": pair.upper()},
        name="streamer",
    )
    streamer.start()
    return q


def _enqueue_tickers_from_exchanges(*exchanges, queue=None, pair=None):
    loop = asyncio.get_event_loop()
    exchanges = initialize_exchanges(loop, *exchanges)
    exchanges = [ex for ex in exchanges if ex.has_pair(pair)]
    ticker_stream_tasks = [
        asyncio.ensure_future(ex.stream_ticker(pair, queue)) for ex in exchanges
    ]
    loop.run_until_complete(asyncio.gather(*ticker_stream_tasks))


def initialize_exchanges(loop, *exchange_classes):
    creation_tasks = [
        asyncio.ensure_future(ex.create(report_coro=enqueue_ticker))
        for ex in exchange_classes
    ]
    exchanges = loop.run_until_complete(asyncio.gather(*creation_tasks))
    return exchanges


async def enqueue_ticker(self, pair, mp_queue):
    while True:
        mp_queue.put_nowait(await self._get_ticker(pair))

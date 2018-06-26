import asyncio
import logging

import uvloop

from .exchanges import all_exchanges


def stream(pair, exchanges=all_exchanges()):
    logging.basicConfig(level=logging.INFO)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    exchanges = initialize_exchanges(loop, *exchanges)
    exchanges = [ex for ex in exchanges if ex.has_pair(pair.upper())]
    ticker_stream_tasks = [
        asyncio.ensure_future(ex.stream_ticker(pair.upper())) for ex in exchanges
    ]
    loop.run_until_complete(asyncio.gather(*ticker_stream_tasks))


def initialize_exchanges(loop, *exchange_classes):
    creation_tasks = [asyncio.ensure_future(ex.create()) for ex in exchange_classes]
    exchanges = loop.run_until_complete(asyncio.gather(*creation_tasks))
    return exchanges

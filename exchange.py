from abc import ABCMeta, abstractmethod
import asyncio
import datetime
from functools import wraps
import logging


class Exchange():
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name

    def wait_time_left(self):
        elapsed_sec = (datetime.now() - self.last_request).total_seconds()
        try:
            return self.wait_time_sec - elapsed_sec
        except TypeError:
            logging.ERROR(f'wait_time_sec is undefined for {self.name}')
            raise

    async def stream_ticker(self, pair, async_queue):
        while True:
            async_queue.put_nowait(await self.get_ticker)

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @abstractmethod
    async def get_ticker(self, pair):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def _create(cls):
        raise NotImplementedError

    @staticmethod
    async def async_rate_limit(api_method):
        @wraps(api_method)
        async def wrapper(*args, **kwargs):
            exchange = args[0]

            if exchange.last_request is None:
                return api_method(*args, **kwargs)

            wait_sec = exchange.wait_time_left()
            if exchange.wait_time_left > 0:
                await asyncio.sleep(wait_sec)

            return api_method(*args, **kwargs)
        return await wrapper

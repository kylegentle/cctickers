from abc import ABCMeta, abstractmethod
import asyncio
from datetime import datetime
from functools import wraps
import logging


class Exchange():
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name
        self.connected = False
        self.currencies = None
        self.last_request = None
        self.wait_time_sec = 5

    async def stream_ticker(self, pair, async_queue):
        while True:
            async_queue.put_nowait(await self._get_ticker(pair))

    def wait_time_left(self):
        elapsed_sec = (datetime.now() - self.last_request).total_seconds()
        try:
            return self.wait_time_sec - elapsed_sec
        except TypeError:
            logging.ERROR(f'wait_time_sec is undefined for {self.name}')
            raise

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @abstractmethod
    async def get_ticker(self, pair):
        raise NotImplementedError

    @classmethod
    async def create(cls):
        self = cls()
        try:
            await self._connect()
            self.connected = True
        except Exception as e:
            logging.INFO = print  # TODO: implement actual logging
            logging.INFO(f'Error initializing {self.name}: ' + str(e))
        return self

    @staticmethod
    def async_static_rate_limit(api_method):
        @wraps(api_method)
        async def wrapper(*args, **kwargs):
            exchange = args[0]

            if exchange.last_request is None:
                exchange.last_request = datetime.now()
                return await api_method(*args, **kwargs)

            wait_sec = exchange.wait_time_left()
            if wait_sec > 0:
                print(f'asynchronously waiting {wait_sec} seconds')
                await asyncio.sleep(wait_sec)
            exchange.last_request = datetime.now()

            return await api_method(*args, **kwargs)
        return wrapper

from abc import ABCMeta, abstractmethod
import asyncio
from functools import wraps
import logging
import time


class Exchange:
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name
        self.connected = False
        self.endpoint = None
        self.last_request = None
        self.markets = None
        self.pairs = None
        self.session = None
        self.wait_time_sec = 5

    async def stream_ticker(self, pair, mp_queue):
        while True:
            mp_queue.put_nowait(await self._get_ticker(pair))

    @classmethod
    async def create(cls, report_coro=None):
        Exchange.stream_ticker = report_coro or Exchange.stream_ticker
        self = cls()
        try:
            self.session = await self._connect()
            self.connected = True
        except Exception as e:
            logging.info(f"Error initializing {self.name}: " + str(e))
        return self

    @staticmethod
    def async_static_rate_limit(api_method):

        @wraps(api_method)
        async def wrapper(*args, **kwargs):
            exchange = args[0]

            if exchange.last_request is None:
                exchange.last_request = time.time()
                return await api_method(*args, **kwargs)

            wait_sec = exchange._wait_time_left()
            if wait_sec > 0:
                logging.debug(f"async waiting {wait_sec}s")
                await asyncio.sleep(wait_sec)
            exchange.last_request = time.time()

            return await api_method(*args, **kwargs)

        return wrapper

    def _wait_time_left(self):
        elapsed_sec = time.time() - self.last_request
        try:
            return self.wait_time_sec - elapsed_sec
        except TypeError:
            logging.error(f"wait_time_sec is undefined for {self.name}")
            raise

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @abstractmethod
    async def _get_ticker(self, pair):
        raise NotImplementedError

import asyncio

import pytest
import uvloop


@pytest.fixture(scope="session")
def event_loop():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

from contextlib import asynccontextmanager, contextmanager

import httpx


@asynccontextmanager
async def async_request_session(**kw):
    async with httpx.AsyncClient(**kw) as client:
        yield client


@contextmanager
def request_client(**kw):
    with httpx.Client(**kw) as client:
        yield client

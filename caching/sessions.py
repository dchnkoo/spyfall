from redis.asyncio import from_url
from settings import redis

from contextlib import asynccontextmanager
import typing as _t


@asynccontextmanager
async def cache_client(db: _t.Optional[int] = None, **kw):
    client = from_url(redis.dsn(db), decode_responses=True, encoding="utf-8", **kw)
    yield client
    await client.close()

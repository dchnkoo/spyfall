from .sessions import cache_client
from settings import redis

from contextlib import asynccontextmanager

from abc import ABC, abstractmethod

import pydantic as _p
import typing as _t


type seconds = int


class CacheModel[_K](ABC, _p.BaseModel):
    db: _t.ClassVar[int] = redis.db
    cache_prefix: _t.ClassVar[str] = ...
    cache_live_time: _t.ClassVar[seconds] = redis.default_cache_live_time

    @property
    @abstractmethod
    def cache_identity(self) -> _K: ...

    @staticmethod
    def build_cache_key(*args):
        return ":".join([str(i) for i in args])

    @classmethod
    def with_prefix(cls, *args):
        return cls.build_cache_key(cls.cache_prefix, *args)

    @property
    def cache_key(self):
        return self.build_cache_key(self.cache_prefix, self.cache_identity)

    @classmethod
    @asynccontextmanager
    async def cache_controller(cls, **kw):
        async with cache_client(cls.db, **kw) as client:
            yield client

    @classmethod
    async def load_raw_cached(cls, cache_identity: _K) -> _t.Optional[str]:
        async with cls.cache_controller() as client:
            return await client.get(cls.with_prefix(cache_identity))

    @classmethod
    async def load_cached(cls, cache_identity: _K):
        model = await cls.load_raw_cached(cache_identity=cache_identity)
        assert model is not None, "Model doesn't exists."
        return cls.model_validate_json(model)

    async def reload_cache(self) -> None:
        model = await self.load_cached(self.cache_identity)
        self.__dict__.update(model.__dict__)

    async def save_in_cache(self) -> None:
        async with self.cache_controller() as client:
            await client.set(
                self.cache_key, self.model_dump_json(), self.cache_live_time
            )

    async def delete_cache(self) -> None:
        async with self.cache_controller() as client:
            await client.delete(self.cache_key)

    @classmethod
    async def delete_cache_by_identity(cls, cache_identity: _K) -> None:
        model = await cls.load_cached(cache_identity)
        await model.delete_cache()

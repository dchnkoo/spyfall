from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from settings import postgres

import typing as _t
import asyncio


async_engine = create_async_engine(postgres.async_dsn)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
async_scoped = async_scoped_session(async_session, asyncio.current_task)


sync_engine = create_engine(postgres.dsn)
sync_session = sessionmaker(sync_engine, expire_on_commit=False)
sync_scoped = scoped_session(sync_session)


def async_session_manager[
    _F
](func: _t.Optional[_F] = None, *, create: bool = False) -> _F:
    """
    Automatically create or pass to the function session as kwarg argument.
    """

    def decorator(func: _F):
        async def wrapper(*args, **kwargs):
            if not create:
                session = async_scoped()
                res = await func(*args, session=session, **kwargs)
                await async_scoped.remove()
                return res
            else:
                async with async_session() as session:
                    return await func(*args, session=session, **kwargs)

        return wrapper

    return decorator(func) if callable(func) else decorator

from .session import async_session_manager

from sqlalchemy import exc
import sqlmodel as _sql

import pydantic as _p
import typing as _t

if _t.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    import uuid


class TableManager[T: _p.BaseModel, _K: (int, "uuid.UUID")]:

    if _t.TYPE_CHECKING:
        id: _K

    @classmethod
    @async_session_manager(create=True)
    async def add(
        cls, d: T | dict, *, session: _t.Optional["AsyncSession"] = None
    ) -> _t.Self:
        assert session is not None
        data = d if isinstance(d, dict) else d.model_dump()
        try:
            instance = cls(**data)
            session.add(instance)
            await session.commit()
        except exc.IntegrityError as e:
            await session.rollback()
            raise e
        else:
            return instance

    @async_session_manager(create=True)
    async def save(self, *, session: _t.Optional["AsyncSession"] = None) -> None:
        assert session is not None
        assert self.id is not None, "You cannot save doesn't exist object."

        await session.merge(self)
        await session.commit()
        await self.reload()

    @classmethod
    @async_session_manager
    async def load(
        cls, id: _K, *, session: _t.Optional["AsyncSession"] = None
    ) -> _t.Self:
        assert session is not None
        return await session.get(cls, id)

    @async_session_manager
    async def reload(self, *, session: _t.Optional["AsyncSession"] = None) -> None:
        assert session is not None
        instance = await self.load(self.id)
        self.__dict__.update(instance.__dict__)

    @async_session_manager(create=True)
    async def remove(self, *, session: _t.Optional["AsyncSession"] = None) -> None:
        assert session is not None
        await session.delete(self)
        await session.flush()

    @async_session_manager
    async def get_relation[
        _R
    ](
        self,
        relation_table: _R,
        *expr,
        one: bool = False,
        session: _t.Optional["AsyncSession"] = None,
    ) -> _t.Optional[_R | _t.Sequence[_R]]:
        assert session is not None

        query = _sql.select(relation_table).where(*expr)
        res = await session.execute(query)
        data = res.scalars().all()

        if one and not data:
            return None
        elif one and data:
            return data[0]
        return data

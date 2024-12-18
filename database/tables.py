from .session import async_session_manager
from .manager import TableManager
from .models import *
from . import bases

from functools import partial

from settings import spygame

import datetime as _date
import sqlmodel as _sql
import pydantic as _p
import typing as _t
import uuid

if _t.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from aiogram.types import User


metadata = _sql.SQLModel


class TelegramUser(
    metadata,
    bases.Dates,
    TelegramUserModel,
    TableManager[_t.Union[TelegramUserModel, "User"], int],
    table=True,
):

    @property
    def package_expression(self):
        return Package.owner_id == self.id

    async def get_settings(self) -> _t.Optional["Settings"]:
        return await self.get_relation(Settings, Settings.user_id == self.id, one=True)

    async def get_packages(self) -> _t.Sequence["Package"]:
        return await self.get_relation(Package, self.package_expression)

    async def get_with_base_package(self) -> _t.Tuple["Package"]:
        packages = await self.get_packages()
        base_package = await Package.get_base_package()
        return tuple([*packages, base_package])

    async def get_random_package(self) -> _t.Optional["Package"]:
        return await self.get_random(
            Package,
            _sql.or_(self.package_expression, Package.type == enums.PackageType.BASE),
        )

    async def number_of_packages(self) -> int:
        return await self.count(Package, self.package_expression)


class Package(
    metadata,
    bases.Dates,
    PackageModel,
    TableManager[PackageModel, uuid.UUID],
    table=True,
):

    owner_id: int = _sql.Field(
        foreign_key="telegramuser.id", ondelete="CASCADE", sa_type=_sql.BigInteger
    )

    @property
    def location_expression(self):
        return Location.package_id == self.id

    async def get_owner(self) -> TelegramUser:
        return await self.get_relation(
            TelegramUser, TelegramUser.id == self.owner_id, one=True
        )

    @classmethod
    @async_session_manager
    async def get_base_package(
        cls, *, session: _t.Union["AsyncSession", None] = None
    ) -> "Package":
        query = _sql.select(cls).where(cls.type == enums.PackageType.BASE)
        return (await session.execute(query)).scalar_one()

    async def get_random_location(self) -> _t.Optional["Location"]:
        return await self.get_random(Location, self.location_expression)

    async def get_locations(self) -> _t.Sequence["Location"]:
        return await self.get_relation(Location, self.location_expression)

    async def number_of_locations(self) -> int:
        return await self.count(Location, self.location_expression)


class Location(
    metadata,
    bases.Dates,
    LocationModel,
    TableManager[LocationModel, uuid.UUID],
    table=True,
):

    package_id: uuid.UUID = _sql.Field(foreign_key="package.id", ondelete="CASCADE")

    @property
    def role_expression(self):
        return Role.location_id == self.id

    async def get_package(self) -> Package:
        return await self.get_relation(Package, Package.id == self.package_id, one=True)

    async def get_roles(self) -> _t.Sequence["Role"]:
        return await self.get_relation(Role, self.role_expression)

    async def number_of_roles(self) -> int:
        return await self.count(Role, self.role_expression)


class Role(
    metadata, bases.Dates, RoleModel, TableManager[RoleModel, uuid.UUID], table=True
):

    location_id: uuid.UUID = _sql.Field(foreign_key="location.id", ondelete="CASCADE")

    @property
    def is_spy(self):
        return False

    async def get_location(self) -> Location:
        return await self.get_relation(
            Location, Location.id == self.location_id, one=True
        )


class Settings(
    metadata,
    bases.PrimaryKey,
    bases.Dates,
    TableManager["Settings", uuid.UUID],
    table=True,
):
    model_config = _p.ConfigDict(validate_assignment=True)

    user_id: int = _sql.Field(
        foreign_key="telegramuser.id", ondelete="CASCADE", sa_type=_sql.BigInteger
    )
    package_id: _t.Optional[uuid.UUID] = _sql.Field(
        foreign_key="package.id", ondelete="SET NULL"
    )
    use_locations_id: list[str] = _sql.Field(
        default_factory=list, sa_type=_sql.ARRAY(_sql.String)
    )
    use_roles_id: dict[str, list[str]] = _sql.Field(
        default_factory=dict, sa_type=_sql.JSON
    )
    two_spies: bool = False
    know_each_other: bool = False
    round_time: _date.timedelta = _sql.Field(
        sa_type=_sql.Interval,
        default_factory=partial(_date.timedelta, minutes=spygame.default_round_time),
    )
    rounds: int = spygame.default_rounds

    def reset_locations_and_roles(self):
        self.use_locations_id = []
        self.use_roles_id = {}

    def remove_game_package(self):
        self.package_id = None
        self.reset_locations_and_roles()

    def set_new_package(self, package_id: uuid.UUID):
        self.package_id = package_id
        self.reset_locations_and_roles()

    def get_location_roles(self, location_id: str) -> list[str]:
        arr = self.use_roles_id.get(location_id, None)
        if arr is None:
            arr = []
            self.use_roles_id[location_id] = arr
        return arr

    async def get_user(self) -> _t.Optional[TelegramUser]:
        return await self.get_relation(
            TelegramUser, TelegramUser.id == self.user_id, one=True
        )

    async def get_package(self) -> _t.Optional[Package]:
        return await self.get_relation(Package, Package.id == self.package_id, one=True)

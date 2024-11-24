from .manager import TableManager
from .models import *
from . import bases

from functools import partial

from settings import spygame

import datetime as _date
import sqlmodel as _sql
import typing as _t
import uuid

if _t.TYPE_CHECKING:
    from aiogram.types import User


metadata = _sql.SQLModel


class TelegramUser(
    metadata,
    bases.Dates,
    TelegramUserModel,
    TableManager[_t.Union[TelegramUserModel, "User"], int],
    table=True,
):

    packages: _t.List["Package"] = _sql.Relationship(back_populates="owner")
    settings: _t.Optional["Settings"] = _sql.Relationship(back_populates="user")

    @property
    def package_expression(self):
        return Package.owner_id == self.id

    async def get_settings(self) -> _t.Optional["Settings"]:
        return await self.get_relation(Settings, Settings.user_id == self.id, one=True)

    async def get_packages(self) -> _t.Sequence["Package"]:
        return await self.get_relation(Package, self.package_expression)

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

    owner: TelegramUser = _sql.Relationship(back_populates="packages")
    locations: _t.List["Location"] = _sql.Relationship(back_populates="package")

    @property
    def location_expression(self):
        return Location.package_id == self.id

    async def get_owner(self) -> _t.Optional[TelegramUser]:
        return await self.get_relation(
            TelegramUser, TelegramUser.id == self.owner_id, one=True
        )

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

    package: Package = _sql.Relationship(back_populates="locations")
    roles: _t.List["Role"] = _sql.Relationship(back_populates="location")

    @property
    def role_expression(self):
        return Role.location_id == self.id

    async def get_package(self) -> _t.Optional[Package]:
        return await self.get_relation(Package, Package.id == self.package_id, one=True)

    async def get_roles(self) -> _t.Sequence["Role"]:
        return await self.get_relation(Role, self.role_expression)

    async def number_of_roles(self) -> int:
        return await self.count(Role, self.role_expression)


class Role(
    metadata, bases.Dates, RoleModel, TableManager[RoleModel, uuid.UUID], table=True
):

    location_id: uuid.UUID = _sql.Field(foreign_key="location.id", ondelete="CASCADE")

    location: Location = _sql.Relationship(back_populates="roles")

    async def get_location(self) -> _t.Optional[Location]:
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

    user: TelegramUser = _sql.Relationship(back_populates="settings")
    package: _t.Optional[Package] = _sql.Relationship()

    async def get_user(self) -> _t.Optional[TelegramUser]:
        return await self.get_relation(
            TelegramUser, TelegramUser.id == self.user_id, one=True
        )

    async def get_package(self) -> _t.Optional[Package]:
        return await self.get_relation(Package, Package.id == self.package_id, one=True)

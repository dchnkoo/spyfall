from database import (
    async_session_manager,
    PackageScope,
    PackageType,
    Location,
    Package,
    Role,
)

from settings import ROOT_DIR

from spy.routers import spybot

import sqlmodel as _sql
import typing as _t
import json

if _t.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from database.models import BaseModel


BASE_LOCATION = (ROOT_DIR / __file__).parent / "base_locations.json"


BASE_PACKAGE_NAME = "BASE PACKAGE"


@async_session_manager
async def upload_base_locations(*, session: "AsyncSession"):
    query = _sql.select(Package).where(
        Package.name == BASE_PACKAGE_NAME, Package.type == PackageType.BASE
    )
    if (await session.execute(query)).scalar_one_or_none() is not None:
        return

    me = await spybot.get_me()

    package = Package(
        name=BASE_PACKAGE_NAME,
        scope=PackageScope.PUBLIC,
        type=PackageType.BASE,
        owner_id=me.id,
    )
    await package.save()

    with open(BASE_LOCATION, "r") as f:
        locations: list[dict] = json.load(f)

        for location in locations:
            roles_raw = location.pop("roles")

            location = Location(**location, package_id=package.id)
            await location.save()

            roles = [Role(**role, location_id=location.id) for role in roles_raw]
            for role in roles:
                await role.save()

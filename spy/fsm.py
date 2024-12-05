from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types

from database import Location, LocationModel, Package, Role, RoleModel
from settings import spygame

from pydantic import ValidationError

from utils.msg import create_new_query

from spy.callback import CallbackPrefix
from spy import texts

import typing as _t
import asyncio
import uuid

if _t.TYPE_CHECKING:
    from database import TelegramUser


class UpgradedStatesGroup(StatesGroup):

    msgs = {}

    @classmethod
    async def _save(
        cls,
        message: types.Message,
        state: FSMContext,
        user: "TelegramUser",
        **_,
    ):
        raise NotImplementedError


class PackageFSM(UpgradedStatesGroup):
    name = State()


class LocationFSM(UpgradedStatesGroup):
    name = State()
    image_url = State()
    save = State()

    @classmethod
    async def _save(
        cls,
        message: types.Message,
        state: FSMContext,
        user: "TelegramUser",
        **_,
    ):
        data = await state.get_data()

        package_id = uuid.UUID(data.pop("package_id"))

        package = await Package.load(package_id)

        try:
            location = LocationModel(**data)
            if location.image_url is not None:
                validate_image = await location.check_if_image_valid(location.image_url)
                if validate_image is False:
                    raise ValueError()
        except (ValidationError, ValueError):
            await user.send_message(texts.YOU_PROVIDED_NOT_VALID_IMAGE)
            await state.update_data(image_url=None)
            return

        locations = await package.get_locations()

        create_query = lambda msg: create_new_query(
            msg, data=CallbackPrefix.show_package + str(package_id), from_user=user
        )

        try:
            assert location not in set(locations), texts.FAILED_TO_ADD_LOCATION_EXIST
            assert (
                len(locations) != spygame.locations_limit
            ), texts.FAILED_TO_ADD_LOCATION_LIMIT
        except AssertionError as e:
            msg = await user.send_message(e.args[0])
            await state.clear()

            await asyncio.sleep(0.6)
            query = create_query(msg)
            return query

        await Location.add(location, package_id=package_id)

        await state.clear()
        msg = await user.send_message(texts.LOCATION_ADDED_SECCESSFULLY)

        query = create_query(msg)
        return query


class RoleFSM(UpgradedStatesGroup):
    name = State()
    description = State()
    save = State()

    @classmethod
    async def _save(
        cls,
        message: types.Message,
        state: FSMContext,
        user,
        **_,
    ):
        data = await state.get_data()
        location_id = uuid.UUID(data.pop("location_id"))

        location = await Location.load(location_id)

        try:
            role = RoleModel(**data)
        except ValidationError:
            await user.send_message(texts.DESCRIPTION_VALIDATION_ERROR)
            await state.update_data(description=None)
            return

        roles = await location.get_roles()

        create_query = lambda msg: create_new_query(
            msg, data=CallbackPrefix.show_location + str(location_id), from_user=user
        )

        try:
            assert role not in set(roles), texts.FAILED_TO_ADD_ROLE_EXISTS
            assert len(roles) != spygame.roles_limit, texts.FAILED_TO_ADD_ROLE_LIMIT
        except AssertionError as e:
            msg = await user.send_message(e.args[0])
            await state.clear()

            await asyncio.sleep(0.6)
            query = create_query(msg)
            return query

        await Role.add(role, location_id=location_id)

        await state.clear()
        msg = await user.send_message(texts.ROLE_ADDED)

        query = create_query(msg)
        return query

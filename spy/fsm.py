from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types

from database import Location, LocationModel, Package
from settings import spygame

from pydantic import ValidationError

from utils.msg import create_new_query

from spy.callback import CallbackPrefix
from spy import texts

import typing as _t
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

    msgs = {
        "name": (texts.ENTER_LOCATION_NAME, ()),
        "image_url": (texts.ENTER_LINK_ON_IMAGE_OR_SKIP, ()),
    }

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
        except ValidationError:
            await user.send_message(
                await texts.YOU_PROVIDED_NOT_VALID_IMAGE(user.language)
            )
            return

        if location.image_url is not None:
            if not (await location.check_if_image_valid(location.image_url)):
                await user.send_message(
                    await texts.YOU_PROVIDED_NOT_VALID_IMAGE(user.language)
                )
                return

        locations = await package.get_locations()

        if location in set(locations):
            await user.send_message(
                await texts.FAILED_TO_ADD_LOCATION_EXIST(user.language)
            )
            return

        if len(locations) == spygame.locations_limit:
            await user.send_message(
                await texts.FAILED_TO_ADD_LOCATION_LIMIT(user.language)
            )

        await Location.add(location, package_id=package_id)

        await state.clear()
        msg = await user.send_message(
            await texts.LOCATION_ADDED_SECCESSFULLY(user.language)
        )

        query = create_new_query(
            msg, data=CallbackPrefix.show_package + str(package_id), from_user=user
        )
        return query

from spy.routers import (
    private_only_msg_without_state,
    extract_message_filters,
    private_only_msg,
    no_command,
)
from spy.points.package import show_package
from spy.callback import CallbackPrefix
from spy import fsm, texts

from database import TelegramUser, Package, Location
from spy.decorators import with_user_cache

from utils.msg import create_new_query, handle_content_type_text
from utils.call_save import call_save
from utils.no_skip import no_skip

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, filters, F

import typing as _t
import asyncio
import uuid

if _t.TYPE_CHECKING:
    from database import TelegramUser


@no_skip(private_only_msg, filters.StateFilter(fsm.LocationFSM.name))
@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.add_location)
)
@with_user_cache
async def add_location(
    query: types.CallbackQuery, state: fsm.FSMContext, user: "TelegramUser", **_
):
    package_id = query.data.split(":", 1)[1]

    await state.set_state(fsm.LocationFSM.name)
    await state.update_data(package_id=package_id)

    await query.message.edit_text(await texts.ENTER_LOCATION_NAME(user.language))


@call_save(
    private_only_msg,
    filters.StateFilter(fsm.LocationFSM.image_url),
    call_after=show_package,
)
@private_only_msg.message(
    filters.StateFilter(fsm.LocationFSM.name), *extract_message_filters(no_command)
)
@with_user_cache
async def handle_location_name(
    message: types.Message, state: fsm.FSMContext, user: "TelegramUser", **_
):
    await state.update_data(name=message.text)
    await state.set_state(fsm.LocationFSM.image_url)

    await message.answer(await texts.ENTER_LINK_ON_IMAGE_OR_SKIP(user.language))


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.show_locations)
)
@with_user_cache
async def show_locations(query: types.CallbackQuery, user: "TelegramUser", **_):
    package_id = uuid.UUID(query.data.removeprefix(CallbackPrefix.show_locations))

    package = await Package.load(package_id)
    locations = await package.get_locations()

    if not locations:
        func = await handle_content_type_text(query)
        msg = await func(await texts.YOU_DOES_NOT_HAVE_LOCATIONS(user.language))

        if isinstance(msg, types.Message):
            query = create_new_query(
                query, data=CallbackPrefix.show_package + str(package_id)
            )

        await asyncio.sleep(0.6)
        await show_package(query)
        return

    keyboard = InlineKeyboardBuilder()
    for location in locations:
        keyboard.add(
            types.InlineKeyboardButton(
                text=location.name,
                callback_data=CallbackPrefix.show_location + str(location.id),
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=await texts.BACK(user.language),
                callback_data=CallbackPrefix.show_package + str(package_id),
            )
        )
        keyboard.adjust(1)

    text = (await texts.INFO_PACKAGE(user.language)).format(
        len(locations),
        package=package,
    )

    await (await handle_content_type_text(query))(
        text, reply_markup=keyboard.as_markup()
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.show_location)
)
@with_user_cache
async def show_location(query: types.CallbackQuery, user: "TelegramUser", **_):
    location_id = uuid.UUID(query.data.removeprefix(CallbackPrefix.show_location))
    location = await Location.load(location_id)

    await query.message.delete()

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.DELETE_LOCATION(user.language),
            callback_data=CallbackPrefix.delete_location + str(location.id),
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.ROLES(user.language),
            callback_data=CallbackPrefix.show_roles + str(location.id),
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.ADD_ROLE(user.language),
            callback_data=CallbackPrefix.add_role + str(location.id),
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.BACK(user.language),
            callback_data=CallbackPrefix.show_locations + str(location.package_id),
        )
    )
    keyboard.adjust(1)
    markup = keyboard.as_markup()

    roles = await location.number_of_roles()

    txt = (await texts.INFO_LOCATION(user.language)).format(
        roles,
        location=location,
    )

    if location.image_url:
        await user.send_photo(location.image_url, caption=txt, reply_markup=markup)
        return

    await user.send_message(txt, reply_markup=markup)


@private_only_msg.callback_query(F.data.startswith(CallbackPrefix.delete_location))
async def delete_location(query: types.CallbackQuery, **_):
    location_id = uuid.UUID(query.data.split(":")[1])

    location = await Location.load(location_id)
    await location.remove()

    new_query = create_new_query(
        query, CallbackPrefix.show_locations + str(location.package_id)
    )

    await show_locations(new_query)

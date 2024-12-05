from spy.routers import (
    private_only_msg_without_state,
    extract_message_filters,
    private_only_msg,
    no_command,
)
from spy.points.location import show_location
from spy.callback import CallbackPrefix
from spy import fsm, texts

from spy.decorators import with_user_cache

from database import TelegramUser, Location, Role

from utils.msg import handle_content_type_text, create_new_query
from utils.call_save import call_save
from utils.no_skip import no_skip

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, filters, F, enums

import typing as _t
import asyncio
import uuid

if _t.TYPE_CHECKING:
    from database import TelegramUser


@no_skip(private_only_msg, filters.StateFilter(fsm.RoleFSM.name))
@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.add_role)
)
@with_user_cache
async def add_role(
    query: types.CallbackQuery, state: fsm.FSMContext, user: "TelegramUser", **_
):
    location_id = query.data.removeprefix(CallbackPrefix.add_role)

    await state.set_state(fsm.RoleFSM.name)
    await state.update_data(location_id=location_id)

    func = await handle_content_type_text(query)
    await func(
        texts.ENTER_ROLE_NAME,
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@call_save(
    private_only_msg,
    filters.StateFilter(fsm.RoleFSM.description),
    call_after=show_location,
)
@private_only_msg.message(
    filters.StateFilter(fsm.RoleFSM.name),
    *extract_message_filters(no_command),
)
@with_user_cache
async def handle_location_name(
    message: types.Message, state: fsm.FSMContext, user: "TelegramUser", **_
):
    await state.update_data(name=message.text)
    await state.set_state(fsm.RoleFSM.description)

    await user.send_message(texts.ENTER_ROLE_DESCRIPTION)


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.show_roles)
)
@with_user_cache
async def show_roles(query: types.CallbackQuery, user: "TelegramUser", **_):
    location_id = uuid.UUID(query.data.removeprefix(CallbackPrefix.show_roles))
    location = await Location.load(location_id)

    roles = await location.get_roles()

    if not roles:
        func = await handle_content_type_text(query)
        msg = await func(
            texts.YOU_DOESNT_HAVE_ANY_ROLES,
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )

        if msg is not None:
            query = create_new_query(
                msg, CallbackPrefix.show_location + str(location_id), from_user=user
            )

        await asyncio.sleep(0.6)
        await show_location(query)
        return

    keyboard = InlineKeyboardBuilder()
    for role in roles:
        keyboard.add(
            types.InlineKeyboardButton(
                text=role.name, callback_data=CallbackPrefix.show_role + str(role.id)
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=texts.BACK,
                callback_data=CallbackPrefix.show_location + str(location_id),
            )
        )

    if (roles_count := len(roles)) > 1:
        adjust = [2] * (roles_count // 2)
        keyboard.adjust(*adjust, 1)
    else:
        keyboard.adjust(1)

    text = texts.ROLES_INFO.format(
        len(roles),
        location=location,
    )

    func = await handle_content_type_text(query)
    await func(
        text=text,
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.show_role)
)
@with_user_cache
async def show_role(query: types.CallbackQuery, user: "TelegramUser", **_):
    role_id = uuid.UUID(query.data.removeprefix(CallbackPrefix.show_role))
    role = await Role.load(role_id)

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.DELETE_ROLE,
            callback_data=CallbackPrefix.delete_role + str(role.id),
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.BACK,
            callback_data=CallbackPrefix.show_roles + str(role.location_id),
        )
    )
    keyboard.adjust(1)

    text = texts.ROLE_INFO.format(role=role)

    func = await handle_content_type_text(query)
    await func(
        text=text,
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.delete_role)
)
async def delete_role(query: types.CallbackQuery, **_):
    role_id = uuid.UUID(query.data.removeprefix(CallbackPrefix.delete_role))
    role = await Role.load(role_id)

    await role.remove()

    new_query = create_new_query(
        query, data=CallbackPrefix.show_roles + str(role.location_id)
    )
    await show_roles(new_query)

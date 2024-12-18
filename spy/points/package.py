from spy.routers import (
    private_only_msg_without_state,
    extract_message_filters,
    private_only_msg,
    no_command,
)
from spy.decorators import with_user_cache, with_user
from spy.callback import CallbackPrefix
from spy.commands import private
from spy import fsm, texts

from utils.msg import edit_or_answer, create_new_query
from utils.no_skip import no_skip

from database import Package

from aiogram.utils.markdown import markdown_decoration
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import filters, types, F, enums

import typing as _t
import uuid

if _t.TYPE_CHECKING:
    from database import TelegramUser


@private_only_msg_without_state.message(
    filters.Command(private.create_package),
)
@with_user_cache
async def create_package(
    msg: types.Message, state: fsm.FSMContext, user: "TelegramUser", **_
):
    await state.set_state(fsm.PackageFSM.name)

    await msg.delete()
    await user.send_message(texts.NAME_FOR_PACKAGE)


@no_skip(private_only_msg, filters.StateFilter(fsm.PackageFSM.name))
@private_only_msg.message(
    filters.StateFilter(fsm.PackageFSM.name),
    *extract_message_filters(no_command),
)
@with_user
async def handle_package_name(
    msg: types.Message, state: fsm.FSMContext, user: "TelegramUser", **_
):
    packages = await user.get_packages()

    if (name := msg.text) in set(packages):
        await user.send_message(
            texts.PACKAGE_ALREADY_EXISTS.format(name=markdown_decoration.quote(name))
        )
        return

    package = await Package.add({"name": name, "owner_id": user.id})
    await state.clear()

    message = await user.send_message(texts.PACKAGE_CREATED)
    query = create_new_query(
        message, data=CallbackPrefix.show_package + str(package.id), from_user=user
    )
    await show_package(query)


@private_only_msg_without_state.callback_query(F.data == CallbackPrefix.show_packages)
@private_only_msg_without_state.message(
    filters.Command(private.show_packages),
)
@with_user_cache
async def show_packages(
    msg: types.Message | types.CallbackQuery, user: "TelegramUser", **_
):
    packages = await user.get_packages()

    if not packages:
        await edit_or_answer(msg)(text=texts.YOU_DOESNT_HAVE_ANY_PACKAGE)
        return

    keyboard = InlineKeyboardBuilder()
    for package in packages:
        keyboard.add(
            types.InlineKeyboardButton(
                text=package.name,
                callback_data=CallbackPrefix.show_package + str(package.id),
            )
        )
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.CLOSE_LIST,
            callback_data=CallbackPrefix.delete_msg,
        )
    )
    keyboard.adjust(1)

    text = texts.INFO_PACKAGES.format(len(packages))

    await edit_or_answer(msg)(text=text, reply_markup=keyboard.as_markup())


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.show_package)
)
async def show_package(msg: types.CallbackQuery):
    package_id = uuid.UUID(msg.data.removeprefix(CallbackPrefix.show_package))

    package = await Package.load(package_id)
    number_of_locations = await package.number_of_locations()

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.DELETE_PACKAGE,
            callback_data=CallbackPrefix.delete_package + str(package.id),
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.ADD_LOCATION,
            callback_data=CallbackPrefix.add_location + str(package.id),
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.LOCATIONS,
            callback_data=CallbackPrefix.show_locations + str(package.id),
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.BACK,
            callback_data=CallbackPrefix.show_packages,
        )
    )
    keyboard.adjust(1)

    text = texts.INFO_PACKAGE.format(number_of_locations, package=package)
    await msg.message.edit_text(
        text=text,
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.delete_package)
)
async def delete_package(msg: types.CallbackQuery):
    package_id = uuid.UUID(msg.data.removeprefix(CallbackPrefix.delete_package))

    await Package.remove_by_id(package_id)

    text = texts.PACKAGE_WAS_DELETED
    await msg.message.edit_text(
        text,
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )
    await show_packages(msg)

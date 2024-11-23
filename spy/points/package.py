from spy.routers import (
    private_only_msg_without_state,
    extract_message_filters,
    private_only_msg,
    no_command,
)
from spy.decorators import with_user_cache, with_user
from spy.commands import private
from spy import fsm, texts

from utils.no_skip import no_skip

from database import Package

from aiogram import filters, types

import typing as _t

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
        await user.send_message(texts.PACKAGE_ALREADY_EXISTS.format(name=name))
        return

    await Package.add({"name": name, "owner_id": user.id})
    await state.clear()
    await user.send_message(texts.PACKAGE_CREATED)

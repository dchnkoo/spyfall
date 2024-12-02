from spy.routers import private_only_msg_without_state
from spy.points.location import show_location
from spy.points.package import show_package
from spy.callback import CallbackPrefix
from spy.commands import private
from spy import texts

from settings import spygame

from utils.msg import create_new_query, edit_or_answer
from utils.exc.callback import CallbackAlert

from spy.decorators import with_user_cache

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import filters, types, F, enums

from datetime import timedelta

import typing as _t
import asyncio
import uuid

from database import Location, Role

from settings import spygame

if _t.TYPE_CHECKING:
    from database import TelegramUser


@private_only_msg_without_state.message(filters.Command(private.game_settings))
@private_only_msg_without_state.callback_query(F.data == CallbackPrefix.game_settings)
@with_user_cache
async def show_the_settings(
    message: types.Message | types.CallbackQuery,
    user: "TelegramUser",
    **_,
):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.SELECT_GAME_PACKAGE(user.language),
            callback_data=CallbackPrefix.select_game_package,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.CHOOSE_GAME_LOCATIONS(user.language),
            callback_data=CallbackPrefix.choose_game_locations,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.CHOOSE_GAME_ROLES(user.language),
            callback_data=CallbackPrefix.select_location_for_roles,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.CONFIGURE_SPIES(user.language),
            callback_data=CallbackPrefix.configure_spies,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.CONFIGURE_ROUNDS(user.language),
            callback_data=CallbackPrefix.configure_rounds,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.CLOSE_MENU(user.language),
            callback_data=CallbackPrefix.delete_msg,
        )
    )
    keyboard.adjust(1)

    func = edit_or_answer(message)
    await func(
        text=await texts.GAME_SETTINGS(user.language), reply_markup=keyboard.as_markup()
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.configure_rounds)
)
@with_user_cache
async def configure_rounds(query: types.CallbackQuery, user: "TelegramUser", **_):
    settings = await user.get_settings()
    assert settings is not None

    minutes = settings.round_time.seconds // 60

    text = (await texts.ROUNDS_MENU(user.language)).format(
        round_duration=minutes, rounds=settings.rounds
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.NUMBER_OF_ROUNDS(user.language),
            callback_data=CallbackPrefix.round_settings,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.ROUND_TIME(user.language),
            callback_data=CallbackPrefix.configure_round_time,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.BACK(user.language),
            callback_data=CallbackPrefix.game_settings,
        )
    )
    keyboard.adjust(1)

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data == CallbackPrefix.configure_round_time
)
@with_user_cache
async def configure_round_time(query: types.CallbackQuery, user: "TelegramUser", **_):
    settings = await user.get_settings()
    minutes = settings.round_time.seconds // 60

    text = (await texts.CONFIGURE_ROUND_TIME(user.language)).format(time=minutes)

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text="-",
            callback_data=CallbackPrefix.decrease_round_time,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text="+",
            callback_data=CallbackPrefix.increase_round_time,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.BACK(user.language),
            callback_data=CallbackPrefix.configure_rounds,
        )
    )
    keyboard.adjust(2, 1)

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data == CallbackPrefix.decrease_round_time
)
@private_only_msg_without_state.callback_query(
    F.data == CallbackPrefix.increase_round_time
)
@with_user_cache
async def round_time(query: types.CallbackQuery, user: "TelegramUser", **_):
    settings = await user.get_settings()

    minutes = settings.round_time.seconds // 60

    if query.data == CallbackPrefix.decrease_round_time:
        minutes -= 1
    else:
        minutes += 1

    if minutes < spygame.min_round_time or minutes > spygame.max_round_time:
        text = await texts.TIME_ERROR(user.language)
        raise CallbackAlert(text, show_alert=True)

    settings.round_time = timedelta(minutes=minutes)
    await settings.save()

    await configure_round_time(query)
    raise CallbackAlert(await texts.TIME_EDITED(user.language))


@private_only_msg_without_state.callback_query(F.data == CallbackPrefix.round_settings)
@with_user_cache
async def configure_number_of_rounds(
    query: types.CallbackQuery, user: "TelegramUser", **_
):
    settings = await user.get_settings()

    text = (await texts.CONFIGURE_NUMBER_OF_ROUNDS(user.language)).format(
        rounds=settings.rounds
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text="-",
            callback_data=CallbackPrefix.decrease_rounds,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text="+",
            callback_data=CallbackPrefix.increase_rounds,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.BACK(user.language),
            callback_data=CallbackPrefix.configure_rounds,
        )
    )
    keyboard.adjust(2, 1)

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(F.data == CallbackPrefix.decrease_rounds)
@private_only_msg_without_state.callback_query(F.data == CallbackPrefix.increase_rounds)
@with_user_cache
async def round_number(query: types.CallbackQuery, user: "TelegramUser", **_):
    settings = await user.get_settings()
    rounds = settings.rounds

    if query.data == CallbackPrefix.decrease_rounds:
        rounds -= 1
    else:
        rounds += 1

    if rounds < spygame.min_rounds or rounds > spygame.max_rounds:
        text = await texts.ROUNDS_ERROR(user.language)
        raise CallbackAlert(text, show_alert=True)

    settings.rounds = rounds
    await settings.save()

    await configure_number_of_rounds(query)
    raise CallbackAlert(await texts.ROUNDS_EDITED(user.language))


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.select_game_package)
)
@with_user_cache
async def select_game_package(callback: types.CallbackQuery, user: "TelegramUser", **_):
    packages = await user.get_packages()

    if not packages:
        new_callback = await callback.message.edit_text(
            await texts.YOU_DOESNT_HAVE_ANY_PACKAGE(user.language),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )

        await asyncio.sleep(0.6)
        await new_callback.edit_text(
            callback.message.text, reply_markup=callback.message.reply_markup
        )
        return

    settings = await user.get_settings()
    keyboard = InlineKeyboardBuilder()

    for package in packages:
        keyboard.add(
            types.InlineKeyboardButton(
                text=package.name
                + (" 👈" if package.id == settings.package_id else ""),
                callback_data=CallbackPrefix.choose_game_package + str(package.id),
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=await texts.BACK(user.language),
                callback_data=CallbackPrefix.game_settings,
            )
        )
        keyboard.adjust(1)

    await callback.message.edit_text(
        await texts.CLICK_ON_PACKAGE(user.language),
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.choose_game_package)
)
@with_user_cache
async def choose_game_package(callback: types.CallbackQuery, user: "TelegramUser", **_):
    package_id = uuid.UUID(
        callback.data.removeprefix(CallbackPrefix.choose_game_package)
    )

    settings = await user.get_settings()
    if settings.package_id == package_id:
        settings.remove_game_package()
    else:
        settings.set_new_package(package_id)

    await settings.save()

    await select_game_package(callback)


async def validate_locations(user: "TelegramUser", callback: types.CallbackQuery):
    settings = await user.get_settings()

    if not settings.package_id:
        await callback.message.edit_text(
            await texts.YOU_NEED_TO_SELECT_PACKAGE_FOR_SELECTING_LOCATIONS(
                user.language
            ),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )

        await asyncio.sleep(1.5)
        await select_game_package(callback)
        return

    package = await settings.get_package()
    locations = await package.get_locations()

    if not locations:
        await callback.message.edit_text(
            await texts.YOU_NEED_ADD_LOCATIONS_FOR_PACKAGE_TO_CHOOSE(user.language),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )

        await asyncio.sleep(2)
        new_callback = create_new_query(
            callback, CallbackPrefix.show_package + str(package.id)
        )
        await show_package(new_callback)
        return

    return settings, locations


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.choose_game_locations)
)
@with_user_cache
async def choose_game_locations(
    callback: types.CallbackQuery, user: "TelegramUser", **_
):
    data = await validate_locations(user, callback)

    if not data:
        return

    settings, locations = data

    keyboard = InlineKeyboardBuilder()
    for location in locations:
        keyboard.add(
            types.InlineKeyboardButton(
                text=location.name
                + (
                    " ✅"
                    if (item_id_str := str(location.id)) in settings.use_locations_id
                    else ""
                ),
                callback_data=CallbackPrefix.add_game_location + item_id_str,
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=await texts.BACK(user.language),
                callback_data=CallbackPrefix.game_settings,
            )
        )
        keyboard.adjust(1)

    await callback.message.edit_text(
        await texts.SELECT_GAME_LOCATIONS(user.language),
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.add_game_location)
)
@with_user_cache
async def add_game_location(callback: types.CallbackQuery, user: "TelegramUser", **_):
    settings = await user.get_settings()
    location_id = callback.data.removeprefix(CallbackPrefix.add_game_location)

    if location_id in settings.use_locations_id:
        settings.use_locations_id.remove(location_id)
    else:
        settings.use_locations_id.append(location_id)

    settings.use_roles_id = {
        k: v for k, v in settings.use_roles_id.items() if k in settings.use_locations_id
    }
    await settings.save()

    await choose_game_locations(callback)


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.select_location_for_roles)
)
@with_user_cache
async def select_location_for_role(
    callback: types.CallbackQuery, user: "TelegramUser", **_
):
    data = await validate_locations(user, callback)

    if not data:
        return

    settings, locations = data

    if settings.use_locations_id:
        locations = [
            location
            for location in locations
            if str(location.id) in settings.use_locations_id
        ]

    keyboard = InlineKeyboardBuilder()
    for location in locations:
        keyboard.add(
            types.InlineKeyboardButton(
                text=location.name,
                callback_data=CallbackPrefix.choose_game_roles + str(location.id),
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=await texts.BACK(user.language),
                callback_data=CallbackPrefix.game_settings,
            )
        )
        keyboard.adjust(1)

    await callback.message.edit_text(
        await texts.SELECT_LOCATION_FOR_ROLE(user.language),
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.choose_game_roles)
)
@with_user_cache
async def choose_game_roles(callback: types.CallbackQuery, user: "TelegramUser", **_):
    location_id = uuid.UUID(
        callback.data.removeprefix(CallbackPrefix.choose_game_roles)
    )
    location = await Location.load(location_id)

    roles = await location.get_roles()

    if not roles:
        await callback.message.edit_text(
            await texts.YOU_NEED_ADD_ROLES_FOR_LOCATION_TO_CHOOSE(user.language),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )

        await asyncio.sleep(2)
        new_callback = create_new_query(
            callback, CallbackPrefix.show_location + str(location_id)
        )
        await show_location(new_callback)
        return

    settings = await user.get_settings()

    keyboard = InlineKeyboardBuilder()
    location_roles = settings.get_location_roles(str(location_id))
    for role in roles:
        text = role.name + (" 🟢" if str(role.id) in location_roles else " ⚪️")

        keyboard.add(
            types.InlineKeyboardButton(
                text=text,
                callback_data=CallbackPrefix.choose_role + str(role.id),
            )
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(
                text=await texts.BACK(user.language),
                callback_data=CallbackPrefix.select_location_for_roles
                + str(location_id),
            )
        )
        keyboard.adjust(1)

    await callback.message.edit_text(
        await texts.SELECT_GAME_ROLES(user.language),
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.choose_role)
)
@with_user_cache
async def choose_role(callback: types.CallbackQuery, user: "TelegramUser", **_):
    role_id = callback.data.removeprefix(CallbackPrefix.choose_role)

    settings = await user.get_settings()

    role = await Role.load(uuid.UUID(role_id))
    roles = settings.get_location_roles(str(role.location_id))

    if role_id in roles:
        roles.remove(role_id)
    else:
        roles.append(role_id)

    if not roles:
        del settings.use_roles_id[str(role.location_id)]

    await settings.save()

    new_callback = create_new_query(
        callback,
        CallbackPrefix.choose_game_roles + str(role.location_id),
        id=callback.id,
    )
    await choose_game_roles(new_callback)


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.configure_spies)
)
@with_user_cache
async def configure_spies(callback: types.CallbackQuery, user: "TelegramUser", **_):
    settings = await user.get_settings()

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.SET_TWO_SPIES(user.language)
            + (" ✅" if settings.two_spies else ""),
            callback_data=CallbackPrefix.set_two_spies,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.SPIES_KNOW_EACH_OTHER(user.language)
            + (" ✅" if settings.know_each_other else ""),
            callback_data=CallbackPrefix.set_spies_know_each_other,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.BACK(user.language),
            callback_data=CallbackPrefix.game_settings,
        )
    )
    keyboard.adjust(1)

    await callback.message.edit_text(
        await texts.SPIES_CONFIGURE_EXPLAIN(user.language),
        reply_markup=keyboard.as_markup(),
        parse_mode=enums.ParseMode.MARKDOWN_V2,
    )


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.set_two_spies)
)
@with_user_cache
async def set_two_spies(callback: types.CallbackQuery, user: "TelegramUser", **_):
    settings = await user.get_settings()
    settings.two_spies = not settings.two_spies

    await settings.save()
    await configure_spies(callback)


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.set_spies_know_each_other)
)
@with_user_cache
async def set_spies_know_each_other(
    callback: types.CallbackQuery, user: "TelegramUser", **_
):
    settings = await user.get_settings()
    settings.know_each_other = not settings.know_each_other

    await settings.save()
    await configure_spies(callback)

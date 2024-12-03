from spy.routers import private_only_msg_without_state
from spy.game import GameStatus, Player, GameManager
from spy.decorators import with_player, with_manager
from spy import filters as game_filters, texts
from spy.callback import CallbackPrefix
from spy.commands import private

from settings import spygame

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, filters, F

import asyncio
import uuid


@private_only_msg_without_state.message(
    filters.Command(private.guess_location, ignore_case=True),
    game_filters.GameProccessFilter(GameStatus.playing, by_user_id=True),
    game_filters.PlayerFilter("in_game", is_spy=True),
)
@with_player
async def start_guess(msg: types.Message, player: Player, **_):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.CONTINUE(player.language),
            callback_data=CallbackPrefix.continue_guess,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.CANCEL(player.language),
            callback_data=CallbackPrefix.delete_msg,
        )
    )
    keyboard.adjust(2)

    await player.send_message(
        text=await texts.WANRING_GUESS_MESSAGE(player.language),
        reply_markup=keyboard.as_markup(),
    )


@private_only_msg_without_state.callback_query(
    F.data == CallbackPrefix.continue_guess,
    game_filters.GameProccessFilter(GameStatus.playing, by_user_id=True),
    game_filters.PlayerFilter("in_game", is_spy=True),
)
@with_player
@with_manager(by_user_id=True)
async def guess_location(
    msg: types.CallbackQuery, manager: GameManager, player: Player, **_
):
    async with manager.block_game_proccess():
        await manager.put_task(GameStatus.guess_location, msg, player)
        await manager.tasks.wait_until_current_task_complete()


@private_only_msg_without_state.callback_query(
    F.data.startswith(CallbackPrefix.guess_location),
    game_filters.GameProccessFilter(GameStatus.guess_location, by_user_id=True),
    game_filters.PlayerFilter("in_game", is_spy=True),
)
@with_manager(by_user_id=True)
async def guess_proccess(msg: types.CallbackQuery, manager: GameManager, **_):
    manager.tasks.cancel_current_task()
    guess_location_id = uuid.UUID(msg.data.removeprefix(CallbackPrefix.guess_location))

    player = manager.room.guess_spy_player
    if manager.room.location.id == guess_location_id:
        settings = manager.room.game_settings
        if settings.two_spies and settings.know_each_other:
            manager.room.players.in_game.spies.increase_score(2)
        else:
            player.increase_score(2)
        await manager.room.send_message(
            (
                await texts.SUCCESSFULLY_GUESS_LOCATION(manager.room.language_code)
            ).format(player.mention_markdown(), manager.room.location.escaped_name)
        )
        await player.send_message(
            await texts.YOU_SUCCESSFULLY_GUESS_LOCATION(player.language)
        )
    else:
        manager.room.players.in_game.ordinary.increase_score(1)
        await manager.room.send_message(
            (
                await texts.UNSUCCESSFULLY_GUESS_LOCATION(manager.room.language_code)
            ).format(player.mention_markdown())
        )
        await player.send_message(
            await texts.YOU_UNSUCCESSFULLY_GUESS_LOCATION(player.language)
        )

    await manager.go_to_next_round()
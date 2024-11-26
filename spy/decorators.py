from utils.exc.assertion import AssertionAnswer, handler as assertion_handler
from utils.msg import extract_message, extract_chat_id
from utils.exc.callback import CallbackAlert

from database import TelegramUser

from spy.game import GameRoom, Player
from spy.routers import spybot
from spy import texts

from aiogram.utils.deep_linking import decode_payload
from aiogram import types, filters

from functools import wraps

from sqlalchemy import exc

from loguru import logger


def create_user_or_update(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kwargs):
        new_user = msg.from_user
        try:
            assert new_user is not None, AssertionAnswer(
                texts.SOMETHING_WRONG_TRY_START
            )
            user = await TelegramUser.add(new_user)
        except exc.IntegrityError:
            user = TelegramUser.model_validate(new_user)
            del user.updated_date
            await user.save()
        await user.save_in_cache()
        return await func(msg, *args, user=user, **kwargs)

    return error_handler(wrapper)


def with_user(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
        user = msg.from_user
        assert user is not None, AssertionAnswer(texts.SOMETHING_WRONG_TRY_START)

        user = await TelegramUser.load(user.id)
        assert user is not None, AssertionAnswer(texts.SOMETHING_WRONG_TRY_START)

        return await func(msg, *args, user=user, **kw)

    return error_handler(wrapper)


def with_user_cache(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
        from_user = msg.from_user
        assert from_user is not None, AssertionAnswer(texts.SOMETHING_WRONG_TRY_START)
        user_id = from_user.id
        try:
            user = await TelegramUser.load_cached(user_id)
        except AssertionError:
            user = await TelegramUser.load(user_id)
            await user.save_in_cache()
        return await func(msg, *args, user=user, **kw)

    return error_handler(wrapper)


def decode_start_link(func):
    @wraps(func)
    async def wrapper(msg: types.Message, command: filters.CommandObject, *args, **kw):
        playload = decode_payload(command.args)
        return await func(msg, *args, playload=playload, **kw)

    return wrapper


def with_play_room(f=None, *, by_user_id: bool = False, save_after: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
            chat_id = extract_chat_id(msg)
            if by_user_id:
                player = await Player.load_cached(chat_id)
                room = await GameRoom.load_cached(player.room_id)
            else:
                room = await GameRoom.load_cached(chat_id)
                player = room.players.get(msg.from_user.id)
                assert player is not None
            async with room.manager(save_room=save_after):
                return await func(msg, *args, play_room=room, player=player, **kw)

        return error_handler(wrapper)

    return decorator if not callable(f) else decorator(f)


def error_handler(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
        try:
            return await func(msg, *args, **kw)
        except AssertionError as e:
            await assertion_handler(e, msg, *args, **kw)
        except CallbackAlert as e:
            assert isinstance(msg, types.CallbackQuery)
            await spybot.answer_callback_query(
                callback_query_id=msg.id,
                text=e.message,
                show_alert=e.show_alert,
                **e.kw
            )
        except Exception as e:
            logger.exception(e)
            await extract_message(msg).answer(texts.SOMETHING_WRONG_TRY_START)

    return wrapper

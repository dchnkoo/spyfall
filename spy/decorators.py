from utils.exc.assertion import AssertionAnswer, handler as assertion_handler
from utils.msg import extract_message, extract_chat_id
from utils.exc.callback import CallbackAlert

from database import TelegramUser

from spy.game import GameManager, exc as game_exception
from spy.routers import spybot
from spy import texts

from aiogram.utils.deep_linking import decode_payload
from aiogram import types, filters

from functools import wraps

from sqlalchemy import exc

from loguru import logger

import typing as _t


def create_user_or_update(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kwargs):
        new_user = msg.from_user
        lang_code = new_user.language_code or "en"
        try:
            assert new_user is not None, AssertionAnswer(
                texts.SOMETHING_WRONG_TRY_START, translate=lang_code
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
        lang_code = user.language_code or "en"
        assert user is not None, AssertionAnswer(
            texts.SOMETHING_WRONG_TRY_START, translate=lang_code
        )

        user = await TelegramUser.load(user.id)
        assert user is not None, AssertionAnswer(
            texts.SOMETHING_WRONG_TRY_START, translate=lang_code
        )

        return await func(msg, *args, user=user, **kw)

    return error_handler(wrapper)


def with_user_cache(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
        from_user = msg.from_user
        lang_code = from_user.language_code or "en"
        assert from_user is not None, AssertionAnswer(
            texts.SOMETHING_WRONG_TRY_START, translate=lang_code
        )
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


def with_manager(func: _t.Callable | None = None, *, by_user_id: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
            chat_id = extract_chat_id(msg)
            if by_user_id:
                manager = await GameManager.meta.load_by_user_id(chat_id)
                if manager is None:
                    await extract_message(msg).answer(
                        await texts.ROOM_NOT_FOUND(msg.from_user.language_code or "en")
                    )
                    return
            else:
                manager = GameManager.meta.get_room(chat_id)
            return await func(msg, *args, manager=manager, **kw)

        return error_handler(wrapper)

    return decorator(func) if callable(func) else decorator


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
        except (game_exception.GameException, game_exception.GameExceptionWrapper) as e:
            chat_id = extract_chat_id(msg)
            manager = GameManager.meta.get_room(chat_id)
            if manager is None:
                await e.handle(manager)
                return
            await e.handle(manager)
        except Exception as e:
            logger.exception(e)
            await extract_message(msg).answer(texts.SOMETHING_WRONG_TRY_START)

    return wrapper

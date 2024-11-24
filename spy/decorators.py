from database import TelegramUser

from utils.exc.assertion import Assertion, AssertionAnswer
from utils.exc.callback import CallbackAlert
from utils.msg import extract_message

from spy.routers import spybot
from spy import texts

from aiogram import types

from functools import wraps

from sqlalchemy import exc

from loguru import logger


def create_user_or_update(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kwargs):
        new_user = msg.from_user
        try:
            assert new_user is not None, AssertionAnswer(texts.SOMETHING_WRONG)
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
        assert user is not None, AssertionAnswer(texts.SOMETHING_WRONG)

        user = await TelegramUser.load(user.id)
        assert user is not None, AssertionAnswer(texts.SOMETHING_WRONG_TRY_START)

        return await func(msg, *args, user=user, **kw)

    return error_handler(wrapper)


def with_user_cache(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
        user = msg.from_user
        assert user is not None, AssertionAnswer(texts.SOMETHING_WRONG)
        try:
            user = await TelegramUser.load_cached(user.id)
        except AssertionError:
            user = await TelegramUser.load(user.id)
            await user.save_in_cache()
        return await func(msg, *args, user=user, **kw)

    return error_handler(wrapper)


def error_handler(func):
    @wraps(func)
    async def wrapper(msg: types.Message | types.CallbackQuery, *args, **kw):
        try:
            return await func(msg, *args, **kw)
        except AssertionError as e:
            handler = None
            for handler in Assertion.is_assertion(e):
                await handler.send(msg, *args, **kw)
            if not handler:
                raise e
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
            await extract_message(msg).answer(texts.SOMETHING_WRONG)

    return wrapper

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types

import typing as _t

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

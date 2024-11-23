from abc import ABC, abstractmethod
from utils.msg import msg_answer

from aiogram import types


class Assertion(ABC):

    @classmethod
    def is_assertion(cls, error: AssertionError):
        for handler in error.args:
            if isinstance(handler, cls):
                yield handler

    @abstractmethod
    async def send(self, msg: types.Message | types.CallbackQuery, *args, **kwargs): ...

    @abstractmethod
    def __str__(self) -> str: ...


class AssertionAnswer(Assertion):

    def __init__(self, msg: str) -> None:
        self.msg = msg

    async def send(self, msg: types.Message | types.CallbackQuery, *args, **kwargs):
        await msg_answer(msg, self.msg)

    def __str__(self) -> str:
        return self.msg

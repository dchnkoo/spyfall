from utils.msg import extract_message
from abc import ABC, abstractmethod

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
        await extract_message(msg).answer(self.msg)

    def __str__(self) -> str:
        return self.msg

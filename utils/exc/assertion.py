from utils.msg import extract_message
from abc import ABC, abstractmethod

from aiogram import types
import typing as _t

if _t.TYPE_CHECKING:
    from utils.translate import TranslateStr


async def handler(error: AssertionError, *args, **kw):
    handler = None
    for handler in Assertion.is_assertion(error):
        await handler.send(*args, **kw)
    if not handler:
        raise error


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

    def __init__(
        self,
        msg: _t.Union[str, "TranslateStr"],
        *args,
        translate: _t.Optional[str] = None,
        **kw
    ) -> None:
        self.msg = msg
        self.translate = translate
        self.args = args
        self.kw = kw

    async def send(self, msg: types.Message | types.CallbackQuery, *args, **kwargs):
        to_send = self.msg
        if self.translate:
            to_send = (await to_send(self.translate)).format(*self.args, **self.kw)
        await extract_message(msg).answer(to_send)

    def __str__(self) -> str:
        return self.msg

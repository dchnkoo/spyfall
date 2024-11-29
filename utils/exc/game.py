from abc import ABC, abstractmethod

import typing as _t

if _t.TYPE_CHECKING:
    from spy.game import GameManager


class GameException(Exception, ABC):
    @abstractmethod
    async def handle(self, manager: "GameManager"): ...


class Exit(GameException):
    async def handle(self, manager: "GameManager"):
        return


class GameEnd(GameException):

    async def handle(self, manager: "GameManager"):
        await manager.finish_game()


class FinishGame(GameEnd):
    async def handle(self, manager: "GameManager"):
        await manager.room.send_winners()
        await manager.finish_game()


class GameExceptionWrapper(Exception):
    def __init__(
        self, manager: "GameManager", exc: GameException, *args: object
    ) -> None:
        super().__init__(*args)
        self.manager = manager
        self.exc = exc

    async def handle(self, manager: _t.Union["GameManager", None] = None):
        await self.exc.handle(manager or self.manager)

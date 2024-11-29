from .room import GameStatus, GameRoom, ROOM_ID

from contextlib import asynccontextmanager

from .players import Player

from functools import wraps

from utils.exc import game as exc

from settings import spygame

from loguru import logger

from aiogram import enums

from spy import texts

import typing as _t
import asyncio


class GameRoomMeta(type):

    _managers: dict[ROOM_ID, "GameManager"] = {}

    @classmethod
    def get_room(cls, room_id: ROOM_ID):
        return cls._managers.get(room_id)

    def __call__(cls, room: GameRoom) -> "GameManager":
        if room.id in cls._managers:
            return cls.get_room(room_id=room.id)

        manager = super().__call__(room)
        cls._managers[room.id] = manager
        return manager

    @classmethod
    async def load_by_user_id(cls, user_id: int):
        player = await Player.load_cached(user_id)
        manager = cls.get_room(player.room_id)
        if manager is None:
            await player.delete_cache()
        return manager

    @classmethod
    async def register(cls, room: GameRoom):
        manager = GameManager(room=room)
        return manager

    @classmethod
    def clear(cls):
        cls._managers.clear()

    @classmethod
    def remove_room(cls, room_id: ROOM_ID):
        return cls._managers.pop(room_id)


EVENT_HANDLERS: dict[GameStatus, _t.Callable[["GameManager"], _t.Coroutine]] = {}


def task_error_handler(func):
    @wraps(func)
    async def wrapper(self: "GameManager"):
        try:
            return await func(self)
        except asyncio.CancelledError:
            return
        except exc.GameException as e:
            await e.handle(self)

    return wrapper


def on_status(s: GameStatus):
    def decorator(func):
        EVENT_HANDLERS[s] = func
        return func

    return decorator


class GameManager(metaclass=GameRoomMeta):

    meta = GameRoomMeta

    def __init__(self, room: GameRoom) -> None:
        global EVENT_HANDLERS
        self._tasks = EVENT_HANDLERS

        self.current_task: asyncio.Task | None = None
        self.queue = asyncio.Queue()

        self.task_handler = asyncio.create_task(self.queue_handler())

        self._game_blocked = False
        self._condition = asyncio.Condition()

        self._room = room
        self.rounds = self.iter_rounds()
        self.round_event = asyncio.Event()

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, value: GameRoom):
        raise ValueError("You cannot set new room to this manager.")

    @property
    def bot(self):
        return self.room.__bot__

    @property
    def current_round(self):
        return self.room.current_round

    @current_round.setter
    def current_round(self, value: int):
        assert isinstance(
            value, int
        ), f"Round value need to be integer. Your value {type(value)}"
        self.room.current_round = value

    @property
    def round(self):
        return next(self.rounds)

    def iter_rounds(self):
        while True:
            self.current_round += 1
            yield self.current_round

    @property
    def status(self):
        return self.room.status

    def set_status(self, s: GameStatus):
        assert (
            self._game_blocked is False or not self.room.playing
        ), "Use block_game_proccess context manager."
        self.room.set_status(s)
        task = self.get_task(status=s)
        new_task = self._create_current_task(task, name=s + str(self.room.id))
        return new_task

    @property
    def previous_status(self):
        return self.room.previous_status

    def get_task(self, status: GameStatus):
        task = self._tasks.get(status)
        assert task is not None, "Any task not found."
        return task

    @classmethod
    async def register(cls, room: GameRoom):
        return await cls.meta.register(room=room)

    def _create_current_task(
        self, task: _t.Callable[["GameManager"], _t.Coroutine], **kw
    ):
        new_task = asyncio.create_task(task_error_handler(task)(self), **kw)
        self.current_task = new_task
        return new_task

    async def wait_until_current_task_complete(self):
        if (task := self.current_task) is not None:
            return await task

    def cancel_current_task(self):
        if (task := self.current_task) is not None:
            task.cancel()

    async def queue_handler(self):
        while True:
            try:
                status = await self.queue.get()
            except asyncio.CancelledError:
                break
            self.set_status(status)

    def clear_queue(self):
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break

    @on_status(GameStatus.recruitment)
    async def recruitment(self):
        await self.room.append_player(self.room.creator)

        await self.room.send_message(
            await texts.RECRUITMENT_MESSAGE(self.room.language_code),
            reply_markup=await self.room.recruitment_join_button(),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )
        await self.room.display_players_in_join_message()

        message = await self.room.send_message(
            (await texts.RECRUITMENT_WILL_END(self.room.language_code)).format(
                (recruitment_time := spygame.recruitment_time)
            ),
        )

        interval = spygame.recruitment_edit_interval
        text = message.text

        while recruitment_time > 0:
            await asyncio.sleep(interval)

            i = str(recruitment_time)
            recruitment_time -= interval

            text = text.replace(i, str(recruitment_time))

            await message.edit_text(text)

        await self.room.delete_sended_messages()
        await self.queue.put(GameStatus.playing)

    @on_status(GameStatus.playing)
    async def play(self):
        await self.room.choose_game_package()
        await self.room.choose_game_location()
        await self.room.distribute_roles()
        await self.room.define_game_players()
        await self.room.send_message(
            text=(await texts.GAME_STARTED(self.room.language_code)).format(
                (self.room.game_settings.round_time.seconds + 10) // 60,
                self.room.game_settings.rounds,
            ),
            parse_mode=enums.ParseMode.MARKDOWN,
        )

        while (round := self.round) < self.room.game_settings.rounds:
            await self.room.notify_users_about_roles()
            await self.room.notify_about_time_to_the_end_of_round()
            await self.room.notify_about_round()
            await self.room.send_ask_question_msg()

            await asyncio.wait_for(
                self.round_event.wait(),
                timeout=self.room.time_to_end_of_round_in_seconds,
            )
            async with self._condition:
                await self._condition.wait_for(lambda: self._game_blocked is False)

            await self.room.send_round_results(round)
        else:
            raise exc.FinishGame()

    async def finish_game(self):
        self.room.set_status(GameStatus.end)
        await self.room.finish_game()

        self.meta.remove_room(self.room.id)
        self.cancel_current_task()
        self.task_handler.cancel()
        self.rounds.close()
        del self

    @asynccontextmanager
    async def block_game_proccess(self):
        assert self.room.playing

        self._game_blocked = True
        game_task = self.current_task

        async with self._condition:
            yield
            self._game_blocked = False
            self._condition.notify_all()

        self.current_task = game_task

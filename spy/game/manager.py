from .room import GameStatus, GameRoom, ROOM_ID

from contextlib import asynccontextmanager

from .players import Player

from functools import wraps, partial

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
        if manager is None or (
            manager is not None and manager.room.players.get(user_id) is None
        ):
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
        except Exception as e:
            logger.exception(e)
            await self.room.only_send_message(
                text=await texts.SOMETHING_WRONG(self.room.language_code)
            )
            await self.finish_game()

    return wrapper


def on_status(s: GameStatus):
    def decorator(func):
        EVENT_HANDLERS[s] = func
        return func

    return decorator


class TasksHistory(list[asyncio.Task]):

    @property
    def current_task(self):
        if len(self) > 0:
            return self[-1]

    @current_task.setter
    def current_task(self, value: asyncio.Task):
        assert isinstance(value, asyncio.Task)
        self.insert(len(self), value)

    @property
    def previous_task(self):
        if len(self) > 1:
            return self[-2]

    @property
    def task_handler(self):
        return self.get_task("task_handler")

    @property
    def play(self):
        return self.get_task(GameStatus.playing)

    @property
    def recruitment(self):
        return self.get_task(GameStatus.recruitment)

    @property
    def voting(self):
        return self.get_task(GameStatus.voting)

    @property
    def summary_voting(self):
        return self.get_task(GameStatus.summary_vote)

    def get_task(self, name: str):
        for task in self[::-1]:
            if task.get_name() == name:
                return task

    def _exists(self, name: str):
        for t in self:
            if t.get_name() == name:
                if t.done() is True:
                    self.remove(t)
                elif t.cancelled() is False or t.cancelling() < 1:
                    return self.index(t)
        return False

    def append(self, task: asyncio.Task) -> None:
        name = task.get_name()
        if self._exists(name) is not False:
            raise ValueError("You cannot add the same and not canceled task.")
        super(TasksHistory, self).append(task)

    def insert(self, index: _t.SupportsIndex, object: asyncio.Task) -> None:
        if (indx := self._exists(object.get_name())) is not False:
            del self[indx]
        super(TasksHistory, self).insert(index, object)

    def clear(self) -> None:
        for task in self:
            if task.cancelling() < 1 and task.cancelled() is False:
                task.cancel()
        super(TasksHistory, self).clear()

    def create_task(
        self,
        manager: "GameManager",
        task: _t.Callable[["GameManager"], _t.Coroutine],
        name: str,
    ):
        if (t := self.get_task(name)) is not None:
            if t.done() is False:
                raise ValueError("Task already exist")
        created = asyncio.create_task(task_error_handler(task)(manager), name=name)
        self.append(created)
        return created

    def copy(self):
        return self.__class__([i for i in self])

    async def wait_until_current_task_complete(self):
        if (task := self.current_task) is not None:
            return await task

    def cancel_current_task(self):
        if (task := self.current_task) is not None:
            task.cancel()


class GameManager(metaclass=GameRoomMeta):

    meta = GameRoomMeta

    def __init__(self, room: GameRoom) -> None:
        global EVENT_HANDLERS
        self._status_handlers = EVENT_HANDLERS

        self.queue = asyncio.Queue()
        self.tasks = TasksHistory()
        self.task_handler = self.create_task(
            GameManager.queue_handler, name="task_handler"
        )

        self._game_blocked = False
        self.condition = asyncio.Condition()

        self.room = room
        self.rounds = self.iter_rounds()
        self.round_event = asyncio.Event()

    @property
    def bot(self):
        return self.room.__bot__

    @property
    def game_blocked(self):
        return self._game_blocked

    @game_blocked.setter
    def game_blocked(self, value: bool):
        assert isinstance(value, bool)
        self._game_blocked = value

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
            self.game_blocked is True or not self.room.playing
        ), "Use block_game_proccess context manager."
        self.room.set_status(s)
        task = self.get_status_handler(status=s)
        new_task = self.create_task(task, name=s)
        return new_task

    @property
    def previous_status(self):
        return self.room.previous_status

    def get_status_handler(self, status: GameStatus):
        handler = self._status_handlers.get(status)
        assert handler is not None, "Any status handler not found."
        return handler

    @classmethod
    async def register(cls, room: GameRoom):
        return await cls.meta.register(room=room)

    @property
    def create_task(self):
        return partial(self.tasks.create_task, self)

    async def put_task(self, event: GameStatus):
        await self.queue.put(event)
        await asyncio.sleep(0.2)

    async def queue_handler(self):
        while True:
            try:
                status = await self.queue.get()
            except asyncio.CancelledError:
                break
            assert (
                status in GameStatus
            ), f"You provided to queue not GameStatus: {type(status)} - {status}"
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

            await message.edit_text(text, parse_mode=enums.ParseMode.MARKDOWN_V2)

        await self.room.delete_sended_messages()
        await self.queue.put(GameStatus.playing)

    @on_status(GameStatus.playing)
    async def play(self):
        # await self.room.check_if_enough_players()
        await self.room.choose_game_package()
        await self.room.choose_game_location()
        await self.room.distribute_roles()
        await self.room.define_game_players()
        await self.room.send_message(
            text=(await texts.GAME_STARTED(self.room.language_code)).format(
                (self.room.game_settings.round_time.seconds + 10) // 60,
                self.room.game_settings.rounds,
            ),
        )

        while (round := self.round) < (
            total_rounds := (self.room.game_settings.rounds + 1)
        ):
            await self.room.notify_users_about_roles()
            await self.room.notify_about_round()
            await self.room.notify_about_time_to_the_end_of_round()
            await self.room.send_ask_question_msg()

            try:
                await asyncio.wait_for(
                    self.round_event.wait(),
                    timeout=self.room.time_to_end_of_round_in_timedelta.seconds,
                )
            except asyncio.TimeoutError:
                locked = self.condition.locked()
                if not locked:
                    async with self.block_game_proccess():
                        await self.put_task(GameStatus.summary_vote)
                        await self.tasks.wait_until_current_task_complete()
                del locked

            async with self.condition:
                await self.condition.wait_for(lambda: self.game_blocked is False)

            await self.room.players.set_status("in_game")
            await self.room.send_round_results(round)
            if (round + 1) < total_rounds:
                await self.room.redefine_location_and_roles()
        else:
            raise exc.FinishGame()

    @on_status(GameStatus.summary_vote)
    async def summary_voting(self):
        with self.room.create_summary_vote() as vote:
            await self.room.send_message(
                await texts.SUMMARY_VOTING_MSG(self.room.language_code)
            )

            text, reply_markup = vote.vote_message()
            await self.room.send_message(
                await text(self.room.language_code), reply_markup=reply_markup
            )

            try:
                await asyncio.sleep(spygame.summmary_vote_time)
            finally:
                if self.room.summary_voting:
                    await self.room.delete_last_sended_msg()

            result = self.room.vote_results()

            if result is False:
                await self.room.send_message(
                    await texts.ANY_PLAYER_WASNT_KICKED(self.room.language_code)
                )
            else:
                assert isinstance(
                    result, Player
                ), "In success case result need to be Player instance."
                if result.is_spy:
                    await self.room.send_message(
                        (
                            await texts.SUCCESSFULLY_SUMMARY_VOTE(
                                self.room.language_code
                            )
                        ).format(link=result.mention_markdown())
                    )

                    for player in (voted := vote.voted):
                        if voted[player] == result and not player.is_spy:
                            player.increase_score(1)
                else:
                    await self.room.send_message(
                        (
                            await texts.UNSUCCESSFULLY_SUMMARY_VOTE(
                                self.room.language_code
                            )
                        ).format(result.mention_markdown())
                    )
                    self.room.players.in_game.spies.increase_score(2)

    @on_status(GameStatus.voting)
    async def voting(self):
        message, reply_murkup = self.room.vote_message()
        vote = self.room.vote

        msg = await self.room.send_message(
            text=(await message(self.room.language_code)).format(
                vote.author.mention_markdown(), vote.suspected.mention_markdown()
            ),
            reply_markup=reply_murkup,
        )

        try:
            await asyncio.sleep(spygame.early_vote_time)
        finally:
            await msg.delete()

        vote_result = self.room.vote_results()
        assert isinstance(
            vote_result, bool
        ), "In Early vote results need to be boolean."

        try:
            if vote_result:
                if not vote.suspected.is_spy:
                    self.room.players.in_game.spies.increase_score(2)
                    await self.room.send_unsuccessfully_early_voting_msg()
                else:
                    for player in (voted := vote.voted):
                        if voted[player]:
                            player.increase_score(1)

                    await self.room.send_successfully_early_voting_msg()

                await vote.suspected.set_stauts("kicked")
            else:
                await self.room.send_message(
                    await texts.ANYONE_WASNT_KICKED(self.room.language_code)
                )

            if vote.suspected.is_spy and len(self.room.players.in_game.spies) > 0:
                minutes, _ = self.room.time_to_end_of_round_in_minutes_and_seconds
                if minutes > 1:
                    await self.room.send_message(
                        await texts.CONTINUE_THE_ROUND(self.room.language_code)
                    )
                    await self.room.notify_about_time_to_the_end_of_round()
                    return
            await self.go_to_next_round()
        finally:
            if vote.suspected.is_spy:
                vote.author.score += 1

    async def finish_game(self):
        self.meta.remove_room(self.room.id)
        self.clear_queue()
        self.rounds.close()

        self.room.set_status(GameStatus.end)
        await self.room.finish_game()

        self.tasks.clear()

    async def go_to_next_round(self):
        self.round_event.set()
        await asyncio.sleep(0.1)
        self.round_event.clear()

    @asynccontextmanager
    async def block_game_proccess(self):
        async with self.condition:
            await self.condition.wait_for(
                lambda: self.room.playing and (self.game_blocked is False)
            )
            self.game_blocked = True
            yield
            self.game_blocked = False
            self.condition.notify_all()
        if not (game_task := self.tasks.play):
            raise exc.Exit()
        self.tasks.current_task = game_task
        self.room.set_status(GameStatus.playing)

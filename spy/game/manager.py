from .room import GameStatus, GameRoom, ROOM_ID

from contextlib import asynccontextmanager

from .players import Player

from .tasks import Tasks

from functools import wraps

from utils.exc import game as exc

from settings import spygame

from loguru import logger

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import enums, types

from spy.callback import CallbackPrefix
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
    async def wrapper(self: "GameManager", *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except asyncio.CancelledError:
            return
        except exc.GameException as e:
            await e.handle(self)
        except Exception as e:
            logger.exception(e)
            await self.room.only_send_message(text=texts.SOMETHING_WRONG)
            await self.finish_game()

    return wrapper


def on_status(s: GameStatus):
    def decorator(func):
        EVENT_HANDLERS[s] = func
        return func

    return decorator


class TasksHistory(Tasks):

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

    @property
    def guess_location(self):
        return self.get_task(GameStatus.guess_location)

    def create_task(self, coro, name, *args, context=None, **kw):
        return super(TasksHistory, self).create_task(
            task_error_handler(coro), name, *args, context=context, **kw
        )


class GameManager(metaclass=GameRoomMeta):

    meta = GameRoomMeta
    __slots__ = (
        "_status_handlers",
        "_game_blocked",
        "task_handler",
        "round_event",
        "condition",
        "rounds",
        "queue",
        "tasks",
        "room",
    )

    def __init__(self, room: GameRoom) -> None:
        global EVENT_HANDLERS
        self._status_handlers = EVENT_HANDLERS

        self.queue = asyncio.Queue()
        self.tasks = TasksHistory()
        self.task_handler = self.create_task(
            GameManager.queue_handler, "task_handler", self
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

    def set_status(self, s: GameStatus, *func_args, **func_kwds):
        assert (
            self.game_blocked is True or not self.room.playing
        ), "Use block_game_proccess context manager."
        self.room.set_status(s)
        task = self.get_status_handler(status=s)
        new_task = self.create_task(task, s, self, *func_args, **func_kwds)
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
        return self.tasks.create_task

    async def put_task(self, event: GameStatus, *func_args, **func_kwds):
        await self.queue.put([event, func_args, func_kwds])
        await asyncio.sleep(0.2)

    async def queue_handler(self):
        while True:
            try:
                status, args, kwds = await self.queue.get()
            except asyncio.CancelledError:
                break
            assert (
                status in GameStatus
            ), f"You provided to queue not GameStatus: {type(status)} - {status}"
            self.set_status(status, *args, **kwds)

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
            texts.RECRUITMENT_MESSAGE,
            reply_markup=await self.room.recruitment_join_button(),
        )
        await self.room.display_players_in_join_message()

        message = await self.room.send_message(
            texts.RECRUITMENT_WILL_END.format(
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
        await self.put_task(GameStatus.playing)

    @on_status(GameStatus.playing)
    async def play(self):
        await self.room.check_if_enough_players()
        await self.room.choose_game_package()
        await self.room.choose_game_location()
        await self.room.distribute_roles()
        await self.room.define_game_players()
        await self.room.send_message(
            text=texts.GAME_STARTED.format(
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
                        await self.tasks.wait_until_complete_current_task()
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
            await self.room.send_message(texts.SUMMARY_VOTING_MSG)

            text, reply_markup = vote.vote_message()
            await self.room.send_message(text, reply_markup=reply_markup)

            try:
                await asyncio.sleep(spygame.summmary_vote_time)
            finally:
                if self.room.summary_voting:
                    await self.room.delete_last_sended_msg()

            result = self.room.vote_results()

            if result is False:
                await self.room.send_message(texts.ANY_PLAYER_WASNT_KICKED)
            else:
                assert isinstance(
                    result, Player
                ), "In success case result need to be Player instance."
                if result.is_spy:
                    await self.room.send_message(
                        texts.SUCCESSFULLY_SUMMARY_VOTE.format(
                            link=result.mention_markdown()
                        )
                    )

                    for player in (voted := vote.voted):
                        if voted[player] == result and not player.is_spy:
                            player.increase_score(1)
                else:
                    await self.room.send_message(
                        texts.UNSUCCESSFULLY_SUMMARY_VOTE.format(
                            result.mention_markdown()
                        )
                    )
                    self.room.players.in_game.spies.increase_score(2)

    @on_status(GameStatus.voting)
    async def voting(self):
        message, reply_murkup = self.room.vote_message()
        vote = self.room.vote

        msg = await self.room.send_message(
            text=message.format(
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
                await self.room.send_message(texts.ANYONE_WASNT_KICKED)

            if vote.suspected.is_spy and len(self.room.players.in_game.spies) > 0:
                minutes, _ = self.room.time_to_end_of_round_in_minutes_and_seconds
                if minutes > 1:
                    await self.room.send_message(texts.CONTINUE_THE_ROUND)
                    await self.room.notify_about_time_to_the_end_of_round()
                    return
            await self.go_to_next_round()
        finally:
            if vote.suspected.is_spy:
                vote.author.score += 1

    @on_status(GameStatus.guess_location)
    async def guess_location(self, msg: types.CallbackQuery, player: Player):
        with self.room.with_guess_spy(player):
            self.room.set_status(GameStatus.guess_location)
            await self.room.send_message(
                texts.NOTIFY_USERS_ABOUT_SPY.format(player.mention_markdown())
            )

            locations = await self.room.package.get_locations()
            keyboard = InlineKeyboardBuilder()
            for location in locations:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=location.name,
                        callback_data=CallbackPrefix.guess_location + str(location.id),
                    )
                )
            keyboard.adjust(1)

            try:
                await msg.message.edit_text(
                    text=texts.TRY_TO_GUESS,
                    reply_markup=keyboard.as_markup(),
                    parse_mode=enums.ParseMode.MARKDOWN_V2,
                )

                await asyncio.sleep(spygame.guess_location_time)
            finally:
                await msg.message.delete()

            self.room.players.in_game.ordinary.increase_score(1)
            await self.room.send_message(
                texts.NOT_GUESS_LOCATION_IN_TIME.format(player.mention_markdown())
            )
            await player.send_message(texts.YOU_DOESNT_GUESS_LOCATION_IN_TIME)
            await self.go_to_next_round()

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
        self.room.set_status(GameStatus.playing)

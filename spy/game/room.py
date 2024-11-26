from database import Settings, TelegramUser, Location, Package, Role

from .players import Player, PlayersCollection

from caching import CachePrefix, CacheModel

from utils.exc.assertion import AssertionAnswer
from utils.translate import LanguageCode
from utils.chat.model import ChatModel
from utils.schedule import call_later
from utils.waiter import wait
from utils.exc import game

from contextlib import asynccontextmanager

from functools import wraps

from spy.routers import spybot
from spy import texts

from settings import redis, spygame

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link
from aiogram import enums, types, exceptions

import datetime as _date
import pydantic as _p
import typing as _t
import asyncio
import random
import enum


def check_field_is_not_none(field: str, msg: _t.Optional[str] = None):
    def decorator[F](func: F) -> F:
        @wraps(func)
        async def wrapper(self: "GameRoom", *args, **kwargs):
            assert getattr(self, field) is not None, msg or ""
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator


class Round(_p.BaseModel):
    current_round: int = 0
    end_of_round: _t.Optional[_date.datetime] = None

    @property
    def now_utc(self):
        return _date.datetime.now(_date.timezone.utc)

    @property
    @check_field_is_not_none(field="end_of_round")
    def seconds_to_end_of_round(self) -> int:
        return (self.end_of_round - self.now_utc).seconds

    def _set_end_of_round(self, round_duration: _date.timedelta) -> None:
        self.end_of_round = self.now_utc + round_duration

    def set_end_of_round(self, round_duration: _date.timedelta) -> None:
        if self.end_of_round is None:
            self._set_end_of_round(round_duration)
            return

        now = self.now_utc

        if now < self.end_of_round:
            raise game.RoundNotEnded("Round not ended!")

        self._set_end_of_round(round_duration)

    def increase_round(self, max_rounds: int):
        if self.current_round == max_rounds:
            raise game.GameEnd("All rounds passed.")
        self.current_round += 1


class GameStatus(enum.StrEnum):
    define_location_and_roles = "define_location_and_roles"
    notify_users_about_roles = "notify_users_about_roles"
    say_spies_about_each_other = "say_spies_about_each_other"
    define_game_players = "define_game_players"
    choose_package = "choose_package"
    check_location = "check_location"
    guess_location = "guess_location"
    summary_vote = "summary_vote"
    recruitment = "recruitment"
    playing = "playing"
    voting = "voting"
    end = "end"


type CHAT_ID = int | str


async def check_status(instance: "GameRoom", s: _t.Sequence[GameStatus]):
    assert not isinstance(instance, type), "check_status need instance of GameRoom"
    try:
        await instance.reload_cache()
    except AssertionError:
        raise game.GameRoomNotExists()
    return instance.status in s or "*" in s


def from_status[
    F
](
    func: F,
    *,
    s: _t.Sequence[GameStatus],
    after_set_status: _t.Optional[GameStatus] = None,
    raise_error: bool = True,
    _for: int = 60,
    interval: int = 2,
) -> F:
    async def wrapper(self: "GameRoom", *args, **kwargs):
        if (
            await wait(check_status, _for=_for, interval=interval, instance=self, s=s)
        ) is False:
            if raise_error:
                raise TimeoutError(
                    f"For {_for} seconds function {func.__name__} doesn't return True."
                )
            else:
                return
        res = await func(self, *args, **kwargs)
        if after_set_status is not None:
            await self.set_status(after_set_status)
        return res

    return wrapper


class GameRoom(CacheModel[CHAT_ID], ChatModel):
    model_config = _p.ConfigDict(
        use_enum_values=True,
        validate_default=True,
        ser_json_timedelta="iso8601",
    )

    cache_prefix: _t.ClassVar[str] = CachePrefix.game_room
    save_msg_id: _t.ClassVar[bool] = True
    db: _t.ClassVar[int] = redis.game_db

    id: CHAT_ID
    creator: TelegramUser
    round: Round = Round()
    game_settings: Settings
    language_code: LanguageCode
    status: GameStatus = GameStatus.recruitment
    package: _t.Optional[Package] = None
    location: _t.Optional[Location] = None
    players: PlayersCollection = _p.Field(default_factory=PlayersCollection)

    question_to_player: _t.Optional[Player] = None
    previous_player: _t.Optional[Player] = None
    cur_player: _t.Optional[Player] = None

    @property
    def join_message_id(self) -> int | str:
        if not self.saved_msgs_ids:
            return
        return self.saved_msgs_ids[0]

    @property
    def chat_id(self) -> CHAT_ID:
        return self.id

    @property
    def cache_identity(self) -> CHAT_ID:
        return self.chat_id

    @property
    def __bot__(self):
        return spybot

    def clear(self):
        """
        Delete all attributes in instance.
        """
        del self.__dict__

    @asynccontextmanager
    async def manager(self, save_room: bool):
        try:
            yield
        except game.Exit:
            return
        except game.GameEnd:
            await self.finish_game()
        except game.GameRoomNotExists:
            await self.clear()
        except game.RoundNotEnded:
            await self.notify_about_time_to_the_and_of_round()
        except game.NotSave:
            return
        except AttributeError:
            pass
        else:
            if save_room is True:
                await self.save_in_cache()

    async def exists(self) -> bool:
        try:
            await self.load_cached(self.cache_identity)
        except AssertionError:
            return False
        else:
            return True

    async def not_exists(self):
        if not (await self.exists()):
            raise game.Exit()

    async def set_status(self, s: GameStatus) -> None:
        self.status = s
        await self.save_in_cache()

    def append_player(self, player: TelegramUser):
        self.players.append(player, room_id=self.id)

    async def add_player(self, player: TelegramUser):
        self.append_player(player)

        await self.save_in_cache()
        await self.display_players_in_join_message()

        text = await texts.YOU_JOINED_TO_THE_GAME(player.language)
        link = (
            await self.create_chat_invite_link(expire_date=_date.timedelta(seconds=30))
        ).invite_link

        await player.send_message(
            text=text.format(link),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
            link_preview_options=types.LinkPreviewOptions(is_disabled=True),
        )

    def start_round(self):
        self.round.increase_round(self.game_settings.rounds)
        self.round.set_end_of_round(self.game_settings.round_time)

    async def notify_about_round(self):
        await self.send_message(
            (await texts.BEGIN_ROUND(self.language_code)).format(
                self.round.current_round
            )
        )

    async def notify_about_time_to_the_and_of_round(self):
        text = texts.TO_END_OF_ROUND_REMAINS
        seconds = self.round.seconds_to_end_of_round

        if seconds > 120:
            text = text.replace("seconds", "minutes")
            seconds = seconds // 60

        text = (await text(self.language_code)).format(seconds)

        await self.send_message(text=text)

    async def recruitment_link(self):
        return await create_start_link(
            bot=self.__bot__, payload=self.cache_key, encode=True
        )

    async def recruitment_join_button(self):
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            types.InlineKeyboardButton(
                text=await texts.JOIN_TO_THE_GAME(self.language_code),
                url=await self.recruitment_link(),
            )
        )
        return keyboard.as_markup()

    async def display_players_in_join_message(self):
        join_message_id = self.join_message_id
        assert join_message_id is not None, "Join message not found."

        txt = await texts.RECRUITMENT_MESSAGE(self.language_code)
        display_players = await texts.DISPLAY_PLAYERS(self.language_code)

        players = ", ".join(
            [
                player.mention_markdown(player.full_name)
                for player in self.players.in_game
            ]
        )
        display_players = display_players.format(players, len(self.players.in_game))

        await self.edit_message_text(
            text=txt + "\n\n" + display_players,
            message_id=join_message_id,
            parse_mode=enums.ParseMode.MARKDOWN_V2,
            reply_markup=await self.recruitment_join_button(),
        )

    async def start_recruitment(self):
        await self.set_status(GameStatus.recruitment)
        self.append_player(self.creator)
        await self.save_in_cache()

        await self.send_message(
            await texts.RECRUITMENT_MESSAGE(self.language_code),
            reply_markup=await self.recruitment_join_button(),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )
        await self.display_players_in_join_message()

        message = await self.send_message(
            (await texts.RECRUITMENT_WILL_END(self.language_code)).format(
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

            if await self.exists():
                await message.edit_text(text)
            else:
                raise game.Exit()

        if await self.exists():
            await self.reload_cache()

        if self.status != GameStatus.recruitment:
            raise game.Exit()

        await self.delete_all_sended_msgs()
        await self.save_in_cache()

    async def start_game(self):
        await self.choose_game_package()
        await self.start_recruitment()

    @classmethod
    async def load_by_user_id(cls, user_id: int) -> tuple["GameRoom", Player]:
        player = await Player.load_cached(user_id)
        room = await cls.load_cached(player.room_id)
        return room, player

    @check_field_is_not_none(
        field="location", msg="You need specify the location first."
    )
    async def notify_users_about_roles(self) -> None:
        for player in self.players:
            await player.notify_about_role(self.location)

    async def say_spies_about_each_other(self) -> None:
        assert self.game_settings.two_spies
        first_spy, second_spy = self.players.spies

        await first_spy.send_message(
            (await texts.THE_SECOND_SPY_IS(first_spy.language)).format(
                player=second_spy
            ),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )

        await second_spy.send_message(
            (await texts.THE_SECOND_SPY_IS(second_spy.language)).format(
                player=first_spy
            ),
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )

    async def choose_game_package(self) -> None:
        await self.set_status("choose_package")
        package = (await self.game_settings.get_package()) or (
            await self.creator.get_random_package()
        )

        if package is None:
            await self.send_message(
                await texts.YOU_DOESNT_HAVE_ANY_PACKAGE(self.language_code),
            )
            await asyncio.sleep(1)
            raise game.GameEnd()

        self.package = package

    @check_field_is_not_none(field="package", msg="You need to define package first")
    async def choose_game_location(self) -> None:
        locations = await self.package.get_locations()

        assert bool(locations), AssertionAnswer(
            texts.YOU_DOES_NOT_HAVE_LOCATIONS,
            self.package.name,
            translate=self.language_code,
        )

        if self.game_settings.use_locations_id:
            locations = [
                location
                for location in locations
                if str(location.id) in self.game_settings.use_locations_id
            ]

            location = random.choice(locations)
        else:
            location = random.choice(locations)

        number_of_locations = len(locations)
        assert number_of_locations > self.game_settings.rounds, AssertionAnswer(
            texts.LOCATIONS_NEED_TO_BE_MORE_THAN_ROUNDS.format(
                number_of_locations, self.game_settings.rounds
            ),
            translate=self.language_code,
        )

        self.location = location

    @check_field_is_not_none(field="location", msg="You need to define location first.")
    async def distribute_roles(self) -> None:
        roles = list((await self.location.get_roles()))
        number_of_players = len(self.players)

        spies = 2 if self.game_settings.two_spies else 1

        if roles_id := self.game_settings.use_roles_id:
            location_roles = roles_id.get(str(self.location.id), None)

            if location_roles is not None and isinstance(location_roles, list):
                roles = [role for role in roles if str(role.id) in location_roles]

        assert (len(location_roles) + spies) >= number_of_players, AssertionAnswer(
            texts.SELECTED_ROLES_LESS_THAN_PLAYERS, translate=self.language_code
        )

        random.shuffle(roles)
        roles = roles[: number_of_players - spies]

        for _ in range(spies):
            roles.insert(0, Role.get_spy_role())

        random.shuffle(roles)

        players = self.players.model_copy()
        random.shuffle(players)

        players_range = list(range(number_of_players))
        roles_range = list(range(len(roles)))

        while players_range and roles_range:
            player_index = random.choice(players_range)
            roles_index = random.choice(roles_range)

            players_range.remove(player_index)
            roles_range.remove(roles_index)

            players[player_index].role = roles[roles_index]

    async def redefine_location_and_roles(self) -> None:
        await self.set_status(GameStatus.define_location_and_roles)
        await self.choose_game_location()
        await self.distribute_roles()

    async def finish_game(self) -> None:
        await self.set_status(GameStatus.end)
        await self.unset_players()
        await self.delete_all_sended_msgs()
        await self.send_message(await texts.GAME_ENDED(self.language_code))
        await self.delete_cache()

    async def set_current_player(self, player: Player) -> None:
        assert player in self.players.in_game
        self.previous_player = self.cur_player
        self.cur_player = player
        await self.save_in_cache()

    async def define_current_player(self) -> None:
        players = self.players.in_game

        if self.previous_player:
            players.safety_remove(self.previous_player)

        if self.cur_player:
            players.safety_remove(self.cur_player)

        await self.set_current_player(random.choice(players))

    async def define_question_to_player(self) -> None:
        players = self.players.in_game
        players.remove_players(self.previous_player, self.cur_player)

        self.question_to_player = random.choice(players)
        await self.save_in_cache()

    async def define_game_players(self) -> None:
        await self.set_status(GameStatus.define_game_players)
        await self.define_current_player()
        await self.define_question_to_player()

    async def redefine_game_players(self, player: Player):
        await self.set_status(GameStatus.define_game_players)
        if player.id == self.cur_player.id:
            await self.define_current_player()

        question_player_id = self.question_to_player.id
        if player.id == question_player_id or self.cur_player.id == question_player_id:
            await self.define_question_to_player()

    async def set_players(self):
        for player in self.players:
            await player.save_in_cache()

    async def unset_players(self):
        for player in self.players:
            try:
                await player.delete_cache()
            except AssertionError:
                continue

from database import Settings, TelegramUser, Location, Package, Role

from .players import Player, PlayersCollection

from .vote import EarlyVote, SummaryVote, Vote

from utils.chat.model import ChatModel
from utils.exc import game as exc

from contextlib import contextmanager

from functools import wraps

from spy import texts, enums as spy_enums
from spy.routers import spybot

from settings import spygame

from aiogram.utils.deep_linking import create_start_link, create_telegram_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import enums, types

import datetime as _date
import pydantic as _p
import typing as _t
import inspect
import random
import enum


def check_field_is_not_none(field: str, msg: _t.Optional[str] = None):
    def decorator[F](func: F) -> F:
        is_coro = inspect.iscoroutinefunction(func)

        @wraps(func)
        async def async_wrapper(self: "GameRoom", *args, **kwargs):
            assert getattr(self, field) is not None, msg or ""
            return await func(self, *args, **kwargs)

        @wraps(func)
        def sync_wrapper(self: "GameRoom", *args, **kwargs):
            assert getattr(self, field) is not None, msg or ""
            return func(self, *args, **kwargs)

        return async_wrapper if is_coro else sync_wrapper

    return decorator


class GameStatus(enum.StrEnum):
    guess_location = "guess_location"
    summary_vote = "summary_vote"
    recruitment = "recruitment"
    playing = "playing"
    voting = "voting"
    end = "end"


ROOM_ID = int


def now_utc():
    return _date.datetime.now(_date.timezone.utc)


class GameRoom(ChatModel):
    model_config = _p.ConfigDict(
        use_enum_values=True,
        validate_default=True,
        validate_assignment=True,
    )

    prefix: _t.ClassVar[str] = spy_enums.GameEnum.game_room
    save_msg_id: _t.ClassVar[bool] = True

    id: ROOM_ID
    creator: TelegramUser
    game_settings: Settings
    package: _t.Optional[Package] = None
    location: _t.Optional[Location] = None
    status: GameStatus = GameStatus.recruitment
    vote: _t.Optional[EarlyVote | SummaryVote] = None
    status_history: list[GameStatus] = _p.Field(default_factory=list)
    players: PlayersCollection = _p.Field(default_factory=PlayersCollection)

    question_to_player: _t.Optional[Player] = None
    previous_player: _t.Optional[Player] = None
    cur_player: _t.Optional[Player] = None

    _end_of_round: _date.datetime = _p.PrivateAttr(default=None)
    _current_round: int = _p.PrivateAttr(default=0)
    _spy_player_guess: Player | None = _p.PrivateAttr(default=None)

    @property
    def playing(self):
        return self.status == GameStatus.playing

    @property
    def recruitment(self):
        return self.status == GameStatus.recruitment

    @property
    def voting(self):
        return self.status == GameStatus.voting

    @property
    def summary_voting(self):
        return self.status == GameStatus.summary_vote

    @property
    def guess_location(self):
        return self.status == GameStatus.guess_location

    @property
    def current_round(self):
        return self._current_round

    @current_round.setter
    def current_round(self, value: int):
        assert isinstance(value, int)
        self._end_of_round = now_utc() + self.game_settings.round_time
        self._current_round = value

    @property
    def time_to_end_of_round(self):
        assert (
            self._end_of_round is not None
        ), "Time to end of round cannot be None, something wrong with iter_rounds generator."
        return self._end_of_round

    @property
    def time_to_end_of_round_in_timedelta(self):
        return self.time_to_end_of_round - now_utc()

    @property
    def time_to_end_of_round_in_seconds(self):
        return self.time_to_end_of_round_in_timedelta.seconds

    @property
    def time_to_end_of_round_in_minutes_and_seconds(self):
        seconds = self.time_to_end_of_round_in_seconds
        return (seconds // 60, seconds % 60)

    @property
    def key(self):
        return self.prefix + str(self.id)

    @property
    def join_message_id(self) -> int | str:
        if not self.saved_msgs_ids:
            return
        return self.saved_msgs_ids[0]

    @property
    def previous_status(self):
        if not self.status_history:
            return
        return self.status_history[-1]

    @property
    def chat_id(self) -> ROOM_ID:
        return self.id

    @property
    def cache_identity(self) -> ROOM_ID:
        return self.chat_id

    @property
    def __bot__(self):
        return spybot

    @property
    def guess_spy_player(self):
        spy = self._spy_player_guess
        assert (
            spy is not None
        ), "Spy player which try to guess location cannot be None in that context."
        return spy

    @guess_spy_player.setter
    def guess_spy_player(self, value: Player):
        assert (
            isinstance(value, Player) and self._spy_player_guess is None
        ), "To set player you need to delete previous gueser."
        self._spy_player_guess = value

    def set_status(self, s: GameStatus) -> None:
        self.status_history.append(self.status)
        self.status = s

    async def bot_link(self):
        me = await self.__bot__.get_me()
        link = create_telegram_link(me.username)
        return link

    async def append_player(self, player: TelegramUser):
        if (await Player.load_raw_cached(player.id)) is not None:
            await player.send_message(texts.YOU_ALREADY_IN_GAME)
            raise exc.Exit()

        player = self.players.append(player, room_id=self.id)
        await player.save_in_cache()

    async def add_player(self, player: TelegramUser):
        await self.append_player(player)
        await self.display_players_in_join_message()

        text = texts.YOU_JOINED_TO_THE_GAME
        link = (
            await self.create_chat_invite_link(
                expire_date=_date.timedelta(seconds=spygame.recruitment_time)
            )
        ).invite_link

        await player.send_message(
            text=text.format(link),
            link_preview_options=types.LinkPreviewOptions(is_disabled=True),
        )

    async def send_round_results(self, round: int):
        text = texts.RESULTS_PREV_ROUND.format(round)

        for player in self.players:
            text += "\n\t" + player.mention_markdown() + " \\- " + str(player.score)

        await self.send_message(text=text)

    async def send_winners(self):
        winners = self.players.max_score
        if not winners:
            await self.send_message(text=texts.NO_WINNERS)
            return

        text = texts.WINNERS
        for player in winners:
            text += "\n\t" + player.mention_markdown() + " \\- " + str(player.score)
        await self.send_message(text=text)

    async def notify_about_round(self):
        await self.send_message(
            texts.BEGIN_ROUND.format(self.current_round),
        )

    async def notify_about_time_to_the_end_of_round(self):
        minutes, seconds = self.time_to_end_of_round_in_minutes_and_seconds

        text = texts.TO_END_OF_ROUND_REMAINS.format(minutes, seconds)
        await self.send_message(text=text)

    async def recruitment_link(self):
        return await create_start_link(bot=self.__bot__, payload=self.key, encode=True)

    async def recruitment_join_button(self):
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            types.InlineKeyboardButton(
                text=texts.JOIN_TO_THE_GAME,
                url=await self.recruitment_link(),
            )
        )
        return keyboard.as_markup()

    async def display_players_in_join_message(self):
        join_message_id = self.join_message_id
        assert join_message_id is not None, "Join message not found."

        txt = texts.RECRUITMENT_MESSAGE
        display_players = texts.DISPLAY_PLAYERS

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
            texts.THE_SECOND_SPY_IS.format(player=second_spy),
        )

        await second_spy.send_message(
            texts.THE_SECOND_SPY_IS.format(player=first_spy),
        )

    async def choose_game_package(self) -> None:
        package = (await self.game_settings.get_package()) or (
            await self.creator.get_random_package()
        )

        if package is None:
            await self.send_error_msg_and_finish_game(
                texts.YOU_DOESNT_HAVE_ANY_PACKAGE,
            )

        self.package = package

    @check_field_is_not_none(field="package", msg="You need to define package first")
    async def choose_game_location(self) -> None:
        locations = await self.package.get_locations()

        if not locations:
            await self.send_error_msg_and_finish_game(
                texts.YOU_DOES_NOT_HAVE_LOCATIONS_IN_THAT_PACKAGE.format(
                    self.package.escaped_name
                ),
            )

        if self.game_settings.use_locations_id:
            locations = [
                location
                for location in locations
                if str(location.id) in self.game_settings.use_locations_id
            ]

            location = random.choice(locations)
        else:
            location = await self.package.get_random_location()
            assert location is not None, "Location cannot be None in that context."

        number_of_locations = len(locations)
        if number_of_locations < self.game_settings.rounds:
            await self.send_error_msg_and_finish_game(
                texts.LOCATIONS_NEED_TO_BE_MORE_THAN_ROUNDS.format(
                    number_of_locations, self.game_settings.rounds
                )
            )

        self.location = location

    @check_field_is_not_none(field="location", msg="You need to define location first.")
    async def distribute_roles(self) -> None:
        roles = list((await self.location.get_roles()))
        number_of_players = len(self.players.in_game)

        await self.check_if_can_use_two_spies()

        spies = 2 if self.game_settings.two_spies else 1

        if roles_id := self.game_settings.use_roles_id:
            location_roles = roles_id.get(str(self.location.id), None)

            if location_roles is not None and isinstance(location_roles, list):
                roles = [role for role in roles if str(role.id) in location_roles]

        if (len(roles) + spies) < number_of_players:
            await self.send_error_msg_and_finish_game(
                texts.ROLES_LESS_THAN_PLAYERS.format(self.location.escaped_name)
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

    async def send_redefine_location_roles_message(self):
        text = texts.REDEFINED_LOCATION_ROLES_MESSAGE
        text = text.format(await self.bot_link())
        await self.send_message(text)

    async def redefine_location_and_roles(self) -> None:
        await self.choose_game_location()
        await self.distribute_roles()
        await self.send_redefine_location_roles_message()

    async def finish_game(self) -> None:
        await self.unset_players()
        if self.previous_status == GameStatus.recruitment:
            await self.delete_sended_messages()
        await self.send_message(texts.GAME_ENDED)

    def set_current_player(self, player: Player) -> None:
        assert player in self.players.in_game, "Player doesn't in game."
        self.previous_player = self.cur_player
        self.cur_player = player

    def remove_cur_and_previous(self, players: PlayersCollection):
        if self.previous_player:
            players.safety_remove(self.previous_player)

        if self.cur_player:
            players.safety_remove(self.cur_player)

    def define_current_player(self) -> None:
        players = self.players.in_game
        self.remove_cur_and_previous(players)
        self.set_current_player(random.choice(players))

    def define_question_to_player(self) -> None:
        players = self.players.in_game
        if self.cur_player:
            players.safety_remove(self.cur_player)
        if self.question_to_player:
            players.safety_remove(self.question_to_player)
        self.question_to_player = random.choice(players)

    async def define_game_players(self) -> None:
        try:
            self.define_current_player()
            self.define_question_to_player()
        except IndexError:
            await self.send_message(texts.NOT_ENOUGH_TO_DISTRIBUTE)
            raise exc.GameEnd()

    async def send_ask_question_msg(self):
        cur_player_link = self.cur_player.mention_markdown()
        qiestion_to_player_link = self.question_to_player.mention_markdown()
        await self.send_message(
            texts.ASK_QUESTION_MSG.format(cur_player_link, qiestion_to_player_link),
        )

    async def redefine_game_players(self, player: Player):
        if player.id == self.cur_player.id:
            self.define_current_player()

        question_player_id = self.question_to_player.id
        if player.id == question_player_id or self.cur_player.id == question_player_id:
            self.define_question_to_player()

    async def unset_players(self):
        for player in self.players:
            try:
                await player.delete_cache()
            except AssertionError:
                continue

    async def send_error_msg_and_finish_game(self, text: str):
        await self.only_send_message(text=text)
        raise exc.GameEnd()

    async def check_room(self):
        await self.check_if_spies_exists()
        await self.check_if_can_use_two_spies()
        await self.check_if_enough_players()

    async def check_if_can_use_two_spies(self):
        if (
            self.game_settings.two_spies
            and len(self.players) < spygame.two_spies_limits_on_players
        ):
            await self.send_error_msg_and_finish_game(
                texts.YOU_NEED_MIN_THE_PLAYERS_TO_PLAY_WITH_TWO_SPIES
            )

    async def check_if_spies_exists(self):
        if not self.players.spies:
            await self.send_error_msg_and_finish_game(texts.NO_SPIES_FOR_CONTINUE)

    async def check_if_enough_players(self):
        if len(self.players) < spygame.min_players_in_room:
            await self.send_error_msg_and_finish_game(
                texts.NOT_ENOUGH_PLAYERS_TO_CONTINUE
            )

    async def quit(self, player: Player):
        await self.players.quit(player)
        try:
            if player == self.creator:
                await self.send_error_msg_and_finish_game(texts.CREATOR_LEFT_THE_GAME)
            if not self.recruitment:
                await self.check_room()
        except Exception as e:
            raise e
        else:
            if self.recruitment:
                await self.display_players_in_join_message()
            else:
                await self.redefine_game_players(player)

            if self.playing:
                await self.send_ask_question_msg()
        finally:
            if not self.recruitment:
                await self.only_send_message(
                    text=texts.PLAYER_LEFT_GAME.format(player.mention_markdown()),
                    parse_mode=enums.ParseMode.MARKDOWN_V2,
                )
            await player.send_message(
                texts.PLAYER_LEFT_GAME.format("Ти"),
            )

    def vote_message(self):
        assert self.vote is not None, "You need to init voting first."
        return self.vote.vote_message()

    @_t.overload
    def make_vote(sself, voter: Player, _for: Player, vote: bool = True) -> bool:
        """
        In summary voting you need to include per the voter vote.
        """

    @_t.overload
    def make_vote(
        sself, voter: Player, _for: Player | None = None, vote: bool = True
    ) -> bool:
        """
        In early voting you doesn't need to include user because he specified when vote initialized.
        """

    def make_vote(
        self, voter: Player, _for: Player | None = None, vote: bool = True
    ) -> bool:
        assert self.vote is not None, "You need to init voting first."
        return self.vote.vote(voter=voter, _for=_for, vote=vote)

    @contextmanager
    def vote_manager(self, vote: Vote):
        assert self.vote is None, f"You need to finish {type(self.vote)} as first."
        self.vote = vote
        try:
            yield
        finally:
            self.vote = None

    @contextmanager
    def create_summary_vote(self):
        vote = SummaryVote.create_vote(self.players)
        with self.vote_manager(vote):
            yield vote

    @contextmanager
    def create_early_vote(self, author: Player | TelegramUser, suspected: Player):
        if isinstance(author, TelegramUser):
            author = self.players.get(author.id)
        vote = EarlyVote.create_vote(author=author, suspected=suspected)
        with self.vote_manager(vote):
            yield vote

    def vote_results(self) -> bool | Player:
        assert self.vote is not None, "Vote doesn't exitsts."
        return self.vote.results(self.players.in_game)

    async def send_successfully_early_voting_msg(self):
        assert isinstance(
            self.vote, EarlyVote
        ), "Voting need to be early for that action."
        assert (
            self.vote_results() is True and self.vote.suspected.is_spy
        ), "Voting wasn't successful, you cannot send that message"
        await self.send_message(
            texts.SUCCESSFULY_EARLY_VOTING.format(self.vote.author.mention_markdown()),
        )

    async def send_unsuccessfully_early_voting_msg(self):
        assert isinstance(
            self.vote, EarlyVote
        ), "Voting need to be early for that action."
        assert (
            self.vote_results() is True and not self.vote.suspected.is_spy
        ), "Voting wasn't unsuccessful, you cannot send that message"
        await self.send_message(texts.NOT_SUCCESSFULY_EARLY_VOTING)

    @contextmanager
    def with_guess_spy(self, spy: Player):
        self.guess_spy_player = spy
        try:
            yield
        finally:
            self._spy_player_guess = None

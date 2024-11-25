from database import TelegramUserModel, RoleModel, LocationModel

from pydantic_collections import BaseCollectionModel

from caching import CachePrefix, CacheModel

from utils.exc.assertion import AssertionAnswer
from utils.chat.model import ChatModel

from settings import redis, spygame

from spy.routers import spybot
from spy import texts

import typing as _t


type PLAYER_STATUS = _t.Literal[
    "in_game",
    "kicked",
    "left",
]


type room_id = int | str


def role_check(func):
    async def wrapper(self: Player, *args, **kwargs):
        assert self.role is not None
        return await func(self, *args, **kwargs)

    return wrapper


class Player(TelegramUserModel, CacheModel, ChatModel):
    db: _t.ClassVar[int] = redis.game_db
    cache_prefix: _t.ClassVar[str] = CachePrefix.in_game
    save_msg: _t.ClassVar[bool] = True

    role: _t.Optional[RoleModel] = None
    status: PLAYER_STATUS = "in_game"
    room_id: room_id
    score: int = 0

    @property
    def cache_identity(self):
        return self.chat_id

    @property
    def chat_id(self):
        return self.id

    @property
    def __bot__(self):
        return spybot

    async def set_stauts(self, s: PLAYER_STATUS):
        self.status = s
        await self.save_in_cache()

    async def kick(self):
        self.status = "kicked"
        await self.save_in_cache()

    async def leave(self):
        self.status = "left"
        await self.save_in_cache()

    async def remove(self):
        await self.delete_cache()

    @role_check
    async def notify_about_role(self, location: LocationModel):
        role_text = (await texts.NOTIFY_USER_ABOUT_ROLE(self.language)).format(
            role=self.role
        )

        if self.role.is_spy:
            await self.send_message(text=role_text)
            return

        location_text = (await texts.NOTIFY_ABOUT_LOCATION(self.language)).format(
            location=location
        )

        text = location_text + "\n" + role_text
        if location.image_url is not None:
            await self.send_photo(location.image_url, caption=text)
            return
        await self.send_message(text)


class PlayersCollection(BaseCollectionModel[Player]):

    def append(self, __object: TelegramUserModel, room_id: room_id):
        assert __object is TelegramUserModel or issubclass(
            __object.__class__, TelegramUserModel
        )
        assert not self.get(__object.id), AssertionAnswer(
            texts.YOU_ALREADY_IN_GAME, translate=__object.language
        )
        assert len(self) < spygame.max_players_in_room, AssertionAnswer(
            texts.GAME_ROOM_ALREADY_FULL, translate=__object.language
        )

        player = Player(**__object.model_dump(), room_id=room_id)
        super(PlayersCollection, self).append(player)

    def get(self, player_id: int) -> _t.Optional[Player]:
        for p in self:
            if player_id == p.id:
                return p

    def filter_by_status(self, *s: PLAYER_STATUS):
        return self.__class__([player for player in self if player.status in s])

    @property
    def spies(self):
        return self.__class__(
            [player for player in self if (role := player.role) and role.is_spy]
        )

    @property
    def ordinary(self):
        return self.__class__(
            [player for player in self if (role := player.role) and not role.is_spy]
        )

    @property
    def in_game(self):
        return self.filter_by_status("in_game")

    @property
    def kicked(self):
        return self.filter_by_status("kicked")

    @property
    def lefted(self):
        return self.filter_by_status("left")

    async def set_status(self, s: PLAYER_STATUS):
        for player in self.filter_by_status("in_game", "kicked"):
            await player.set_stauts(s)

    def increase_score(self, num: int):
        for player in self:
            player.score += num

    def safety_remove(self, player: Player):
        try:
            self.remove(player)
        except ValueError:
            return

    def remove_players(self, *players: Player):
        for player in players:
            self.safety_remove(player)

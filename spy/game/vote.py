from abc import ABC, abstractmethod

from collections import defaultdict
from .players import Player

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from spy.callback import CallbackPrefix
from spy import texts

import pydantic as _p
import typing as _t


class Vote(_p.BaseModel, ABC):

    voted: dict[Player, _t.Any] = _p.Field(default_factory=dict)

    def percent_voted(self, votes: int, players: list[Player]) -> float:
        return (votes / len(players)) * 100

    @abstractmethod
    def vote(self, voter: Player, _for: Player, vote: bool) -> bool: ...

    @abstractmethod
    def results(self, players: list[Player]) -> bool: ...

    @abstractmethod
    def vote_message(self) -> tuple[str, types.InlineKeyboardMarkup]: ...

    @abstractmethod
    def create_vote(self) -> _t.Self: ...


class EarlyVote(Vote):

    voted: dict[Player, bool] = _p.Field(default=dict)
    suspected: Player
    author: Player
    against: int = 0
    per: int = 0

    def vote(
        self, voter: Player, _for: Player | None = None, vote: bool = True
    ) -> bool:
        if (voter in self.voted) or voter == self.suspected:
            return False

        if vote:
            self.per += 1
        else:
            self.against += 1

        self.voted[voter] = vote
        return True

    def results(self, players: list[Player]) -> bool:
        players = players.copy()
        players.remove(self.suspected)
        if self.percent_voted(len(self.voted), players) < 80:
            return False
        per = self.percent_voted(self.per, players)
        againts = self.percent_voted(self.against, players)
        return per > againts

    def vote_message(self):
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"👍🏻 {self.per}",
                callback_data=CallbackPrefix.vote_per,
            )
        )
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"👎🏻 {self.against}",
                callback_data=CallbackPrefix.vote_againts,
            )
        )
        keyboard.adjust(1)

        return texts.EARLY_VOTE, keyboard.as_markup()

    @staticmethod
    def create_vote(author: Player, suspected: Player):
        return EarlyVote(
            author=author, suspected=suspected, voted={author: True}, per=1
        )


class SummaryVote(Vote):

    voted: dict[Player, Player] = _p.Field(default=dict)
    suspected: dict[Player, int] = _p.Field(default_factory=lambda: defaultdict(int))
    msg_counter: int = 0

    def vote(self, voter: Player, _for: Player, vote: bool = True) -> bool:
        if voter in self.voted or voter == _for:
            return False

        self.suspected[_for] += 1
        self.voted[voter] = _for
        return True

    def results(self, players: list[Player]):
        max_votes = max(self.suspected, key=self.suspected.get)
        suspected_votes = self.suspected.pop(max_votes)
        assert suspected_votes is not None, "Suspected votes is None"

        if suspected_votes == 0:
            return False

        for votes in self.suspected.values():
            if votes == suspected_votes:
                return False

        return max_votes

    def vote_message(self):
        keyboard = InlineKeyboardBuilder()
        for player, votes in self.suspected.items():
            keyboard.add(
                types.InlineKeyboardButton(
                    text=player.full_name + " - " + str(votes),
                    callback_data=CallbackPrefix.vote + str(player.id),
                )
            )
        keyboard.adjust(1)

        return texts.VOTE_FOR_SPY, keyboard.as_markup()

    @staticmethod
    def create_vote(players: list[Player]):
        vote = SummaryVote()
        for player in players:
            vote.suspected[player]
        return vote

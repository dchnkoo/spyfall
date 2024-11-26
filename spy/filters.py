from aiogram.utils.deep_linking import decode_payload, create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import filters, types, Bot, enums

from spy.game import GameStatus, GameRoom, PLAYER_STATUS
from spy import texts

from database import TelegramUser

from utils.msg import extract_message

import typing as _t


class GameProccessFilter(filters.Filter):

    def __init__(self, *s: GameStatus) -> None:
        self.statuses = s

    async def __call__(self, msg: types.Message | types.CallbackQuery, *args, **kwds):
        msg = extract_message(msg)

        try:
            room = await GameRoom.load_cached(msg.chat.id)
        except AssertionError:
            return False

        if not self.statuses:
            return True

        return room.status in self.statuses


class RegisteredUser(filters.Filter):

    def __init__(self, send_msg: bool = True) -> None:
        self.send_msg = send_msg

    async def __call__(self, msg: types.Message, bot: Bot, *args, **kwds):
        try:
            await TelegramUser.load_cached(msg.from_user.id)
        except AssertionError:
            if self.send_msg:
                lang_code = msg.from_user.language_code or "en"

                keyboard = InlineKeyboardBuilder()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=await texts.FIX(lang_code),
                        url=await create_start_link(bot, payload=""),
                    )
                )

                await msg.answer(
                    await texts.YOU_NEED_TO_GO_TO_THE_BOT(lang_code),
                    reply_markup=keyboard.as_markup(),
                )
            return False
        else:
            return True


class PlayerFilter(filters.Filter):
    def __init__(
        self,
        *status: PLAYER_STATUS,
        is_creator: bool = False,
        is_current: bool = False,
        is_question_to: bool = False,
    ) -> None:
        self.status = status
        self.is_creator = is_creator
        self.is_current = is_current
        self.is_question_to = is_question_to

    async def __call__(self, message: types.Message | types.CallbackQuery, **_):
        chat_id = extract_message(message).chat.id
        user_id = message.from_user.id

        try:
            room = await GameRoom.load_cached(chat_id)
        except AssertionError:
            return False

        player = room.players.get(user_id)
        status = True if not self.status else player.status in self.status
        is_creator = True if not self.is_creator else player.id == room.creator.id
        is_current = (
            True
            if not self.is_current
            else player.id == room.cur_player.id if room.cur_player else False
        )
        is_question_to = (
            True
            if not self.is_question_to
            else (
                player.id == room.question_to_player
                if room.question_to_player
                else False
            )
        )

        return status and is_creator and is_current and is_question_to


class ChatMemberIsAdmin(filters.Filter):

    def __init__(self, answer: bool = True) -> None:
        self.answer = answer
        super(ChatMemberIsAdmin, self).__init__()

    async def __call__(self, message: types.Message, **_):
        member = await message.chat.get_member(message.from_user.id)

        if member.status not in (
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.CREATOR,
        ):
            if self.answer:
                lang_code = message.from_user.language_code or "en"
                await message.reply(await texts.COMMAND_ONLY_FOR_ADMINS(lang_code))
            return False

        return True

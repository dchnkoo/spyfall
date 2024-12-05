from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import filters, types, Bot, enums

from spy.game import GameStatus, PLAYER_STATUS, GameManager
from spy import texts

from database import TelegramUser

from utils.msg import extract_message


class GameProccessFilter(filters.Filter):

    def __init__(self, *s: GameStatus, by_user_id: bool = False) -> None:
        self.statuses = s
        self.by_user_id = by_user_id

    async def __call__(self, msg: types.Message | types.CallbackQuery, *args, **kwds):
        message = extract_message(msg)
        if self.by_user_id:
            try:
                manager = await GameManager.meta.load_by_user_id(msg.from_user.id)
            except AssertionError:
                return False
        else:
            manager = GameManager.meta.get_room(message.chat.id)

        if manager is None:
            return False

        if not self.statuses:
            return True

        return manager.status in self.statuses


class RegisteredUser(filters.Filter):

    def __init__(self, send_msg: bool = True) -> None:
        self.send_msg = send_msg

    async def __call__(self, msg: types.Message, bot: Bot, *args, **kwds):
        try:
            await TelegramUser.load_cached(msg.from_user.id)
        except AssertionError:
            if self.send_msg:
                keyboard = InlineKeyboardBuilder()
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=texts.FIX,
                        url=await create_start_link(bot, payload=""),
                    )
                )

                await msg.answer(
                    texts.YOU_NEED_TO_GO_TO_THE_BOT,
                    reply_markup=keyboard.as_markup(),
                    parse_mode=enums.ParseMode.MARKDOWN_V2,
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
        is_spy: bool = False,
    ) -> None:
        self.status = status
        self.is_creator = is_creator
        self.is_current = is_current
        self.is_question_to = is_question_to
        self.is_spy = is_spy

    async def __call__(self, message: types.Message | types.CallbackQuery, **_):
        user_id = message.from_user.id

        try:
            manager = await GameManager.meta.load_by_user_id(user_id)
        except AssertionError:
            return False

        if manager is None:
            return False

        room = manager.room
        player = room.players.get(user_id)

        if not player:
            return False

        status = True if not self.status else player.status in self.status
        is_creator = True if not self.is_creator else player.id == room.creator.id
        is_current = (
            True
            if not self.is_current
            else player == room.cur_player if room.cur_player else False
        )
        is_question_to = (
            True
            if not self.is_question_to
            else (
                player == room.question_to_player if room.question_to_player else False
            )
        )
        is_spy = True if not self.is_spy else player.is_spy

        return status and is_creator and is_current and is_question_to and is_spy


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
                await message.reply(texts.COMMAND_ONLY_FOR_ADMINS)
            return False

        return True

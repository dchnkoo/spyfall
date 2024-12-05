from spy.decorators import (
    with_user_cache,
    with_manager,
    with_player,
)
from spy.routers import group_only_msg_without_state, group_clear, group_without_state
from spy.game import GameManager, GameStatus, GameRoom, Player
from spy import filters as game_filters, texts
from spy.callback import CallbackPrefix
from spy.commands import group

from settings import spygame

from utils.exc.callback import CallbackAlert

from aiogram import filters, types, F, enums

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@group_only_msg_without_state.message(
    filters.Command(group.play),
    ~game_filters.GameProccessFilter(),
    ~game_filters.PlayerFilter(),
    game_filters.RegisteredUser(),
)
@with_user_cache
async def play(msg: types.Message, user: "TelegramUser", **_):
    settings = await user.get_settings()
    assert settings is not None

    room = GameRoom(
        id=msg.chat.id,
        creator=user,
        game_settings=settings,
        language_code=user.language,
    )

    manager = await GameManager.register(room=room)
    await manager.put_task(GameStatus.recruitment)


@group_only_msg_without_state.message(
    filters.Command(group.start_playing),
    game_filters.GameProccessFilter(GameStatus.recruitment),
    game_filters.PlayerFilter(is_creator=True),
)
@with_manager
async def start_playing(msg: types.Message, manager: GameManager, **_):
    manager.tasks.cancel_current_task()
    await manager.room.delete_sended_messages()
    await manager.put_task(GameStatus.playing)


@group_only_msg_without_state.message(
    filters.Command(group.leave),
    game_filters.GameProccessFilter(),
    filters.or_f(
        game_filters.PlayerFilter("in_game"),
        game_filters.PlayerFilter("kicked"),
    ),
)
@with_player
@with_manager
async def left_the_game(msg: types.Message, manager: GameManager, player: Player, **_):
    try:
        await manager.room.quit(player)
    finally:
        await msg.delete()


def validate_entities(entities: list[types.MessageEntity]):
    if (count_enitities := len(entities)) > 2 or count_enitities < 2:
        return False
    enitity = entities[1]
    if enitity.type in (
        enums.MessageEntityType.MENTION,
        enums.MessageEntityType.TEXT_MENTION,
    ):
        return True
    return False


@group_only_msg_without_state.message(
    filters.Command(group.vote, magic=F.args.func(lambda args: args is not None)),
    game_filters.GameProccessFilter(GameStatus.playing),
    game_filters.PlayerFilter("in_game"),
    F.entities.func(validate_entities),
)
@with_player
@with_manager
async def vote_for_spy(msg: types.Message, manager: GameManager, player: Player, **_):
    try:
        entity = msg.entities[1]
        assert entity is not None, "Vote enitity is None"

        match entity.type:
            case enums.MessageEntityType.MENTION:
                username = msg.text[entity.offset + 1 :]
                suspected = manager.room.players.get_by_username(username.strip())
            case enums.MessageEntityType.TEXT_MENTION:
                suspected = manager.room.players.get(entity.user.id)
            case _:
                raise Exception("Something goes wrong while handle msg enitity type.")

        if suspected is None:
            await msg.answer(
                texts.YOU_CAN_VOTE_ONLY_FOR_USER_WHICH_IN_GAME,
                parse_mode=enums.ParseMode.MARKDOWN_V2,
            )
            return

        if suspected == player:
            await msg.answer(
                texts.YOU_CANNOT_VOTE_FOR_YOUR_SELF,
                parse_mode=enums.ParseMode.MARKDOWN_V2,
            )
            return

        async with manager.block_game_proccess():
            with manager.room.create_early_vote(author=player, suspected=suspected):
                await manager.put_task(GameStatus.voting)
                await manager.tasks.wait_until_current_task_complete()
    finally:
        await msg.delete()


voting_filters = (
    game_filters.GameProccessFilter(GameStatus.voting),
    game_filters.PlayerFilter("in_game"),
)


@group_only_msg_without_state.callback_query(
    F.data == CallbackPrefix.vote_per, *voting_filters
)
@group_only_msg_without_state.callback_query(
    F.data == CallbackPrefix.vote_againts, *voting_filters
)
@with_player
@with_manager
async def early_voting(
    msg: types.CallbackQuery, manager: GameManager, player: Player, **_
):
    if player == manager.room.vote.suspected:
        raise CallbackAlert(
            message=texts.SUSPECTED_CANNOT_VOTE_FOR_SELF,
            show_alert=True,
        )

    if msg.data == CallbackPrefix.vote_per:
        vote = manager.room.make_vote(voter=player)
    else:
        vote = manager.room.make_vote(voter=player, vote=False)

    if vote is False:
        raise CallbackAlert(message=texts.YOU_ALREADY_VOTED, show_alert=True)

    _, reply_markup = manager.room.vote_message()
    await msg.message.edit_reply_markup(
        msg.inline_message_id, reply_markup=reply_markup
    )
    raise CallbackAlert(message=texts.YOU_VOTED)


@group_only_msg_without_state.callback_query(
    game_filters.GameProccessFilter(GameStatus.summary_vote),
    F.data.startswith(CallbackPrefix.vote),
)
@with_player
@with_manager
async def summary_voting(
    msg: types.CallbackQuery, manager: GameManager, player: Player, **_
):
    suspected_id = msg.data.removeprefix(CallbackPrefix.vote)
    suspected = manager.room.players.get(int(suspected_id))
    assert suspected is not None, "Player cannot be None in that context."

    if player == suspected:
        raise CallbackAlert(
            message=texts.YOU_CANNOT_VOTE_FOR_YOUR_SELF,
            show_alert=True,
        )

    voted = manager.room.make_vote(player, suspected)

    if voted is False:
        raise CallbackAlert(message=texts.YOU_ALREADY_VOTED, show_alert=True)

    _, reply_markup = manager.room.vote_message()
    await msg.message.edit_reply_markup(
        msg.inline_message_id, reply_markup=reply_markup
    )
    raise CallbackAlert(message=texts.YOU_VOTED)


@group_only_msg_without_state.message(
    filters.Command(group.end),
    game_filters.GameProccessFilter(),
    filters.or_f(
        game_filters.PlayerFilter(is_creator=True),
        game_filters.ChatMemberIsAdmin(answer=False),
    ),
)
@with_manager
async def end_the_game(msg: types.Message, manager: GameManager, **_):
    await manager.finish_game()


@group_without_state.message(
    game_filters.GameProccessFilter(GameStatus.summary_vote),
)
@with_manager
async def resender(msg: types.Message, manager: GameManager, **_):
    vote = manager.room.vote
    if vote.msg_counter >= spygame.resend_summary_vote_msg_after:

        vote.msg_counter = 0
        await manager.room.delete_last_sended_msg()

        text, reply_markup = vote.vote_message()
        await manager.room.send_message(
            text=text,
            reply_markup=reply_markup,
        )
        return

    vote.msg_counter += 1


@group_only_msg_without_state.message(
    filters.Command(group.next, ignore_case=True),
    game_filters.GameProccessFilter(GameStatus.playing),
    game_filters.PlayerFilter(is_current=True),
)
@with_manager
async def puss_turn(msg: types.Message, manager: GameManager, **_):
    await manager.room.define_game_players()
    await manager.room.send_ask_question_msg()


@group_clear.message(
    game_filters.GameProccessFilter(),
    ~game_filters.GameProccessFilter(GameStatus.summary_vote),
    ~filters.or_f(
        game_filters.PlayerFilter(is_current=True),
        game_filters.PlayerFilter(is_question_to=True),
    ),
)
async def cleaner(msg: types.Message):
    await msg.delete()

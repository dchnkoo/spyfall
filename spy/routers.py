from aiogram import Bot, Dispatcher, Router, F, filters, enums
from aiogram.dispatcher.event.handler import CallbackType
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import chat_type

from settings import redis, bot


spybot = Bot(bot.token)
storage = RedisStorage.from_url(
    redis.dsn(redis.states_db),
    state_ttl=redis.default_cache_live_time,
    data_ttl=redis.default_cache_live_time,
)
dp = Dispatcher(storage=storage)


def extract_message_filters(*routers: Router) -> tuple[CallbackType]:
    return tuple(i.callback for j in routers for i in j.message._handler.filters)


clear_router = Router()

without_state = Router()
without_state.message.filter(filters.StateFilter(None))

only_msg_router = Router()
only_msg_router.message.filter(
    F.content_type == enums.ContentType.TEXT,
)

no_command = Router()
no_command.message.filter(~F.text.startswith("/"))

private_clear = Router()
private_clear.message.filter(F.chat.type == chat_type.ChatType.PRIVATE)

private_without_state = Router()
private_without_state.message.filter(
    *extract_message_filters(private_clear, without_state),
)

private_only_msg = Router()
private_only_msg.message.filter(
    *extract_message_filters(private_clear, only_msg_router)
)

private_only_msg_without_state = Router()
private_only_msg_without_state.message.filter(
    *extract_message_filters(without_state, private_only_msg)
)

group_clear = Router()
group_clear.message.filter(
    F.chat.type.in_((chat_type.ChatType.GROUP, chat_type.ChatType.SUPERGROUP))
)


group_without_state = Router()
group_without_state.message.filter(*extract_message_filters(group_clear, without_state))

group_only_msg = Router()
group_only_msg.message.filter(*extract_message_filters(group_clear, only_msg_router))

group_only_msg_without_state = Router()
group_only_msg_without_state.message.filter(
    *extract_message_filters(without_state, group_only_msg)
)

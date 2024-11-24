from aiogram import types, enums

import random


def random_id():
    return random.randint(10000, 5000000)


def random_str_id():
    return str(random_id())


def extract_message(msg: types.Message | types.CallbackQuery) -> types.Message:
    message = msg.message if isinstance(msg, types.CallbackQuery) else msg
    assert isinstance(message, types.Message)
    return message


def edit_or_answer(msg: types.Message | types.CallbackQuery):
    if isinstance(msg, types.CallbackQuery):
        return extract_message(msg).edit_text
    return extract_message(msg).answer


def create_new_query(
    msg: types.Message | types.CallbackQuery,
    data: str | None = None,
    from_user: types.User | None = None,
    **kw,
):
    exctracted = extract_message(msg)

    return types.CallbackQuery(
        id=(random_str_id() if not "id" in kw else kw.pop("id")),
        from_user=(from_user or msg.from_user),
        chat_instance=str(exctracted.chat.id),
        message=exctracted,
        data=(data or (msg.data if isinstance(msg, types.CallbackQuery) else None)),
        **kw,
    )


async def handle_content_type_text(msg: types.CallbackQuery | types.Message):
    exctracted = extract_message(msg)

    if exctracted.content_type != enums.ContentType.TEXT:
        await exctracted.delete()
        return exctracted.answer
    return exctracted.edit_text

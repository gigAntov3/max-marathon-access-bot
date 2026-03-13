from maxapi import Dispatcher, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext

from models.chats import Chat
from repositories.chats import ChatsRepository

from handlers.admin.marathons.keyboards import (
    get_chats_keyboard,
    get_chat_keyboard,
)

chats_repo = ChatsRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


async def marathons_chats(event: MessageCallback):
    marathon_id = get_id(event.callback.payload)

    chats = await chats_repo.find_all(
        marathon_id=marathon_id
    )

    await event.message.edit(
        text="Чаты",
        attachments=[get_chats_keyboard(chants=chats, marathon_id=marathon_id)]
    )


async def marathons_chat(event: MessageCallback):
    chat_id = get_id(event.callback.payload)

    chat: Chat = await chats_repo.get_one(id=chat_id)

    text = (
        f"💬 Название: {chat.title}\n"
        
        f"🟢 Статус: {'Активен' if chat.is_active else 'Неактивен'}\n"

        f"📅 Дата создания: {chat.created_at.strftime('%d.%m.%Y')}\n"
    )

    await event.message.edit(
        text=text,
        attachments=[get_chat_keyboard(chat_id=chat.id, marathon_id=chat.marathon_id)]
    )


async def delete_marathon_chat(event: MessageCallback):
    chat_id = get_id(event.callback.payload)

    chat: Chat = await chats_repo.get_one(id=chat_id)

    await chats_repo.delete_one(id=chat.id)

    chats = await chats_repo.find_all(
        marathon_id=chat.marathon_id
    )

    await event.message.edit(
        text="Чаты",
        attachments=[get_chats_keyboard(chants=chats, marathon_id=chat.marathon_id)]
    )


def register_handlers(dp: Dispatcher):
    dp.message_callback.register(marathons_chats, F.callback.payload.startswith("marathon_chats:"))
    dp.message_callback.register(marathons_chat, F.callback.payload.startswith("marathon_chat:"))
    dp.message_callback.register(delete_marathon_chat, F.callback.payload.startswith("delete_marathon_chat:"))
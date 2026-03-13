from maxapi import Dispatcher, F
from maxapi.types import Command, MessageCreated, MessageCallback
from maxapi.context import MemoryContext

from .keyboards import get_main_admin_keyboard
from .states import EnterAdminPasswordState

from models.chats import Chat
from models.marathons import Marathon

from repositories.marathons import MarathonsRepository
from repositories.chats import ChatsRepository

from config import settings


marathons_repo = MarathonsRepository()
chats_repo = ChatsRepository()


async def start_admin(event: MessageCreated, context: MemoryContext):
    if event.from_user.user_id in settings.bot.admins:
        await event.message.answer(
            text=f"Пример чат-бота для MAX 💙",
            attachments=[get_main_admin_keyboard()]
        )


# async def enter_admin_password(event: MessageCreated, context: MemoryContext):
#     if event.message.body.text == settings.bot.admin_password:
#         await context.clear()
        
#         await event.message.answer(
#             text=f"Пример чат-бота для MAX 💙",
#             attachments=[get_main_admin_keyboard()]
#         )
#     else:
#         await event.message.answer(
#             text=f"Неверный пароль! Попробуйте ещё раз.",
#         )


async def back_to_admin(event: MessageCallback):
    await event.message.edit(
        text=f"Пример чат-бота для MAX 💙",
        attachments=[get_main_admin_keyboard()]
    )



async def connect_chat_to_marathon(event: MessageCreated):
    if event.from_user.user_id in settings.bot.admins:
        # Получаем id марафона из сообщения
        try:
            marathon_id = int(event.message.body.text.split()[1])
        except (IndexError, ValueError):
            await event.message.answer(
                text="❌ Неверный формат команды. Используйте: /connect <marathon_id>"
            )
            return

        marathon: Marathon = await marathons_repo.get_one(id=marathon_id)

        if not marathon:
            await event.message.answer(
                text=f"❌ Марафон с ID {marathon_id} не найден."
            )
            return

        await chats_repo.add_one(
            marathon_id=marathon_id,
            chat_id=event.chat.chat_id,
            title=event.chat.title,
            image_url=event.chat.icon.url if event.chat.icon else None,
            link=event.chat.link
        )

        text = (
            f"✅ Чат успешно связан с марафоном!\n\n"
            f"Информация о марафоне:\n"
            f"🆔 ID: {marathon.id}\n"
            f"📛 Название: {marathon.name}\n"
            f"📝 Описание: {marathon.description}\n"
            f"🏷 Тип: {'Групповой' if marathon.type == 'group' else 'Индивидуальный'}\n"
            f"📅 Даты: {marathon.start_date.strftime('%d.%m.%Y')} — {marathon.end_date.strftime('%d.%m.%Y')}\n"
            f"💰 Цена: {marathon.price} руб.\n"
            f"🟢 Статус: {'Активен' if marathon.is_active else 'Неактивен'}"
        )

        await event.message.answer(text=text)

    else:
        await event.message.answer(
            text="❌ У вас недостаточно прав для выполнения этой команды."
        )


def register_handlers(dp: Dispatcher):
    dp.message_created.register(start_admin, Command('admin'))

    # dp.message_created.register(enter_admin_password, EnterAdminPasswordState.password)
    
    dp.message_callback.register(back_to_admin, F.callback.payload == 'back:admin')

    dp.message_created.register(connect_chat_to_marathon, Command('connect_chat'))
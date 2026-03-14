import re

from maxapi import Dispatcher, F
from maxapi.types import Command, MessageCreated, MessageCallback
from maxapi.context import MemoryContext

from .states import EnterPhoneState
from .keyboards import get_main_client_keyboard

from models.users import User

from repositories.users import UsersRepository

from config import settings


users_repo = UsersRepository()


async def start(event: MessageCreated, context: MemoryContext):
    user: User = await users_repo.get_or_create(
        first_name=event.from_user.first_name,
        last_name=event.from_user.last_name,
        username=event.from_user.username,
        user_id=event.from_user.user_id
    )

    if user.phone:
        await event.message.answer(
            text=f"Пример чат-бота для MAX 💙",
            attachments=[get_main_client_keyboard()]
        )
        return

    else:
        await context.set_state(EnterPhoneState.phone)

        await event.message.answer(
            text="Введите номер телефона",
        )



async def request_contact(event: MessageCreated, context: MemoryContext):
    phone = event.message.body.text.strip()

    if not re.fullmatch(r'\+?\d{10,15}', phone):
        await event.message.answer(
            text="❌ Некорректный номер телефона. Введите номер в формате +79991234567 или 89991234567."
        )
        return

    await users_repo.update_phone_by_user_id(
        user_id=event.from_user.user_id,
        phone=phone
    )

    await context.clear()

    await event.message.answer(
        text="✅ Ваш номер успешно сохранён!",
    )

    await event.message.answer(
        text="Пример чат-бота для MAX 💙",
        attachments=[get_main_client_keyboard()]
    )


async def back_to_clients(event: MessageCallback):
    await event.message.edit(
        text=f"Пример чат-бота для MAX 💙",
        attachments=[get_main_client_keyboard()]
    )


def register_handlers(dp: Dispatcher):
    dp.message_created.register(start, Command('start'))

    dp.message_created.register(request_contact, EnterPhoneState.phone)

    dp.message_callback.register(back_to_clients, F.callback.payload == 'back:clients')
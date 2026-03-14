from datetime import datetime

from maxapi import Dispatcher, F
from maxapi.types import MessageCallback, MessageCreated
from maxapi.context import MemoryContext

from repositories.mailings import (
    MailingsRepository,
    MailingImageRepository,
    MailingButtonRepository,
)
from repositories.marathons import MarathonsRepository

from handlers.admin.mailings.states import AddMailingState
from handlers.admin.mailings.keyboards import get_mailing_marathons_keyboard, get_mailing_buttons_keyboard
from handlers.base.keyboards import get_back_keyboard

from handlers.admin.mailings.keyboards import get_mailings_keyboard


mailings_repo = MailingsRepository()
mailing_images_repo = MailingImageRepository()
mailing_buttons_repo = MailingButtonRepository()
marathons_repo = MarathonsRepository()


async def add_mailing(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMailingState.title)

    await event.message.edit(
        text="Введите название рассылки",
        attachments=[get_back_keyboard("mailings")]
    )


async def enter_mailing_title(event: MessageCreated, context: MemoryContext):
    await context.update_data(
        title = event.message.body.text
    )

    await context.set_state(AddMailingState.message)

    await event.message.answer(
        text="Отправьте сообщение рассылки (текст + изображения)",
        attachments=[get_back_keyboard("mailing_title")]
    )


async def back_to_enter_mailing_title(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMailingState.title)

    await event.message.edit(
        text="Введите название рассылки",
        attachments=[get_back_keyboard("mailings")]
    )


async def enter_mailing_message(event: MessageCreated, context: MemoryContext):

    text = event.message.body.text
    attachments = event.message.body.attachments or []

    images = []

    for att in attachments:
        if att.type == "image":
            images.append({
                "photo_id": att.payload.photo_id,
                "photo_token": att.payload.token,
                "photo_url": att.payload.url
            })

    await context.update_data(
        text=text,
        images=images
    )

    marathons = await marathons_repo.find_all(offset=0, limit=10)

    await event.message.answer(
        text="Выберите марафон для фильтра рассылки",
        attachments=[get_mailing_marathons_keyboard(marathons, 0)]
    )


async def back_to_enter_mailing_message(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMailingState.message)

    await event.message.edit(
        text="Отправьте сообщение рассылки (текст + изображения)",
        attachments=[get_back_keyboard("mailing_title")]
    )


async def choose_mailing_marathon(event: MessageCallback, context: MemoryContext):

    payload = event.callback.payload

    marathon_id = None

    if payload.startswith("mailing_marathon:"):
        marathon_id = int(payload.split(":")[1])

    await context.update_data(marathon_id=marathon_id)

    await context.set_state(AddMailingState.buttons)

    await event.message.edit(
        text=(
            "Введите кнопки в формате:\n\n"
            "Текст - https://site.com\n"
            "Текст2 - https://site2.com\n\n"
            "Или нажмите «Без кнопок»"
        ),
        attachments=[get_mailing_buttons_keyboard()]
    )


async def back_to_enter_mailing_marathon(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMailingState.marathon)

    marathons = await marathons_repo.find_all(offset=0, limit=10)

    await event.message.edit(
        text="Выберите марафон для фильтра рассылки",
        attachments=[get_mailing_marathons_keyboard(marathons, 0)]
    )


async def enter_mailing_buttons(event: MessageCreated, context: MemoryContext):
    text = event.message.body.text

    buttons = []
    lines = text.split("\n")

    for line in lines:
        try:
            btn_text, url = line.split(" - ")
            buttons.append({
                "text": btn_text.strip(),
                "url": url.strip()
            })
        except:
            await event.message.answer(
                text="Неверный формат кнопок\n\nПример:\nКупить - https://site.com"
            )
            return

    await context.update_data(buttons=buttons)

    await context.set_state(AddMailingState.send_at)

    await event.message.answer(
        text="Введите время отправки (YYYY-MM-DD HH:MM)",
        attachments=[get_back_keyboard("mailing_buttons")]
    )


async def skip_mailing_buttons(event: MessageCallback, context: MemoryContext):

    await context.update_data(buttons=[])

    await context.set_state(AddMailingState.send_at)

    await event.message.edit(
        text="Введите время отправки (YYYY-MM-DD HH:MM)",
        attachments=[get_back_keyboard("mailing_buttons")]
    )


async def back_to_enter_mailing_buttons(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMailingState.buttons)

    await event.message.edit(
        text=(
            "Введите кнопки в формате:\n\n"
            "Текст - https://site.com\n"
            "Текст2 - https://site2.com"
        ),
        attachments=[get_mailing_buttons_keyboard()]
    )


async def enter_mailing_send_time(event: MessageCreated, context: MemoryContext):
    try:

        send_at = datetime.strptime(
            event.message.body.text,
            "%Y-%m-%d %H:%M"
        )

        data = await context.get_data()

        mailing = await mailings_repo.add_one(
            title=data["title"],
            text=data["text"],
            marathon_id=data["marathon_id"],
            send_at=send_at
        )

        for image in data["images"]:
            await mailing_images_repo.add_one(
                mailing_id=mailing.id,
                photo_id=image["photo_id"],
                photo_token=image["photo_token"],
                photo_url=image["photo_url"]
            )

        for button in data["buttons"]:
            await mailing_buttons_repo.add_one(
                mailing_id=mailing.id,
                text=button["text"],
                url=button["url"]
            )

        await context.clear()

        await event.message.answer(
            text=f"Рассылка успешно создана"
        )

        mailings = await mailings_repo.find_all()

        await event.message.answer(
            text="📨 Рассылки",
            attachments=[get_mailings_keyboard(mailings)]
        )

    except ValueError:

        await event.message.answer(
            text="Неверный формат времени\nИспользуйте YYYY-MM-DD HH:MM"
        )


def register_handlers(dp: Dispatcher):

    dp.message_callback.register(
        add_mailing,
        F.callback.payload == "add_mailing"
    )

    dp.message_created.register(
        enter_mailing_title,
        AddMailingState.title
    )

    dp.message_created.register(
        enter_mailing_message,
        AddMailingState.message
    )

    dp.message_callback.register(
        choose_mailing_marathon,
        F.callback.payload.startswith("mailing_marathon")
    )

    dp.message_callback.register(
        choose_mailing_marathon,
        F.callback.payload == "mailing_marathon_skip"
    )

    dp.message_created.register(
        enter_mailing_buttons,
        AddMailingState.buttons
    )

    dp.message_callback.register(
        skip_mailing_buttons,
        F.callback.payload == "mailing_buttons_skip"
    )

    dp.message_created.register(
        enter_mailing_send_time,
        AddMailingState.send_at
    )

    dp.message_callback.register(
        back_to_enter_mailing_title,
        F.callback.payload == "back:mailing_title"
    )

    dp.message_callback.register(
        back_to_enter_mailing_message,
        F.callback.payload == "back:mailing_message"
    )

    dp.message_callback.register(
        back_to_enter_mailing_marathon,
        F.callback.payload == "back:mailing_marathon"
    )

    dp.message_callback.register(
        back_to_enter_mailing_buttons,
        F.callback.payload == "back:mailing_buttons"
    )
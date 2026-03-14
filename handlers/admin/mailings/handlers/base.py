from maxapi import Dispatcher, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext

from models.mailings import Mailing
from repositories.mailings import MailingsRepository

from handlers.admin.mailings.keyboards import (
    get_mailings_keyboard,
    get_mailing_keyboard,
    get_mailing_preview_keyboard,
)

mailings_repo = MailingsRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


async def start_admin_mailings(event: MessageCallback, context: MemoryContext):
    await context.clear()

    mailings = await mailings_repo.find_all()

    await event.message.edit(
        text="📨 Рассылки",
        attachments=[get_mailings_keyboard(mailings)]
    )


async def back_to_mailings(event: MessageCallback, context: MemoryContext):
    await context.clear()

    mailings = await mailings_repo.find_all()

    await event.message.edit(
        text="📨 Рассылки",
        attachments=[get_mailings_keyboard(mailings)]
    )


from maxapi.types import Attachment, PhotoAttachmentPayload

from __init__ import bot


async def mailing(event: MessageCallback):
    mailing_id = get_id(event.callback.payload)

    mailing: Mailing = await mailings_repo.get_full(id=mailing_id)

    attachments = []

    for image in mailing.images:
        attachments.append(
            Attachment(
                type="image",
                payload=PhotoAttachmentPayload(
                    photo_id=image.photo_id,
                    token=image.photo_token,
                    url=image.photo_url,
                ),
                bot=bot
            )
        )

    if mailing.buttons != []:
        attachments.append(get_mailing_preview_keyboard(mailing.buttons))

    await event.message.answer(
        text=mailing.text,
        attachments=attachments
    )

    await event.message.answer(
        text=f"📨 Рассылка\n\nНазвание: {mailing.title}\n\nМарафон: {mailing.marathon_id if mailing.marathon_id else 'Не указано'}",
        attachments=[get_mailing_keyboard(mailing_id)]
    )


async def delete_mailing(event: MessageCallback):
    mailing_id = get_id(event.callback.payload)

    await mailings_repo.delete_one(id=mailing_id)

    mailings = await mailings_repo.find_all()

    await event.message.edit(
        text="📨 Рассылки",
        attachments=[get_mailings_keyboard(mailings)]
    )


def register_handlers(dp: Dispatcher):

    dp.message_callback.register(start_admin_mailings, F.callback.payload == "mailings")
    dp.message_callback.register(back_to_mailings, F.callback.payload == "back:mailings")

    dp.message_callback.register(mailing, F.callback.payload.startswith("mailing:"))

    dp.message_callback.register(delete_mailing, F.callback.payload.startswith("delete_mailing:"))
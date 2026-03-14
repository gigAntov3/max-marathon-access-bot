from maxapi import Dispatcher, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext

from models.marathons import Marathon
from repositories.marathons import MarathonsRepository

from handlers.admin.marathons.keyboards import (
    get_marathons_keyboard,
    get_marathon_keyboard,
)

marathons_repo = MarathonsRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


async def start_admin_marathons(event: MessageCallback, context: MemoryContext):
    await context.clear()

    marathons = await marathons_repo.find_all()

    await event.message.edit(
        text="Марафоны",
        attachments=[get_marathons_keyboard(marathons)]
    )


async def back_to_marathons(event: MessageCallback, context: MemoryContext):
    await context.clear()

    marathons = await marathons_repo.find_all()

    await event.message.edit(
        text="Марафоны",
        attachments=[get_marathons_keyboard(marathons)]
    )



from maxapi.types import Attachment, PhotoAttachmentRequestPayload, PhotoAttachmentPayload
# from maxapi.types.

from __init__ import bot



async def marathon(event: MessageCallback):
    marathon_id = get_id(event.callback.payload)

    marathon: Marathon = await marathons_repo.get_one(id=marathon_id)

    photo = None
    if marathon.photo_id:
        photo = Attachment(
            type="image",
            payload=PhotoAttachmentPayload(
                photo_id=marathon.photo_id,
                token=marathon.photo_token,
                url=marathon.photo_url,
            ),
            bot=bot
        )


    start_date = marathon.start_date.strftime("%d.%m.%Y")
    end_date = marathon.end_date.strftime("%d.%m.%Y")

    type_text = "Индивидуальный" if marathon.type == "individual" else "Групповой"

    text = (
        f"🏃 {marathon.name}\n\n"
        f"📝 {marathon.description}\n\n"
        f"📊 Тип: {type_text}\n"
        f"📅 {start_date} - {end_date}\n\n"
        f"💰 Цена: {marathon.price} ₽"
    )

    if photo:
        await event.message.edit(
            text=text,
            attachments=[photo, get_marathon_keyboard(marathon_id)]
        )
    else:
        await event.message.edit(
            text=text,
            attachments=[get_marathon_keyboard(marathon_id)]
        )


async def delete_marathon(event: MessageCallback):
    marathon_id = get_id(event.callback.payload)

    await marathons_repo.delete_one(id=marathon_id)

    marathons = await marathons_repo.find_all()

    await event.message.edit(
        text="Марафоны",
        attachments=[get_marathons_keyboard(marathons)]
    )


async def set_marathons_offset(event: MessageCallback):
    offset = int(event.callback.payload.split(":")[1])

    if offset < 0:
        offset = 0

    marathons = await marathons_repo.find_all(offset=offset, limit=10)

    await event.message.edit(
        text="Марафоны",
        attachments=[get_marathons_keyboard(marathons, offset)]
    )


def register_handlers(dp: Dispatcher):

    dp.message_callback.register(start_admin_marathons, F.callback.payload == "marathons")
    dp.message_callback.register(back_to_marathons, F.callback.payload == "back:marathons")

    dp.message_callback.register(marathon, F.callback.payload.startswith("marathon:"))
    dp.message_callback.register(delete_marathon, F.callback.payload.startswith("delete_marathon:"))
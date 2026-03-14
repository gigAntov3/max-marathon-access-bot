from maxapi import Dispatcher, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext
from maxapi.types import Attachment, PhotoAttachmentPayload

from models.marathons import Marathon
from repositories.marathons import MarathonsRepository
from repositories.promocodes import PromocodesRepository

from handlers.clients.marathons.keyboards import (
    get_marathons_keyboard as get_client_marathons_keyboard,
)
from handlers.admin.marathons.keyboards import (
    get_marathons_keyboard as get_admin_marathons_keyboard
)
from handlers.admin.promocodes.keyboards import (
    get_promocodes_keyboard
)

from __init__ import bot


marathons_repo = MarathonsRepository()
promocodes_repo = PromocodesRepository()



async def set_marathons_offset(event: MessageCallback, context: MemoryContext):
    offset = int(event.callback.payload.split(":")[2])

    if offset < 0:
        offset = 0


    if "client_marathons:" in event.callback.payload:
        marathons = await marathons_repo.find_all(offset=offset, limit=10)

        await event.message.edit(
            text="Марафоны",
            attachments=[get_client_marathons_keyboard(marathons, offset)]
        )

    elif "admin_marathons:" in event.callback.payload:
        marathons = await marathons_repo.find_all(offset=offset, limit=10)

        await event.message.edit(
            text="Марафоны",
            attachments=[get_admin_marathons_keyboard(marathons, offset)]
        )

    elif "promocodes:" in event.callback.payload:
        promocodes = await promocodes_repo.find_all(offset=offset, limit=10)

        await event.message.edit(
            text="Промокоды",
            attachments=[get_promocodes_keyboard(promocodes, offset)]
        )


def register_handlers(dp: Dispatcher):
    dp.message_callback.register(
        set_marathons_offset,
        F.callback.payload.startswith("offset:")
    )
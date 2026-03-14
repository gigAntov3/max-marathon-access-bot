from maxapi import Dispatcher, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext
from maxapi.types import Attachment, PhotoAttachmentPayload

from models.marathons import Marathon
from repositories.marathons import MarathonsRepository
from repositories.promocodes import PromocodesRepository
from repositories.guides import GuidesRepository

from handlers.clients.marathons.keyboards import (
    get_marathons_keyboard as get_client_marathons_keyboard,
)
from handlers.admin.marathons.keyboards import (
    get_marathons_keyboard as get_admin_marathons_keyboard
)
from handlers.admin.promocodes.keyboards import (
    get_promocodes_keyboard
)
from handlers.admin.guides.keyboards import (
    get_guides_keyboard as get_admin_guides_keyboard
)
from handlers.clients.guides.keyboards import (
    get_guides_keyboard as get_client_guides_keyboard
)

from __init__ import bot


marathons_repo = MarathonsRepository()
promocodes_repo = PromocodesRepository()
guides_repo = GuidesRepository()


async def set_marathons_offset(event: MessageCallback, context: MemoryContext):
    print(11111111)
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

    elif "mailing_marathons:" in event.callback.payload:
        marathons = await marathons_repo.find_all(offset=offset, limit=10)

        from handlers.admin.mailings.keyboards import (
            get_mailing_marathons_keyboard
        )

        await event.message.edit(
            text="Выберите марафон для рассылки",
            attachments=[get_mailing_marathons_keyboard(marathons, offset)]
        )

    elif "admin_guides:" in event.callback.payload:
        guides = await guides_repo.find_all(offset=offset, limit=10)
    
        await event.message.edit(
            text="📚 Бесплатные гайды",
            attachments=[get_admin_guides_keyboard(guides, offset)]
        )

    elif "client_guides:" in event.callback.payload:
        guides = await guides_repo.find_all(offset=offset, limit=10)
    
        await event.message.edit(
            text="📚 Бесплатные гайды",
            attachments=[get_client_guides_keyboard(guides, offset)]
        )


def register_handlers(dp: Dispatcher):
    dp.message_callback.register(
        set_marathons_offset,
        F.callback.payload.startswith("offset:")
    )
from maxapi import Dispatcher, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext

from models.guides import Guide
from repositories.guides import GuidesRepository

from .keyboards import (
    get_guides_keyboard,
    get_guide_keyboard,
)


guides_repo = GuidesRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


async def start_clients_guides(event: MessageCallback, context: MemoryContext):
    print(44444444444444)
    await context.clear()
    
    guides = await guides_repo.find_all()
    
    await event.message.edit(
        text="📚 Бесплатные гайды",
        attachments=[get_guides_keyboard(guides)]
    )


async def view_guide(event: MessageCallback):
    guide_id = get_id(event.callback.payload)
    
    guide: Guide = await guides_repo.get_one(id=guide_id)
    
    text = (
        f"📚 {guide.title}\n\n"
        f"📄 Описание:\n{guide.description}\n\n"
        f"📅 Добавлен: {guide.created_at.strftime('%d.%m.%Y')}"
    )
    
    await event.message.edit(
        text=text,
        attachments=[get_guide_keyboard(guide.link)]
    )


def register_handlers(dp: Dispatcher):
    dp.message_callback.register(start_clients_guides, F.callback.payload == "client_guides")
    dp.message_callback.register(start_clients_guides, F.callback.payload == "back:client_guides")
    
    dp.message_callback.register(view_guide, F.callback.payload.startswith("client_guide:"))
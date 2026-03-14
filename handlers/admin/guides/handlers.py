from datetime import datetime

from maxapi import Dispatcher, F
from maxapi.types import MessageCallback, MessageCreated
from maxapi.context import MemoryContext

from models.guides import Guide
from repositories.guides import GuidesRepository

from .states import AddGuideState, EditGuideState
from .keyboards import (
    get_guides_keyboard,
    get_guide_keyboard,
    get_edit_guide_keyboard,
    get_back_edit_guide_keyboard,
    get_back_guides_keyboard,
)

from handlers.base.keyboards import get_back_keyboard


guides_repo = GuidesRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


# =========================
# GUIDES LIST
# =========================

async def start_admin_guides(event: MessageCallback, context: MemoryContext):
    await context.clear()
    
    guides = await guides_repo.find_all()
    
    await event.message.edit(
        text="📚 Бесплатные гайды",
        attachments=[get_guides_keyboard(guides)]
    )


# =========================
# VIEW GUIDE
# =========================

async def view_guide(event: MessageCallback):
    guide_id = get_id(event.callback.payload)
    
    guide: Guide = await guides_repo.get_one(id=guide_id)
    
    text = (
        f"📚 **{guide.title}**\n\n"
        f"📄 **Описание:**\n{guide.description}\n\n"
        f"🔗 **Ссылка:**\n{guide.link}\n\n"
        f"📅 Добавлен: {guide.created_at.strftime('%d.%m.%Y')}"
    )
    
    await event.message.edit(
        text=text,
        attachments=[get_guide_keyboard(guide_id)]
    )


# =========================
# ADD GUIDE
# =========================

async def add_guide(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddGuideState.title)
    
    await event.message.edit(
        text="Введите название гайда",
        attachments=[get_back_guides_keyboard()]
    )


async def enter_guide_title(event: MessageCreated, context: MemoryContext):
    title = event.message.body.text
    
    existing = await guides_repo.find_one(title=title)
    
    if existing:
        await event.message.answer(
            text="Гайд с таким названием уже существует!"
        )
        return
    
    await context.update_data(title=title)
    await context.set_state(AddGuideState.description)
    
    await event.message.answer(
        text="Введите описание гайда",
        attachments=[get_back_keyboard("guides_title")]
    )


async def enter_guide_description(event: MessageCreated, context: MemoryContext):
    description = event.message.body.text
    
    await context.update_data(description=description)
    await context.set_state(AddGuideState.link)
    
    await event.message.answer(
        text="Введите ссылку на гайд",
        attachments=[get_back_keyboard("guides_description")]
    )


async def enter_guide_link(event: MessageCreated, context: MemoryContext):
    link = event.message.body.text
    
    data = await context.get_data()
    
    guide = await guides_repo.add_one(
        title=data["title"],
        description=data["description"],
        link=link
    )
    
    await context.clear()
    
    guides = await guides_repo.find_all()
    
    await event.message.answer(
        text=f"✅ Гайд '{guide.title}' успешно создан",
        attachments=[get_guides_keyboard(guides)]
    )


# =========================
# EDIT GUIDE
# =========================

async def edit_guide(event: MessageCallback):
    guide_id = get_id(event.callback.payload)
    
    await event.message.edit(
        text="Что хотите изменить?",
        attachments=[get_edit_guide_keyboard(guide_id)]
    )


async def edit_title(event: MessageCallback, context: MemoryContext):
    guide_id = get_id(event.callback.payload)
    
    await context.update_data(id=guide_id)
    await context.set_state(EditGuideState.title)
    
    await event.message.edit(
        text="Введите новое название гайда",
        attachments=[get_back_edit_guide_keyboard(guide_id)]
    )


async def update_title(event: MessageCreated, context: MemoryContext):
    title = event.message.body.text
    
    data = await context.get_data()
    
    await guides_repo.update_one(
        id=data["id"],
        title=title
    )
    
    await context.clear()
    
    guide_id = data["id"]
    guide = await guides_repo.get_one(id=guide_id)
    
    await event.message.answer("✅ Название обновлено")
    
    text = (
        f"📚 **{guide.title}**\n\n"
        f"📄 **Описание:**\n{guide.description}\n\n"
        f"🔗 **Ссылка:**\n{guide.link}\n\n"
        f"📅 Добавлен: {guide.created_at.strftime('%d.%m.%Y')}"
    )
    
    await event.message.answer(
        text=text,
        attachments=[get_edit_guide_keyboard(guide_id)]
    )


async def edit_description(event: MessageCallback, context: MemoryContext):
    guide_id = get_id(event.callback.payload)
    
    await context.update_data(id=guide_id)
    await context.set_state(EditGuideState.description)
    
    await event.message.edit(
        text="Введите новое описание гайда",
        attachments=[get_back_edit_guide_keyboard(guide_id)]
    )


async def update_description(event: MessageCreated, context: MemoryContext):
    description = event.message.body.text
    
    data = await context.get_data()
    
    await guides_repo.update_one(
        id=data["id"],
        description=description
    )
    
    await context.clear()
    
    guide_id = data["id"]
    guide = await guides_repo.get_one(id=guide_id)
    
    await event.message.answer("✅ Описание обновлено")
    
    text = (
        f"📚 {guide.title}\n\n"
        f"📄 Описание:\n{guide.description}\n\n"
        f"🔗 Ссылка:\n{guide.link}\n\n"
        f"📅 Добавлен: {guide.created_at.strftime('%d.%m.%Y')}"
    )
    
    await event.message.answer(
        text=text,
        attachments=[get_edit_guide_keyboard(guide_id)]
    )


async def edit_link(event: MessageCallback, context: MemoryContext):
    guide_id = get_id(event.callback.payload)
    
    await context.update_data(id=guide_id)
    await context.set_state(EditGuideState.link)
    
    await event.message.edit(
        text="Введите новую ссылку на гайд",
        attachments=[get_back_edit_guide_keyboard(guide_id)]
    )


async def update_link(event: MessageCreated, context: MemoryContext):
    link = event.message.body.text
    
    data = await context.get_data()
    
    await guides_repo.update_one(
        id=data["id"],
        link=link
    )
    
    await context.clear()
    
    guide_id = data["id"]
    guide = await guides_repo.get_one(id=guide_id)
    
    await event.message.answer("✅ Ссылка обновлена")
    
    text = (
        f"📚 **{guide.title}**\n\n"
        f"📄 **Описание:**\n{guide.description}\n\n"
        f"🔗 **Ссылка:**\n{guide.link}\n\n"
        f"📅 Добавлен: {guide.created_at.strftime('%d.%m.%Y')}"
    )
    
    await event.message.answer(
        text=text,
        attachments=[get_edit_guide_keyboard(guide_id)]
    )


async def delete_guide(event: MessageCallback):
    guide_id = get_id(event.callback.payload)
    
    guide = await guides_repo.get_one(id=guide_id)
    await guides_repo.delete_one(id=guide_id)
    
    guides = await guides_repo.find_all()
    
    await event.message.edit(
        text=f"✅ Гайд '{guide.title}' удален",
        attachments=[get_guides_keyboard(guides)]
    )


def register_handlers(dp: Dispatcher):
    # Навигация
    dp.message_callback.register(start_admin_guides, F.callback.payload == "guides")
    dp.message_callback.register(start_admin_guides, F.callback.payload == "back:guides")
    
    # Просмотр гайдов
    dp.message_callback.register(view_guide, F.callback.payload.startswith("guide:"))
    
    # Добавление гайда
    dp.message_callback.register(add_guide, F.callback.payload == "add_guide")
    dp.message_created.register(enter_guide_title, AddGuideState.title)
    dp.message_created.register(enter_guide_description, AddGuideState.description)
    dp.message_created.register(enter_guide_link, AddGuideState.link)
    
    # Редактирование гайда
    dp.message_callback.register(edit_guide, F.callback.payload.startswith("edit_guide:"))
    dp.message_callback.register(edit_title, F.callback.payload.startswith("guide_title:"))
    dp.message_callback.register(edit_description, F.callback.payload.startswith("guide_description:"))
    dp.message_callback.register(edit_link, F.callback.payload.startswith("guide_link:"))
    
    dp.message_created.register(update_title, EditGuideState.title)
    dp.message_created.register(update_description, EditGuideState.description)
    dp.message_created.register(update_link, EditGuideState.link)
    
    # Удаление гайда
    dp.message_callback.register(delete_guide, F.callback.payload.startswith("delete_guide:"))
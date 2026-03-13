from datetime import datetime

from maxapi import Dispatcher, F
from maxapi.types import MessageCallback, MessageCreated
from maxapi.context import MemoryContext

from models.marathons import Marathon
from repositories.marathons import MarathonsRepository

from handlers.admin.marathons.states import EditMarathonState
from handlers.admin.marathons.keyboards import (
    get_edit_marathon_keyboard,
    get_back_edit_marathon_keyboard,
)

marathons_repo = MarathonsRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


async def edit_marathon(event: MessageCallback):
    marathon_id = get_id(event.callback.payload)

    await event.message.edit(
        text="Что хотите изменить?",
        attachments=[get_edit_marathon_keyboard(marathon_id)]
    )


async def edit_marathon_name(event: MessageCallback, context: MemoryContext):
    marathon_id = get_id(event.callback.payload)

    await context.update_data(id=marathon_id)
    await context.set_state(EditMarathonState.name)

    await event.message.edit(
        text="Введите новое название",
        attachments=[get_back_edit_marathon_keyboard(marathon_id)]
    )


async def update_marathon_name(event: MessageCreated, context: MemoryContext):
    data = await context.get_data()

    await marathons_repo.update_one(
        id=data["id"],
        name=event.message.body.text
    )

    marathon = await marathons_repo.get_one(id=data["id"])

    await context.clear()

    await event.message.answer(
        text=f"Название обновлено",
    )
    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_marathon_keyboard(marathon.id)]
    )


async def edit_marathon_description(event: MessageCallback, context: MemoryContext):
    marathon_id = get_id(event.callback.payload)

    await context.update_data(id=marathon_id)
    await context.set_state(EditMarathonState.description)

    await event.message.edit(
        text="Введите новое описание",
        attachments=[get_back_edit_marathon_keyboard(marathon_id)]
    )


async def update_marathon_description(event: MessageCreated, context: MemoryContext):
    data = await context.get_data()

    await marathons_repo.update_one(
        id=data["id"],
        description=event.message.body.text
    )

    marathon = await marathons_repo.get_one(id=data["id"])

    await context.clear()

    await event.message.answer(
        text=f"Описание обновлено",
    )
    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_marathon_keyboard(marathon.id)]
    )


async def edit_marathon_start(event: MessageCallback, context: MemoryContext):
    marathon_id = get_id(event.callback.payload)

    await context.update_data(id=marathon_id)
    await context.set_state(EditMarathonState.start_date)

    await event.message.edit(
        text="Введите новую дату начала (YYYY-MM-DD)",
        attachments=[get_back_edit_marathon_keyboard(marathon_id)]
    )


async def update_marathon_start(event: MessageCreated, context: MemoryContext):
    start_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

    data = await context.get_data()

    await marathons_repo.update_one(
        id=data["id"],
        start_date=start_date
    )

    marathon = await marathons_repo.get_one(id=data["id"])

    await context.clear()

    await event.message.answer(
        text="Дата начала обновлена",
    )
    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_marathon_keyboard(marathon.id)]
    )


async def edit_marathon_end(event: MessageCallback, context: MemoryContext):
    marathon_id = get_id(event.callback.payload)

    await context.update_data(id=marathon_id)
    await context.set_state(EditMarathonState.end_date)

    await event.message.edit(
        text="Введите новую дату окончания (YYYY-MM-DD)",
        attachments=[get_back_edit_marathon_keyboard(marathon_id)]
    )


async def update_marathon_end(event: MessageCreated, context: MemoryContext):
    end_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

    data = await context.get_data()

    await marathons_repo.update_one(
        id=data["id"],
        end_date=end_date
    )

    marathon = await marathons_repo.get_one(id=data["id"])

    await context.clear()

    await event.message.answer(
        text="Дата окончания обновлена",
    )
    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_marathon_keyboard(marathon.id)]
    )


async def edit_marathon_price(event: MessageCallback, context: MemoryContext):
    marathon_id = get_id(event.callback.payload)

    await context.update_data(id=marathon_id)
    await context.set_state(EditMarathonState.price)

    await event.message.edit(
        text="Введите новую цену",
        attachments=[get_back_edit_marathon_keyboard(marathon_id)]
    )


async def update_marathon_price(event: MessageCreated, context: MemoryContext):
    price = float(event.message.body.text)

    data = await context.get_data()

    await marathons_repo.update_one(
        id=data["id"],
        price=price
    )

    marathon = await marathons_repo.get_one(id=data["id"])

    await context.clear()

    await event.message.answer(
        text=f"Цена обновлена",
    )
    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_marathon_keyboard(marathon.id)]
    )


def register_handlers(dp: Dispatcher):
    dp.message_callback.register(edit_marathon, F.callback.payload.startswith("edit_marathon:"))

    dp.message_callback.register(edit_marathon_name, F.callback.payload.startswith("edit_marathon_name:"))
    dp.message_created.register(update_marathon_name, EditMarathonState.name)

    dp.message_callback.register(edit_marathon_description, F.callback.payload.startswith("edit_marathon_description:"))
    dp.message_created.register(update_marathon_description, EditMarathonState.description)

    dp.message_callback.register(edit_marathon_start, F.callback.payload.startswith("edit_marathon_start:"))
    dp.message_created.register(update_marathon_start, EditMarathonState.start_date)

    dp.message_callback.register(edit_marathon_end, F.callback.payload.startswith("edit_marathon_end:"))
    dp.message_created.register(update_marathon_end, EditMarathonState.end_date)

    dp.message_callback.register(edit_marathon_price, F.callback.payload.startswith("edit_marathon_price:"))
    dp.message_created.register(update_marathon_price, EditMarathonState.price)
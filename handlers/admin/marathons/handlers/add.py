from datetime import datetime

from maxapi import Dispatcher, F
from maxapi.types import MessageCallback, MessageCreated
from maxapi.context import MemoryContext

from models.marathons import Marathon
from repositories.marathons import MarathonsRepository

from handlers.admin.marathons.states import AddMarathonState
from handlers.admin.marathons.keyboards import (
    get_marathons_keyboard,
    get_marathon_type_keyboard,
)
from handlers.base.keyboards import get_back_keyboard


marathons_repo = MarathonsRepository()


async def add_marathon(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMarathonState.name)

    await event.message.edit(
        text="Введите название марафона",
        attachments=[get_back_keyboard("marathons")]
    )


async def enter_marathon_name(event: MessageCreated, context: MemoryContext):
    await context.update_data(name=event.message.body.text)
    await context.set_state(AddMarathonState.description)

    await event.message.answer(
        text="Введите описание марафона",
        attachments=[get_back_keyboard("marathons_name")]
    )


async def back_to_enter_marathon_name(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMarathonState.name)

    await event.message.edit(
        text="Введите название марафона",
        attachments=[get_back_keyboard("marathons")]
    )


async def enter_marathon_description(event: MessageCreated, context: MemoryContext):
    await context.update_data(description=event.message.body.text)
    await context.set_state(AddMarathonState.photo)

    await event.message.answer(
        text="Отправьте фотографию марафона",
        attachments=[get_back_keyboard("marathons_description")]
    )


async def back_to_enter_marathon_description(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMarathonState.description)

    await event.message.edit(
        text="Введите описание марафона",
        attachments=[get_back_keyboard("marathons_name")]
    )


async def enter_marathon_photo(event: MessageCreated, context: MemoryContext):
    if not event.message.body.attachments:
        await event.message.answer(
            text="Пожалуйста отправьте фотографию"
        )
        return

    photo = event.message.body.attachments[0]

    if photo.type != "image":
        await event.message.answer(
            text="Нужно отправить именно фотографию"
        )
        return

    await context.update_data(photo_id=photo.payload.photo_id)
    await context.update_data(photo_token=photo.payload.token)
    await context.update_data(photo_url=photo.payload.url)

    await context.set_state(AddMarathonState.type)

    await event.message.answer(
        text="Выберите тип марафона",
        attachments=[get_marathon_type_keyboard()]
    )


async def back_to_enter_marathon_photo(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMarathonState.photo)

    await event.message.edit(
        text="Отправьте фотографию марафона",
        attachments=[get_back_keyboard("marathons_description")]
    )


async def choose_marathon_type(event: MessageCallback, context: MemoryContext):
    marathon_type = event.callback.payload.split(":")[1]

    await context.update_data(type=marathon_type)
    await context.set_state(AddMarathonState.start_date)

    await event.message.edit(
        text="Введите дату начала марафона (YYYY-MM-DD)",
        attachments=[get_back_keyboard("marathons_type")]
    )


async def back_to_enter_marathon_type(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMarathonState.type)

    await event.message.edit(
        text="Выберите тип марафона",
        attachments=[get_marathon_type_keyboard()]
    )


async def enter_marathon_start_date(event: MessageCreated, context: MemoryContext):
    try:
        start_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

        await context.update_data(start_date=start_date)
        await context.set_state(AddMarathonState.end_date)

        await event.message.answer(
            text="Введите дату окончания марафона (YYYY-MM-DD)",
            attachments=[get_back_keyboard("marathons_start_date")]
        )

    except ValueError:
        await event.message.edit(
            text="Неверный формат даты. Используйте YYYY-MM-DD",
            attachments=[get_back_keyboard("marathons_start_date")]
        )


async def back_to_enter_marathon_start_date(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMarathonState.start_date)

    await event.message.edit(
        text="Введите дату начала марафона (YYYY-MM-DD)",
        attachments=[get_back_keyboard("marathons_type")]
    )


async def enter_marathon_end_date(event: MessageCreated, context: MemoryContext):
    try:
        end_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

        data = await context.get_data()

        if end_date < data["start_date"]:
            await event.message.edit(
                text="Дата окончания не может быть раньше даты начала"
            )
            return

        await context.update_data(end_date=end_date)
        await context.set_state(AddMarathonState.price)

        await event.message.answer(
            text="Введите цену марафона",
            attachments=[get_back_keyboard("marathons_end_date")]
        )

    except ValueError:
        await event.message.edit(
            text="Неверный формат даты. Используйте YYYY-MM-DD"
        )


async def back_to_enter_marathon_end_date(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddMarathonState.end_date)

    await event.message.edit(
        text="Введите дату окончания марафона (YYYY-MM-DD)",
        attachments=[get_back_keyboard("marathons_start_date")]
    )


async def enter_marathon_price(event: MessageCreated, context: MemoryContext):
    try:
        price = float(event.message.body.text)

        data = await context.get_data()

        marathon: Marathon = await marathons_repo.add_one(
            name=data["name"],
            description=data["description"],
            photo_id=data["photo_id"],
            photo_token=data["photo_token"],
            photo_url=data["photo_url"],
            type=data["type"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            price=price
        )

        await context.clear()

        marathons = await marathons_repo.find_all()

        await event.message.answer(
            text=f"Марафон '{marathon.name}' успешно создан!",
            attachments=[get_marathons_keyboard(marathons)]
        )

    except ValueError:
        await event.message.edit(
            text="Цена должна быть числом"
        )


def register_handlers(dp: Dispatcher):
    dp.message_callback.register(add_marathon, F.callback.payload == "add_marathon")

    dp.message_created.register(enter_marathon_name, AddMarathonState.name)
    dp.message_callback.register(back_to_enter_marathon_name, F.callback.payload == "back:marathons_name")
    dp.message_created.register(enter_marathon_description, AddMarathonState.description)
    dp.message_callback.register(back_to_enter_marathon_description, F.callback.payload == "back:marathons_description")

    dp.message_created.register(enter_marathon_photo, AddMarathonState.photo)
    dp.message_callback.register(back_to_enter_marathon_photo, F.callback.payload == "back:marathons_photo")

    dp.message_callback.register(choose_marathon_type, F.callback.payload.startswith("marathon_type:"))
    dp.message_callback.register(back_to_enter_marathon_type, F.callback.payload == "back:marathons_type")
    dp.message_created.register(enter_marathon_start_date, AddMarathonState.start_date)
    dp.message_callback.register(back_to_enter_marathon_start_date, F.callback.payload == "back:marathons_start_date")
    dp.message_created.register(enter_marathon_end_date, AddMarathonState.end_date)
    dp.message_callback.register(back_to_enter_marathon_end_date, F.callback.payload == "back:marathons_end_date")
    dp.message_created.register(enter_marathon_price, AddMarathonState.price)
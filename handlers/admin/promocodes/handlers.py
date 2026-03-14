from datetime import datetime

from maxapi import Dispatcher, F
from maxapi.types import MessageCallback, MessageCreated
from maxapi.context import MemoryContext

from models.promocodes import Promocode
from repositories.promocodes import PromocodesRepository

from .states import AddPromoCodeState, EditPromoCodeState
from .keyboards import (
    get_promocodes_keyboard,
    get_promocode_keyboard,
    get_edit_promocode_keyboard,
    get_back_edit_promocode_keyboard,
)

from handlers.base.keyboards import get_back_keyboard


promocodes_repo = PromocodesRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


# =========================
# PROMOCODES LIST
# =========================

async def start_admin_promocodes(event: MessageCallback, context: MemoryContext):
    await context.clear()

    promocodes = await promocodes_repo.find_all()

    await event.message.edit(
        text="Промокоды",
        attachments=[get_promocodes_keyboard(promocodes)]
    )


async def set_promocodes_offset(event: MessageCallback):
    offset = int(event.callback.payload.split(":")[1])
    if offset < 0:
        offset = 0

    promocodes = await promocodes_repo.find_all(offset=offset, limit=10)

    await event.message.edit(
        text="Промокоды",
        attachments=[get_promocodes_keyboard(promocodes, offset)]
    )


# =========================
# VIEW PROMOCODE
# =========================

async def promocode(event: MessageCallback):
    promocode_id = get_id(event.callback.payload)

    promocode: Promocode = await promocodes_repo.get_one(id=promocode_id)

    start_date = promocode.start_date.strftime("%d.%m.%Y")
    end_date = promocode.end_date.strftime("%d.%m.%Y")

    text = (
        f"🎟 Промокод: {promocode.code}\n\n"
        f"🔢 Использований: {promocode.uses}/{promocode.max_uses}\n"
        f"💸 Скидка: {promocode.discount}%\n\n"
        f"📅 Действует с: {start_date}\n"
        f"📅 Действует до: {end_date}"
    )

    await event.message.edit(
        text=text,
        attachments=[get_promocode_keyboard(promocode_id)]
    )


# =========================
# ADD PROMOCODE
# =========================

async def add_promocode(event: MessageCallback, context: MemoryContext):
    await context.set_state(AddPromoCodeState.code)

    await event.message.edit(
        text="Пришлите код промокода",
        attachments=[get_back_keyboard("promocodes")]
    )


async def enter_promocode_code(event: MessageCreated, context: MemoryContext):
    existing = await promocodes_repo.find_one(code=event.message.body.text)

    if existing:
        await event.message.answer(
            text="Промокод с таким кодом уже существует!"
        )
        return

    await context.update_data(code=event.message.body.text)
    await context.set_state(AddPromoCodeState.max_uses)

    await event.message.answer(
        text="Введите максимальное количество использований",
        attachments=[get_back_keyboard("promocodes_code")]
    )


async def enter_promocode_max_uses(event: MessageCreated, context: MemoryContext):
    try:
        max_uses = int(event.message.body.text)

        if max_uses < 1:
            raise ValueError

        await context.update_data(max_uses=max_uses)
        await context.set_state(AddPromoCodeState.discount)

        await event.message.answer(
            text="Введите скидку в процентах",
            attachments=[get_back_keyboard("promocodes_max_uses")]
        )

    except ValueError:
        await event.message.answer(
            text="Введите корректное число",
            attachments=[get_back_keyboard("promocodes_max_uses")]
        )


async def enter_promocode_discount(event: MessageCreated, context: MemoryContext):
    try:
        discount = float(event.message.body.text)

        if discount <= 0 or discount > 100:
            raise ValueError

        await context.update_data(discount=discount)
        await context.set_state(AddPromoCodeState.start_date)

        await event.message.answer(
            text="Введите дату начала (YYYY-MM-DD)",
            attachments=[get_back_keyboard("promocodes_discount")]
        )

    except ValueError:
        await event.message.answer(
            text="Введите число от 1 до 100",
            attachments=[get_back_keyboard("promocodes_discount")]
        )


async def enter_promocode_start_date(event: MessageCreated, context: MemoryContext):
    try:
        start_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

        await context.update_data(start_date=start_date)
        await context.set_state(AddPromoCodeState.end_date)

        await event.message.answer(
            text="Введите дату окончания (YYYY-MM-DD)",
            attachments=[get_back_keyboard("promocodes_start_date")]
        )

    except ValueError:
        await event.message.answer(
            text="Неверный формат даты",
            attachments=[get_back_keyboard("promocodes_start_date")]
        )


async def enter_promocode_end_date(event: MessageCreated, context: MemoryContext):
    try:
        end_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

        data = await context.get_data()

        if end_date < data["start_date"]:
            await event.message.answer(
                text="Дата окончания не может быть раньше даты начала"
            )
            return

        promocode = await promocodes_repo.add_one(
            code=data["code"],
            max_uses=data["max_uses"],
            discount=data["discount"],
            start_date=data["start_date"],
            end_date=end_date
        )

        await context.clear()

        promocodes = await promocodes_repo.find_all()

        await event.message.answer(
            text=f"Промокод '{promocode.code}' создан",
            attachments=[get_promocodes_keyboard(promocodes)]
        )

    except ValueError:
        await event.message.answer(
            text="Неверный формат даты",
            attachments=[get_back_keyboard("promocodes_end_date")]
        )


# =========================
# EDIT PROMOCODE
# =========================

async def edit_promocode(event: MessageCallback):
    promocode_id = get_id(event.callback.payload)

    await event.message.edit(
        text="Что хотите изменить?",
        attachments=[get_edit_promocode_keyboard(promocode_id)]
    )


async def edit_max_uses(event: MessageCallback, context: MemoryContext):
    promocode_id = get_id(event.callback.payload)

    await context.update_data(id=promocode_id)
    await context.set_state(EditPromoCodeState.max_uses)

    await event.message.edit(
        text="Введите новое максимальное количество использований",
        attachments=[get_back_edit_promocode_keyboard(promocode_id)]
    )


async def update_max_uses(event: MessageCreated, context: MemoryContext):
    max_uses = int(event.message.body.text)

    data = await context.get_data()

    await promocodes_repo.update_one(
        id=data["id"],
        max_uses=max_uses
    )

    await context.clear()

    promocode_id = data["id"]

    await event.message.answer("Максимальное количество использований обновлено")

    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_promocode_keyboard(promocode_id)]
    )


async def edit_discount(event: MessageCallback, context: MemoryContext):
    promocode_id = get_id(event.callback.payload)

    await context.update_data(id=promocode_id)
    await context.set_state(EditPromoCodeState.discount)

    await event.message.edit(
        text="Введите новую скидку",
        attachments=[get_back_edit_promocode_keyboard(promocode_id)]
    )


async def update_discount(event: MessageCreated, context: MemoryContext):
    discount = float(event.message.body.text)

    data = await context.get_data()

    await promocodes_repo.update_one(
        id=data["id"],
        discount=discount
    )

    await context.clear()

    await event.message.answer("Скидка обновлена")

    promocode_id = data["id"]

    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_promocode_keyboard(promocode_id)]
    )


async def edit_start_date(event: MessageCallback, context: MemoryContext):
    promocode_id = get_id(event.callback.payload)

    await context.update_data(id=promocode_id)
    await context.set_state(EditPromoCodeState.start_date)

    await event.message.edit(
        text="Введите новую дату начала (YYYY-MM-DD)",
        attachments=[get_back_edit_promocode_keyboard(promocode_id)]
    )


async def update_start_date(event: MessageCreated, context: MemoryContext):
    start_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

    data = await context.get_data()

    await promocodes_repo.update_one(
        id=data["id"],
        start_date=start_date
    )

    await context.clear()

    await event.message.answer("Дата начала обновлена")
    
    promocode_id = data["id"]

    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_promocode_keyboard(promocode_id)]
    )


async def edit_end_date(event: MessageCallback, context: MemoryContext):
    promocode_id = get_id(event.callback.payload)

    await context.update_data(id=promocode_id)
    await context.set_state(EditPromoCodeState.end_date)

    await event.message.edit(
        text="Введите новую дату окончания (YYYY-MM-DD)",
        attachments=[get_back_edit_promocode_keyboard(promocode_id)]
    )


async def update_end_date(event: MessageCreated, context: MemoryContext):
    end_date = datetime.strptime(event.message.body.text, "%Y-%m-%d")

    data = await context.get_data()

    await promocodes_repo.update_one(
        id=data["id"],
        end_date=end_date
    )

    await context.clear()

    await event.message.answer("Дата окончания обновлена")

    promocode_id = data["id"]

    await event.message.answer(
        text="Что хотите изменить?",
        attachments=[get_edit_promocode_keyboard(promocode_id)]
    )


# =========================
# DELETE
# =========================

async def delete_promocode(event: MessageCallback):
    promocode_id = get_id(event.callback.payload)

    await promocodes_repo.delete_one(id=promocode_id)

    promocodes = await promocodes_repo.find_all()

    await event.message.edit(
        text="Промокоды",
        attachments=[get_promocodes_keyboard(promocodes)]
    )


# =========================
# REGISTER
# =========================


def register_handlers(dp: Dispatcher):
    dp.message_callback.register(start_admin_promocodes, F.callback.payload == "promocodes")
    dp.message_callback.register(start_admin_promocodes, F.callback.payload == "back:promocodes")

    dp.message_callback.register(add_promocode, F.callback.payload == "add_promocode")

    dp.message_created.register(enter_promocode_code, AddPromoCodeState.code)
    dp.message_created.register(enter_promocode_max_uses, AddPromoCodeState.max_uses)
    dp.message_created.register(enter_promocode_discount, AddPromoCodeState.discount)
    dp.message_created.register(enter_promocode_start_date, AddPromoCodeState.start_date)
    dp.message_created.register(enter_promocode_end_date, AddPromoCodeState.end_date)

    dp.message_callback.register(promocode, F.callback.payload.startswith("promocode:"))

    dp.message_callback.register(edit_promocode, F.callback.payload.startswith("edit_promocode:"))
    dp.message_callback.register(edit_max_uses, F.callback.payload.startswith("edit_max_uses:"))
    dp.message_callback.register(edit_discount, F.callback.payload.startswith("edit_discount:"))
    dp.message_callback.register(edit_start_date, F.callback.payload.startswith("edit_start_date:"))
    dp.message_callback.register(edit_end_date, F.callback.payload.startswith("edit_end_date:"))

    dp.message_created.register(update_max_uses, EditPromoCodeState.max_uses)
    dp.message_created.register(update_discount, EditPromoCodeState.discount)
    dp.message_created.register(update_start_date, EditPromoCodeState.start_date)
    dp.message_created.register(update_end_date, EditPromoCodeState.end_date)

    dp.message_callback.register(delete_promocode, F.callback.payload.startswith("delete_promocode:"))
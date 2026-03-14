from maxapi import Dispatcher, F
from maxapi.types import MessageCallback, MessageCreated
from maxapi.context import MemoryContext
from maxapi.types import Attachment, PhotoAttachmentPayload

from models.users import User
from models.marathons import Marathon
from models.promocodes import Promocode

from repositories.users import UsersRepository
from repositories.marathons import MarathonsRepository
from repositories.payments import PaymentsRepository
from repositories.promocodes import PromocodesRepository

from handlers.clients.marathons.keyboards import (
    get_marathons_keyboard,
    get_marathon_keyboard,
    get_buy_marathon_keyboard,
    get_pay_marathon_keyboard,
)
from handlers.base.keyboards import get_back_keyboard

from .states import EnterPromocodeState

from __init__ import bot
from utils.payments import yookassa


users_repo = UsersRepository()
marathons_repo = MarathonsRepository()
payments_repo = PaymentsRepository()
promocodes_repo = PromocodesRepository()


def get_id(payload: str):
    return int(payload.split(":")[1])


async def start_clients_marathons(event: MessageCallback, context: MemoryContext):
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


async def buy_marathon(event: MessageCallback):
    marathon_id = get_id(event.callback.payload)

    await event.message.edit(
        text="Выберите дальнейшее действие",
        attachments=[get_buy_marathon_keyboard(marathon_id)]
    )


async def pay_marathon(event: MessageCallback, context: MemoryContext):
    marathon_id = get_id(event.callback.payload)

    user: User = await users_repo.find_one(user_id=event.from_user.user_id)
    marathon: Marathon = await marathons_repo.get_one(id=marathon_id)

    payment = await yookassa.create_payment(marathon.price)

    await payments_repo.add_one(
        user_id=user.id,
        marathon_id=marathon.id,
        amount=marathon.price,
    )

    await event.message.edit(
        text="Оплатите марафон",
        attachments=[get_pay_marathon_keyboard(marathon_id, payment['confirmation']['confirmation_url'])]
    )


async def enter_promocode(event: MessageCallback, context: MemoryContext):
    marathon_id = get_id(event.callback.payload)

    await context.update_data(marathon_id=marathon_id)
    
    await context.set_state(EnterPromocodeState.code)

    await event.message.edit(
        text="Введите промокод",
        attachments=[get_back_keyboard(f"buy_marathon:{marathon_id}")]
    )


async def check_promocode(event: MessageCreated, context: MemoryContext):
    code = event.message.body.text

    data = await context.get_data()

    marathon_id = data["marathon_id"]

    promocode: Promocode = await promocodes_repo.find_one(code=code)

    if not promocode:
        await event.message.answer(
            text="Промокод не найден"
        )
        await event.message.answer(
            text="Введите промокод",
            attachments=[get_back_keyboard(f"buy_marathon:{marathon_id}")]
        )
        return

    if promocode.is_valid():
        used = await promocodes_repo.use_promocode(
            user_id=event.from_user.user_id,
            promocode_id=promocode.id
        )

        if not used:
            await event.message.answer(
                text="Промокод уже использован"
            )
            await event.message.answer(
                text="Введите промокод",
                attachments=[get_back_keyboard(f"buy_marathon:{marathon_id}")]
            )
            return
        
        user: User = await users_repo.find_one(user_id=event.from_user.user_id)
        marathon: Marathon = await marathons_repo.get_one(id=marathon_id)
        
        total_amount = int(marathon.price * (100 - promocode.discount) / 100)

        discount_amount = marathon.price - total_amount

        payment = await yookassa.create_payment(total_amount)

        await payments_repo.add_one(
            user_id=user.id,
            marathon_id=marathon.id,
            promocode_id=promocode.id,
            amount=marathon.price,
            discount_amount=discount_amount
        )

        await event.message.answer(
            text="Оплатите марафон",
            attachments=[get_pay_marathon_keyboard(marathon_id, payment['confirmation']['confirmation_url'])]
        )

    await context.clear()



def register_handlers(dp: Dispatcher):

    dp.message_callback.register(start_clients_marathons, F.callback.payload == "client_marathons")
    dp.message_callback.register(back_to_marathons, F.callback.payload == "back:client_marathons")

    dp.message_callback.register(marathon, F.callback.payload.startswith("client_marathon:"))

    dp.message_callback.register(buy_marathon, F.callback.payload.startswith("buy_marathon:"))

    dp.message_callback.register(pay_marathon, F.callback.payload.startswith("pay_marathon:"))

    dp.message_callback.register(enter_promocode, F.callback.payload.startswith("enter_promocode:"))
    dp.message_created.register(check_promocode, EnterPromocodeState.code)

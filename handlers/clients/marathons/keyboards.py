from typing import List

from maxapi.types.attachments.buttons import CallbackButton, LinkButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from models.marathons import Marathon
from models.chats import Chat


def get_marathons_keyboard(marathons: List[Marathon], offset: int = 0):
    builder = InlineKeyboardBuilder()

    for marathon in marathons:
        builder.row(
            CallbackButton(
                text=marathon.name,
                payload=f"client_marathon:{marathon.id}"
            )
        )

    builder.row(CallbackButton(text='◀️', payload=f'offset:client_marathons:{offset-10}'))
    builder.add(CallbackButton(text='⬅️ Назад', payload='back:clients'))
    builder.add(CallbackButton(text='▶️', payload=f'offset:client_marathons:{offset+10}'))

    return builder.as_markup()


def get_marathon_keyboard(marathon_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="🛍 Купить", payload=f"buy_marathon:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:client_marathons")
    )

    return builder.as_markup()


def get_buy_marathon_keyboard(marathon_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="💰 Оплатить", payload=f"pay_marathon:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="🎁 Ввести промокод", payload=f"enter_promocode:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"client_marathon:{marathon_id}")
    )

    return builder.as_markup()


def get_pay_marathon_keyboard(marathon_id: int, pay_link: str):
    builder = InlineKeyboardBuilder()

    builder.row(
        LinkButton(
            text="💳 Оплатить",
            url=pay_link
        )
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"buy_marathon:{marathon_id}")
    )

    return builder.as_markup()
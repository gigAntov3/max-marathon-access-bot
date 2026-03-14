from typing import List

from maxapi.types.attachments.buttons import CallbackButton, LinkButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from models.mailings import Mailing, MailingButton
from models.marathons import Marathon


def get_mailings_keyboard(mailings: List[Mailing], offset: int = 0):
    builder = InlineKeyboardBuilder()

    for mailing in mailings:
        builder.row(
            CallbackButton(
                text=mailing.title,
                payload=f"mailing:{mailing.id}"
            )
        )

    builder.row(
        CallbackButton(text="◀️", payload=f"offset:admin_mailings:{offset-10}")
    )

    builder.add(
        CallbackButton(text="✅ Создать", payload="add_mailing")
    )

    builder.add(
        CallbackButton(text="▶️", payload=f"offset:admin_mailings:{offset+10}")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:admin")
    )

    return builder.as_markup()


def get_mailing_preview_keyboard(buttons: List[MailingButton]):
    builder = InlineKeyboardBuilder()

    for button in buttons:
        builder.row(
            LinkButton(
                text=button.text,
                url=button.url
            )
        )

    return builder.as_markup()


def get_mailing_keyboard(mailing_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(
            text="❌ Удалить",
            payload=f"delete_mailing:{mailing_id}"
        )
    )

    builder.row(
        CallbackButton(
            text="⬅️ Назад",
            payload="back:mailings"
        )
    )

    return builder.as_markup()


def get_mailing_marathons_keyboard(marathons: List[Marathon], offset: int = 0):
    builder = InlineKeyboardBuilder()

    for marathon in marathons:
        builder.row(
            CallbackButton(
                text=marathon.name,
                payload=f"mailing_marathon:{marathon.id}"
            )
        )

    builder.row(
        CallbackButton(
            text="◀️",
            payload=f"offset:mailing_marathons:{offset-10}"
        )
    )

    builder.add(
        CallbackButton(
            text="Без фильтра",
            payload="mailing_marathon_skip"
        )
    )

    builder.add(
        CallbackButton(
            text="▶️",
            payload=f"offset:mailing_marathons:{offset+10}"
        )
    )

    builder.row(
        CallbackButton(
            text="⬅️ Назад",
            payload="back:mailing_message"
        )
    )

    return builder.as_markup()


def get_mailing_buttons_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(
            text="⏭ Без кнопок",
            payload="mailing_buttons_skip"
        )
    )

    builder.row(
        CallbackButton(
            text="⬅️ Назад",
            payload="back:mailing_marathon"
        )
    )

    return builder.as_markup()
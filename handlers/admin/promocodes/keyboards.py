from typing import List
from maxapi.types.attachments.buttons import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from models.promocodes import Promocode


def get_promocodes_keyboard(promocodes: List[Promocode], offset: int = 0):
    builder = InlineKeyboardBuilder()

    for promocode in promocodes:
        builder.row(
            CallbackButton(
                text=promocode.code,
                payload=f'promocode:{promocode.id}'
            )
        )

    builder.row(CallbackButton(text='◀️', payload=f'offset:promocodes:{offset-10}'))
    builder.add(CallbackButton(text='✅ Добавить', payload='add_promocode'))
    builder.add(CallbackButton(text='▶️', payload=f'offset:promocodes:{offset+10}'))

    builder.row(CallbackButton(text='⬅️ Назад', payload='back:admin'))

    return builder.as_markup()


def get_promocode_keyboard(promocode_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="✏️ Изменить", payload=f"edit_promocode:{promocode_id}")
    )

    builder.row(
        CallbackButton(text="❌ Удалить", payload=f"delete_promocode:{promocode_id}")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:promocodes")
    )

    return builder.as_markup()


def get_edit_promocode_keyboard(promocode_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="🔢 Макс. использования", payload=f"edit_max_uses:{promocode_id}")
    )

    builder.row(
        CallbackButton(text="💸 Скидка", payload=f"edit_discount:{promocode_id}")
    )

    builder.row(
        CallbackButton(text="📅 Дата начала", payload=f"edit_start_date:{promocode_id}")
    )

    builder.row(
        CallbackButton(text="📅 Дата окончания", payload=f"edit_end_date:{promocode_id}")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"promocode:{promocode_id}")
    )

    return builder.as_markup()


def get_back_edit_promocode_keyboard(promocode_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"edit_promocode:{promocode_id}")
    )

    return builder.as_markup()
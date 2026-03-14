from typing import List

from maxapi.types.attachments.buttons import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from models.marathons import Marathon
from models.chats import Chat


def get_marathons_keyboard(marathons: List[Marathon], offset: int = 0):
    builder = InlineKeyboardBuilder()

    for marathon in marathons:
        builder.row(
            CallbackButton(
                text=marathon.name,
                payload=f"marathon:{marathon.id}"
            )
        )

    builder.row(CallbackButton(text='◀️', payload=f'offset:admin_marathons:{offset-10}'))
    builder.add(CallbackButton(text='✅ Добавить', payload='add_marathon'))
    builder.add(CallbackButton(text='▶️', payload=f'offset:admin_marathons:{offset+10}'))

    builder.row(CallbackButton(text='⬅️ Назад', payload='back:admin'))

    return builder.as_markup()


def get_marathon_type_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="👤 Индивидуальный", payload="marathon_type:individual")
    )

    builder.row(
        CallbackButton(text="👥 Групповой", payload="marathon_type:group")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:marathons_photo")
    )

    return builder.as_markup()


def get_marathon_keyboard(marathon_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="💬 Чаты", payload=f"marathon_chats:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="✏️ Изменить", payload=f"edit_marathon:{marathon_id}"),
    )

    builder.row(
        CallbackButton(text="❌ Удалить", payload=f"delete_marathon:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:marathons")
    )

    return builder.as_markup()


def get_edit_marathon_keyboard(marathon_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="Название", payload=f"edit_marathon_name:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="Описание", payload=f"edit_marathon_description:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="Дата начала", payload=f"edit_marathon_start:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="Дата окончания", payload=f"edit_marathon_end:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="Цена", payload=f"edit_marathon_price:{marathon_id}")
    )

    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"marathon:{marathon_id}")
    )

    return builder.as_markup()


def get_back_edit_marathon_keyboard(marathon_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"edit_marathon:{marathon_id}")
    )

    return builder.as_markup()




def get_chats_keyboard(chants: List[Chat], marathon_id: int):
    builder = InlineKeyboardBuilder()

    for chat in chants:
        builder.row(
            CallbackButton(
                text=chat.title,
                payload=f"marathon_chat:{chat.id}"
            )
        )
    
    builder.row(
        CallbackButton(
            text="⬅️ Назад",
            payload=f"marathon:{marathon_id}"
        )
    )

    return builder.as_markup()


def get_chat_keyboard(marathon_id: int, chat_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        CallbackButton(
            text="❌ Удалить",
            payload=f"delete_marathon_chat:{chat_id}"
        )
    )
    
    builder.row(
        CallbackButton(
            text="⬅️ Назад",
            payload=f"marathon_chats:{marathon_id}"
        )
    )

    return builder.as_markup()
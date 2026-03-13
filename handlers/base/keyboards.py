from maxapi.types.attachments.buttons import CallbackButton

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder



def get_back_keyboard(back_to: str):
    builder = InlineKeyboardBuilder()

    builder.row(CallbackButton(text='⬅️ Назад', payload=f'back:{back_to}'))

    return builder.as_markup()
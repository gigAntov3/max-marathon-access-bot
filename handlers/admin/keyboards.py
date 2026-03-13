from maxapi.types.attachments.buttons import CallbackButton

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder



def get_main_admin_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(CallbackButton(text='Марафоны', payload='marathons'))
    builder.row(CallbackButton(text='Промокоды', payload='promocodes'))

    return builder.as_markup()
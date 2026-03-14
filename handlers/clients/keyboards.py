from maxapi.types.attachments.buttons import CallbackButton

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder



def get_main_client_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(CallbackButton(text='Марафоны', payload='client_marathons'))
    # builder.row(CallbackButton(text='Промокоды', payload='promocodes'))

    return builder.as_markup()
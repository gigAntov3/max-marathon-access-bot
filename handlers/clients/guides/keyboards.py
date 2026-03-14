from typing import List
from maxapi.types.attachments.buttons import CallbackButton, LinkButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from models.guides import Guide

def get_guides_keyboard(guides: List[Guide], offset: int = 0):
    builder = InlineKeyboardBuilder()
    
    for guide in guides:
        builder.row(
            CallbackButton(
                text=f"📚 {guide.title}",
                payload=f'client_guide:{guide.id}'
            )
        )
    
    builder.row(CallbackButton(text='◀️', payload=f'offset:client_guides:{offset-10}'))
    builder.add(CallbackButton(text='⬅️ Назад', payload='back:clients'))
    builder.add(CallbackButton(text='▶️', payload=f'offset:client_guides:{offset+10}'))
    
    return builder.as_markup()


def get_guide_keyboard(guide_link: str):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        LinkButton(
            text="🔗 Перейти",
            url=guide_link
        )
    )
    
    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:client_guides")
    )
    
    return builder.as_markup()
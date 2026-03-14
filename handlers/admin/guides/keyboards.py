from typing import List
from maxapi.types.attachments.buttons import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from models.guides import Guide

def get_guides_keyboard(guides: List[Guide], offset: int = 0):
    builder = InlineKeyboardBuilder()
    
    for guide in guides:
        builder.row(
            CallbackButton(
                text=f"📚 {guide.title}",
                payload=f'guide:{guide.id}'
            )
        )
    
    builder.row(CallbackButton(text='◀️', payload=f'offset:admin_guides:{offset-10}'))
    builder.add(CallbackButton(text='✅ Добавить гайд', payload='add_guide'))
    builder.add(CallbackButton(text='▶️', payload=f'offset:admin_guides:{offset+10}'))

    builder.row(CallbackButton(text='⬅️ Назад', payload='back:admin'))
    
    return builder.as_markup()


def get_guide_keyboard(guide_id: int):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="✏️ Изменить", payload=f"edit_guide:{guide_id}")
    )
    
    builder.row(
        CallbackButton(text="❌ Удалить", payload=f"delete_guide:{guide_id}")
    )
    
    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:guides")
    )
    
    return builder.as_markup()


def get_edit_guide_keyboard(guide_id: int):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="📝 Название", payload=f"guide_title:{guide_id}")
    )
    
    builder.row(
        CallbackButton(text="📄 Описание", payload=f"guide_description:{guide_id}")
    )
    
    builder.row(
        CallbackButton(text="🔗 Ссылка", payload=f"guide_link:{guide_id}")
    )
    
    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"guide:{guide_id}")
    )
    
    return builder.as_markup()


def get_back_edit_guide_keyboard(guide_id: int, field: str = ""):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="⬅️ Назад", payload=f"edit_guide:{guide_id}")
    )
    
    return builder.as_markup()


def get_back_guides_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="⬅️ Назад", payload="back:guides")
    )
    
    return builder.as_markup()
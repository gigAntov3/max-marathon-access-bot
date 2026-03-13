from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from models.users import User


class Messages:
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="MESSAGES_CONFIG__",
    )

    START_MESSAGE = """
👋 Привет, {name}!

🤖 Этот бот предназначен для автоматической работы с Telegram-каналами.

Возможности:
• 🔁 Пересылка контента между каналами
• 🖼️ Наложение водяных знаков
• 🎞️ Добавление превью к видео
• ⚙️ Управление парами каналов и настройками

🚀 Выберите действие ниже, чтобы начать работу.
"""

    START_ADMIN_MESSAGE = """
👋 Вы вощли в админ панель. Выберите дальнейшее действие:
"""

    ENTER_PASSWORD_MESSAGE = "🔑 Введите пароль администратора"

    CHANNELS_MESSAGE = """
📺 Выберите канал:
"""

    CONFIRM_DELETE_CHANNELS_MESSAGE = """
📺 Вы уверены, что хотите удалить каналы?
"""

    CHANNEL_MESSAGE = """
📌 Информация о канале:

🆔 ID: {id}
📝 Название: {title}
👤 Username: {username}
💬 Telegram chat ID: {telegram_chat_id}
📅 Добавлен: {created_at}
""" 

    ENTER_CHANNEL_TYPE_MESSAGE = """
📺 Выберите тип канала:
"""

    ENTER_CHANNEL_PAIR_NAME_MESSAGE = """
📝 Введите название пары канала:
"""

    ADD_CHANNEL_MESSAGE = """
📺 Выберите канал:
"""

    CHANNELS_PAIRS_MESSAGE = """
📺 Выберите пару каналов:
"""

    ENTER_CHANNELS_PAIR_NAME_MESSAGE = """
📝 Введите название пары каналов:
"""

    ENTER_CHANNELS_PAIR_SOURCE_MESSAGE = """
📺 Выберите исходящий канал:
"""

    ENTER_CHANNELS_PAIR_TARGET_MESSAGE = """
📺 Выберите входящий канал:
"""

    ENTER_CHANNELS_PAIR_WATERMARK_MESSAGE = """
📁 Выберите водянку для pdf:
"""

    CHANNEL_PAIR_MESSAGE = """
📌 Информация о паре:

🆔 ID: {id}
📝 Название: {name}

📤 Исходящий канал: {source_channel_id}
📥 Входящий канал: {target_channel_id}

📁 Водяной знак для документов: {document_watermark}

🖼️ Превью для видео: {video_preview}
🎬 Водяной знак для видео: {video_watermark}

👤 Статус: {is_active}
📅 Добавлен: {created_at}
"""

    CHANNEL_PAIR_SETTINGS_MESSAGE = """
📝 Что вы ходите изменить?
"""

    CONFIRM_DELETE_CHANNELS_PAIR_MESSAGE = """
📌 Подтвердите удаление пары каналов:
"""

    WATERMARKS_MESSAGE = """
📺 Выберите водяную марку:
"""

    ENTER_WATERMARKS_NAME_MESSAGE = """
📝 Введите название водяной марки:
"""

    ENTER_WATERMARKS_FILE_MESSAGE = """
📁 Пришлите файл водяной марки:
"""

    WATERMARK_MESSAGE = """
📌 Информация о водяной марке:

🆔 ID: {id}
📝 Название: {name}
📅 Добавлен: {created_at}
"""

    CHANGE_CHANNELS_PAIR_WATERMARK_MESSAGE = """
📁 Выберите водянку для pdf:
"""

    PREVIEWS_MESSAGE = """
📺 Выберите превью:
"""

    PREVIEW_MESSAGE = """
📌 Информация о превью:

🆔 ID: {id}
📝 Название: {name}
📅 Добавлен: {created_at}
"""

    ENTER_PREVIEW_NAME_MESSAGE = """
📝 Введите название превью:
"""

    ENTER_PREVIEW_FILE_MESSAGE = """
📁 Пришлите файл превью:
"""

    CHANNELS_PAIRS_MESSAGE = """
📺 Выберите пару каналов:
"""

    CHANGE_CHANNELS_PAIR_VIDEO_WATERMARK_MESSAGE = """
📺 Выберите водяную марку:
"""

    CHANGE_CHANNELS_PAIR_VIDEO_PREVIEW_MESSAGE = """
📺 Выберите превью:
"""

#     SESSION_MESSAGE = """
# 🔑 Текущая сессия:

# 🆔 API ID: {api_id}
# 🆔 API Hash: {api_hash}
# 📞 Номер телефона: {phone}
# """

    SESSION_MESSAGE = """
🔑 Текущая сессия:

📞 Номер телефона: {phone}
"""

    ENTER_SESSION_API_ID_MESSAGE = """
🆔 Введите API ID:
"""

    ENTER_SESSION_API_HASH_MESSAGE = """
🆔 Введите API Hash:
"""

    ENTER_SESSION_PHONE_MESSAGE = """
📞 Введите номер телефона:
"""

    ENTER_SESSION_CODE_MESSAGE = """
📝 Введите код подтверждения и добавьте пробел между цифр:
"""

    ENTER_CHANNELS_PAIR_VIDEO_PREVIEW_MESSAGE = """
📺 Выберите превью:
"""

    ENTER_CHANNELS_PAIR_VIDEO_WATERMARK_MESSAGE = """
📺 Выберите водяную марку для видео:
"""

    ENTER_CHANNEL_PAIR_CHANNELS_MESSAGE = """
📺 Выберите канал:
"""

    ENTER_CHANNEL_PAIR_WATERMARK_MESSAGE = """
📺 Выберите водяную марку:
"""

    ENTER_CHANNEL_PAIR_VIDEO_PREVIEW_MESSAGE = """
📺 Выберите превью:
"""

    ENTER_CHANNEL_PAIR_VIDEO_WATERMARK_MESSAGE = """
📺 Выберите водяную марку для видео:
"""

    ENTER_DOCUMENT_FILTER_MESSAGE = """
📝 Введите фильтр документов:
"""

    ENTER_COPY_OFFSET_MESSAGE = """
📝 Введите смещение:
"""

    COPY_CHANNELS_MESSAGE = """
📝 Копирование канала...
"""

    COPIED_CHANNELS_MESSAGE = """
✅ Канал скопирован!
"""

    COPY_ERROR_CHANNELS_MESSAGE = """
❌ Не удалось скопировать канал!

{error}
"""

    FILTERS_MESSAGE = """
📝 Выберите фильтр:
"""

    ENTER_FILTERS_NAME_MESSAGE = """
📝 Введите название фильтра:
"""

    FILTER_MESSAGE = """
📌 Информация о фильтре:

🆔 ID: {id}
📝 Фильтр: {word}
📅 Добавлен: {created_at}
"""

    ENTER_VIDEO_WATERMARK_FILTER_MESSAGE = """
🔍 Фильтр для видео: {duration}

📝 Введите фильтр для видео:
"""

messages = Messages()
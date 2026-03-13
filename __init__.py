from maxapi import Bot, Dispatcher

from config import settings


bot = Bot(token=settings.bot.token)
dp = Dispatcher()
from maxapi import Dispatcher

from .handlers import register_handlers as promocodes_register_handlers


def register_handlers(dp: Dispatcher):
    promocodes_register_handlers(dp)
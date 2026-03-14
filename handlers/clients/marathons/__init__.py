from maxapi import Dispatcher

from .handlers import register_handlers as marathon_register_handlers


def register_handlers(dp: Dispatcher):
    marathon_register_handlers(dp)
from maxapi import Dispatcher

from .handlers import register_handlers as register_base_handlers


def register_handlers(dp: Dispatcher):
    register_base_handlers(dp)
from maxapi import Dispatcher

from .handlers import register_handlers as register_guides_handlers


def register_handlers(dp: Dispatcher):
    register_guides_handlers(dp)
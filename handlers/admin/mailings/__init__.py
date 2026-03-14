from maxapi import Dispatcher

from .handlers.add import register_handlers as register_add_mailing_handlers
from .handlers.base import register_handlers as register_base_handlers


def register_handlers(dp: Dispatcher):
    register_base_handlers(dp)
    register_add_mailing_handlers(dp)
from maxapi import Dispatcher

from .add import register_handlers as add_marathon_handlers
from .edit import register_handlers as edit_marathon_handlers
from .base import register_handlers as base_handlers
from .chats import register_handlers as register_marathons_chats


def register_handlers(dp: Dispatcher):
    base_handlers(dp)
    add_marathon_handlers(dp)
    edit_marathon_handlers(dp)
    register_marathons_chats(dp)
from maxapi import Dispatcher

from .handlers import register_handlers as register_clients_handlers
from .marathons import register_handlers as marathon_register_handlers


def register_handlers(dp: Dispatcher):
    register_clients_handlers(dp)
    marathon_register_handlers(dp)
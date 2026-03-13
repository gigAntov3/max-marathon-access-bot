from maxapi import Dispatcher

from .handlers import register_handlers as register_clients_handlers


def register_handlers(dp: Dispatcher):
    register_clients_handlers(dp)
from maxapi import Dispatcher

from .admin import register_handlers as register_admin_handlers
from .clients import register_handlers as register_clients_handlers



def register_handlers(dp: Dispatcher):
    register_admin_handlers(dp)
    register_clients_handlers(dp)
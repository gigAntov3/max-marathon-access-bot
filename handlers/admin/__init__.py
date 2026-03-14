from maxapi import Dispatcher

from .handlers import register_handlers as register_admin_handlers
from .marathons import register_handlers as register_marathons_handlers
from .promocodes import register_handlers as register_promocodes_handlers
from .mailings import register_handlers as register_mailings_handlers


def register_handlers(dp: Dispatcher):
    register_admin_handlers(dp)
    register_marathons_handlers(dp)
    register_promocodes_handlers(dp)
    register_mailings_handlers(dp)
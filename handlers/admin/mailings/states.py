from maxapi.context import State, StatesGroup


class AddMailingState(StatesGroup):
    title = State()
    message = State()
    marathon = State()
    buttons = State()
    send_at = State()
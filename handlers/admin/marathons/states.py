from maxapi.context import State, StatesGroup


class AddMarathonState(StatesGroup):
    name = State()
    description = State()
    type = State()
    start_date = State()
    end_date = State()
    price = State()


class EditMarathonState(StatesGroup):
    name = State()
    description = State()
    start_date = State()
    end_date = State()
    price = State()


class AddMarathonChatState(StatesGroup):
    chat_id = State()
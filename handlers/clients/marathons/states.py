from maxapi.context import State, StatesGroup


class EnterPromocodeState(StatesGroup):
    code = State()
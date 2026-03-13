from maxapi.context import State, StatesGroup

class EnterAdminPasswordState(StatesGroup):
    password = State()
from maxapi.context import State, StatesGroup

class AddGuideState(StatesGroup):
    title = State()
    description = State()
    link = State()

class EditGuideState(StatesGroup):
    title = State()
    description = State()
    link = State()
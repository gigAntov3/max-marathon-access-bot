from maxapi.context import State, StatesGroup


class AddPromoCodeState(StatesGroup):
    code = State()
    max_uses = State()
    discount = State()
    start_date = State()
    end_date = State()


class EditPromoCodeState(StatesGroup):
    max_uses = State()
    discount = State()
    start_date = State()
    end_date = State()
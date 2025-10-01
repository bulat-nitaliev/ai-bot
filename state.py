from aiogram.fsm.state import State, StatesGroup


class DomainState(StatesGroup):
    domain = State()
    query = State()

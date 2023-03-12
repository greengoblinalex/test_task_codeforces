from aiogram.dispatcher.filters.state import StatesGroup, State


class GetRecords(StatesGroup):
    complexity = State()
    theme = State()

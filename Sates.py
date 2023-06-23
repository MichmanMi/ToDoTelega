from aiogram.dispatcher.filters.state import State,StatesGroup

class Forma(StatesGroup): #форма для создания задач
    title = State()
    date = State()
    time = State()
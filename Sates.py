from aiogram.dispatcher.filters.state import State,StatesGroup

class Forma(StatesGroup): #����� ��� �������� �����
    title = State()
    date = State()
    time = State()
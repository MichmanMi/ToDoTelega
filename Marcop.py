from itertools import zip_longest

from aiogram import types

import Connect_DataBase


def Marcop_main():
    key_main = types.InlineKeyboardMarkup()

    key_main.add(types.InlineKeyboardButton("Список задач📋", callback_data="Список задач📋"),
                 types.InlineKeyboardButton("Добавить задачу📝", callback_data="Добавить задачу📝"),
                 types.InlineKeyboardButton("Удалить задачу❌", callback_data="Удалить задачу❌"))

    key_main.insert(types.InlineKeyboardButton('Время🕓', callback_data='Время🕓'))

    return key_main

def back_menu():
    back_menu = types.InlineKeyboardMarkup()
    back_menu.insert(types.InlineKeyboardButton("Назад", callback_data='Назад в меню'))
    return back_menu

def AddTask():
    Button_task = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Добавить на сегодня📅'),
                                                                      types.KeyboardButton('Добавить на другую дату🗓'))
    Button_task = Button_Back_Reply(Button_task)
    return Button_task


def Button_Back_Reply(Back: types.ReplyKeyboardMarkup):
    Back.insert(types.KeyboardButton('Назад🔙'))
    return Back


def Button_Back_Inline(Back: types.InlineKeyboardMarkup):
    Back.row(types.InlineKeyboardButton('Назад🔙', callback_data='Назад'))
    return Back


def split_list(lst, size):
    return [list(filter(None, sublist)) for sublist in zip_longest(*([iter(lst)] * size))]


def marcop_task_list_today(task_list, page):
    marcop = types.InlineKeyboardMarkup(row_width=1)
    sorted_list = sorted(task_list, key=lambda x: x[1])
    result_list_of_dicts = split_list(sorted_list, 5)
    for task in result_list_of_dicts[page]:
        marcop.add(types.InlineKeyboardButton(f'{task[1]}', callback_data=f'task,select,{task[2]},{task[0]},{page}'))
    if page == 0:
        if len(result_list_of_dicts) != 1:
            marcop.row(types.InlineKeyboardButton('>', callback_data=f'task,{page},+,{result_list_of_dicts[page][0][-1]}'))
    if  0 < page < len(result_list_of_dicts)-1:
        marcop.row(types.InlineKeyboardButton('<', callback_data=f'task,{page},-,{result_list_of_dicts[page][0][-1]}'),
                   types.InlineKeyboardButton('>', callback_data=f'task,{page},+,{result_list_of_dicts[page][0][-1]}'))
    if page >= len(result_list_of_dicts)-1:
        if len(result_list_of_dicts) != 1:
            marcop.row(types.InlineKeyboardButton('<', callback_data=f'task,{page},-,{result_list_of_dicts[page][0][-1]}'))
    marcop = Button_Back_Inline_Task(marcop)
    return marcop


def confirmation():
    confirmation = types.InlineKeyboardMarkup()
    confirmation.add(types.InlineKeyboardButton("Да👍", callback_data="Yes"),
                     types.InlineKeyboardButton("Нет👎", callback_data="No"))
    return confirmation


def timeInlineButton(hour: int, min: int):
    timeInlineButton = types.InlineKeyboardMarkup()

    if hour == 0:
        hour = 23
    elif hour == 24:
        hour = 00
    if min == -10:
        min = 60
    elif min == 70:
        min = 00

    timeInlineButton.row(types.InlineKeyboardButton("➕ 1️⃣ Час", callback_data=f"time:{hour + 1}:{min}"),
                         types.InlineKeyboardButton("➖ ️ 1️⃣ Час", callback_data=f"time:{hour - 1}:{min}"))

    timeInlineButton.row(types.InlineKeyboardButton(f"{hour}:{min}", callback_data='0'))

    timeInlineButton.row(types.InlineKeyboardButton("➕ 1️⃣0️⃣ минут", callback_data=f"time:{hour}:{min + 10}"),
                         types.InlineKeyboardButton("➖ ️ 1️⃣0️⃣ минут", callback_data=f"time:{hour}:{min - 10}"))
    timeInlineButton = Button_Back_Inline(timeInlineButton)
    return timeInlineButton


def Button_Back_Inline_Task(Back):
    Back.row(types.InlineKeyboardButton('Назад🔙', callback_data="task,back"))
    return Back


def Button_Back_Inline_Time(Back, page, date):
    Back.row(types.InlineKeyboardButton('Назад🔙', callback_data=f"task,{page},{date},back-page"))
    return Back

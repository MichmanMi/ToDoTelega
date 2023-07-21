from aiogram import types

import Connect_DataBase


def Marcop_main():
    key_main = types.ReplyKeyboardMarkup(resize_keyboard=True)

    key_main.add(types.KeyboardButton('Список задач📋'),
                 types.KeyboardButton('Добавить задачу📝'),
                 types.KeyboardButton('Удалить задачу❌'))

    key_main.insert(types.KeyboardButton('Время🕓'))

    return key_main


def AddTask():
    Button_task = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Добавить на сегодня'),
                                                                      types.KeyboardButton('Добавить на другую дату'))
    Button_task = Button_Back_Reply(Button_task)
    return Button_task


def Button_Back_Reply(Back: types.ReplyKeyboardMarkup):
    Back.insert(types.KeyboardButton('Назад'))
    return Back


def Button_Back_Inline(Back: types.InlineKeyboardMarkup):
    Back.row(types.InlineKeyboardButton('Назад', callback_data='Назад'))
    return Back


def marcop_task_list_today(task_list):
    marcop = types.InlineKeyboardMarkup(row_width=1)
    sorted_list = sorted(task_list, key=lambda x: x[2])
    for task in sorted_list:
        marcop.add(types.InlineKeyboardButton(f'{task[2]}', callback_data=f'task,{task[2]},{task[0]}'))
    return marcop


marcop_task_list_today(Connect_DataBase.all_Tasks())


def confirmation():
    confirmation = types.InlineKeyboardMarkup()
    confirmation.add(types.InlineKeyboardButton("Да", callback_data="Yes"),
                     types.InlineKeyboardButton("Нет", callback_data="No"))
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

def Button_Back_Inline_Task():
    Back = types.InlineKeyboardMarkup()
    Back.row(types.InlineKeyboardButton('Назад', callback_data="task,back"))
    return Back
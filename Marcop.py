from aiogram import types

import Connect_DataBase


def Marcop_main():
    key_main=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Список задач📋'),
                                                                 types.KeyboardButton('Добавить задачу📝'),
                                                                 types.KeyboardButton('Удалить задачу❌',
                                                                                      ))
    return key_main   #1)Добавить кнопку "Время"

def AddTask():
    Button_task=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton('Добавить на сегодня'),
                                                                    types.KeyboardButton('Добавить на другую дату'))
    Button_task=Button_Back_Reply(Button_task)
    return Button_task

def Button_Back_Reply(Back:types.ReplyKeyboardMarkup):
    Back.insert(types.KeyboardButton('Назад'))
    return Back

# def Button_Back_Inline(Back:types.InlineKeyboardMarkup):
#     Back.insert(types.KeyboardButton('Назад'))
#     return Back

def marcop_task_list_today(task_list):
    marcop = types.InlineKeyboardMarkup(row_width=1)
    sorted_list = sorted(task_list,key=lambda x: x[2])
    for task in sorted_list:
        marcop.add(types.InlineKeyboardButton(f'{task[2]}', callback_data=f'{task[2]}:{task[0]}'))
    return marcop

marcop_task_list_today(Connect_DataBase.all_Tasks())

def confirmation():
    confirmation = types.InlineKeyboardMarkup()
    confirmation.add(types.InlineKeyboardButton("Да",callback_data="Yes"),
                     types.InlineKeyboardButton("Нет",callback_data="No"))
    return confirmation

#3)добавить инлайт кнопки, которые вызываются во 2-м пункте (5 шт)
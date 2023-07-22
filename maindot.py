from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from Log_Config import *
from datetime import datetime
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar

import Marcop
import Connect_DataBase
import Sates

bot = Bot(token=open("Canfic.txt", mode="r").read())
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    await msg.answer('Hi', reply_markup=Marcop.Marcop_main())
    logging.info(f"Пользователь {msg.from_user.username} \n"
                 f"написал сообщение: {msg.text}")


@dp.callback_query_handler(text=["Список задач📋", "Добавить задачу📝", "Удалить задачу❌", "Время🕓"])
async def main_menu(call: types.callback_query, state: FSMContext):
    if call.data == "Список задач📋":
        await call.message.edit_text('Пожалуйста, выберите дату:', reply_markup=await SimpleCalendar().start_calendar())
    elif call.data == "Добавить задачу📝":
        await call.message.edit_text("Отправьте название задачи", reply_markup=Marcop.back_menu())
        await state.set_state(Sates.Forma.title)
    elif call.data == "Удалить задачу❌":
        await call.message.edit_text("Удалить задачу пока в разработке🤷🏻‍♀️........",reply_markup=Marcop.Marcop_main())
    elif call.data == "Время🕓":
        await call.message.edit_text("Время:",
                                     reply_markup=Marcop.timeInlineButton(hour=00, min=00))

@dp.callback_query_handler(text=["Назад в меню"])
async def back_main_menu(call: types.callback_query):
    await call.message.edit_text('Hi', reply_markup=Marcop.Marcop_main())

@dp.callback_query_handler(text=["Назад в меню"],state=Sates.Forma.title)
async def back_main_menu(call: types.callback_query):
    await call.message.edit_text('Hi', reply_markup=Marcop.Marcop_main())
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        result = Connect_DataBase.Get_Data(date.strftime("%d/%m/%Y"))
        await callback_query.message.edit_text(f"Ваш список на {date.strftime('%d/%m/%Y')}",
                                               reply_markup=Marcop.marcop_task_list_today(result, 0))


@dp.message_handler(content_types=types.ContentType.ANY, state=Sates.Forma.title)
async def task_title(msg: types.Message, state: FSMContext):
    if msg.content_type == types.ContentType.TEXT:
        await state.update_data(title=msg.text)
        await msg.answer("Записал")
        await msg.answer("Отправье дату 'день/месяц/год'")
        await state.set_state(Sates.Forma.date)
    else:
        await msg.answer(f"Вы отправили {msg.content_type}\n"
                         f"я могу обработать только текст")


@dp.message_handler(content_types=types.ContentType.ANY, state=Sates.Forma.date)
async def task_title(msg: types.Message, state: FSMContext):
    if msg.content_type == types.ContentType.TEXT:
        if msg.text.find("/"):
            await state.update_data(date=msg.text)
            await msg.answer("Записал")
            await msg.answer("Отправье время '00:00' в формате 24 часа")
            await state.set_state(Sates.Forma.time)
        else:
            await msg.answer("Вы отправили дату не по форме")
    else:
        await msg.answer(f"Вы отправили {msg.content_type}\n"
                         f"я могу обработать только текст")


@dp.message_handler(content_types=types.ContentType.ANY, state=Sates.Forma.time)
async def task_title(msg: types.Message, state: FSMContext):
    if msg.content_type == types.ContentType.TEXT:
        if msg.text.find(":"):
            await state.update_data(time=msg.text)
            await msg.answer("Записал")
            data = await state.get_data()
            await msg.answer("Проверьте правильность задачи:\n"
                             f"<b> название задачи </b>: {data['title']}\n"
                             f"<b> дата </b>: {data['date']}\n"
                             f"<b> время </b>: {data['time']}", parse_mode='HTML',
                             reply_markup=Marcop.confirmation())
        else:
            await msg.answer("Вы отправили дату не по форме")
    else:
        await msg.answer(f"Вы отправили {msg.content_type}\n"
                         f"я могу обработать только текст")


@dp.callback_query_handler(state=Sates.Forma.time)
async def callback_add_task(call: types.callback_query, state: FSMContext):
    if call.data == "Yes":
        data = await state.get_data()
        result = Connect_DataBase.all_Tasks_Write_Down(data['title'], data['date'], data['time'])
        if result == True:
            await call.message.edit_text("Отлично! Записал!", reply_markup=None)
            await state.finish()
        else:
            await call.message.edit_text("Ошибка! Не записал!", reply_markup=None)
            await state.finish()

    elif call.data == "No":
        await call.message.delete()
        await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('time'))
async def callback_time(call: types.callback_query):
    msg, hour, min = call.data.split(':')
    await call.message.edit_text('Время:', reply_markup=Marcop.timeInlineButton(int(hour), int(min)))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('task'))
async def callback_task(call: types.callback_query):
    print(call.data)
    if call.data.split(',')[-1] == 'back-page':
        result = Connect_DataBase.Get_Data(call.data.split(',')[-2])
        await call.message.edit_text(f"Ваш список на {call.data.split(',')[-2]}",
                                     reply_markup=Marcop.marcop_task_list_today(result,
                                                                                int(call.data.split(',')[-3])))
    if call.data.split(',')[-1] == 'back':
        await call.message.edit_text('Пожалуйста, выберите дату:', reply_markup=await SimpleCalendar().start_calendar())
    if call.data.split(',')[-2] == '+':
        result = Connect_DataBase.Get_Data(call.data.split(',')[-1])
        await call.message.edit_text(f"Ваш список на {call.data.split(',')[-1]}",
                                               reply_markup=Marcop.marcop_task_list_today(result, int(call.data.split(',')[1])+1))
    if call.data.split(',')[-2] == '-':
        result = Connect_DataBase.Get_Data(call.data.split(',')[-1])
        await call.message.edit_text(f"Ваш список на {call.data.split(',')[-1]}",
                                               reply_markup=Marcop.marcop_task_list_today(result, int(call.data.split(',')[1])-1))
    if call.data.split(',')[1] == 'select':
        result = Connect_DataBase.Get_Task(call.data.split(',')[-2])
        Task = result[0][0]
        Time = result[0][1]
        Data = result[0][2]
        marcup = types.InlineKeyboardMarkup()
        await call.message.edit_text(f"Вот Ваша задача: \n"
                                     f"<b> название задачи </b>: {Task}\n"
                                     f"<b> дата </b>: {Data}\n"
                                     f"<b> время </b>: {Time}", parse_mode='HTML',
                                     reply_markup=Marcop.Button_Back_Inline_Time(marcup,call.data.split(',')[-1],Data))


@dp.callback_query_handler(text=['Назад'])
async def callback_back(call: types.callback_query):
    await call.message.edit_text('Hi', reply_markup=Marcop.Marcop_main())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

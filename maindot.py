import asyncio
from aiogram.types import InputFile
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

background = ['https://b1.filmpro.ru/c/390499.jpg']


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    logging.error(f'Ошибка при обработке запроса {update}: {exception}')


@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    # await msg.answer_photo(background[0], caption='Привет, что ты хочешь?', reply_markup=Marcop.Marcop_main())
    await msg.answer_sticker('CAACAgIAAxkBAAEJzCJkvlyzxwK7DEb2hS1V_h0iQk4-MAACAQYAAkb7rAQJuBy3H-Ro9y8E', reply_markup=Marcop.Marcop_main())


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def image(msg: types.Message):
    print(msg.photo[-1]["file_id"])


@dp.callback_query_handler(text=["Список задач📋", "Добавить задачу📝", "Удалить задачу❌", "Время🕓"])
async def main_menu(call: types.callback_query, state: FSMContext):
    if call.data == "Список задач📋":
        await call.message.edit_text('Пожалуйста, выберите дату:', reply_markup=await SimpleCalendar().start_calendar())
    elif call.data == "Добавить задачу📝":
        await call.message.edit_text("Отправьте название задачи", reply_markup=Marcop.back_menu())
        await state.set_state(Sates.Forma.title)
    elif call.data == "Удалить задачу❌":
        await call.message.edit_text("Удалить задачу пока в разработке🤷🏻‍♀️........", reply_markup=Marcop.Marcop_main())


@dp.callback_query_handler(text=["Назад в меню"])
async def back_main_menu(call: types.callback_query):
    await call.message.edit_text('Hi', reply_markup=Marcop.Marcop_main())


@dp.callback_query_handler(text=["Назад в меню"], state=Sates.Forma.title)
async def back_main_menu(call: types.callback_query, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Hi', reply_markup=Marcop.Marcop_main())


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(call: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        result = Connect_DataBase.Get_Data(date.strftime("%d/%m/%Y"))
        if result:
            await call.message.edit_text(f"Ваш список на {date.strftime('%d/%m/%Y')}",
                                         reply_markup=Marcop.marcop_task_list_today(result, 0))
        else:
            await call.answer('Нет задач на этот День')


@dp.message_handler(content_types=types.ContentType.ANY, state=Sates.Forma.title)
async def task_title(msg: types.Message, state: FSMContext):
    if msg.content_type == types.ContentType.TEXT:
        await bot.edit_message_reply_markup(msg.chat.id, message_id=msg.message_id - 1, reply_markup=None)
        await state.update_data(title=msg.text)
        await msg.answer("Записал")
        await msg.answer('Пожалуйста, выберите дату:', reply_markup=await SimpleCalendar().start_calendar())
        await state.set_state(Sates.Forma.date)
    else:
        await msg.answer(f"Вы отправили {msg.content_type}\n"
                         f"я могу обработать только текст")


@dp.callback_query_handler(text=["Назад в меню"], state=Sates.Forma.date)
async def back_main_menu(call: types.callback_query, state: FSMContext):
    await call.message.edit_text("Отправьте название задачи", reply_markup=Marcop.back_menu())
    await state.set_state(Sates.Forma.title)


@dp.callback_query_handler(simple_cal_callback.filter(), state=Sates.Forma.date)
async def process_simple_calendar(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        await state.update_data(date=date.strftime("%d/%m/%Y"))
        await call.message.edit_text("Выберите время: ",
                                     reply_markup=Marcop.timeInlineButton(hour=00, min=00))
        await state.set_state(Sates.Forma.time)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('time'), state=Sates.Forma.time)
async def callback_time(call: types.callback_query, state: FSMContext):
    select = call.data.split(':')[-1]
    hour = call.data.split(':')[1]
    min = call.data.split(':')[2]
    if select == 'select':
        await state.update_data(time=f'{hour}:{min}')
        data = await state.get_data()
        await call.message.edit_text("Проверьте правильность задачи:\n"
                                     f"<b> название задачи </b>: {data['title']}\n"
                                     f"<b> дата </b>: {data['date']}\n"
                                     f"<b> время </b>: {data['time']}", parse_mode='HTML',
                                     reply_markup=Marcop.confirmation())
    else:
        await call.message.edit_text('Выберите время: ', reply_markup=Marcop.timeInlineButton(int(hour), int(min)))


@dp.callback_query_handler(text=['Назад'], state=Sates.Forma.time)
async def callback_back(call: types.callback_query, state: FSMContext):
    await call.answer('Пожалуйста, выберите дату:', reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(Sates.Forma.date)


@dp.callback_query_handler(state=Sates.Forma.time)
async def callback_add_task(call: types.callback_query, state: FSMContext):
    if call.data == "Yes":
        data = await state.get_data()
        result = Connect_DataBase.all_Tasks_Write_Down(data['title'], data['date'], data['time'])
        if result == True:
            await call.message.edit_text("Отлично! Записал!", reply_markup=Marcop.Marcop_main())
            await state.finish()
        else:
            await call.message.edit_text("Ошибка! Не записал!", reply_markup=Marcop.Marcop_main())
            await state.finish()

    elif call.data == "No":
        await call.message.edit_text("Отмена записи", reply_markup=Marcop.Marcop_main())
        await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('Delete'))
async def callback_delete_task(call: types.callback_query):
    Task = call.data.split(',')[-1]
    Time = call.data.split(',')[-2]
    Data = call.data.split(',')[-3]
    try:
        Connect_DataBase.Delete_Task(Task, Data, Time)
    except:
        logging.error('Ошибка удаления задачи из базы данных')
    result = Connect_DataBase.Get_Data(Data)
    print(result)
    if result:
        await call.message.edit_text(f"Ваш список на {Data}",
                                     reply_markup=Marcop.marcop_task_list_today(result,
                                                                                int(call.data.split(',')[1])))
    else:
        await call.message.edit_text('Пожалуйста, выберите дату:', reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('task'))
async def callback_task(call: types.callback_query):
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
                                     reply_markup=Marcop.marcop_task_list_today(result,
                                                                                int(call.data.split(',')[1]) + 1))
    if call.data.split(',')[-2] == '-':
        result = Connect_DataBase.Get_Data(call.data.split(',')[-1])
        await call.message.edit_text(f"Ваш список на {call.data.split(',')[-1]}",
                                     reply_markup=Marcop.marcop_task_list_today(result,
                                                                                int(call.data.split(',')[1]) - 1))
    if call.data.split(',')[1] == 'select':
        Task = call.data.split(',')[-3]
        Time = call.data.split(',')[-1]
        Data = call.data.split(',')[-4]
        marcup = types.InlineKeyboardMarkup()
        await call.message.edit_text(f"Вот Ваша задача: \n"
                                     f"<b> название задачи </b>: {Task}\n"
                                     f"<b> дата </b>: {Data}\n"
                                     f"<b> время </b>: {Time}", parse_mode='HTML',
                                     reply_markup=Marcop.Button_Back_Inline_Time(marcup, call.data.split(',')[-2], Data,
                                                                                 Time, Task))


@dp.callback_query_handler(text=['Назад'])
async def callback_back(call: types.callback_query):
    await call.message.edit_text('Hi', reply_markup=Marcop.Marcop_main())


async def reminder():
    while True:
        now = datetime.now()
        time = now.strftime("%H:%M")
        date = now.strftime("%d/%m/%Y")
        if time == '12:00':
            results = Connect_DataBase.Get_Data(date)
            if results:
                message = f'Ваш список задач на {date}:\n'
                for i in range(0, len(results)):
                    message = message + f'\n{i + 1}) {results[i][0]} - Время: {results[i][1]}'
                await bot.send_message('437819952', message)
        await asyncio.sleep(60)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(reminder())
    executor.start_polling(dp, skip_updates=True)

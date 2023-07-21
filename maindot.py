from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from Log_Config import *


import Marcop
import Connect_DataBase
from datetime import datetime
import Sates




bot = Bot(token=open("Canfic.txt", mode="r").read())
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    await msg.answer('Hi', reply_markup=Marcop.Marcop_main())
    logging.info(f"Пользователь {msg.from_user.username} \n"
                 f"написал сообщение: {msg.text}")


@dp.message_handler(content_types=["text"])
async def main_menu(msg: types.Message, state: FSMContext):
    if msg.text == "Список задач📋":
        All_Tasks = Connect_DataBase.all_Tasks()
        if All_Tasks:
            Today = datetime.now().date().strftime('%d/%m/%Y')
            result = [task for task in All_Tasks if Today == task[1]]
            await msg.answer("Ваш список на сегодня", reply_markup=Marcop.marcop_task_list_today(result))
        else:
            await msg.answer("Задач нет")
    elif msg.text == "Добавить задачу📝":
        await msg.answer("Отправьте название задачи")
        await state.set_state(Sates.Forma.title)
    elif msg.text == "Удалить задачу❌":
        await msg.answer("Удалить задачу пока в разработке🤷🏻‍♀️........")
    elif msg.text == "Время🕓":
        await msg.answer("Время:",
                         reply_markup=Marcop.timeInlineButton(hour=00, min=00))


    else:
        await msg.answer(f"Вы отправили: <span class='tg-spoiler'><ins><i>{msg.text}</i></ins></span>",
                         parse_mode='HTML')


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
        result=Connect_DataBase.all_Tasks_Write_Down(data['title'], data['date'], data['time'])
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
    if call.data.split(',')[-1] == 'back':
        All_Tasks = Connect_DataBase.all_Tasks()
        if All_Tasks:
            Today = datetime.now().date().strftime('%d/%m/%Y')
            result = [task for task in All_Tasks if Today == task[1]]
            await call.message.edit_text("Ваш список на сегодня", reply_markup=Marcop.marcop_task_list_today(result))
        else:
            await call.message.edit_text("Задач нет")
    else:
        result=Connect_DataBase.Get_Task(call.data.split(',')[-1])

        Task = result[0][0]
        Time = result[0][1]
        Data = result[0][2]
        await call.message.edit_text(f"Вот Ваша задача: \n"
                                     f"<b> название задачи </b>: {Task}\n"
                                     f"<b> дата </b>: {Data}\n"
                                     f"<b> время </b>: {Time}", parse_mode='HTML',
                                     reply_markup=Marcop.Button_Back_Inline_Task())




@dp.callback_query_handler(text=['Назад'])
async def callback_back(call: types.callback_query):
    await call.message.delete()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

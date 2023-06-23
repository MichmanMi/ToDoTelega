from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


import logging
import Marcop
import Connect_DataBase
from datetime import datetime
import Sates

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("Error.log"),
                              logging.StreamHandler()])
bot = Bot(token=open("Canfic.txt",mode="r").read())
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
            await msg.answer("Ваш список на сегодня",reply_markup=Marcop.marcop_task_list_today(result))
        else:
            await msg.answer("Задач нет")
    elif msg.text == "Добавить задачу📝":
        await msg.answer("Отправьте название задачи")
        await state.set_state(Sates.Forma.title)
    elif msg.text == "Удалить задачу❌":
        await msg.answer("Удалить задачу пока в разработке🤷🏻‍♀️........")
    #2)отработчик кнопки "Время", которая выводит сообщение и инлайт кнопками
    else:
        await msg.answer(f"Вы отправили: <span class='tg-spoiler'><ins><i>{msg.text}</i></ins></span>", parse_mode='HTML')

@dp.message_handler(content_types=types.ContentType.ANY,state=Sates.Forma.title)
async def task_title(msg:types.Message, state: FSMContext):
    if msg.content_type == types.ContentType.TEXT:
        await state.update_data(title=msg.text)
        await msg.answer("Записал")
        await msg.answer("Отправье дату 'день/месяц/год'")
        await state.set_state(Sates.Forma.date)
    else:
        await msg.answer(f"Вы отправили {msg.content_type}\n"
                         f"я могу обработать только текст")

@dp.message_handler(content_types=types.ContentType.ANY,state=Sates.Forma.date)
async def task_title(msg:types.Message, state: FSMContext):
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

@dp.message_handler(content_types=types.ContentType.ANY,state=Sates.Forma.time)
async def task_title(msg:types.Message, state: FSMContext):
    if msg.content_type == types.ContentType.TEXT:
        if msg.text.find(":"):
            await state.update_data(time=msg.text)
            await msg.answer("Записал")
            data=await state.get_data()
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
async def callback_add_task(call:types.callback_query,state:FSMContext):
    if call.data == "Yes":
        await call.message.edit_text("Отлично! Записал!", reply_markup=None)
        await state.finish()
    elif call.data == "No":
        await call.message.delete()
        await state.finish()



if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)
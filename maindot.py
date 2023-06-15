from aiogram import Bot, Dispatcher, executor, types
import logging
import Marcop
import Connect_DataBase
from datetime import datetime


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("Error.log"),
                              logging.StreamHandler()])
bot = Bot(token=open("Canfic.txt",mode="r").read())
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    await msg.answer('Hi', reply_markup=Marcop.Marcop_main())
    logging.info(f"Пользователь {msg.from_user.username} \n"
                 f"написал сообщение: {msg.text}")

@dp.message_handler(content_types=["text"])
async def main_menu(msg: types.Message):
    if msg.text == "Список задач📋":
        Today = datetime.now().date().strftime('%d/%m/%Y')
        All_Tasks = Connect_DataBase.all_Tasks()
        result = [task for task in All_Tasks if Today == task[1]]
        await msg.answer("Ваш список на сегодня",reply_markup=Marcop.marcop_task_list_today(result))
    elif msg.text == "Добавить задачу📝":
        await msg.answer("Добавить задачу пока в разработке🤷🏻‍♀️........")
    elif msg.text == "Удалить задачу❌":
        await msg.answer("Удалить задачу пока в разработке🤷🏻‍♀️........")
    else:
        await msg.answer(f"Вы отправили: <span class='tg-spoiler'><ins><i>{msg.text}</i></ins></span>", parse_mode='HTML')


if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)
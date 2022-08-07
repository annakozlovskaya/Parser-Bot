import asyncio
from aiogram import types, executor, Dispatcher, Bot
from aiogram.utils.markdown import hbold, hunderline, hlink
from aiogram.dispatcher.filters import Text
from CONFIG import TOKEN, user_id
import json
import sqlite3
from parser_kwork import check_new_task_kwork
from parser_habr import check_new_task_habr

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



# Старт-команда, которая выводит краткое описание бота, меню
@dp.message_handler(commands='start')
async def start(message: types.Message):
    help_buttons = ['Kwork', 'Habr']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*help_buttons)
    await message.answer('Привет! я Бот, который отправляет тебе новые заказы с фриланс бирж.', reply_markup=keyboard)


    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute('''CREATE TABLE IF NOT EXISTS users_id(id INTEGER PRIMARY KEY AUTOINCREMENT)''')
    # connect.commit()
    # human_id = message.chat.id
    # cursor.execute(f'''SELECT id FROM users_id WHERE id = {human_id} ''')
    # data = cursor.fetchone()
    # if data is None:
    #     users_list = [message.chat.id]
    #     cursor.execute('''INSERT INTO users_id VALUES(?);''', users_list)
    #     connect.commit()



@dp.message_handler(Text(equals='Kwork'))
async def get_all_tasks(message: types.Message):

    with open('task_kwork_dict.json', encoding='utf-8') as file:
        task_kwork_dict = json.load(file)

    for k, v in sorted(task_kwork_dict.items()):
        tasks = f"{hlink(v['title'],v['link'])}\n"\
                f"{hunderline(v['price'])}"
        await message.answer(tasks)


@dp.message_handler(Text(equals='Habr'))
async def get_all_tasks(message: types.Message):
    with open('task_habr_dict.json', encoding='utf-8') as file:
        task_habr_dict = json.load(file)
    for k, v in sorted(task_habr_dict.items()):
        tasks = f"{hlink(v['title'],v['link'])}\n"\
                f"{hunderline(v['price'])}"
        await message.answer(tasks)


async def every_ten_minutes_kwork():
    while True:
        fresh_tasks_kwork = check_new_task_kwork()
        if len(fresh_tasks_kwork) >= 1:
            for k, v in sorted(fresh_tasks_kwork.items()):
                tasks = f"{hlink(v['title'], v['link'])}\n" \
                        f"{hunderline(v['price'])}"
                await bot.send_message(user_id, tasks)
        # else:
        #     await bot.send_message(user_id, 'nothing new on kwork', disable_notification=True)
        await asyncio.sleep(600)


async def every_ten_minutes_habr():
    while True:
        fresh_tasks_habr = check_new_task_habr()
        if len(fresh_tasks_habr) >= 1:
            for k, v in sorted(fresh_tasks_habr.items()):
                tasks = f"{hlink(v['title'], v['link'])}\n" \
                        f"{hunderline(v['price'])}"
                await bot.send_message(user_id, tasks)
        # else:
        #     await bot.send_message(user_id, 'nothing new on habr', disable_notification=True)
        await asyncio.sleep(500)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(every_ten_minutes_kwork())
    loop.create_task(every_ten_minutes_habr())
    executor.start_polling(dp)


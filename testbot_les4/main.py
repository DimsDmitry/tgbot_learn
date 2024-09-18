import telebot
import webbrowser  # для открытия веб-страниц
from telebot import types

import sqlite3

bot = telebot.TeleBot('7005730206:AAGt4kOBtnyNTllH7wy-lWQHInJwXoPlFNs')
name = None


@bot.message_handler(commands=['start'])
# при команде start создаётся таблица users с 3 полями
def start(message):
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))'
    )
    # сохраняет изменения
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите ваше имя:')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    # получаем текст введённый пользователем, записываем его в переменную
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите пароль:')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    # получаем текст введённый пользователем, записываем его в переменную
    password = message.text.strip()
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    # сохраняет изменения
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # вывести всех пользователей
    conn = sqlite3.connect('itproger.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)

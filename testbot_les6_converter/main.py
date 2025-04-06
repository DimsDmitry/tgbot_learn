import json

from telebot import *
import requests
from currency_converter import CurrencyConverter


bot = telebot.TeleBot('7530134956:AAG0eNszJK6lO3Hc_b-HiPdQRr6-8MZyWYQ')
# API = '135b46a59fd34bb8f2b485d430aa50d7'
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму')
        # след действие - эта же функция
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:

        markup = types.InlineKeyboardMarkup(row_width=2)  # сколько кнопок в одном ряду
        # кнопки
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение:', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0.')
        # след действие - эта же функция
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)  # ф-я фозвращает True
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэш')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    values = message.text.upper().split('/')
    res = currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
    bot.register_next_step_handler(message, summa)


bot.polling(none_stop=True)

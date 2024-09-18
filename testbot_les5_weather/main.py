import json

import telebot
import requests

bot = telebot.TeleBot('7415267101:AAHfwIAl8enL0QTUsMvr0tWcg4H_PVLfQ3g')
API = '135b46a59fd34bb8f2b485d430aa50d7'


@bot.message_handler(commands=['start'])
# при команде start - приветственное сообщение, запрос названия города
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    # bot.reply_to(message, f'Сейчас погода: {res.json()}')

    data = json.loads(res.text)
    bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]}')


bot.polling(none_stop=True)

# https://api.openweathermap.org/data/2.5/weather?q=London&appid={API key}

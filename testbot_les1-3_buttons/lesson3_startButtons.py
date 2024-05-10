import telebot
import webbrowser  # для открытия веб-страниц
from telebot import types

# bot = telebot.TeleBot('7000307834:AAFTB_6tcIWufjjYtNo6aNp4MTbmf4iBWco')


@bot.message_handler(commands=['start'])
# обработчик команды start, чтобы при запуске бота появлялись кнопки
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    file = open('photo.JPG', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    # соответственно есть методы send_video, audio и тд
    # bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    # функция будет срабатывать при вводе текста в чат 1 раз:
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is open😃')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Deleted')


@bot.message_handler(commands=['site', 'website'])
# при вызове одной из команд открывает веб-страницу в браузере
def site(message):
    webbrowser.open('https://itproger.com/')


@bot.message_handler(commands=['main', 'hello'])
def main(message):
    # стартовая функция
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')


@bot.message_handler(commands=['help'])
def main(message):
    # стартовая функция
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')


@bot.message_handler()
# пустые скобки - любые данные от пользователя
# метод с обработкой текста нужно сдвигать вниз
def info(message):
    # узнаём что вводит пользователь (параметр text)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        # метод reply_to - ответ на предыдущее сообщение
        bot.reply_to(message, f'ID: {message.from_user.id}')


# отслеживание отправки файла
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.google.ru/')
    # по умолчанию кнопки расставляются по рядам. изменим дизайн
    markup.row(btn1)  # в первом ряду одна кнопка
    btn2 = types.InlineKeyboardButton('Удалить фото:', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст:', callback_data='edit')
    markup.row(btn2, btn3)
    # во втором ряду две кнопки.
    # callback_data - подписка на функцию при нажатии кнопки
    bot.reply_to(message, f'Вы невероятно красивый, {message.from_user.first_name}!', reply_markup=markup)


# лямбда-функция - анонимная функция. Если значение будет пустым, возвращаем True
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        # если пользователь жмет на кнопку "удалить фото", удаляем сообщение
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        # message_id-1 - идентификатор предпоследнего сообщения
    elif callback.data == 'edit':
        # редактирование сообщения
        bot.edited_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


'''СОЗДАНИЕ КНОПОК'''
bot.polling(none_stop=True)

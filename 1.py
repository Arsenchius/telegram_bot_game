import requests
import telebot
from telebot import types
import sqlite3
import parsers
import json

token = '1812611840:AAHoHVMW7LB_clbUq5n3OErNLf6Sj2THlss'
bot = telebot.TeleBot(token)

# инициализируем соединение с БД
#sqlite_connection = sqlite3.connect('db.db')
#cursor = sqlite_connection.cursor()

name = '';

@bot.message_handler(content_types=['text'])
def start(message):
    global name
    if message.text == '/reg':
        payload = {'key': 'KeyPas', 'type': 'auth', 'id': message.from_user.id}
        r = requests.post('https://easy-choice.ru/bot/api.php', data=payload, verify=False)
        #print(r.text)
        temp = json.dumps(r.text)
        print(temp)
        bot.send_message(message.from_user.id, "Как мне тебя называть?");
        bot.register_next_step_handler(message, checker); #следующий шаг – функция get_name
    else:
        answer = parsers.main(message.text.lower())
        bot.send_message(message.from_user.id, answer);

def checker(message):
    global name
    name = message.text
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text = 'Да', callback_data = 'yes');
    key_no = types.InlineKeyboardButton(text = 'Нет', callback_data = 'no');
    keyboard.add(key_yes);
    keyboard.add(key_no);
    question = 'Твой никнейм ' + name + ' ?';
    bot.send_message(message.from_user.id, text=question,reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Напиши /reg');

bot.polling()
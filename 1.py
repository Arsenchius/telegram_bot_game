import pandas as pd
token = '1812611840:AAHoHVMW7LB_clbUq5n3OErNLf6Sj2THlss'
import telebot
from telebot import types
bot = telebot.TeleBot(token)
import parsers

name = '';
surname = '';
age = 0;

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        answer = parsers.main(message.text.lower())
        bot.send_message(message.from_user.id, answer);

def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами пожалуйста');
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text = 'Да', callback_data = 'yes');
    key_no = types.InlineKeyboardButton(text = 'Нет', callback_data = 'no');
    keyboard.add(key_yes);
    keyboard.add(key_no);
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?';
    bot.send_message(message.from_user.id, text=question,reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Напиши /reg');

bot.polling()
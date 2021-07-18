from types import SimpleNamespace
import requests
import telebot
from telebot import types
import parsers
import json

token = '1812611840:AAHoHVMW7LB_clbUq5n3OErNLf6Sj2THlss'
bot = telebot.TeleBot(token)

name = ''
id = -1
user = None
curr_pack = None
iterator = 0
score = 0

def request(pack):
    r = requests.post('https://easy-choice.ru/bot/api.php', data=pack, verify=False)
    temp = json.loads(r.text, object_hook=lambda d:SimpleNamespace(**d))
    return temp

@bot.message_handler(content_types=['text'])
def start(message):
    
    global name, user, id, curr_pack
    
    if message.text == '/auth':
        if id == -1:
            payload = {'key': 'KeyPas', 'type': 'auth', 'id': message.from_user.id}
            temp = request(payload)
            bot.send_message(message.from_user.id, "О привет "+temp.name+"\nТвой счёт сейчас : "+temp.score+"\nТвой ид в системе : "+temp.id + "\nДля начала игры пиши /game")
            id = temp.id
        else:
            bot.send_message(message.from_user.id, "Ты уже авторизиторан")
    
    elif message.text == "/info":
        if id != -1:
            temp = request({'key': 'KeyPas', 'type': 'info', 'id': id})
            bot.send_message(message.from_user.id, "Информация о "+temp.nick+"\nТвой счёт сейчас : "+temp.score+"\nТвой ид в системе : "+temp.id + "\nДля начала игры пиши /game")
        else:
           bot.send_message(message.from_user.id, "Тебе надо зарегаться или авторизоваться") 
    
    elif message.text == "/reg":
        if id == -1:
            bot.send_message(message.from_user.id, "Отлично, вводи свой ник")
            bot.register_next_step_handler(message, get_nick)
        else:
            bot.send_message(message.from_user.id, "Кажется ты уже авторизирован")
    
    elif message.text == '/start':
        user = message
        keyboard = types.InlineKeyboardMarkup();
        key_yes = types.InlineKeyboardButton(text = 'Регистрация', callback_data = 'reg');
        key_no = types.InlineKeyboardButton(text = 'Авторизация', callback_data = 'auth');
        keyboard.add(key_yes);
        keyboard.add(key_no);
        bot.send_message(message.from_user.id, 'Привет я игровой бот!\nДля начала игры тебе необходимо зарегистрироваться (/reg)\nЕсли ты уже играл ранее, то нажми авторизацию(/auth)', reply_markup=keyboard)
    
    elif message.text == "/game":
        if id != -1:
            user = message
            bot.send_message(message.from_user.id, 'Подожди немного, я готовлю для тебя набор вопросов...')
            pack = parsers.complite_pack(72)
            curr_pack = pack
            name1 = pack[0][0].name
            name2 = pack[0][1].name
            keyboard = types.InlineKeyboardMarkup()
            key_one = types.InlineKeyboardButton(text = name1.encode('cp1251').decode('utf8'), callback_data = 'first');
            key_two = types.InlineKeyboardButton(text = name2.encode('cp1251').decode('utf8'), callback_data = 'second');
            key_exit = types.InlineKeyboardButton(text = "Выйти", callback_data = 'exit')
            keyboard.add(key_one);
            keyboard.add(key_two);
            keyboard.add(key_exit);
            bot.send_message(message.from_user.id, 'Вопрос ('+str(iterator+1)+'/36)\nКак думаешь какое из этих слов чаще встречается в объявлениях на Avito.ru?', reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, 'Необходимо авторизироваться (/auth)')
    
    else:
        bot.send_message(message.from_user.id, 'Для начала игры напиши /game')

def get_nick(message):
    global id
    nick = message.text
    payload = {'key':"KeyPas","type":"regi", "nick":nick,"id":message.from_user.id}
    temp = request(payload)
    if temp.status == 500:
        bot.send_message(message.from_user.id,'Такой пользователь уже есть (/auth)')
    elif temp.status == 200:
        id = temp.id
        bot.send_message(message.from_user.id,'Отлично теперь ты есть в системе\nДля получения информации о себе напиши /info\nДля старта игры пиши /game')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global user,id,curr_pack,iterator,score

    if call.data == "reg":
        bot.send_message(user.from_user.id, "Отлично, вводи свой ник")
        bot.register_next_step_handler(user, get_nick)
    
    elif call.data == 'auth':
        payload = {'key': 'KeyPas', 'type': 'auth', 'id': user.from_user.id}
        temp = request(payload)
        bot.send_message(user.from_user.id, "О привет "+temp.name+"\nТвой счёт сейчас : "+temp.score+"\nТвой ид в системе : "+temp.id + "\nДля начала игры пиши /game")
        id = temp.id
    
    elif call.data == 'first':
        
        if curr_pack[iterator][0].count > curr_pack[iterator][1].count:
            bot.send_message(user.from_user.id, "О да\nВариант который ты выбрал встречался на сайте: " + str(curr_pack[iterator][0].count) + " раз!\nДругое: " + str(curr_pack[iterator][1].count) + " раз.")
            score+=1
        
        elif curr_pack[iterator][0].count < curr_pack[iterator][1].count:
            bot.send_message(user.from_user.id, "Увы...\nВариант который ты выбрал встречался на сайте: " + str(curr_pack[iterator][0].count) + " раз!\nДругое: " + str(curr_pack[iterator][1].count) + " раз.")
        
        elif curr_pack[iterator][0].count == curr_pack[iterator][1].count:
            score+=1
            bot.send_message(user.from_user.id, "Вау у нас ничья!\nНо я все равно дам тебе балл))\nОба слова встречались на сайте :"+str(curr_pack[iterator][0].count) + " раз" )

        iterator+=1
        
        if iterator != 35:
            name1 = curr_pack[iterator][0].name
            name2 = curr_pack[iterator][1].name
            keyboard = types.InlineKeyboardMarkup()
            key_one = types.InlineKeyboardButton(text = name1.encode('cp1251').decode('utf8'), callback_data = 'first')
            key_two = types.InlineKeyboardButton(text = name2.encode('cp1251').decode('utf8'), callback_data = 'second')
            key_exit = types.InlineKeyboardButton(text = 'выйти', callback_data = 'exit')
            keyboard.add(key_one)
            keyboard.add(key_two)
            keyboard.add(key_exit)
            bot.send_message(user.from_user.id, 'Вопрос ('+str(iterator+1)+'/36)\nКак думаешь какое из этих слов чаще встречается в объявлениях на Avito.ru?', reply_markup=keyboard)
        
        else:
            bot.send_message(user.from_user.id, 'Отлично, ты прошёл все вопросы которые я для тебя подготовил\nЕсли хочешь ещё поиграть пиши (/game)\nДля выхода пиши (/exit)')
            
    elif call.data == 'second':
        
        if curr_pack[iterator][1].count > curr_pack[iterator][0].count:
            bot.send_message(user.from_user.id, "О да\nВариант который ты выбрал встречался на сайте: " + str(curr_pack[iterator][1].count) + " раз!\nДругое: " + str(curr_pack[iterator][0].count) + " раз.")
            score+=1
        
        elif curr_pack[iterator][1].count < curr_pack[iterator][0].count:
            bot.send_message(user.from_user.id, "Увы...\nВариант который ты выбрал встречался на сайте: " + str(curr_pack[iterator][1].count) + " раз!\nДругое: " + str(curr_pack[iterator][0].count) + " раз.")
        
        elif curr_pack[iterator][1].count == curr_pack[iterator][0].count:
            score+=1
            bot.send_message(user.from_user.id, "Вау у нас ничья!\nНо мы все равно дадим тебе балл))\nОба слова встречались на сайте :"+str(curr_pack[iterator][0].count) + " раз" )

        iterator+=1

        if iterator != 35:
            name1 = curr_pack[iterator][0].name
            name2 = curr_pack[iterator][1].name
            keyboard = types.InlineKeyboardMarkup()
            key_one = types.InlineKeyboardButton(text = name1.encode('cp1251').decode('utf8'), callback_data = 'first')
            key_two = types.InlineKeyboardButton(text = name2.encode('cp1251').decode('utf8'), callback_data = 'second')
            key_exit = types.InlineKeyboardButton(text = 'выйти', callback_data = 'exit')
            keyboard.add(key_one)
            keyboard.add(key_two)
            keyboard.add(key_exit)
            bot.send_message(user.from_user.id, 'Вопрос ('+str(iterator+1)+'/36)\nКак думаешь какое из этих слов чаще встречается в объявлениях на Avito.ru?', reply_markup=keyboard)
        
        else:
            #сохранение резов тут
            bot.send_message(user.from_user.id, 'Отлично, ты прошёл все вопросы которые я для тебя подготовил\nЕсли хочешь ещё поиграть пиши (/game)\nДля выхода пиши (/exit)')

    elif call.data == "exit":
        temp = request({'key': 'KeyPas', 'type': 'updt', 'id': id,'up':score})
        bot.send_message(user.from_user.id, 'Твой результат:'+str(score)+'\nЕсли хочешь ещё поиграть пиши (/game)\nЧтобы получить свою статистику напиши (/info)')
        score = 0
        curr_pack = None

bot.polling()
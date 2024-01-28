import telebot
from telebot import types
from info import user_data, lok
import json
token = '6668531597:AAG8Uy3tgPBbuRKTeE7t9pGAd0eKtlsQySE'
bot = telebot.TeleBot(token)


def load_data():
    #чтение json файла
    try:
        with open('users.json', "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def save_data(data):
    #запись данных
    with open('users.json', "w") as f:
        json.dump(data, f)


@bot.message_handler(commands=['start'])
def handle_hi(message):
    bot.send_message(message.chat.id, 'Привет, это бот квест по вселенной ведьмака 🐺⚔️.'
                                      ' Чтобы начать игру воспользуйся командой /play.'
                                      ' Если для начала хочешь ознакомиться, то используй /help')
    save_user_name(message)



def save_user_name(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    data = load_data()
    user_data[user_id] = {}
    user_data[user_id]["user_id"] = user_id
    user_data[user_id]["name"] = name
    # data[str(user_id)] = {'Новиград': '', 'Арт Скелиге': '', 'Ундвик': 'Вампир', '': ''}
    save_data(user_data)
    print(user_data)


@bot.message_handler(commands=['play'])

def loc_Novigrad(message):
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[1]['Новиград']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[1]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket, reply_markup=kb)
    bot.register_next_step_handler(msg, con_1)
    save_data(data)


def con_1(message):
    if message.text == 'Отправится на Скелиге':
        loc_Scelige(message)
    elif message.text == 'Взять заказ в Новиграде':
        loc_att_place(message)

def loc_Scelige(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[2]['Скелиге']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[2]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket, reply_markup=kb)
    bot.register_next_step_handler(msg, con_2)
    save_data(data)


def con_2(message):
    if message.text == 'Помочь':
        loc_Undvic(message)
    elif message.text == "Вернуться в Новиград":
        loc_Novigrad(message)


def loc_Undvic(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[5]['Ундвик']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[5]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket, reply_markup=kb)
    bot.register_next_step_handler(msg, con_3)
    save_data(data)


def con_3(message):
    if message.text == 'Помочь сейчас':
        Undvic_good(message)
    elif message.text == 'Сразиться с великаном':
        Undvic_bad(message)


def Undvic_bad(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[8]['Ундвик плохой исход']['description']
    bot.send_message(message.chat.id, loket)
    save_data(data)


def Undvic_good(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[9]['Ундвик хороший исход']['description']
    bot.send_message(message.chat.id, loket)
    save_data(data)


def loc_att_place(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[3]['место нападения']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[3]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket, reply_markup=kb)
    bot.register_next_step_handler(msg, con_4)
    save_data(data)


def con_4(message):
    if message.text == 'Заготовить зелья и отправится по следам':
        battle(message)
    elif message.text == "Отправится на Скелиге":
        loc_Scelige(message)


def battle(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[4]['логово']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[4]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket, reply_markup=kb)
    data[str(user_id)]["loc4"] = message.text
    bot.register_next_step_handler(msg, con_5)
    save_data(data)


def con_5(message):
    if message.text == 'Отказаться':
        pub(message)
    elif message.text == 'Согласиться':
        enemy_lair(message)


def pub(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[6]['корчма']['description']
    bot.send_message(message.chat.id, loket)


def enemy_lair(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[7]['Убежище врага']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[7]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket, reply_markup=kb)
    data[str(user_id)]["loc4"] = message.text
    bot.register_next_step_handler(msg, con_6)
    save_data(data)


def con_6(message):
    if message.text == 'Убить Таулера':
        Caer_Morhen(message)
    elif message.text == 'Пощадить':
        tawerna(message)


def Caer_Morhen(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[10]['Ламбрет хороший исход']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[10]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket)
    data[str(user_id)]["loc4"] = message.text
    bot.register_next_step_handler(msg, con_5)
    save_data(data)


def tawerna(message):
    msg = None
    user_id = str(message.from_user.id)
    data = load_data()
    loket = lok[11]['Ламбрет плохой исход']['description']
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    for answer in lok[11]['answers']:
        kb.add(answer)
    msg = bot.send_message(message.chat.id, loket)
    data[str(user_id)]["loc4"] = message.text
    bot.register_next_step_handler(msg, con_5)
    save_data(data)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Я бот-квест. По задумке\n'
                                      ' игры ты находишься в фентези мире ведьмака.'
                                      ' Выбирай дальнейшие действия, опираясь'
                                      ' на интуицию и узнай, что будет дальше.'
                                      ' чтобы начать сначала, напиши /start.\n'
                                      ' Вот список функций бота 👇\n'
                                      '/help - список команд и справочная информация\n'
                                      '/start - регистрация и приветственное сообщение\n'
                                      '/play - начать игру\n'
                                      '/lore - немного информации о мире 🗺\n'
                                      '/bestiary - некоторые монстры, которые встретятся по сюжету 📖')

# if __name__ == "__bot__":
#     bot.infinity_polling(none_stop=True)
bot.infinity_polling()

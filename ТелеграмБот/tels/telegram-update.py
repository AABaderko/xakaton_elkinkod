import modules.telebot_data as tbd
import telebot
from telebot.types import (
    BotCommand,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import requests
from modules.bot_datasender import robot_stats

robot_directions = {
    -30: 30,
    -45: 45,
    -60: 60,
    -90: 90
}

URL = "http://127.0.0.1:8000/send_tg"
URL_bots = "http://127.0.0.1:5000/"
# r = requests.post(URL, data = {})

bot = telebot.TeleBot(tbd.token_id)
selectedRobot = None

commands = [
    BotCommand('getrobots', 'Получение списка роботов'),
    BotCommand('getrobotstrouble', 'Получение списка роботов в неисправности'),
    BotCommand('robotpos', 'Получение текущего положение робота'),
    BotCommand('robotstatus', 'Получение текущего состояния робота'),
    BotCommand('setrobotstatus', 'Задать текущее состояние робота'),
    BotCommand('setrobotdirection', 'Задать направление движения')
]
bot.set_my_commands( commands )

print("Run Telegram Bot EventListener")
print(bot.user.first_name)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Добро пожаловать в бота для управления роботами уборщиками, {message.chat.first_name}")
    print(f"Start message: {message.chat.id}")

@bot.message_handler(commands=['getrobots'])
def get_robots(message):
    requests.post(URL, data = {"msg_chat_id": message.chat.id,"func": "getRobotsNames"})
    print(f"Get robots message: {message.chat.id}")

@bot.message_handler(commands=['getrobotstrouble'])
def get_robots_in_trouble(message):
    requests.post(URL, data = {"msg_chat_id": message.chat.id,"func": "getRobotsInTrouble"})
    print(f"Get robots in trouble message: {message.chat.id}")

@bot.message_handler(commands=['robotpos'])
def get_robot_pos(message):
    global selectedRobot
    if not selectedRobot:
       bot.send_message(message.chat.id, "Не выбран робот")
       return
    requests.post(URL, data = {"msg_chat_id": message.chat.id, "bot_id": selectedRobot,"func": "getRobotPosition"})
    print(f"Get robot position: {message.chat.id}")

@bot.message_handler(commands=['robotstatus'])
def get_robot_status(message):
    global selectedRobot
    if not selectedRobot:
       bot.send_message(message.chat.id, "Не выбран робот")
       return
    requests.post(URL, data = {"msg_chat_id": message.chat.id, "bot_id": selectedRobot,"func": "getRobotStatus"})
    print(f"Get robot status: {message.chat.id}")

@bot.message_handler(commands=['setrobotstatus'])
def set_robot_status(message):
    global selectedRobot
    if not selectedRobot:
       bot.send_message(message.chat.id, "Не выбран робот")
       return
    
    markup = InlineKeyboardMarkup()
    for name in robot_stats:
        button = InlineKeyboardButton(text = name, callback_data=f"setStatus {name}")
        markup.add(button)

    bot.send_message(message.chat.id, 'Выберите режим управления', parse_mode='html', reply_markup=markup)
    print(f"Set robot status: {message.chat.id}")

@bot.message_handler(commands=['setrobotdirection'])
def set_robot_direction(message):
    global selectedRobot
    if not selectedRobot:
       bot.send_message(message.chat.id, "Не выбран робот")
       return
      
    markup = InlineKeyboardMarkup()
    for dir1, dir2 in robot_directions.items():
        button1 = InlineKeyboardButton(text = f'⬅️ {-dir1}', callback_data=f"setDirection {dir1}")
        button2 = InlineKeyboardButton(text = f'{dir2} ➡️', callback_data=f"setDirection {dir2}")
        markup.add(button1, button2)

    bot.send_message(message.chat.id, 'Выберите направление', parse_mode='html', reply_markup=markup)
    print(f"Set robot direction: {message.chat.id}")

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
  if function_call.message:
     message = function_call.message
     if function_call.data:
        data = function_call.data.split(" ")
        if data[0] == "selectRobot":
            global selectedRobot
            selectedRobot = data[1]

            bot.send_message(message.chat.id, f"Выбран робот под номером: {selectedRobot}")
            print(f"Robot selected: {message.chat.id}")
        elif data[0] == "setStatus":
            # requests.post(URL_bots, data = {"bot_id": selectedRobot, "status": data[1]})
            
            bot.send_message(message.chat.id, "Режим был изменён")
            print(f"Status selected: {message.chat.id}")
        elif data[0] == "setDirection":

            bot.send_message(message.chat.id, "Направление было изменено")
            print(f"Direction changed: {message.chat.id}")

bot.polling(none_stop=True, interval=1)
    
    
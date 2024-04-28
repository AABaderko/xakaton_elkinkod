from django.shortcuts import render

from django.http import HttpResponse

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .models import (
    RobotsData,
    RobotsInfo
)

import modules.telebot_data as tbd
import telebot
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

bot = telebot.TeleBot(tbd.token_id)

botsInTroubleList = []

import json

def sendTelegramMessage(bot_id, text):
    if not (bot_id in botsInTroubleList):
        bot.send_message(tbd.user_id, f"Робот уборщик с индентификатором: {bot_id}\n"+text)
        botsInTroubleList.append(bot_id)


@never_cache
@csrf_exempt
def update_data(request):
    if len(request.POST) > 0:
        json_data = request.POST.get('json', '')
        if json_data:
            


            sended_data = json.loads(json_data)
            print(sended_data)
            # bot.send_message(tbd.user_id, f"https://yandex.ru/maps/?ll={sended_data['location']['long']}%2C{sended_data['location']['lat']}&mode=whatshere&whatshere%5Bpoint%5D={sended_data['location']['long']}%2C{sended_data['location']['lat']}&whatshere%5Bzoom%5D=20&z=20")

            bot_id = sended_data['id']
            objects_find = RobotsInfo.objects.filter(bot_id=bot_id).values()
            if objects_find:
                botInTrouble = False

                object_last = objects_find[len(objects_find)-1]
                if ( sended_data['movement_direction'] == 'forward' or
                        sended_data['movement_direction'] == 'backward' ):
                    if ( sended_data['location']['lat'] == object_last['latitude'] and
                            sended_data['location']['long'] == object_last['longitude'] ):
                        sendTelegramMessage(bot_id, "Прекратил движение")
                        botInTrouble = True
                elif ( sended_data['direction']['pitch'] > 0,785398 or
                    sended_data['direction']['pitch'] < -0,785398 ):
                    sendTelegramMessage(bot_id, "Перевернулся")
                    botInTrouble = True
                
                if not botInTrouble:
                    if bot_id in botsInTroubleList:
                        botsInTroubleList.remove(bot_id)
                        bot.send_message(tbd.user_id, f"Робот уборщик с индентификатором: {bot_id}\nВозобновил работу")
                RobotsInfo.info_manager.add_info(sended_data)
            else:
                RobotsInfo.info_manager.add_info(sended_data)
    return HttpResponse('')


@never_cache
@csrf_exempt
def send_tg(request):
    if len(request.POST) > 0:
        function_name = request.POST.get('func', '')
        if function_name:
            print(function_name)
            message_chat_id = request.POST.get('msg_chat_id')
            if function_name == "getRobotsNames":
                robots_list = RobotsData.objects.all()
                markup = InlineKeyboardMarkup()

                for data in robots_list.values():
                    button_text = str(data['id'])+'. '+data['name']
                    button = InlineKeyboardButton(text = button_text, callback_data=f"selectRobot {data['id']}")
                    markup.add(button)
                
                bot.send_message(message_chat_id, 'Выберите робота', parse_mode='html', reply_markup=markup)
            elif function_name == "getRobotsInTrouble":
                robots_list = RobotsData.objects.all()
                text_troubles = ""
                for robot_data in robots_list.values():
                    bot_id = robot_data['id']
                    robot_infos = RobotsInfo.objects.filter(bot_id=bot_id).values()

                    if len(robot_infos) == 0: continue

                    object_last = robot_infos[len(robot_infos)-1]
                    object_pre_last = None
                    if len(robot_infos) > 1:
                        object_pre_last = robot_infos[len(robot_infos)-2]

                    if ( object_last['movement_direction'] == 'forward' or
                        object_last['movement_direction'] == 'backward' ):
                        if object_pre_last:
                            if ( object_last['latitude'] == object_pre_last['latitude'] and
                                object_last['longitude'] == object_pre_last['longitude'] ):
                                text_troubles += f"Робот уборщик: \"{bot_id}. {robot_data['name']}\"\nПрекратил движение\n"
                    elif ( object_last['pitch'] > 0,785398 or
                        object_last['pitch'] < -0,785398 ):
                            text_troubles += f"Робот уборщик: \"{bot_id}. {robot_data['name']}\"\nПеревернулся\n"
                bot.send_message(message_chat_id, text_troubles or "Все роботы в исправном состоянии")
            elif function_name == "getRobotPosition":
                bot_id = request.POST.get('bot_id', '')
                if bot_id:
                    robot_data = RobotsInfo.objects.filter(bot_id=bot_id).values()
                    if robot_data:
                        robot_data_n = RobotsData.objects.filter(id=bot_id).values()[0]
                        robot_last = robot_data[len(robot_data)-1]
                        URL_ya = f"https://yandex.ru/maps/?ll={robot_last['longitude']}%2C{robot_last['latitude']}&mode=whatshere&whatshere%5Bpoint%5D={robot_last['longitude']}%2C{robot_last['latitude']}&whatshere%5Bzoom%5D=20&z=20"
                        bot.send_message(message_chat_id, f"Текущее положение робота \"{robot_data_n['name']}\", указано на карте:\n{URL_ya}")
                    else:
                        bot.send_message(message_chat_id, f"Не найдено последнего положения робота")
            elif function_name == "getRobotStatus":
                bot_id = request.POST.get('bot_id', '')
                if bot_id:
                    robot_data = RobotsInfo.objects.filter(bot_id=bot_id).values()
                    if robot_data:
                        robot_data_n = RobotsData.objects.filter(id=bot_id).values()[0]
                        robot_last = robot_data[len(robot_data)-1]
                        bot.send_message(
                            message_chat_id,
                            f"Имя робота: {robot_data_n['name']}\nСтатус управления: {robot_last['status']}\nЗаряд батареи: {robot_last['battery_capacity']}\nПоложение робота: {robot_last['latitude']}, {robot_last['longitude']}\nТекущая задача: {robot_last['task']}\nНаправление движения: {robot_last['movement_direction']}\nФары включены: {robot_last['light_state']}"
                        )
        # print(request.POST)
    return HttpResponse('')
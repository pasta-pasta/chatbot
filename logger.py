import asyncio
import datetime

import time
import random
import requests

import sys

from misc import find_value

#Данный класс обрабатывает все логи, в нем происходит вся основная логика приложения.

class Logger:
    def __init__(self, listener):
        self.listener = listener

    async def handle_log(self, event_type, object_data, misc_inf=None): #основная функция, которая вызывает вторичные в зависимости от типа лога
        print(f"Обрабатываю лог! {event_type}, {object_data}")
        if event_type == "message_new":
            await self.log_msg(object_data)
        elif event_type == "command":
            await self.log_command(object_data) 


    async def log_command(self, object_data): #Обратаывает команду. Получает все данные о команде, и вызывает нужную функцию
        user_id = find_value(object_data, "from_id") #айди юзера, который отправил команду
        peer = find_value(object_data, "peer_id") - 2000000000 #айди чата, в котором была отправлена команда
        text = find_value(object_data, "text")[1:] 
        parts = text.split(" ", 1) 
        command = parts[0].lower() #название команды
        date = find_value(object_data, "date")
        if time.time() - date > 6:
            return
        arguments = parts[1] if len(parts) > 1 else None #аргументы команды
        #if find_value(object_data, "reply_message"):
        #   arguments = str(find_value(find_value(object_data, "reply_message"), "from_id")) Данный фрагмент кода меняет аргументы команды на айди пользователя, на сообщение которого был ответ. Можно включить, если в качестве аргументов передаются айдишники.
        print(f"AAAAAH {text}")
        chat = self.listener.main.chats[peer] #чат, в котором была отправлена команда в виде класса, можно вызывать методы.


        match command:
            case "init":
                pass #имплементация команд



    async def log_msg(self, object_data): #Обработка сообщений, если боту нужно постоянно следить за любыми сообщениями, не только командами.
        from_id = find_value(object_data, "from_id")
        peer = find_value(object_data, "peer_id")-2000000000
        message_id = find_value(object_data, "conversation_message_id")
        text = find_value(object_data, "text")
        date = find_value(object_data, "date")
        user = self.listener.main.chats[peer].users[from_id]
        chat = self.listener.main.chats[peer]
        #получены все данные, делай с ними че хочешь

import datetime

from icecream import ic


import requests
import asyncio
import aiohttp
import aiohttp_requests
import user
from logger import Logger
import sys
from misc import find_value

#Данный класс -- обработчик апдейтов. Он принимает апдейты, и, в зависимости от типа, вызывает нужные функции.

class Listener:
    def __init__(self, token, panopticon):
        self.token = token
        self.logger = Logger(self)
        self.main = panopticon

    async def handle_update(self, update):
        event_type = update['type']
        object_data = update['object']

        # Забирает айди пользователя и чата 
        from_id = find_value(object_data, 'from_id')
        try:
            peer_id = int(find_value(object_data, 'peer_id'))
        except:
            peer_id = None
        print(f"Поймал апдейт! {update}")
        if event_type == "message_new":

            if (peer_id-2000000000) not in self.main.chats.keys():
                self.main.initialize_chat(peer_id-2000000000) #инициализируем чат, если его нет 

            if from_id not in self.main.chats[peer_id-2000000000].users.keys(): #инициализируем (приветствуем) юзера, если его нет в чате
                self.main.chats[peer_id-2000000000].fetch_users()
                await self.logger.handle_log("join", object_data)

            if find_value(object_data, "text"):
                if find_value(object_data, "text").lower() == "_init": #инициализация бота в чате. Команда init может быть применена от любого пользователя, 
                                                                            #ибо, пока бот не инициализирован, он не может отличить админов от не админов.
                    await self.logger.handle_log("command", object_data)
                elif find_value(object_data, "text")[0] == "_" and (self.main.chats[peer_id-2000000000].users[from_id].is_admin): #Инициализация команды. Префикс -- "_", можно изменить. Справа праверка на админа, можно убрать
                    await self.logger.handle_log("command", object_data)


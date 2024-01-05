import datetime
import random

import aiohttp
import aiohttp_requests
import requests
from user import User

#Класс для чата. Тут происходит все взаимодействие с вк апи в плане отправки сообщений и получения данных о пользователях

class Chat:
    def __init__(self,token, group_chat_id=None, bootlog = True):
        self.token = token
        self.chat_id = group_chat_id
        self.users = {}
        self.fetch_users()
        self.bootlog = bootlog


    def fetch_users(self): #получение данных о пользователях. Добавляет их в массив users, обьекты класса User. У них есть поле is_admin, которое используется для проверки команд.
        self.users = {}
        params = {
            'peer_id': self.chat_id+2000000000,
            'fields': 'id, is_admin',  # Тут можно добавить другие поля, если нужно
            'access_token': self.token,
            'v': '5.130'
        }
        response = requests.get(
            'https://api.vk.com/method/messages.getConversationMembers', params=params)
        data = response.json()

        if 'response' in data and 'items' in data['response']:
            for item in data['response']['items']:
                user_id = item['member_id']
                is_admin = 'is_admin' in item and item['is_admin']
                new_user = User(user_id, is_admin)
                self.users[user_id] = new_user

    def fetch_user_ids(self): #возвращает список пользователей в виде цифровых айди
        users = []
        params = {
            'peer_id': self.chat_id + 2000000000,
            'fields': 'id',  # Тут можно добавить другие поля, если нужно
            'access_token': self.token,
            'v': '5.130'
        }
        response = requests.get(
            'https://api.vk.com/method/messages.getConversationMembers', params=params)
        data = response.json()

        if 'response' in data and 'items' in data['response']:
            for item in data['response']['items']:
                user_id = item['member_id']
                users.append(user_id)
        return users

    async def send_message(self, message): #отправляет сообщение в чат
        params = {
            'chat_id': self.chat_id,
            'message': F"{datetime.datetime.now()} \n {message}", #первый фрагмент строки -- текущее время, можно убрать
            'access_token': self.token,
            "random_id": random.randint(1, 1000000000),
            'v': '5.130'
        }


        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post('https://api.vk.com/method/messages.send', params=params) as response:
                return await response.json()
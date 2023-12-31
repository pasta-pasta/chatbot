import asyncio
import json
import os
import random
import re
import time

import requests

import chat
import listener
import logger
import sys

#Этот класс -- синхронизатор между всеми частями приложения. 

class bot:
    def __init__(self, token: str):
        self.token = token
        self.chats = self.load_chats()
        self.listener = listener.Listener(self.token, self)
        self.logger = self.listener.logger

    async def init(self):
        for i in self.chats.values():
            await self.initialize_chat(i)

    async def initialize_chat(self, new_chat):
        if isinstance(new_chat, int):
            new_chat = chat.Chat(self.token, new_chat)  #Эта функция инициализирует все чаты, которые есть в словаре чатов. Также может быть вызвана внешне, и вызывается при добавлении бота в новый чат.
            self.chats[new_chat.chat_id] = new_chat
        if new_chat.bootlog:
            pass #соо о включениии

    def shutdown(self):
        for i in self.chats.values():
            if i.bootlog:
                pass  # соо о выключениии
        self.save_chats() #сохранение чатов, и, если нужно, соо о выключении

    #логика сохранений и загрузки чатов
    def save_chats(self):
        chat_data = []
        for chat in self.chats.values():
            chat_data.append({
                'chat_id': chat.chat_id,
                "bootlog": chat.bootlog
            })
        try:
            with open("chats.json", 'w') as file:
                json.dump(chat_data, file)
        except:
            with open("chats_temp.json", 'w') as file:
                json.dump(chat_data, file)
            os.rename("chats_temp.json", "chats.json")

    def load_chats(self):
        chat_dic = {}
        print("CHATS ARE LOADING!")
        try:
            with open("chats.json", 'r') as file:
                chat_data = json.load(file)
                print(f"CATHED DATA: {chat_data}")
                for data in chat_data:
                    chat_dic[data['chat_id']] = chat.Chat(self.token, data['chat_id'], data["bootlog"])
        except FileNotFoundError:
            chat_dic = {}
            print("FILE NOT FOUND!")
        return chat_dic


    def extract_id(self, tag): #вытаскивает айди из тега (вк передает тег формата @tag как [@tag|id123123123]. функция вытаскивает айди)
        if isinstance(tag, int):
            return tag
        elif isinstance(tag, str):
            try:
                return int(tag)
            except:
                match = re.search(r'id(\d+)', tag)
                if not match:
                    match = re.search(r'club(\d+)', tag)
                return int(match.group(1)) if match else None
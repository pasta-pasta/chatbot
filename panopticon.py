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


class Panopticon:
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
            new_chat = chat.Chat(self.token, new_chat)
            self.chats[new_chat.chat_id] = new_chat
        if new_chat.bootlog:
            pass #соо о включениии

    async def shutdown(self):
        for i in self.chats.values():
            if i.bootlog:
                pass  # соо о выключениии
        self.save_chats()


    def save_chats(self):
        chat_data = []
        for chat in self.chats.values():
            chat_data.append({
                'chat_id': chat.chat_id,
                "bootlog": chat.bootlog
            })
        try:
            with open("/home/panopticon/utils/chats.json", 'w') as file:
                json.dump(chat_data, file)
        except:
            with open("/home/panopticon/utils/chats_temp.json", 'w') as file:
                json.dump(chat_data, file)
            os.rename("/home/panopticon/utils/chats_temp.json", "/home/panopticon/utils/chats.json")

    def load_chats(self):
        chat_dic = {}
        print("CHATS ARE LOADING!")
        try:
            with open("/home/panopticon/utils/chats.json", 'r') as file:
                chat_data = json.load(file)
                print(f"CATHED DATA: {chat_data}")
                for data in chat_data:
                    chat_dic[data['chat_id']] = chat.Chat(self.token, data['chat_id'], data['logging'], data['working'], data["strict"], data["bootlog"])
        except FileNotFoundError:
            chat_dic = {}
            print("FILE NOT FOUND!")
        return chat_dic


    def extract_id(self, tag): #вытаскивает айди из тега
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
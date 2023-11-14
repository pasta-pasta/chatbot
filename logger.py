import asyncio
import datetime

import time
import random
import requests

import sys

from misc import find_value


class Logger:
    def __init__(self, listener):
        self.listener = listener

    async def handle_log(self, event_type, object_data, misc_inf=None):
        print(f"Обрабатываю лог! {event_type}, {object_data}")
        if event_type == "message_new":
            await self.log_msg(object_data)
        elif event_type == "command":
            await self.log_command(object_data)


    async def log_command(self, object_data):
        user_id = find_value(object_data, "from_id")
        peer = find_value(object_data, "peer_id") - 2000000000
        text = find_value(object_data, "text")[1:]
        parts = text.split(" ", 1)
        command = parts[0].lower()
        date = find_value(object_data, "date")
        if time.time() - date > 6:
            return
        arguments = parts[1] if len(parts) > 1 else None
        if find_value(object_data, "reply_message"):
            arguments = str(find_value(find_value(object_data, "reply_message"), "from_id"))
        print(f"AAAAAH {text}")
        chat = self.listener.main.chats[peer]


        if command == "exile":
            pass #имплементируй логику команд, лучше чере з switch

        self.listener.main.save_chats()


    async def log_msg(self, object_data):
        from_id = find_value(object_data, "from_id")
        peer = find_value(object_data, "peer_id")-2000000000
        message_id = find_value(object_data, "conversation_message_id")
        text = find_value(object_data, "text")
        date = find_value(object_data, "date")
        user = self.listener.main.chats[peer].users[from_id]
        chat = self.listener.main.chats[peer]
        #получены все данные, делай с ними че хочешь

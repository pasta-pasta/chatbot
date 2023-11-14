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


class Listener:
    def __init__(self, token, panopticon):
        self.token = token
        self.logger = Logger(self)
        self.main = panopticon

    async def handle_update(self, update):
        event_type = update['type']
        object_data = update['object']

        # Extract the from_id and peer_id
        from_id = find_value(object_data, 'from_id')
        try:
            peer_id = int(find_value(object_data, 'peer_id'))
        except:
            peer_id = None
        print(f"Поймал апдейт! {update}")
        if event_type == "message_new":
            if peer_id:
                # If peer_id is available, it's a conversation
                context_id = peer_id
            else:
                # Fallback to the group_id if peer_id is not available
                context_id = update['group_id']

            if (peer_id-2000000000) not in self.main.chats.keys():
                self.main.initialize_chat(peer_id-2000000000)

            if from_id not in self.main.chats[peer_id-2000000000].users.keys():
                self.main.chats[peer_id-2000000000].fetch_users()

            if find_value(object_data, "text"):
                if find_value(object_data, "text").lower() == "_init":
                    await self.logger.handle_log("command", object_data)
                elif find_value(object_data, "text")[0] == "_" and (self.main.chats[peer_id-2000000000].users[from_id].is_admin):
                    await self.logger.handle_log("command", object_data)
            elif from_id not in self.main.chats[peer_id-2000000000].users.keys():
                await self.logger.handle_log("join", object_data)
                self.main.chats[peer_id-2000000000].fetch_users()


#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Type 'quit' to quit ...
class IRCMockUp():
    def __init__(self, bot):
        # Class attributes
        self.bot = bot
        # Init
        bot.start = self.start # Override start function to avoid connection try

    def start(self):
        # Init
        admin = self.bot.info.ADMIN_NICKNAME
        bot = self.bot.info.BOT_NICKNAME
        mklutra = self.bot.info.LUTRA_NICKNAME
        # Room Mock-Up initialization
        self.bot.room = RoomMockUp("Mock-Up Room", admin, bot, mklutra, "http://127.0.0.1:14623", [admin, bot, mklutra])
        # Supervisor initialization
        self.bot.load_supervisor(self.bot.room)
        # Loop
        input = raw_input()
        while(input != "quit"):
            if(input == "!uptime"):
                self.bot.get_uptime()
            self.bot.supervisor.on_room_message(input, admin, "00:00")
            input = raw_input()

class RoomMockUp():
    def __init__(self, room_name, admin_username, bot_username, lutra_username, website_url, user_list):
        self.room_name = room_name
        self.admin_username = admin_username
        self.bot_username = bot_username
        self.lutra_username = lutra_username
        self.user_list = user_list
        self.website_url = website_url

    def send(self, msg):
        print msg.decode("utf8")

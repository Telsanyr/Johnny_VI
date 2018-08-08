#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

class Room():
    def __init__(self, serv, room_name, admin_username, bot_username, lutra_username, website_url, user_list):
        # Class attributes
        self.serv = serv
        self.room_name = room_name
        self.admin_username = admin_username
        self.bot_username = bot_username
        self.lutra_username = lutra_username
        self.website_url = website_url
        self.user_list = user_list
        # Init
        LOGGER.info("Welcome in ["+self.room_name+"]")
        LOGGER.info("Connected users: " + str(self.user_list))

    def on_user_joined(self, user):
        LOGGER.info("User (" + str(user) + ") joined the room.")
        for u in self.user_list:
            if user == u:
                LOGGER.warning("User (" + str(user) + ") is already in the user list.")
                return
        self.user_list.append(user)
        LOGGER.info("Connected users: " + str(self.user_list))

    def on_user_left(self, user):
        LOGGER.info("User (" + str(user) + ") left the room.")
        present = False
        for u in self.user_list:
            if user == u:
                present = True
                break
        if present:
            self.user_list.remove(user)
            LOGGER.info("Connected users: " + str(self.user_list))
        else:
            LOGGER.warning("User (" + str(user) + ") was not found in user list.")

    def send(self, msg):
        self.serv.privmsg(self.room_name, msg.decode("utf8"))

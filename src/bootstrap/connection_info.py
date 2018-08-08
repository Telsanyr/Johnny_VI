#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import os
import json

class ConnectionInfo():
    def __init__(self):
        # Class attributes
        self.IRC_HOST_IP = "irc.freenode.net"
        self.IRC_HOST_PORT = 6667
        self.IRC_ACCOUNT_USERNAME = ""
        self.IRC_ACCOUNT_PASSWORD = ""
        self.ACTIVE_ROOM = ""
        self.DEBUG_ROOM = ""
        self.ADMIN_NICKNAME = ""             # Nickname, can change
        self.BOT_NICKNAME = ""               # Nickname, can change
        self.LUTRA_NICKNAME = ""             # Nickname, can change
        self.WEBSITE_URL = "http://127.0.0.1:14623"

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        return self.__dict__

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.__dict__.update(data)

    # ------------------------------------------------------------------------ #
    # --- JSON Serialization                                               --- #
    # ------------------------------------------------------------------------ #
    def json_export(self, file):
        if os.path.isfile(file):
            with open(file, 'w') as f:
                data = self.get_dictionary()
                json.dump(data, f, sort_keys=True, indent=4)
                f.close()

    def json_import(self, file):
        if os.path.isfile(file):
            with open(file, 'r') as f:
                data = json.load(f)
                self.from_dictionary(data)
                f.close()

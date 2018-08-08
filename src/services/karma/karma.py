#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "1.0.3"

# Database Paths
DATABASE_FILE = '../database/services/karma/karma.json'

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.karma = KarmaRoomModel()
        self.karma.json_import(DATABASE_FILE) # Load model from database

    def process(self, msg, user):
        update_database = True

        if msg == "!karma":         # Show individual karma
            self._send(self.karma.show_user(user))
        elif msg == "!karmas":      # Show everyone karma
            self._send(self.karma.show())
        elif "nazi" in msg:
            self.karma.get_user(user).add_karma(1)
        else:
            # Nothing has been done in this service, do not update database
            update_database = False

        # Update database if necessary
        if update_database:
            self.karma.json_export(DATABASE_FILE)

#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "1.5.2"

# Database Paths
DATABASE_FILE = '../database/services/ideabox/ideabox.json'
DATABASE_WEB_COPY_FILE = './web/client/db/ideabox.json'

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.ideabox = IdeaBoxTableModel()
        self.ideabox.json_import(DATABASE_FILE)             # Load model from database
        self.ideabox.json_export(DATABASE_WEB_COPY_FILE)    # Initialise web client database

    def process(self, msg, user):
        update_database = True

        if msg == "!ideabox":
            self._send(str(self.room.website_url) + "/ideabox")
        elif msg.startswith("!ideabox new "):
            self._send("Cette commande n'existe plus gros. (!help)")
        elif msg.startswith("!idea "):
            descr = msg[5:len(msg)]
            id = self.ideabox.add_idea(descr)
            self._send(self.ideabox.show_idea(id))
        elif msg.startswith("!ideabox vote "):
            idx = msg[14:len(msg)]
            self.ideabox.vote_idea(idx, 1)
            self._send(self.ideabox.show_idea(idx))
        elif msg.startswith("!ideabox archive "):
            idx = msg[17:len(msg)]
            self.ideabox.archive_idea(idx)
            self._send(self.ideabox.show_idea(idx))
        else:
            # Nothing has been done in this service, do not update database
            update_database = False

        # Update database if necessary
        if update_database:
            self.ideabox.json_export(DATABASE_FILE)
            self.ideabox.json_export(DATABASE_WEB_COPY_FILE)    # Export for web client

#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "0.1.0"

# Database Paths
DATABASE_FILE = '../database/services/dynamic-commands/dcmds.json'
DATABASE_WEB_COPY_FILE = './web/client/db/dcmds.json'

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.table = DynamicCommandTableModel()
        self.table.json_import(DATABASE_FILE)             # Load model from database
        self.table.json_export(DATABASE_WEB_COPY_FILE)    # Initialise web client database

    # ------------------------------------------------------------------------ #
    # --- AbstractFeature implementation                                   --- #
    # ------------------------------------------------------------------------ #
    # @Override
    def process(self, msg, user):
        update_database = True

        if msg.startswith("!setcmd "):
            descr = msg[8:len(msg)]
            cmd = (descr.split(' '))[0]
            answer = descr[len(cmd)+1:len(msg)]
            self.table.set_cmd(cmd, answer)
        elif msg.startswith("!"):
            cmd = msg[1:len(msg)]
            answer = self.table.call_cmd(cmd)
            if answer != None:
                self._send(answer)
            else:
                # Nothing has been done in this service, do not update database
                update_database = False
        else:
            # Nothing has been done in this service, do not update database
            update_database = False

        # Update database if necessary
        if update_database:
            self.table.json_export(DATABASE_FILE)
            self.table.json_export(DATABASE_WEB_COPY_FILE)    # Export for web client

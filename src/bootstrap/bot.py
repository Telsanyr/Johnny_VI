#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import imp # Used to be able to import the supervisor on the fly (and re-import it on demand)
import os
import time
import traceback
from threading import Timer
from datetime import datetime
from datetime import timedelta

# Already loaded libs (they will not be reload, it is only for name linkage)
import ircbot
import irclib

# Supervisor lib path
SUPERVISOR_LOADER_PATH = './src/supervisor/supervisor_loader.py'

# Bootstrap version
BOOTSTRAP_VERSION = "1.3.0"

# Logger
LOGGER = Logger('./logs/bootstrap-logs.txt')

# Databases (Connection Info)
PRODUCTION_CONNECTION_FILE = '../database/bootstrap/prod_connection.json'
DEBUG_CONNECTION_FILE = '../database/bootstrap/debug_connection.json'

# Folders that need to be created
FOLDERS_NEEDED = ['./logs',
                './web/client/db',
                './web/client/db/events']

# Bot Core commands :
#   !update                 for reloading supervisor live
#   !uptime                 give bot uptime
#   !switch debug           switch on debug room
#   !switch standard        switch on standard room
class Bot(ircbot.SingleServerIRCBot):
    def __init__(self, mock_up, debug_mode):
        # Class attributes
        self.VERSION = BOOTSTRAP_VERSION
        self.info = ConnectionInfo()
        self.room = None
        self.supervisor = None
        self.start_time = time.time()
        # Folders creation (need before any log)
        for folder in FOLDERS_NEEDED:
            if not os.path.exists(folder):
                os.makedirs(folder)
        # Init
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info("        __      __                         _    ______  ")
        LOGGER.info("       / /___  / /_  ____  ____  __  __   | |  / /  _/  ")
        LOGGER.info("  __  / / __ \/ __ \/ __ \/ __ \/ / / /   | | / // /    ")
        LOGGER.info(" / /_/ / /_/ / / / / / / / / / / /_/ /    | |/ // /     ")
        LOGGER.info(" \____/\____/_/ /_/_/ /_/_/ /_/\__, /     |___/___/     ")
        LOGGER.info("                              /____/                    ")
        LOGGER.info("--------------------------------------------------------")
        LOGGER.info("Bootstrap Version: "+ self.VERSION)
        LOGGER.info("")
        # Connection info from database
        LOGGER.info("Retrieving connection information..")
        if debug_mode:
            self.info.json_import(DEBUG_CONNECTION_FILE)
        else:
            self.info.json_import(PRODUCTION_CONNECTION_FILE)
        # Mock-up
        if mock_up:
            LOGGER.info("Mock-up mode.")
            mockup = IRCMockUp(self)
        else:
            LOGGER.info("Connecting..")
            # Inheritance
            ircbot.SingleServerIRCBot.__init__(self, [(self.info.IRC_HOST_IP, self.info.IRC_HOST_PORT, self.info.IRC_ACCOUNT_PASSWORD)],
                    self.info.BOT_NICKNAME, self.info.IRC_ACCOUNT_USERNAME)

    # @return status: True if loading successful
    def load_supervisor(self, room):
        LOGGER.info("Loading Supervisor...")
        # Catch any syntax error from module loading (but KeyboardInterrupt & SystemExit).
        # The bootstrap must SURVIVE !
        try:
            # Load Supervisor
            Supervisor = imp.load_source('supervisor_loader', SUPERVISOR_LOADER_PATH).Supervisor # Supervisor load on the fly
            self.supervisor = Supervisor(room)
            return True
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # Loading failed
            LOGGER.error("Fail to load Supervisor")
            LOGGER.error( traceback.format_exc())
            self.supervisor = None
            return False

    def switch_channel(self, serv, room_name):
        LOGGER.info( "Leave current room ["+self.room.room_name+"]")
        serv.part(self.room.room_name, "Bye")
        LOGGER.info( "- - - - - - - - - - - - - - - - - - - - - - - - - - ")
        LOGGER.info( "Joining room ["+room_name+"]")
        serv.join(room_name)

    def get_uptime(self):
        t = timedelta(seconds=(time.time() - self.start_time)) # use str() on this to display HH:MM:SS.ffff
        date = datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.room.send(str(self.info.BOT_NICKNAME) + ' is up since ' + str(date) + ' (uptime: '+ str(t) + ')')

    # ----------------------------------------------
    # --- IRC EVENTS LISTENERS                   ---
    # ----------------------------------------------
    # IRC CONNECTION [LISTENER]
    def on_welcome(self, serv, ev):
        LOGGER.info( "Connected !")
        serv.nick(self.info.BOT_NICKNAME) # Rename ?
        LOGGER.info( "Joining room ["+self.info.ACTIVE_ROOM+"]")
        serv.join(self.info.ACTIVE_ROOM)

    # THE BOT JOINED THE ROOM [LISTENER]
    def on_endofnames(self, serv, ev):
        args = ev.arguments()
        # Room initialization
        self.room = Room(serv, ev.arguments()[0], self.info.ADMIN_NICKNAME, self.info.BOT_NICKNAME, self.info.LUTRA_NICKNAME, self.info.WEBSITE_URL, self.channels[args[0]].users())
        # Supervisor initialization
        self.load_supervisor(self.room)

    # A USER JOINED THE ROOM [LISTENER]
    def on_join(self, serv, ev):
        user = irclib.nm_to_n(ev.source())
        if self.room != None:
            self.room.on_user_joined(user)

    # A USER LEFT THE ROOM [LISTENER]
    def on_part(self, serv, ev):
        user = irclib.nm_to_n(ev.source())
        self.room.on_user_left(user)

    # A USER LEFT IRC [LISTENER]
    def on_quit(self, serv, ev):
        user = irclib.nm_to_n(ev.source())
        self.room.on_user_left(user)

    # PRIVATE MESSAGES [LISTENER]
    def on_privmsg(self, serv, ev):
        message = ev.arguments()[0]
        if message == "!switch debug": # Switch on debug chan
            self.switch_channel(serv, self.info.DEBUG_ROOM)
        elif message == "!switch standard": # Switch on standard chan
            self.switch_channel(serv, self.info.ACTIVE_ROOM)
        # else ignore any other private message

    # MESSAGES IN ROOM [LISTENER]
    def on_pubmsg(self, serv, ev):
        message = ev.arguments()[0]
        user = irclib.nm_to_n(ev.source())
        timestamp = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f')
        # TODO check room
        if message == "!update": # Reload all services on the fly
            success = self.load_supervisor(self.room)
            if success:
                self.supervisor.status() # Show new loaded services
            else:
                self.room.send(str(self.info.BOT_NICKNAME) + " intellect update failed. Bypass all functionalities. " + str(self.info.BOT_NICKNAME) + " is now a vegetable.")
        elif message == "!uptime":
            self.get_uptime()
        elif message == "!switch debug": # Switch on debug chan
            self.switch_channel(serv, self.info.DEBUG_ROOM)
        elif message == "!switch standard": # Switch on standard chan
            self.switch_channel(serv, self.info.ACTIVE_ROOM)
        elif self.supervisor != None:
            self.supervisor.on_room_message(message, user, timestamp)

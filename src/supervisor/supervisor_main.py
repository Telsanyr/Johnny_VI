#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Already loaded libs (they will not be reload, it is only for name linkage)
import bootstrap_module

# Supervisor Version
SUPERVISOR_VERSION = "1.2.2"

# Logger
LOGGER = bootstrap_module.Logger('./logs/supervisor-logs.txt')

class Supervisor():
    def __init__(self, room):
        # Class attributes
        self.VERSION = SUPERVISOR_VERSION
        self.room = room
        self.services = []
        # Init
        LOGGER.info("Supervisor (v" + self.VERSION + "): Initialization")
        # New services should be added there
        self.services.append(ServiceProxy("Core", "./src/services/core/core.py", True))
        self.services.append(ServiceProxy("ElSpanishRigolator", "./src/services/others/elspanishrigolator.py", False))
        self.services.append(ServiceProxy("Flatterie", "./src/services/others/flatterie.py", False))
        self.services.append(ServiceProxy("Karma", "./src/services/karma/service_loader.py", True))
        self.services.append(ServiceProxy("IdeaBox", "./src/services/ideabox/service_loader.py", True))
        self.services.append(ServiceProxy("PokemOnIRC", "./src/services/pokemonirc/service_loader.py", True))
        self.services.append(ServiceProxy("Morse", "./src/services/others/morse.py", True))
        self.services.append(ServiceProxy("SpotifyForPleb", "./src/services/others/spotifyforpleb.py", True))
        self.services.append(ServiceProxy("DynamicCommands", "./src/services/dynamic-commands/service_loader.py", True))
        #self.services.append(ServiceProxy("Chiantos", "./src/services/others/chiantos.py", False))
        #self.services.append(ServiceProxy("CrashTest", "./src/services/others/crashtest.py", True))

        # Load all services
        for service in self.services:
            LOGGER.info("> Loading service [" + service.name + "]")
            success = service.load(room)
            if not success:
                LOGGER.error("Fail to load [" + service.name + "]")

    # Reload a specific
    def reload(self, name):
        for service in self.services:
            if service.name.lower() == name.lower():
                LOGGER.info("> Reloading service [" + service.name + "]")
                success = service.load(self.room)
                if success:
                    self.room.send(str(service.name) + " updated: "+service.status())
                else:
                    LOGGER.error("Fail to reload [" + service.name + "]")
                    self.room.send(str(service.name) + " could not be updated: R.I.P (LOL learn 2 code noob)")

    def status(self):
        my_status = "Supervisor (v" + self.VERSION + "): "
        for service in self.services:
            my_status += service.status() + '   '
        self.room.send(my_status)

    def on_room_message(self, msg, user, time):
        if msg.lower() == "!status":
            self.status()
        elif msg.startswith("!update "):
            self.reload(msg[8:len(msg)])
        else:
            for service in self.services: # Trigger toutes les services
                if service.listener != None:
                    service.listener._on_msg(msg, user)

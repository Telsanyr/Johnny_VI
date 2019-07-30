#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import imp

# Already loaded libs (they will not be reload, it is only for name linkage)
import bootstrap_module
import supervisor_module

# Service version
SERVICE_VERSION = "1.4.2"

# Logger
LOGGER = bootstrap_module.Logger('./logs/pokemonirc-logs.txt')

# Databases Paths
PLAYERS_DATABASE_FILE = '../database/services/pokemonirc/players.json'
PLAYERS_DATABASE_WEB_COPY_FILE = './web/client/db/players.json'
EVENTS_DATABASE_PATH = '../database/services/pokemonirc/'
EVENTS_DATABASE_WEB_COPY_PATH = './web/client/db/events/'
POKEMONS_DATABASE_FILE = './src/services/pokemonirc/pokemons.json' # Static database
POKEMONS_DATABASE_WEB_COPY_FILE = './web/client/db/pokemons.json'

# Initialize singleton classes
POKEMONS.INITIALIZE()

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.engine = GameEngine(room)

    # @return (boolean): True if the msg is a call to the command 'word'
    #                   (if the message is exactly the word or the word plus a
    #                   blank character plus some arguments.)
    def isCommand(self, word, msg):
        l = len(word)
        return msg.startswith(word) and (msg[l:l+1] == ' ' or msg[l:l+1] == '')

    # Escape the blank character following the command word.
    def getCommandArguments(self, word, msg):
        return msg[len(word)+1:len(msg)]

    # ------------------------------------------------------------------------ #
    # --- AbstractFeature implementation                                   --- #
    # ------------------------------------------------------------------------ #
    # @Override
    def dispose(self):
        self.engine.tall_grass.stop() # Otherwise the respawn mechanism will not stop

    # @Override
    def process(self, msg, user):
        # Game commands
        if self.isCommand("!stats", msg):
            self.engine.output.display_STATS()

        elif self.isCommand("!catch", msg): # Try to enroll to catch a pokemon in arena
            self.engine.interpreter.catch(user, args = self.getCommandArguments("!catch", msg))

        elif self.isCommand("!pokedex", msg):
            self.engine.interpreter.pokedex(user, self.getCommandArguments("!pokedex", msg))

        elif self.isCommand("!pokestuff", msg):
            self.engine.interpreter.pokestuff(user, self.getCommandArguments("!pokestuff", msg))

        elif self.isCommand("!crush", msg):
            self.engine.interpreter.crush(user, self.getCommandArguments("!crush", msg))

        elif self.isCommand("!open lootbox", msg):
            self.engine.interpreter.open_lootbox(user)

        elif self.isCommand("!evolve", msg):
            self.engine.interpreter.evolve(user, self.getCommandArguments("!evolve", msg), POKESTUFFS.MOONSTONE)

        elif self.isCommand("!moonevolve", msg):
            self.engine.interpreter.evolve(user, self.getCommandArguments("!moonevolve", msg), POKESTUFFS.MOONSTONE)

        elif self.isCommand("!thunderevolve", msg):
            self.engine.interpreter.evolve(user, self.getCommandArguments("!thunderevolve", msg), POKESTUFFS.THUNDERSTONE)

        elif self.isCommand("!fireevolve", msg):
            self.engine.interpreter.evolve(user, self.getCommandArguments("!fireevolve", msg), POKESTUFFS.FIRESTONE)

        elif self.isCommand("!waterevolve", msg):
            self.engine.interpreter.evolve(user, self.getCommandArguments("!waterevolve", msg), POKESTUFFS.WATERSTONE)

        elif self.isCommand("!pokemon", msg):
            self.engine.interpreter.pokemon(self.getCommandArguments("!pokemon", msg))

        elif self.isCommand("!buy barbapapa", msg):
            self.engine.interpreter.buy(user, self.getCommandArguments("!buy barbapapa", msg), POKESTUFFS.BARBAPAPA)

        elif self.isCommand("!buy pokeball", msg):
            self.engine.interpreter.buy(user, self.getCommandArguments("!buy pokeball", msg), POKESTUFFS.POKEBALL)

        elif self.isCommand("!buy superball", msg):
            self.engine.interpreter.buy(user, self.getCommandArguments("!buy superball", msg), POKESTUFFS.SUPERBALL)

        # Admin commands
        elif self.isCommand("!force arena", msg):
            self.engine.interpreter.admin_force_arena(user)

        elif self.isCommand("!force fouras", msg):
            self.engine.interpreter.admin_force_fouras(user)

        # Deprecated commands
        elif self.isCommand("!broyer", msg): # Try to enroll to catch a pokemon in arena
            self.engine.output.warning_DEPRECATED_COMMAND_BROYER()
            self.engine.interpreter.crush(user, self.getCommandArguments("!broyer", msg))

        elif self.isCommand("?pokemon", msg):
            self.engine.output.warning_DEPRECATED_COMMAND_POKEMON()
            self.engine.interpreter.pokemon(self.getCommandArguments("?pokemon", msg))


        # Messages
        if user == self.room.lutra_username:
            self.engine.link_cable.soul_mate_listener(msg)
        else:
            # If there is any activity other than mklutra,
            self.engine.tall_grass.trigger() # Trigger a new tall grass event manually for every new message
            self.engine.tall_grass.refresh() # Refresh the tall grass for the next hour
            self.engine.riddle.try_answer(msg, user)

#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# This is a module loader. It will reload all the files dedicated to the module
# each time it is reloaded. Therefore, any code modification will be taken into
# account.
# Moreover, because all files are loaded in the same module. All classes and
# global variables are reachable by any other file. When using a module class
# which is outside your file, you do not need to import it.
# However when modifying or adding a new file, you must take care that you do
# not override existing class/variable in the module, outside of your code file.

# Libs imports
import imp

# "pokemonirc_module" is built from all files in pokemonirc folder (apart from the loader)
SERVICE_PATH = "./src/services/pokemonirc/"
imp.load_source("pokemonirc_module", SERVICE_PATH + "pokemons.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "pokestuffs.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "lootboxes.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "tall_grass_deamon.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "link_cable.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "players_models.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "command_interpreter.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "game_output.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "fouras_riddle.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "arena.py")
imp.load_source("pokemonirc_module", SERVICE_PATH + "game_engine.py")
Service = imp.load_source("pokemonirc_module", SERVICE_PATH + "pokemonirc.py").Service

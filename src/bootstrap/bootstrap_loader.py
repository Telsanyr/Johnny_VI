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

# IRC Libs
LIBS_PATH = "./libs/"
imp.load_source("irclib", LIBS_PATH + "irclib.py")
imp.load_source("ircbot", LIBS_PATH + "ircbot.py")

# "bootstrap_module" is built from all files in bootstrap folder (apart from the loader)
BOOTSTRAP_PATH = "./src/bootstrap/"
imp.load_source("bootstrap_module", BOOTSTRAP_PATH + "logger.py")
imp.load_source("bootstrap_module", BOOTSTRAP_PATH + "room.py")
imp.load_source("bootstrap_module", BOOTSTRAP_PATH + "connection_info.py")
imp.load_source("bootstrap_module", BOOTSTRAP_PATH + "irc_mock_up.py")
imp.load_source("bootstrap_module", BOOTSTRAP_PATH + "bot.py")

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

# "ideabox_module" is built from all files in ideabox folder (apart from the loader)
SERVICE_PATH = "./src/services/ideabox/"
imp.load_source("ideabox_module", SERVICE_PATH + "ideabox_models.py")
Service = imp.load_source("ideabox_module", SERVICE_PATH + "ideabox.py").Service

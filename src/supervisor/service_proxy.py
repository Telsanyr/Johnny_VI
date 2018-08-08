#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import imp # Used to be able to import services on the fly (and re-import it on demand)
import traceback

class ServiceProxy():
    def __init__(self, name, path, default_activation):
        # Class attributes
        self.name = name
        self.path = path
        self.default_activation = default_activation
        self.listener = None

    def status(self):
        if self.listener != None:
            return self.listener._get_status()
        else:
            return "[" + self.name + ": MISSING]"  # TODO pas ici ?

    # @return status: True if loading is successful
    def load(self, room):
        # Catch any syntax error from module loading (but KeyboardInterrupt & SystemExit). The main core must SURVIVE !
        try:
            # Begin by disposing old listener
            if self.listener != None:
                self.listener.dispose()
            # Load python module
            # /!\ In order to avoid loading every services in the same module, we use the service name as a module name
            # Otherwise, all services would have been loaded in the same module (e.g. the same context) and some
            # service's global variables could override others.
            Service = imp.load_source(self.name.lower()+'_loader',  self.path).Service
            # Add listener
            self.listener = Service(self.name, room, self.default_activation)
            return True
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # Loading failed
            self.listener = None
            LOGGER.error( traceback.format_exc() )
            return False

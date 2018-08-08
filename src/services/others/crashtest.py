#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "0.0.1"

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.caca = pipi # Syntax Error qui fait planter au loading

    def process(self, msg, user):
        if msg == "!crash":
            # Code qui fait planté pour tester l'encapsulation des modules
            mots = ["jaja"]
            mots.remove("yo")

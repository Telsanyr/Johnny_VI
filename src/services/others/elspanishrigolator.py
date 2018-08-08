#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "1.4.0"

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.dict = ["hah", "xax", "mdr", "XD", "x)", "xD", "xd", "HAH", "jaj", "JAJ",
            "LOL", "lol", ":D", "8D", "hih", "heh", "ptdr", "xpldr", "lul", "loul",
            "^^", "^_^"]


    def process(self, msg, user):
        for mot in self.dict:
            if mot.lower() in msg:
                self._send("Jajaja")
                return

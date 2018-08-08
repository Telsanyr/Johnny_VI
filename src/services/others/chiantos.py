#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import random

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "1.3.0"

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.enter_proba = 0.01
        self.leave_proba = 0.1
        self.triggered = False
        self.target = ""

    def process(self, msg, user):
        if self.triggered:
            if self.target == user:
                self._send(msg)
                self.try_end()
        else:
            self.try_start(user)
        return

    def try_start(self, user):
        if random.random() <= self.enter_proba:
            self.triggered = True
            self.target = user
        return

    def try_end(self):
        if random.random() <= self.leave_proba:
            self.triggered = False
        return

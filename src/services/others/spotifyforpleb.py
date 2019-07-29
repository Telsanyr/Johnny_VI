#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import re

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "1.0.0"

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION

    def process(self, msg, user):
        matchs = re.search("spotify:track:(\w*)",msg)
        if matchs != None:
            result = "https://open.spotify.com/track/" + matchs.group(1)
            self._send(result)

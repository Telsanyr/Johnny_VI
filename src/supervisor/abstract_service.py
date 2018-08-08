#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import traceback

class AbstractService():
    def __init__(self, name, room, active):
        # Class attributes
        self.FEATURE_NAME = name
        self.VERSION = ""                    # @Abstract: Must be override by children classes
        self.room = room
        self.active = active
        self.ded = False

    # ----------------------------------------------
    # --- Public                                 ---
    # ----------------------------------------------
    def process(self, msg, user):   # @Abstract: Must be override by children classes
        # Not Implemented Yet
        return

    def dispose(self):              # @Abstract: Must be override by children classes
        # Not Implemented Yet
        return

    # ----------------------------------------------
    # --- Private                                ---
    # ----------------------------------------------
    def _send(self, msg):
        self.room.send(msg)

    def _get_status(self):
        status = "OFF"
        if self.active:
            status = "ON"
        if self.ded:
            status = "R.I.P"
        return "["+self.FEATURE_NAME+" "+self.VERSION+": "+status+"]"

    def _activate(self, msg):
        on_cmd = ("!enable "+self.FEATURE_NAME).lower()
        off_cmd = ("!disable "+self.FEATURE_NAME).lower()
        if msg.lower() == on_cmd:
            self.active = True
            self._send(self._get_status())
        elif msg.lower() == off_cmd:
            self.active = False
            self._send(self._get_status())

    def _on_msg(self, msg, user):
        self._activate(msg)
        if (not self.ded) and self.active:
            # Catch any errors from module but KeyboardInterrupt & SystemExit. The main core must SURVIVE !
            try:
                self.process(msg, user)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                # Module is ded, kill it !
                LOGGER.error(traceback.format_exc())
                self.ded = True
                self._send(self._get_status())
        else:
            pass # This module is desactivated (ded or inactive)

#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
from threading import Timer

# TallGrassDeamon Class
#
# Once it is started, this deamon will call a callback function every 30 seconds for 1 hour (120 calls)
# The callback is a call to 'onTallGrassEvent' function on a Callbackable object
# You can refresh this deamon for the next hour
# You can stop it at any moment, once stopped it cannot be started or refresh anymore
class TallGrassDeamon():
    def __init__(self, callbackable):
        # Class attributes
        self.callbackable = callbackable
        self.started = False
        self.ded = False
        self.count = 120

    # ------------------------------------------------------------------------ #
    # --- Private                                                          --- #
    # ------------------------------------------------------------------------ #
    # Will be run every 30sec
    def _run(self):
        if not self.ded:
            if self.count >= 1:
                self.trigger()
                self.count -= 1
                timer = Timer(30, self._run)
                timer.start()
            else:
                self.started = False

    # ------------------------------------------------------------------------ #
    # --- Public                                                           --- #
    # ------------------------------------------------------------------------ #
    def start(self):
        self.refresh()

    def refresh(self):
        self.count = 120 # Reset for the next 120 * 30 = 3600 seconds (1 hour) (with 30sec inaccuracy, because we do not know when will happen the next _run)
        if not self.started:
            self.started = True
            timer = Timer(30, self._run)
            timer.start()

    def trigger(self):
        self.callbackable.onTallGrassEvent()

    def stop(self):
        self.ded = True

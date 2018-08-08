#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import traceback
import time
from datetime import datetime

class Logger():
    def __init__(self, file):
        # Class attributes
        self.LOG_FILE_PATH = file

    # ------------------------------------------------------------------------ #
    # --- Private                                                          --- #
    # ------------------------------------------------------------------------ #
    def _log(self, message):
        try:
            with open(self.LOG_FILE_PATH, "a") as myfile:
                myfile.write(message + '\n')
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # We can't log it because logger is broken, so we print it
            print "ERROR: unable to log message"
            print traceback.format_exc()

    # ------------------------------------------------------------------------ #
    # --- Public                                                           --- #
    # ------------------------------------------------------------------------ #
    def info(self, message):
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        self._log("[" + str(timestamp) + "][INFO]: " + str(message))

    def warning(self, message):
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        self._log("[" + str(timestamp) + "][WARNING]: " + str(message))

    def error(self, message):
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        self._log("[" + str(timestamp) + "][ERROR]: " + str(message))

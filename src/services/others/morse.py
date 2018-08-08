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
        self.table = [["", ""], [" ", " "], ["A", "._"],["B", "_..."], ["C", "_._."], ["D", "_.."], ["E", "."],
                ["F", ".._."], ["G", "__."], ["H", "...."], ["I", ".."], ["J", ".___"],
                ["K", "_._"], ["L", "._.."], ["M", "__"], ["N", "_."], ["O", "___"],
                ["P", ".__."], ["Q", "__._"], ["R", "._."], ["S", "..."], ["T", "_"],
                ["U", ".._"], ["V", "..._"], ["W", ".__"], ["X", "_.._"], ["Y", "_.__"],
                ["Z", "__.."]]

    def find(self, word):
        for translation in self.table:
            if translation[1] == word:
                return translation[0]
        return "?"

    def process(self, msg, user):
        if re.match("^[._/ ]+$",msg) != None:
            letter = ""
            result = ""
            for character in msg:
                if character == "." or character == "_":
                    letter += character
                elif character == "/": # end of letter
                    result += " " + self.find(letter)
                    letter = ""
                # ignore spaces
            #Last letter
            result += " " + self.find(letter)
            self._send(result)

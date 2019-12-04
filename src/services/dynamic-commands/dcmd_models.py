#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import os
import json

class DynamicCommandModel():
    def __init__(self, cmd, answer):
        # Class attributes
        self.cmd = cmd
        self.answer = answer
        self.active = True

    def to_string(self):
        return "[cmd: !"+str(self.cmd)+", answer: "+str(self.answer)+", active: "+str(self.active)+"]"

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        return self.__dict__

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.__dict__.update(data)

class DynamicCommandTableModel():
    def __init__(self):
        # Class attributes
        self.dcmds = []

    def set_cmd(self, cmd, answer):
        for dcmd in self.dcmds:
            if dcmd.cmd == cmd:
                dcmd.answer = answer
                dcmd.active = True
                return
        self.dcmds.append(DynamicCommandModel(cmd, answer))

    def call_cmd(self, cmd):
        for dcmd in self.dcmds:
            if dcmd.cmd == cmd:
                return dcmd.answer
        return None

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        # We can't use directly the __dict__ without modifying the object, they are linked, we must copy it
        # This is not a deepcopy (see https://docs.python.org/2/library/copy.html), it is ok for this case but be careful when copying this code
        data = self.__dict__.copy()
        data["dcmds"] = [] # Must be exported in dictionary manualy
        for dcmd in self.dcmds:
            data["dcmds"].append(dcmd.get_dictionary())
        return data

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.dcmds = [] # Reset
        for element in data["dcmds"]:
            item = DynamicCommandModel("","")
            item.from_dictionary(element)
            self.dcmds.append(item)

    # ------------------------------------------------------------------------ #
    # --- JSON Serialization                                               --- #
    # ------------------------------------------------------------------------ #
    def json_export(self, file):
        # W : Overwrites the file if the file exists. If the file does not exist, creates a new file for writing.
        with open(file, 'w') as f:
            data = self.get_dictionary()
            json.dump(data, f, sort_keys=True, indent=4)
            f.close()

    def json_import(self, file):
        if os.path.isfile(file):
            with open(file, 'r') as f:
                data = json.load(f)
                self.from_dictionary(data)
                f.close()

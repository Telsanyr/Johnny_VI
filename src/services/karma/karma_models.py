#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import os
import json

class KarmaUserModel():
    def __init__(self, username):
        # Class attributes
        self.username = username
        self.karma = 0 # Amount of karma for this user

    def add_karma(self, amount):
        self.karma += amount

    def to_string(self):
        return "[_"+str(self.username)+": "+str(self.karma)+"]"

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        return self.__dict__

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.__dict__.update(data)

class KarmaRoomModel():
    def __init__(self):
        # Class attributes
        self.users = []   # List of KarmaUserModel

    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        # User not found
        user = KarmaUserModel(username)
        self.users.append(user)
        return user

    def show(self):
        s = "Karma scores: "
        for user in self.users:
            s += user.to_string() + " "
        return s

    def show_user(self, username):
        return self.get_user(username).to_string()

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        data = []
        for user in self.users:
            data.append(user.get_dictionary())
        return data

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.users = [] # Reset
        for element in data:
            user = KarmaUserModel("Unknown")
            user.from_dictionary(element)
            self.users.append(user)

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

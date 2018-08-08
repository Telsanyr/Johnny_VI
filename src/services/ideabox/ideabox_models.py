#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import os
import json

class IdeaBoxItemModel():
    def __init__(self, id, description, vote):
        # Class attributes
        self.id = id                    # Must be a string
        self.description = description
        self.vote = vote
        self.archive = False

    def to_string(self):
        return "[ID: "+self.id+", Votes: "+str(self.vote)+", "+self.description+"]"

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        return self.__dict__

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.__dict__.update(data)

class IdeaBoxTableModel():
    def __init__(self):
        # Class attributes
        self.last_id = -1
        self.ideas = []

    def add_idea(self, description):
        self.last_id += 1
        self.ideas.append(IdeaBoxItemModel(str(self.last_id), description, 0))
        return self.last_id

    def vote_idea(self, id, vote):
        for idea in self.ideas:
            if idea.id == id:
                idea.vote += vote
                break

    def archive_idea(self, id):
        for idea in self.ideas:
            if idea.id == id:
                idea.archive = True
                return

    def show_idea(self, id):
        for idea in self.ideas:
            if idea.id == str(id):
                return idea.to_string()
        return "[UNKNOWN IDEA]"

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        # We can't use directly the __dict__ without modifying the object, they are linked, we must copy it
        # This is not a deepcopy (see https://docs.python.org/2/library/copy.html), it is ok for this case but be careful when copying this code
        data = self.__dict__.copy()
        data["ideas"] = [] # Must be exported in dictionary manualy
        for idea in self.ideas:
            data["ideas"].append(idea.get_dictionary())
        return data

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.last_id = data["last_id"]
        self.ideas = [] # Reset
        for element in data["ideas"]:
            item = IdeaBoxItemModel("-1","",0)
            item.from_dictionary(element)
            self.ideas.append(item)

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

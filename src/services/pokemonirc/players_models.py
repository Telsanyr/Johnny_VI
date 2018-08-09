#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import os
import json

class PokestuffModel():
    def __init__(self):
        # Class attributes
        self.barbapapa = 0
        self.pokeball = 0
        self.superball = 0
        self.kebab = 0
        self.moonstone = 0
        self.thunderstone = 0
        self.firestone = 0
        self.waterstone = 0
        self.lootbox = 0

    def add_pokestuff(self, pokestuff, amount):
        if pokestuff == POKESTUFFS.BARBAPAPA:
            self.barbapapa += amount
        elif pokestuff == POKESTUFFS.POKEBALL:
            self.pokeball += amount
        elif pokestuff == POKESTUFFS.SUPERBALL:
            self.superball += amount
        elif pokestuff == POKESTUFFS.KEBAB:
            self.kebab += amount
        elif pokestuff == POKESTUFFS.MOONSTONE:
            self.moonstone += amount
        elif pokestuff == POKESTUFFS.THUNDERSTONE:
            self.thunderstone += amount
        elif pokestuff == POKESTUFFS.FIRESTONE:
            self.firestone += amount
        elif pokestuff == POKESTUFFS.WATERSTONE:
            self.waterstone += amount
        elif pokestuff == POKESTUFFS.LOOTBOX:
            self.lootbox += amount
        else:
            LOGGER.error( "Unable to add pokestuff, unknwon pokestuff")

    def add_barbapapa(self, n):
        self.barbapapa += n

    def add_pokeball(self, n):
        self.pokeball += n

    def add_superball(self, n):
        self.superball += n

    def add_kebab(self, n):
        self.kebab += n

    def add_moonstone(self, n):
        self.moonstone += n

    def add_thunderstone(self, n):
        self.thunderstone += n

    def add_firestone(self, n):
        self.firestone += n

    def add_waterstone(self, n):
        self.waterstone += n

    def add_lootbox(self, n):
        self.lootbox += n

    def use_barbapapa(self):
        if self.barbapapa > 0:
            self.barbapapa -= 1
            return True
        else:
            return False

    def use_pokeball(self):
        if self.pokeball > 0:
            self.pokeball -= 1
            return True
        else:
            return False

    def use_superball(self):
        if self.superball > 0:
            self.superball -= 1
            return True
        else:
            return False

    def use_kebab(self):
        if self.kebab > 0:
            self.kebab -= 1
            return True
        else:
            return False

    def use_kebabs(self, amount):
        if self.kebab >= amount:
            self.kebab -= amount
            return True
        else:
            return False

    def use_moonstone(self):
        if self.moonstone > 0:
            self.moonstone -= 1
            return True
        else:
            return False

    def use_thunderstone(self):
        if self.thunderstone > 0:
            self.thunderstone -= 1
            return True
        else:
            return False

    def use_firestone(self):
        if self.firestone > 0:
            self.firestone -= 1
            return True
        else:
            return False

    def use_waterstone(self):
        if self.waterstone > 0:
            self.waterstone -= 1
            return True
        else:
            return False

    def use_lootbox(self):
        if self.lootbox > 0:
            self.lootbox -= 1
            return True
        else:
            return False

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        return self.__dict__

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.__dict__.update(data)

class PokedexItemModel():
    def __init__(self, id):
        # Class attributes
        self.id = id
        self.amount = 0

    def add(self):
        self.amount += 1

    def delete(self):
        if self.amount > 0:
            self.amount -= 1
            return True
        else:
            return False

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        return self.__dict__

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.__dict__.update(data)

class PokedexModel():
    # We maintain a list of 152 items. Those items are created during the initialization.
    # Items are indexed from 0 to 151, 0 is unused, items from 1 to 151 represent every 151 pokemons
    # We keep the following arrangement: items[i].id == i
    # Therefore, id is replicated in PokemonItem but we can fast search in the array by using array index.
    # You must not modify this list, but you can modify items inside.
    def __init__(self):
        # Class attributes
        self.items = []
        # Init
        for i in range(152):
            self.items.append(PokedexItemModel(i))

    # @param id must be an integer : id of the pokemon
    # @return (PokedexItemModel): can be None if id not in [1,151]
    def get(self, id):
        if id >= 1 and id <= 151:
            return self.items[id]
        else:
            return None

    def get_total_amount(self):
        count = 0
        for i in range(1,152):
            count += self.items[i].amount
        return count

    def get_distinct_amount(self):
        count = 0
        for i in range(1,152):
            if self.items[i].amount >= 1:
                count += 1
        return count

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        data = []
        for item in self.items:
            data.append(item.get_dictionary())
        return data

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        # The structure is already initialized. Just update all elements found in the dictionary
        for element in data:
            self.items[element["id"]].from_dictionary(element)

class PlayerModel():
    def __init__(self, username):
        # Class attributes
        self.username = username
        self.pokestuff = PokestuffModel()
        self.pokedex = PokedexModel()

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        data = {}
        data["username"] = self.username
        data["pokestuff"] = self.pokestuff.get_dictionary()
        data["pokedex"] = self.pokedex.get_dictionary()
        return data

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.username = data["username"]
        self.pokestuff.from_dictionary(data["pokestuff"])
        self.pokedex.from_dictionary(data["pokedex"])

class PlayersModel():
    def __init__(self):
        # Class attributes
        self.players = []

    # @return (PlayerModel): can be None if no player has been found with this username
    def get(self, username):
        for player in self.players:
            if player.username == username:
                return player
        # User not found
        return None

    # Safe get, create a new player if needed
    # @return (PlayerModel): is never None
    def safe_get(self, username):
        result = self.get(username)
        if result == None: # No user has been found with this username
            result = PlayerModel(username)
            self.players.append(result)
        return result

    # @param id must be an integer : id of the pokemon
    # @return (Array<PlayerModel>): list of players who own this pokemon
    def get_owners(self, id):
        result = []
        for player in self.players:
            if player.pokedex.get(id).amount > 0:
                result.append(player)
        return result

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Return a dictionary (representation of this object) for JSON serialization
    def get_dictionary(self):
        data = []
        for player in self.players:
            data.append(player.get_dictionary())
        return data

    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.players = [] # Reset
        for element in data:
            player = PlayerModel("")
            player.from_dictionary(element)
            self.players.append(player)

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

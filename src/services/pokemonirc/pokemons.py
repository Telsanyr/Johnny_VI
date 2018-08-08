#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import random
import os
import json
import shutil

class Pokemon():
    def __init__(self):
        # Class attributes
        self.id = -1
        self.name = ""
        self.density = -1
        self.power = -1
        self.link = ""
        self.evolution = 0 # id of its evolution

    # ------------------------------------------------------------------------ #
    # --- Dictionary Representation                                        --- #
    # ------------------------------------------------------------------------ #
    # Load the object from its dictionary representation
    def from_dictionary(self, data):
        self.__dict__.update(data)

class POKEMONS():
    DENSITY_SUM = 0
    POKEMONS_TOTAL = 0
    _DATA = []

    # POKEMONS Singleton initialization
    @staticmethod # A static method does not receive an implicit first argument
    def INITIALIZE():
        file = POKEMONS_DATABASE_FILE
        # Database loading
        if os.path.isfile(file):
            with open(file, 'r') as f:
                data = json.load(f)
                for element in data:
                    pokemon = Pokemon()
                    pokemon.from_dictionary(element)
                    POKEMONS._DATA.append(pokemon)
                f.close()
        else:
            LOGGER.error("Unable to load pokemons database from pokemons.json database.")
        # Initialize web client database
        shutil.copy2(POKEMONS_DATABASE_FILE, POKEMONS_DATABASE_WEB_COPY_FILE)
        # Total density and total pokemons init
        for pokemon in POKEMONS._DATA:
            POKEMONS.DENSITY_SUM += pokemon.density
        POKEMONS.POKEMONS_TOTAL = len(POKEMONS._DATA)

    # @param id must be an integer # TODO
    # @return (Pokemon): can be None if id not in [1,151]
    @staticmethod # A static method does not receive an implicit first argument
    def GET_POKEMON_BY_ID(id):
        if id >= 1 and id <= 151:
            return POKEMONS._DATA[id-1] # Because data array is sorted by id without id.0
        else:
            return None

    # This function is not case sensitive (ncs)
    # @param name must be an string
    # @return (Pokemon): can be None if no pokemon has been found with this name
    @staticmethod # A static method does not receive an implicit first argument
    def GET_POKEMON_BY_NCS_NAME(name):
        for pk in POKEMONS._DATA:
            if pk.name.lower() == name.lower():
                return pk
        return None

    # @return (Pokemon)
    @staticmethod # A static method does not receive an implicit first argument
    def GET_RANDOM_POKEMON():
        count = int(random.random() * POKEMONS.POKEMONS_TOTAL)
        return POKEMONS._DATA[count]

    # @return (Pokemon)
    @staticmethod # A static method does not receive an implicit first argument
    def GET_RANDOM_POKEMON_USING_DENSITY():
        count = int(random.random() * POKEMONS.DENSITY_SUM)
        for pokemon in POKEMONS._DATA:
            count -= pokemon.density
            if count < 0:
                return pokemon
        return None # Should not happen

    # @return (float): in [0,1]
    @staticmethod # A static method does not receive an implicit first argument
    def GET_POKEMON_CONCENTRATION(pokemon):
        return 1.0 * pokemon.density / POKEMONS.DENSITY_SUM

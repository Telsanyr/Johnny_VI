#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import re

# The purpose of this class it to parse command arguments and extract any corresponding objects (username, pokestuffs, pokemons)
class CommandInterpreter():
    def __init__(self, room, engine, output):
        # Class attributes
        self.room = room
        self.engine = engine
        self.output = output

    # ------------------------------------------------------------------------ #
    # --- Private                                                          --- #
    # ------------------------------------------------------------------------ #
    def _extract_username(self, user, args):
        if args == "": # auto-target
            return user
        else:
            return args

    # Found the corresponding pokemon by id or by name
    # @return (Pokemon): can be None if nothing was found
    def _extract_pokemon(self, args):
        # First try by name
        pokemon = POKEMONS.GET_POKEMON_BY_NCS_NAME(args)
        if pokemon == None:
            # Otherwise try by id
            ids = re.findall('\d+', args) # Array of all numbers found by regex
            if(len(ids) >= 1):
                id = int(ids[0]) # number are still stored as strings by regex
                pokemon = POKEMONS.GET_POKEMON_BY_ID(id)
        return pokemon

    # ------------------------------------------------------------------------ #
    # --- Public                                                           --- #
    # ------------------------------------------------------------------------ #
    def catch(self, user, args):
        args = args.lower()
        stuff = POKESTUFFS.UNKNOWN
        amount = 1
        if args == "":
            stuff = POKESTUFFS.BARBAPAPA
            amount = 1
        else:
            # Number determination
            nbrs = re.findall('\d+', args) # Array of all numbers found by regex
            if(len(nbrs) >= 1):
                amount = int(nbrs[0]) # do not forget cast
            else:
                amount = 1 # default

            if ("all-in" in args) or ("allin" in args):
                amount = -1 # Special input for all-in

            # Stuff determination
            stuff_found = POKESTUFFS.in_ncs_string(args)
            if len(stuff_found) >= 1:
                stuff = stuff_found[0]
            else:
                self.output.raise_UNKNOWN_POKESTUFF(args)
                return
        # Engine API Call with rights arguments
        self.engine.arena.enroll(user, stuff, amount)

    def pokedex(self, user, args):
        target = self._extract_username(user, args)
        # Engine API Call with rights arguments
        self.engine.show_pokedex(target)

    def pokestuff(self, user, args):
        target = self._extract_username(user, args)
        # Engine API Call with rights arguments
        self.engine.show_pokestuff(target)

    def crush(self, user, args):
        pokemon = self._extract_pokemon(args)
        # Engine API Call with rights arguments
        self.engine.crush_pokemon(user, pokemon)

    def evolve(self, user, args):
        pokemon = self._extract_pokemon(args)
        # Engine API Call with rights arguments
        self.engine.evolve_pokemon(user, pokemon)

    # @param args (integer or string) pokemon name/id or "arena" or nothing
    def pokemon(self, args):
        pokemon = None
        # Ask to show the pokemon in the arena
        if args == "" or args == "arena":
            pokemon = self.engine.arena.get_pokemon()
            if pokemon == None:
                self.output.raise_EMPTY_ARENA()
                return
        # Ask a specific pokemon
        else:
            pokemon = self._extract_pokemon(args)
        # Engine API Call with rights arguments
        self.engine.show_pokemon(pokemon)

    def buy(self, user, args, pokestuff):
        target = ""
        if args == "": # auto-target
            target = user
        elif args in self.room.user_list:
            target = args
        else:
            self.output.warning_UNKNOWN_BUY_TARGET(args)
            target = user # default target
        # Engine API Call with rights arguments
        self.engine.link_cable.new_buy(target, pokestuff)

    def admin_force_arena(self, user):
        if user == self.room.admin_username:
            self.engine.arena.d_force_spawn()
        else:
            self.output.raise_UNAUTHORIZED_ACTION()
            return

    def admin_force_fouras(self, user):
        if user == self.room.admin_username:
            self.engine.riddle.d_force_spawn()
        else:
            self.output.raise_UNAUTHORIZED_ACTION()
            return

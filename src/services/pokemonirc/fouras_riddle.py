#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import random
from threading import Timer

class FOURAS_RULES():
    PROBA_SPAWN = 0.002 # 0.1% everytime respawn is called

class FourasRiddle():
    def __init__(self, engine, output, players):
        # Class attributes
        self.engine = engine
        self.output = output
        self.players = players
        self.answer = None

    # ------------------------------------------------------------------------ #
    # --- Private                                                          --- #
    # ------------------------------------------------------------------------ #
    def _try_spawn(self):
        proba = random.random()
        if proba <= FOURAS_RULES.PROBA_SPAWN:
            pokemon = POKEMONS.GET_RANDOM_POKEMON()
            self.answer = pokemon.name
            self.output.ack_RIDDLE_SPAWN(pokemon.id)
            timer = Timer(300, self.leave)
            timer.start()

    # ------------------------------------------------------------------------ #
    # --- Public                                                           --- #
    # ------------------------------------------------------------------------ #
    def try_respawn(self):
        if self.answer == None: # Fouras is not here
            self._try_spawn()

    # Most of the time Fouras will leave after 300 seconds, but it can leave before (if another spawn had happen less than 300seconds before)
    def leave(self):
        if self.answer != None: # Fouras is waiting for an answer (Bug: possible end of another spawn, we do not care jaja)
            self.output.ack_RIDDLE_LEAVE()
            self.answer = None

    def try_answer(self, msg, username):
        if self.answer != None: # Fouras is waiting for an answer
            if msg.lower() == self.answer.lower() or msg.lower() == "!pokemon " + self.answer.lower() :
                self.solve_riddle(username)
                self.answer = None

    def solve_riddle(self, username):
        player = self.players.safe_get(username) # Create user if not found
        player.pokestuff.add_lootbox(1)
        self.output.ack_RIDDLE_WINNER(player, POKESTUFFS.LOOTBOX, 1)
        self.engine.save_database() # PokemOnIRC database has been modified

    # ------------------------------------------------------------------------ #
    # --- Debug                                                            --- #
    # ------------------------------------------------------------------------ #
    # @Debug
    def d_force_spawn(self):
        while self.answer == None:
            self._try_spawn()

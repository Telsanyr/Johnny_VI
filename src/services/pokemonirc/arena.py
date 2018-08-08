#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import random
import math
from threading import Timer

class ARENA_RULES():
    PROBA_SPAWN = 0.01 # 1% everytime respawn is called
    _PROBA_CATCH = [[POKESTUFFS.BARBAPAPA,        0.15],         # probability = exp(-power² * c1)
                [POKESTUFFS.POKEBALL,            0.04],          # probability = exp(-power² * c1)
                [POKESTUFFS.SUPERBALL,           0.01],          # probability = exp(-power² * c1)
                [POKESTUFFS.KEBAB,               0.8, -0.005]]   # probability = c1 / power² + c2

    @staticmethod # A static method does not receive an implicit first argument
    def RETRIEVE_PROBA_CATCH(pokestuff, pokemon):
        for coef in ARENA_RULES._PROBA_CATCH:
            if coef[0] == pokestuff:
                if pokestuff == POKESTUFFS.KEBAB: # Specific case for kebab
                    return (coef[1] / (pokemon.power * pokemon.power) ) + coef[2]
                else:
                    return math.exp(-1 * pokemon.power * pokemon.power * coef[1])
        # Unknown pokestuff
        LOGGER.error( "[Error] Unable to compute catch probability, unknown item") # TODO
        return 0.0

class Arena():
    def __init__(self, engine, output, players):
        # Class attributes
        self.engine = engine
        self.output = output
        self.players = players
        self.pokemon = None
        self.enrollment = [] # list of tuples [PlayersModel, POKESTUFFS, amount]

    # ------------------------------------------------------------------------ #
    # --- Private                                                          --- #
    # ------------------------------------------------------------------------ #
    def _try_spawn(self):
        roll = random.random()
        if roll <= ARENA_RULES.PROBA_SPAWN:
            # A new pokemon apear
            self.pokemon = POKEMONS.GET_RANDOM_POKEMON_USING_DENSITY()
            self.output.ack_ARENA_SPAWN(self.pokemon)
            timer = Timer(60, self.fight)
            timer.start()

    # @require a pokemon in the arena
    # @param player: must be a PlayersModel (not None)
    # @param stuff: must be a POKESTUFFS Enum
    # @param amount: must be an integer
    def _try_catch(self, player, stuff, amount):
        proba = ARENA_RULES.RETRIEVE_PROBA_CATCH(stuff, self.pokemon)
        rolls = []
        for k in range(amount):
            allowed = False
            if stuff == POKESTUFFS.BARBAPAPA:
                allowed = player.pokestuff.use_barbapapa()
            elif stuff == POKESTUFFS.KEBAB:
                allowed = player.pokestuff.use_kebab()
            elif stuff == POKESTUFFS.POKEBALL:
                allowed = player.pokestuff.use_pokeball()
            elif stuff == POKESTUFFS.SUPERBALL:
                allowed = player.pokestuff.use_superball()
            else:
                self.output.raise_UNKNOWN_POKESTUFF(stuff) # Should not happen
                return False

            if allowed:
                roll = random.random()
                rolls.append(roll)
                if roll <= proba:
                    player.pokedex.get(self.pokemon.id).add()
                    self.output.ack_ARENA_CATCH_SUCCESS(player, self.pokemon, stuff, k+1, proba, rolls)
                    return True
            else:
                # This player lost stuff between enrollment and fight, therefore no further try will be done.
                self.output.ack_ARENA_CATCH_FAIL(player, self.pokemon, stuff, k, proba, rolls)   # (k+1)-1 = k
                return False

        # All tries done. It failed
        self.output.ack_ARENA_CATCH_FAIL(player, self.pokemon, stuff, amount, proba, rolls)
        return False

    # ------------------------------------------------------------------------ #
    # --- Public                                                           --- #
    # ------------------------------------------------------------------------ #
    # @return (Pokemon): can be None if arena is empty
    def get_pokemon(self):
        return self.pokemon

    def try_respawn(self):
        if self.pokemon == None:
            self._try_spawn()

    # @param username (string)
    # @param stuff: must be a POKESTUFFS Enum
    # @param amount: must be an integer
    def enroll(self, username, stuff, amount):
        player = self.players.get(username) # We do not safe_get here because if this is a new player it will not have any pokestuff for enrollment
        if player == None:
            self.output.raise_UNKNWON_PLAYER(username)
            return

        # Cannot enroll if the arena is empty
        if self.pokemon == None:
            self.output.raise_EMPTY_ARENA()
            return

        # Cannot enroll twice (even with different pokestuff)
        for registration in self.enrollment:
            if registration[0].username == player.username:
                self.output.raise_ALREADY_ENROLLED(player)
                return

        # Cannot enroll without asked pokestuff
        max_allowed = 0
        if stuff == POKESTUFFS.BARBAPAPA:
            max_allowed = player.pokestuff.barbapapa
        elif stuff == POKESTUFFS.KEBAB:
            max_allowed = player.pokestuff.kebab
        elif stuff == POKESTUFFS.POKEBALL:
            max_allowed = player.pokestuff.pokeball
        elif stuff == POKESTUFFS.SUPERBALL:
            max_allowed = player.pokestuff.superball
        else:
            self.output.raise_UNKNOWN_POKESTUFF(stuff) # Should not happen
            return

        # Special amount for all-in
        if amount == -1:
            amount = max_allowed

        if amount < 1:
            self.output.raise_ENROLLED_WITHOUT_POKESTUFF(player)
            return
        elif max_allowed < amount:
            self.output.raise_ENROLLED_WITH_ILLEGAL_POKESTUFF(player, stuff, amount, max_allowed)
            return
        else:
            # We do not reserve the stuff at this moment, the game can still crash without fight. We will check and use the stuff during the fight
            self.enrollment.append([player, stuff, amount])
            self.output.ack_ARENA_ENROLL(player, self.pokemon, stuff, amount)

    def fight(self):
        self.output.ack_ARENA_FIGHT(self.pokemon)
        caught = False
        for registration in self.enrollment:
            caught = self._try_catch(registration[0], registration[1], registration[2])
            if caught:
                break

        self.output.ack_ARENA_CLOSE(self.pokemon, caught)
        self.engine.save_database() # PokemOnIRC database has been modified
        self.pokemon = None         # Reset
        self.enrollment = []

    # ------------------------------------------------------------------------ #
    # --- Debug                                                            --- #
    # ------------------------------------------------------------------------ #
    # @Debug
    def d_force_spawn(self):
        while self.pokemon == None:
            self._try_spawn()

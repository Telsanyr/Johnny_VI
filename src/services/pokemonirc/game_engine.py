#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

class GameEngine():
    def __init__(self, room):
        # Class attributes
        self.room = room
        self.output = GameOutput(room, EVENTS_DATABASE_PATH, EVENTS_DATABASE_WEB_COPY_PATH)
        self.interpreter = CommandInterpreter(room, self, self.output)
        self.players = PlayersModel()
        self.players.json_import(PLAYERS_DATABASE_FILE) # Load database
        self.arena = Arena(self, self.output, self.players)
        self.riddle = FourasRiddle(self, self.output, self.players)
        self.link_cable = LinkCable(self)
        self.tall_grass = TallGrassDeamon(self)
        self.tall_grass.start()

    # ------------------------------------------------------------------------ #
    # --- Database                                                         --- #
    # ------------------------------------------------------------------------ #
    def save_database(self):
        self.players.json_export(PLAYERS_DATABASE_FILE)
        self.players.json_export(PLAYERS_DATABASE_WEB_COPY_FILE)

    # ------------------------------------------------------------------------ #
    # --- Callback                                                         --- #
    # ------------------------------------------------------------------------ #
    def onTallGrassEvent(self):
        self.arena.try_respawn()
        self.riddle.try_respawn()

    # ------------------------------------------------------------------------ #
    # --- Actions                                                          --- #
    # ------------------------------------------------------------------------ #
    def buy_pokestuff(self, username, pokestuff):
        player = self.players.safe_get(username) # Create user if not found
        amount = 0
        if pokestuff == POKESTUFFS.BARBAPAPA:
            amount = 10                     # Barbapapas are bought by 10
            player.pokestuff.add_barbapapa(amount)
        elif pokestuff == POKESTUFFS.POKEBALL:
            amount = 3                      # Pokeballs are bought by 3
            player.pokestuff.add_pokeball(amount)
        elif pokestuff == POKESTUFFS.SUPERBALL:
            amount = 1
            player.pokestuff.add_superball(amount)
        else:
            self.output.raise_UNBUYABLE_POKESTUFF(pokestuff)
            self.save_database() # PokemOnIRC database has been modified (even if nothing has been bought because we did a safe_add)
            return

        self.output.ack_BUY_SHOP(player, pokestuff, amount)
        self.save_database() # PokemOnIRC database has been modified

    def crush_pokemon(self, username, pokemon):
        player = self.players.get(username) # New players do not have any pokemon anyway
        if player == None:
            self.output.raise_UNKNWON_PLAYER(username)
            return

        if pokemon == None:
            self.output.raise_UNKNWON_POKEMON()
            return

        pokedex_item = player.pokedex.get(pokemon.id)
        success = pokedex_item.delete()
        if success:
            kebabs = pokemon.power * pokemon.power
            player.pokestuff.add_kebab(kebabs)
            self.output.ack_CRUSH_POKEMON(player, pokemon, POKESTUFFS.KEBAB, kebabs)
            self.save_database() # PokemOnIRC database has been modified
        else:
            self.output.raise_FAIL_CRUSH_NO_POKEMON(player, pokemon)
            return

    def evolve_pokemon(self, username, pokemon):
        player = self.players.get(username) # New players do not have any pokemon anyway
        if player == None:
            self.output.raise_UNKNWON_PLAYER(username)
            return

        if pokemon == None:
            self.output.raise_UNKNWON_POKEMON()
            return

        if pokemon.evolution == 0: # 0: no evolution
            self.output.raise_NO_EVOLUTION(pokemon)
            return

        pokedex_item = player.pokedex.get(pokemon.id)
        if pokedex_item.amount <= 0:
            self.output.raise_FAIL_EVOLVE_NO_POKEMON(player, pokemon)
            return

        if pokemon.evolution == -1: # -1: special evolution # TODO Not Implemented Yet
            self.output.raise_MOONSTONE_NO_EFFECT(pokemon)
            return
        else:
            # Classic evolution with moonstone
            evolution = POKEMONS.GET_POKEMON_BY_ID(pokemon.evolution)
            evolution_item = player.pokedex.get(evolution.id)

            if player.pokestuff.moonstone <= 0:
                self.output.raise_FAIL_EVOLVE_NO_MOONSTONE(player, pokemon)
                return

            kebab_needed = evolution.power * evolution.power
            if player.pokestuff.kebab < kebab_needed:
                self.output.raise_FAIL_EVOLVE_NO_ENOUGHT_KEBAB(player, pokemon, player.pokestuff.kebab, kebab_needed)
                return

            # Recipe: 1 pokemon, 1 moonstone, x kebabs
            pokemon_delete_success = pokedex_item.delete()
            kebabs_use_success = player.pokestuff.use_kebabs(kebab_needed)
            moonstone_use_success = player.pokestuff.use_moonstone()
            if not (pokemon_delete_success and kebabs_use_success and moonstone_use_success):
                # Should not happen
                LOGGER.error("Should not happen, fail in pokemon evolution (POKEMON = " + str(pokemon_delete_success) + ", KEBAB = " + str(kebabs_use_success) + ", MOONSTONE = " + str(moonstone_use_success) + ")")
            # We give the pokemon even in this case of bug because we are kind ! (it should not happen)
            evolution_item.add()
            self.output.ack_EVOLUTION_MOONSTONE(player, pokemon, evolution, POKESTUFFS.MOONSTONE, 1, POKESTUFFS.KEBAB, kebab_needed)
            self.save_database() # PokemOnIRC database has been modified

    # ------------------------------------------------------------------------ #
    # --- Display                                                          --- #
    # ------------------------------------------------------------------------ #
    def show_pokedex(self, username):
        # Only safe_get if the user is connected (because it could also be a typo)
        player = None
        if username in self.room.user_list:
            player = self.players.safe_get(username) # Create user if not found
            self.save_database() # PokemOnIRC database could have been modified (we did a safe_add)
        else:
            player = self.players.get(username)
        if player == None:
            self.output.raise_UNKNWON_PLAYER(username)
            return

        self.output.display_POKEDEX(player)

    def show_pokestuff(self, username):
        # Only safe_get if the user is connected (because it could also be a typo)
        player = None
        if username in self.room.user_list:
            player = self.players.safe_get(username) # Create user if not found
            self.save_database() # PokemOnIRC database could have been modified (we did a safe_add)
        else:
            player = self.players.get(username)
        if player == None:
            self.output.raise_UNKNWON_PLAYER(username)
            return

        self.output.display_POKESTUFF(player)

    def show_pokemon(self, pokemon):
        if pokemon == None:
            self.output.raise_UNKNWON_POKEMON()
            return

        concentration = 100.0 * POKEMONS.GET_POKEMON_CONCENTRATION(pokemon) # pourcent
        proba_barbapapa = ARENA_RULES.RETRIEVE_PROBA_CATCH(POKESTUFFS.BARBAPAPA, pokemon) * 100
        proba_kebab = ARENA_RULES.RETRIEVE_PROBA_CATCH(POKESTUFFS.KEBAB, pokemon) * 100
        proba_pokeball = ARENA_RULES.RETRIEVE_PROBA_CATCH(POKESTUFFS.POKEBALL, pokemon) * 100
        proba_superball = ARENA_RULES.RETRIEVE_PROBA_CATCH(POKESTUFFS.SUPERBALL, pokemon) * 100
        owners = self.players.get_owners(pokemon.id)

        self.output.display_POKEMON(pokemon, concentration, owners, [proba_barbapapa, proba_kebab, proba_pokeball, proba_superball])

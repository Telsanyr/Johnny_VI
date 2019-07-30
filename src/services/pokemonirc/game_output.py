#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import os
import json
import time
from datetime import datetime

# Rule #1: Always print arguments with str() function
# Rule #2: In order to avoid useless ping, add '_' before any player username if the command can be triggered by someone else
class GameOutput():
    def __init__(self, room, path, web_copy_path):
        # Class attributes
        self.room = room
        # Thoses are only paths of folders, we will determine filename according to the today's date.
        self.database_path = path
        self.web_copy_database_path = web_copy_path

    # ------------------------------------------------------------------------ #
    # --- Display Messages                                                 --- #
    # ------------------------------------------------------------------------ #
    def display_STATS(self):
        link = str(self.room.website_url) + "/stats"
        self.room.send(link)

    def display_POKEMON(self, pokemon, proportion, owners, probabilities):
        s = str(pokemon.name) + ": #" + str(pokemon.id) + ", rate: " + ('%.2f' % proportion) + "%, power: " + str(pokemon.power) + "/10, [ " + str(pokemon.link) + " ]"
        s += ", proba: B(" + ('%.1f' % probabilities[0]) + ")% K(" + ('%.1f' % probabilities[1]) + ")% P(" + ('%.1f' % probabilities[2]) + ")% S(" + ('%.1f' % probabilities[3]) + ")%"
        if len(owners) > 0:
            s += ", déjà possédé par : "
        for i in range(len(owners)):
            s += "_" + str(owners[i].username)
            if i < (len(owners) - 1):
                s += ", "
        self.room.send(s)

    def display_POKEDEX(self, player):
        link = str(self.room.website_url) + "/pokedex?" + str(player.username)
        self.room.send("La collection de _" + str(player.username) + " comptabilise " + str(player.pokedex.get_total_amount()) + " pokemons (" + str(player.pokedex.get_distinct_amount()) + "/151) : " + link)

    def display_POKESTUFF(self, player):
        s = "_" + str(player.username) + " possède "
        s += str(player.pokestuff.barbapapa) + " " + POKESTUFFS.to_string(POKESTUFFS.BARBAPAPA) + ", "
        s += str(player.pokestuff.kebab) + " " + POKESTUFFS.to_string(POKESTUFFS.KEBAB) + ", "
        s += str(player.pokestuff.pokeball) + " " + POKESTUFFS.to_string(POKESTUFFS.POKEBALL) + ", "
        s += str(player.pokestuff.superball) + " " + POKESTUFFS.to_string(POKESTUFFS.SUPERBALL)
        # display only if owned
        if player.pokestuff.moonstone > 0:
            s += ", " + str(player.pokestuff.moonstone) + " " + POKESTUFFS.to_string(POKESTUFFS.MOONSTONE)
        if player.pokestuff.thunderstone > 0:
            s += ", " + str(player.pokestuff.thunderstone) + " " + POKESTUFFS.to_string(POKESTUFFS.THUNDERSTONE)
        if player.pokestuff.firestone > 0:
            s += ", " + str(player.pokestuff.firestone) + " " + POKESTUFFS.to_string(POKESTUFFS.FIRESTONE)
        if player.pokestuff.waterstone > 0:
            s += ", " + str(player.pokestuff.waterstone) + " " + POKESTUFFS.to_string(POKESTUFFS.WATERSTONE)
        if player.pokestuff.lootbox > 0:
            s += ", " + str(player.pokestuff.lootbox) + " " + POKESTUFFS.to_string(POKESTUFFS.LOOTBOX)
        s += "."
        self.room.send(s)

    # ------------------------------------------------------------------------ #
    # --- Acknowledge Messages                                             --- #
    # ------------------------------------------------------------------------ #
    # /!\ Every acknowledge message will log a game event (for game statistics).

    def ack_CRUSH_POKEMON(self, player, pokemon, pokestuff, amount):
        self.log_game_event("CRUSH_POKEMON", {"player": player.username, "pokemon": pokemon.id, "pokestuff": pokestuff, "amount": amount})
        self.room.send(str(player.username) + " déplume son " + str(pokemon.name) + " et obtient " + str(amount) + " " + POKESTUFFS.to_string(pokestuff) + ".")

    def ack_RIDDLE_SPAWN(self, id):
        self.log_game_event("RIDDLE_SPAWN", {"pokemon": id})
        self.room.send("Vous rencontrez le fantôme du père Fouras, celui-ci a une enigme pour vous. Le père Fouras vous demande quel est le pokemon numero " + str(id) + " ?")

    def ack_RIDDLE_WINNER(self, player, pokestuff, amount):
        self.log_game_event("RIDDLE_WINNER", {"player": player.username, "pokestuff": pokestuff, "amount": amount})
        self.room.send("[Fantôme du Père Fouras] : Bonne réponse " + str(player.username) + ". Voici " + str(amount) + " " + POKESTUFFS.to_string(pokestuff) + ".")

    def ack_RIDDLE_LEAVE(self):
        self.log_game_event("RIDDLE_LEAVE", {})
        self.room.send("Le fantôme du père Fouras retourne à ses occupations...")

    def ack_ARENA_SPAWN(self, pokemon):
        self.log_game_event("ARENA_SPAWN", {"pokemon": pokemon.id})
        if(pokemon.power < 10){
            self.room.send("Un " + str(pokemon.name) + " sauvage entre dans l'arène. Vous avez une minute pour essayer de l'attraper !")
        } else {
            self.room.send("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
            self.room.send(str(pokemon.name) + " entre dans l'arène et il est vraiment pas content. Que le COMBAT COMMENCE !")
            self.room.send("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        }

    def ack_ARENA_ENROLL(self, player, pokemon, pokestuff, amount):
        self.log_game_event("ARENA_ENROLL", {"player": player.username, "pokemon": pokemon.id, "pokestuff": pokestuff, "amount": amount})
        self.room.send(str(player.username) + " rentre dans l'arène avec " + str(amount) + " " + POKESTUFFS.to_string(pokestuff) + ".")

    def ack_ARENA_FIGHT(self, pokemon):
        self.log_game_event("ARENA_FIGHT", {"pokemon": pokemon.id})
        self.room.send("Le combat commence ! Dresseurs, avancez-vous dans l'arène.")

    def ack_ARENA_CATCH_SUCCESS(self, player, pokemon, pokestuff, amount, probability, rolls):
        self.log_game_event("ARENA_CATCH_SUCCESS", {"player": player.username, "pokemon": pokemon.id, "pokestuff": pokestuff, "amount": amount, "probability": probability, "rolls": rolls})
        self.room.send(str(player.username) + " réussi à attirer " + str(pokemon.name) + " à l'aide de " + str(amount) + " " + POKESTUFFS.to_string(pokestuff) + ".")

    def ack_ARENA_CATCH_FAIL(self, player, pokemon, pokestuff, amount, probability, rolls):
        self.log_game_event("ARENA_CATCH_FAIL", {"player": player.username, "pokemon": pokemon.id, "pokestuff": pokestuff, "amount": amount, "probability": probability, "rolls": rolls})
        fail_msg = ""
        if pokestuff == POKESTUFFS.BARBAPAPA:
            fail_msg = "Faudrait pas prendre les pokemons pour des cons."
        elif pokestuff == POKESTUFFS.KEBAB:
            fail_msg = "Essayes avec des tacos la prochaine fois, on sait jamais."
        elif pokestuff == POKESTUFFS.POKEBALL:
            fail_msg = "Une brise marine semble alors se lever. Vous sentez cette odeur iodée ?"
        elif pokestuff == POKESTUFFS.SUPERBALL:
            fail_msg = "Il se met à grêler... grêler des cristaux de sel."
        self.room.send("_" + str(player.username) + " utilise ses " + str(amount) + " " + POKESTUFFS.to_string(pokestuff) + " sans succès. " + fail_msg)

    def ack_ARENA_CLOSE(self, pokemon, success):
        self.log_game_event("ARENA_CLOSE", {"pokemon": pokemon.id, "caught": success})
        if not success:
            self.room.send("Personne n'a réussi à convaincre " + str(pokemon.name) + " de le rejoindre. Il s'enfuit.")

    def ack_BUY_SHOP(self, player, pokestuff, amount):
        self.log_game_event("BUY_SHOP", {"player": player.username, "pokestuff": pokestuff, "amount": amount})
        self.room.send(str(player.username) + ", " + str(amount) + " " + POKESTUFFS.to_string(pokestuff) + " ont été ajouté à votre pokestuff.")

    def ack_OPEN_LOOTBOX(self, player, loots):
        self.log_game_event("OPEN_LOOTBOX", {"player": player.username, "loots": loots})
        s = str(player.username) + " ouvre un " + POKESTUFFS.to_string(POKESTUFFS.LOOTBOX) + "."
        if len(loots) == 0:
            s += " Il est vide... Seuls des cristaux de sel se sont formés sur les parois."
        else:
            s += " Il contient "
            for i in range(len(loots)):
                s += str(loots[i]["amount"]) + " " + POKESTUFFS.to_string(loots[i]["pokestuff"])
                if i < len(loots) - 2:
                    s += ", "
                elif i == len(loots) - 2:
                    s += " et "
                else:
                    s += "."
        self.room.send(s)

    def ack_EVOLUTION_STONE(self, player, pokemon, evolution, pokestuff1, pokestuff1_amount, pokestuff2, pokestuff2_amount):
        self.log_game_event("EVOLUTION_STONE", {"player": player.username, "pokemon": pokemon.id, "evolution": evolution.id, "pokestuff": [pokestuff1, pokestuff2], "amount": [pokestuff1_amount, pokestuff2_amount]})
        self.room.send(str(player.username) + " fait ingérer " + str(pokestuff1_amount) + " " + POKESTUFFS.to_string(pokestuff1)
            + " ainsi que " + str(pokestuff2_amount) + " " + POKESTUFFS.to_string(pokestuff2) + " à " + str(pokemon.name)
            + ". Il le prend dans ses bras, le secoue violemment, le repose au sol et la magie commence à opérer. "
            + "*BLURP* *BLUARRG* *BLOUP* " + str(pokemon.name) + " évolue en " + str(evolution.name) + ".")

    # ------------------------------------------------------------------------ #
    # --- Warning Messages                                                 --- #
    # ------------------------------------------------------------------------ #
    def warning_UNKNOWN_BUY_TARGET(self, target):
        self.room.send("Je ne connais aucun " + str(target) + " donc tu lui donneras ça en main propre.")

    def warning_DEPRECATED_COMMAND_BROYER(self):
        self.room.send("Attention, la commande !broyer a été remplacée par la commande !crush depuis la version 1.2")

    def warning_DEPRECATED_COMMAND_POKEMON(self):
        self.room.send("Attention, la commande ?pokemon a été remplacée par la commande !pokemon depuis la version 1.2")

    # ------------------------------------------------------------------------ #
    # --- Error Messages                                                   --- #
    # ------------------------------------------------------------------------ #
    def raise_UNKNWON_PLAYER(self, username):
        self.room.send("Je ne le connais pas moi " + str(username) + " !")

    def raise_UNKNWON_POKEMON_ID(self, id):
        self.room.send("Je ne connais aucun pokemon de numéro #" + str(id) + " !")

    def raise_UNKNWON_POKEMON(self):
        self.room.send("Cela ne correspond à aucun pokemon connu.")

    def raise_EMPTY_ARENA(self):
        self.room.send("Il n'y a aucun pokemon dans l'arène actuellement.")

    def raise_ALREADY_ENROLLED(self, player):
        self.room.send("Tu es déjà dans l'arène " + str(player.username) + ".")

    def raise_ENROLLED_WITHOUT_POKESTUFF(self, player):
        self.room.send("Tu ne peux pas entrer dans l'arène les mains vides " + str(player.username) + ".")

    def raise_ENROLLED_WITH_ILLEGAL_POKESTUFF(self, player, pokestuff, amount, allowed):
        self.room.send(str(player.username) + ", tu ne possèdes que " + str(allowed) + " " + POKESTUFFS.to_string(pokestuff) + " en stock. Il t'en manque " + str(amount-allowed) + " pour pouvoir faire cela.")

    def raise_UNUSABLE_POKESTUFF(self, pokestuff):
        self.room.send("Tu ne peux pas effectuer cette action avec des " + POKESTUFFS.to_string(pokestuff) + ".")

    def raise_UNBUYABLE_POKESTUFF(self, input):
        self.room.send("Ca ne s'achète pas un(e) " + str(input) + ". Si on a essayé de vous en vendre vous vous êtes fait arnaquer !")

    def raise_UNKNOWN_POKESTUFF(self, input):
        self.room.send("Je ne sais pas ce que c'est un(e) " + str(input) + ", ça se mange ?")

    def raise_FAIL_CRUSH_NO_POKEMON(self, player, pokemon):
        self.room.send(str(player.username) + ", je comprends vos envie de broyer un petit " + str(pokemon.name) + " mais vous devez en apprivoiser un pour faire cela.")

    def raise_FAIL_OPEN_NO_LOOTBOX(self, player):
        self.room.send(str(player.username) + ", tu ne disposes d'aucun " + POKESTUFFS.to_string(POKESTUFFS.LOOTBOX) + " à l'heure actuelle.")

    def raise_NO_EVOLUTION(self, pokemon):
        self.room.send(str(pokemon.name) + " ne possède aucune évolution connue à ce jour.")

    def raise_STONE_NO_EFFECT(self, pokemon, stone):
        self.room.send("Les " + POKESTUFFS.to_string(stone) + " n'ont aucun effet sur " + str(pokemon.name) + ".")

    def raise_FAIL_EVOLVE_NO_POKEMON(self, player, pokemon):
        self.room.send(str(player.username) + ", tu dois commencer par apprivoiser un " + str(pokemon.name) + " pour pouvoir le faire évoluer.")

    def raise_FAIL_EVOLVE_NO_STONE(self, player, pokemon, stone):
        self.room.send(str(player.username) + ", pour faire évoluer un " + str(pokemon.name) + " il faut avoir une " + POKESTUFFS.to_string(stone) + ".")

    def raise_FAIL_EVOLVE_NO_ENOUGHT_KEBAB(self, player, pokemon, amount, needed):
        self.room.send(str(player.username) + ", pour faire évoluer un " + str(pokemon.name) + " il faut lui donner " + str(needed) + " " + POKESTUFFS.to_string(POKESTUFFS.KEBAB) + " or tu n'en possèdes que " + str(amount) + ".")

    def raise_UNAUTHORIZED_ACTION(self):
        self.room.send("Vous n'êtes pas autorisé à faire cela.")

    # ------------------------------------------------------------------------ #
    # --- Game Events                                                      --- #
    # ------------------------------------------------------------------------ #
    # The purpose in logging events is to create game statistics
    # In order to do that, any game action should be logged
    # We do not log fail, error or warning that does not impact the game, only effective actions are logged
    # Theoretically we must be able to re-build the game database from scratch just by unstacking every game events
    # Therefore, every ack function must log a game event
    # However, because some game elements can change with patchs, we try to log any computed result to avoid
    # doing it a posteriori when investigating logs (otherwise we will need to store every game changes..)
    def get_filename(self):
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
        return "events_" + timestamp + ".json"

    def log_game_event(self, game_event, args):
        # Create the Game Event
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        event = {"timestamp": str(timestamp), "event": game_event, "args": args}

        # Extract log file with today's date
        filename = self.get_filename()
        db_file = self.database_path + filename
        web_copy = self.web_copy_database_path + filename

        # Read events already logged in file
        data = None
        if os.path.isfile(db_file):
            with open(db_file, 'r') as f:
                data = json.load(f)
                f.close()

        if data != None:
            data.append(event)
        else:
            data = [event]

        # Re-write the file with updated data
        with open(db_file, 'w+') as f:
            json.dump(data, f, indent=2)
            f.close()

        # Save a copy for web client
        with open(web_copy, 'w+') as f:
            json.dump(data, f, indent=2)
            f.close()

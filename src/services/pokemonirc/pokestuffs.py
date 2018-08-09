#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Enumerate-like class
class POKESTUFFS():
    UNKNOWN = 0
    BARBAPAPA = 1
    POKEBALL = 2
    SUPERBALL = 3
    KEBAB = 4
    MOONSTONE = 5
    THUNDERSTONE = 6
    FIRESTONE = 7
    WATERSTONE = 8
    LOOTBOX = 9
    BARBAPAPA_WORDS = ["barbapapa"]
    POKEBALL_WORDS = ["pokeball"]
    SUPERBALL_WORDS = ["superball"]
    KEBAB_WORDS = ["kebab"]
    MOONSTONE_WORDS = ["pierre lune"]
    THUNDERSTONE_WORDS = ["pierre foudre"]
    FIRESTONE_WORDS = ["pierre feu"]
    WATERSTONE_WORDS = ["pierre eau"]
    LOOTBOX_WORDS = ["coffre à butin"]

    # This function is not case sensitive (ncs)
    # @return the corresponding pokestuff
    @staticmethod # A static method does not receive an implicit first argument
    def from_ncs_string(s):
        if s.lower() in POKESTUFFS.BARBAPAPA_WORDS:
            return POKESTUFFS.BARBAPAPA
        elif s.lower() in POKESTUFFS.POKEBALL_WORDS:
            return POKESTUFFS.POKEBALL
        elif s.lower() in POKESTUFFS.SUPERBALL_WORDS:
            return POKESTUFFS.SUPERBALL
        elif s.lower() in POKESTUFFS.KEBAB_WORDS:
            return POKESTUFFS.KEBAB
        elif s.lower() in POKESTUFFS.MOONSTONE_WORDS:
            return POKESTUFFS.MOONSTONE
        elif s.lower() in POKESTUFFS.THUNDERSTONE_WORDS:
            return POKESTUFFS.THUNDERSTONE
        elif s.lower() in POKESTUFFS.FIRESTONE_WORDS:
            return POKESTUFFS.FIRESTONE
        elif s.lower() in POKESTUFFS.WATERSTONE_WORDS:
            return POKESTUFFS.WATERSTONE
        elif s.lower() in POKESTUFFS.LOOTBOX_WORDS:
            return POKESTUFFS.LOOTBOX
        else:
            return POKESTUFFS.UNKNOWN

    # This function is not case sensitive (ncs)
    # @return (Array<POKESTUFF>) a list of all pokestuff found in this message
    @staticmethod # A static method does not receive an implicit first argument
    def in_ncs_string(s):
        result = []
        for word in POKESTUFFS.BARBAPAPA_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.BARBAPAPA)
                break
        for word in POKESTUFFS.POKEBALL_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.POKEBALL)
                break
        for word in POKESTUFFS.SUPERBALL_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.SUPERBALL)
                break
        for word in POKESTUFFS.KEBAB_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.KEBAB)
                break
        for word in POKESTUFFS.MOONSTONE_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.MOONSTONE)
                break
        for word in POKESTUFFS.THUNDERSTONE_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.THUNDERSTONE)
                break
        for word in POKESTUFFS.FIRESTONE_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.FIRESTONE)
                break
        for word in POKESTUFFS.WATERSTONE_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.WATERSTONE)
                break
        for word in POKESTUFFS.LOOTBOX_WORDS:
            if word in s.lower():
                result.append(POKESTUFFS.LOOTBOX)
                break

        return result

    @staticmethod # A static method does not receive an implicit first argument
    def to_string(pk):
        if pk == POKESTUFFS.BARBAPAPA:
            return "morceau(x) de barbapapa"
        elif pk == POKESTUFFS.POKEBALL:
            return "pokeball(s)"
        elif pk == POKESTUFFS.SUPERBALL:
            return "superball(s)"
        elif pk == POKESTUFFS.KEBAB:
            return "kebab(s) de pokemon"
        elif pk == POKESTUFFS.MOONSTONE:
            return "pierre(s) Lune"
        elif pk == POKESTUFFS.THUNDERSTONE:
            return "pierre(s) Foudre"
        elif pk == POKESTUFFS.FIRESTONE:
            return "pierre(s) Feu"
        elif pk == POKESTUFFS.WATERSTONE:
            return "pierre(s) Eau"
        elif pk == POKESTUFFS.LOOTBOX:
            return "coffre(s) à butin"
        else:
            return "<UNKNOWN POKESTUFF>"

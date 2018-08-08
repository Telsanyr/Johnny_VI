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
    BARBAPAPA_WORDS = ["barbapapa"]
    POKEBALL_WORDS = ["pokeball"]
    SUPERBALL_WORDS = ["superball"]
    KEBAB_WORDS = ["kebab"]
    MOONSTONE_WORDS = ["pierre lune"]

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
        else:
            return "<UNKNOWN POKESTUFF>"

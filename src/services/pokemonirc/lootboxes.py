#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import random

class LOOTBOX_RULES():
    _DROP_RATES = [         # Item  |  Number of rolls  |  Drop rate by rolls
                [POKESTUFFS.BARBAPAPA,         10,           0.30],
                [POKESTUFFS.POKEBALL,          5,            0.10],
                [POKESTUFFS.SUPERBALL,         3,            0.01],
                [POKESTUFFS.KEBAB,             30,           0.10],
                [POKESTUFFS.MOONSTONE,         3,            0.33],
                [POKESTUFFS.THUNDERSTONE,      1,            0.005],
                [POKESTUFFS.FIRESTONE,         1,            0.005],
                [POKESTUFFS.WATERSTONE,        1,            0.005]
                ]

    @staticmethod # A static method does not receive an implicit first argument
    def OPEN():
        loots = []  # Array<{"pokestuff", "amount"}>
        for item_drop_rate in LOOTBOX_RULES._DROP_RATES:
            amount = 0
            for i in range(item_drop_rate[1]):
                roll = random.random()
                # LOGGER.info("Roll: " + str(roll) + " <? " + str(item_drop_rate[2]) + " pour " + POKESTUFFS.to_string(item_drop_rate[0]))
                if roll < item_drop_rate[2]:
                    amount += 1
            if amount > 0:
                loots.append({"pokestuff": item_drop_rate[0], "amount": amount})
        return loots

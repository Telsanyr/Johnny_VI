#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# This class is used for the communication between bots
class LinkCable():
    def __init__(self, engine):
        # Class attributes
        self.engine = engine
        self.buy_waiting_ack = False
        self.buy_username = ""
        self.buy_pokestuff = 0

    def new_buy(self, username, pokestuff):
        self.buy_waiting_ack = True
        self.buy_username = username
        self.buy_pokestuff = pokestuff

    def soul_mate_listener(self, msg):
        if self.buy_waiting_ack:
            if msg.startswith("Ca fera "): # Positive ack for the buy
                self.engine.buy_pokestuff(self.buy_username, self.buy_pokestuff)
            else: # Negative ack for the buy, cancel it. (@bug if another message from my soul mate intercalate before the ack)
                pass
            self.buy_waiting_ack = False

#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Libs imports
import imp
import sys

# Bootstrap load (it will be loaded in a module named "boostrap_module")
imp.load_source("bootstrap_loader", "./src/bootstrap/bootstrap_loader.py")

# Already loaded libs (they will not be reload, it is only for name linkage)
import bootstrap_module

if __name__ == "__main__":
    debug_mode = False
    mockup_mode = False

    if "-debug" in sys.argv: # if -debug option
        debug_mode = True

    if "-mockup" in sys.argv: # if -mockup option
        mockup_mode = True

    bootstrap_module.Bot(mockup_mode, debug_mode).start()

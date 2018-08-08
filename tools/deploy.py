#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

import os
import imp
import json

info = imp.load_source("info", "./src/bootstrap/connection_info.py")

print "Deploying database..."
try:
    # Database
    os.mkdir("../database")
    os.mkdir("../database/bootstrap")
    os.mkdir("../database/services")
    os.mkdir("../database/services/ideabox")
    os.mkdir("../database/services/karma")
    os.mkdir("../database/services/pokemonirc")
    
    ci = info.ConnectionInfo()
    data = ci.get_dictionary()
    with open("../database/bootstrap/prod_connection.json", 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
        f.close()
    with open("../database/bootstrap/debug_connection.json", 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
        f.close()
    
    print "Database is almost deployed."
    print "You must fill both files 'database/bootstrap/prod_connection.json' and 'database/bootstrap/prod_connection.json' to complete the process."
except OSError:
    print "ERROR: fail to deploy database"
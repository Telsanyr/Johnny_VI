#!/usr/bin/env python
# -*- coding: utf8 -*-
# coding: utf8

# Already loaded libs (they will not be reload, it is only for name linkage)
import supervisor_module

# Service Version
SERVICE_VERSION = "1.2.1"

class Service(supervisor_module.AbstractService):
    def __init__(self, name, room, active):
        # Inheritance
        supervisor_module.AbstractService.__init__(self, name, room, active)
        # Class attributes
        self.VERSION = SERVICE_VERSION
        self.dict = ["beau", "éblouissant", "absolu", "achevé", "éclatant", "adéquat", "admirable", "adorable", "adroit", "agréable",
            "aimable", "élégant", "élevé", "ami", "éminent", "émouvant", "angélique", "énorme", "épatant", "approprié", "art",
            "astucieux", "étonnant", "étrange", "attrayant", "aux", "pommes", "avantageux", "bath", "beau", "fixe", "beauté",
            "bellâtre", "bellissime", "bien", "bien", "élevé", "bien", "balancé", "bien", "bâti", "bien", "fait", "bien",
            "moulé", "bien", "proportionné", "bien", "roulé", "bienséant", "bien", "tourné", "biquet", "bizarre", "bon",
            "brave", "brillant", "céleste", "calme", "chéri", "charmant", "chic", "choisi", "chouette", "civil", "clair",
            "comique", "considérable", "consommé", "convenable", "coquet", "correct", "coureur", "cultivé", "curieux",
            "décent", "délicat", "délicieux", "dameret", "désirable", "digne", "distingué", "divin", "doux", "drôle", "dru",
            "enchanteur", "enjoué", "ensoleillé", "esthétique", "estimable", "excellent", "exquis", "extra", "fabuleux",
            "féerique", "fallacieux", "fameux", "fantastique", "fastueux", "faux", "favorable", "fichu", "fieffé", "fier",
            "fin", "flatteur", "flirt", "florissant", "formidable", "fort", "fructueux", "gai", "galant", "galantin",
            "généreux", "génial", "gent", "gentil", "girond", "glorieux", "goût", "grâce", "gracieux", "grand",
            "grandiose", "gras", "gros", "habile", "harmonieux", "haut", "heureux", "honnête", "honorable", "idéal",
            "important", "imposant", "incomparable", "intéressant", "joli", "juste", "limpide", "lucratif", "magique",
            "magistral", "magnanime", "magnifique", "majestueux", "mensonger", "menteur", "merveilleux", "mignon", "mirifique",
            "monumental", "noble", "non", "pareil", "paisible", "parader", "parfait", "passionnant", "perfection", "piquant",
            "pittoresque", "plaisant", "poétique", "poli", "précieux", "printanier", "profond", "propice", "prospère", "pur",
            "ravissant", "remarquable", "rengorger", "resplendissant", "riant", "riche", "robuste", "rupin", "sacré", "séduisant",
            "saint", "sélect", "sans", "pareil", "sculptural", "sensationnel", "serein", "seyant", "simple", "solide", "somptueux",
            "sortable", "splendide", "stupéfiant", "sublime", "supérieur", "super", "superbe", "tenter", "trompeur", "unique", "vain", "vertueux"]

    def process(self, msg, user):
        if str(self.room.bot_username) in msg:
            for mot in self.dict:
                if mot.lower() in msg:
                    if user == self.room.admin_username:
                        self._send("C'est très aimable mon cher " + str(user))
                        self._send("!n " + str(user))
                    else:
                        self._send("Oh merci c'est gentil " + str(user) + ". Je ne m'attendais pas à ça de ta part !")
                    return
            self._send("Plaît-il ?")
        return

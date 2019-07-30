# Patchnote Officiel

## Service PokemOnIRC

### Patch 1.1 - *Anti-vegan Update*

Sortie le 24 juillet 2018

- Refonte complète des probabilités d'attraper des pokemons en fonction des objets utilisés
- Affichage des probabilités d'attraper le pokemon dans la commande *?pokemon*
- Lorsqu'on broie un pokemon, celui-ci donne désormais ***(puissance)²*** kébabs
- Les pokeballs s'achètent désormais par **3** au shop
- Les difficultés des pokemon ont été revu afin de mieux satisfaire la majorité des joueurs
- Afin de pouvoir s'habituer au nouveau système de jeu, **10** morceaux de barbapapa, **3** pokeballs et **1** superball ont été donnés à chacun des joueurs

### Patch 1.2 - *Moonstone Update*

Sortie le 29 juillet 2018

- Les formules de probabilités d'attraper des pokemons ont été revus à la hausse après la modification de la 1.1. Le coût moyen étant devenu trop élevé.
- Ajout de l'objet **pierre Lune**. Celle-ci permettra de faire évoluer ses pokemons dans un patch à venir.
- Ajout de l'évènement régulier *La Charade du Père Fouras* permettant de gagner des pierres Lune.
- Affichage du pokedex sur une page web associée. La commande _!pokedex_ n'affichera désormais plus que le nombre total de pokemons différents possédés ainsi qu'un lien vers cette page.
- La commande _!pokestuff_ s'utilise désormais comme la commande _!pokedex_ et permet de cibler un autre joueur.
- La commande _?pokemon_ a été remplacée par la commande _!pokemon_ pour plus de consistance.
- La commande _!broyer_ a été remplacée par la commande _!crush_ pour plus de consistance.
- Correction de la *puissance* du pokemon **Hypnomade** (**4->6**).
- Correction du nom du pokemon **Papilusion** (appelé par erreur **Papillusion** dans la base de données).
- Correction du nom du pokemon **Krabby** (appelé par erreur **Kraby** dans la base de données).
- Correction d'un bug lors de l'achat d'un objet pour une personne inconnue. Tous les achats sont désormais donnés à l'acheteur si aucun destinataire n'a pu être trouvé.

### Patch 1.3 - *Evolution Update*

- Ajout de la commande _!evolve_ permettant de faire évoluer ses pokemons. Pour cela, il faut disposer d'une pierre Lune, puis le nourrir avec un nombre de kébabs qui dépend de la **puissance** de son évolution. Le pokemon **Evoli** fait exception à ce mécanisme puisqu'il faudra disposer de pierres légendaires encore non introduites dans le jeu.
- La *difficulté* d'un pokemon est désormais appelée **puissance** (*power*).
- La *rareté* d'un pokemon est désormais appelée **fréquence** (*rate*).
- Correction de la typo sur le mot **comptabilise**.
- Correction de l'inversion des deux pokemons **M.** et **Mme Nidoran** (rassurez-vous, aucune présupposition de genre n'a été faites ici, cette information ayant été remontée par les pokemons eux-même)

### Patch 1.4 - *Eevee Update*

- Ajout des objets **pierre Foudre**, **pierre Feu**, **pierre Eau**. Celles-ci permettent de faire évoluer le pokemon **Evoli** en respectivement **Voltali**, **Pyroli** et **Aquali**.
- Ajout des commandes :
  - __!moonevolve__ *<pokemon/id>*
  - __!thundervolve__ *<pokemon/id>*
  - __!fireevolve__ *<pokemon/id>*
  - __!waterevolve__ *<pokemon/id>*
- Ces nouvelles commandes permettent de faire évoluer un pokemon en utilisant la pierre correspondante (respectivement **Lune**, **Foudre**, **Feu** et **Eau**).
- La commande _!evolve_ existe toujours et utilise la **pierre Lune** par défaut.
- Ajout de l'objet **coffre à butin**. Un fois ouvert, celui-ci permet d'obtenir des butins plus ou moins rares. Les **coffre à butin** permettent notamment d'obtenir les pierres légendaires **Foudre**, **Feu** et **Eau**.
- Ajout de la commande _!open lootbox_ permettant d'ouvrir un **coffre à butin**
- *La Charade du Père Fouras* fait désormais gagner un **coffre à butin** et non une **pierre Lune**.
- Lorsque vous vous balladez dans des hautes herbes, vos chances de rencontrer des pokemons ou le père Fouras sont multiplier par 10.
- Ajout de la page de statistiques du jeu.

### Patch 1.5 Soon™

Rien de prévu pour l'instant

### A venir prochainement

Annonces racoleuses et non contractuelles.

- Affichage des profils des joueurs sur une page web associée
- API Rest pour consulter la base de données du jeu
- API Rest pour consulter l'ensemble des statistiques liées aux évènements du jeu
- Mise en place des badges pokemon
- Echange de pokemons
- Ajout des pierres legendaires (feu, eau, foudre) pour faire évoluer Evoli.

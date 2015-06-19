============
Flexagone 72
============

Qu'est-ce que c'est ?
=====================

Le flexagone est une forme géométrique, topologiquement analogue à un ruban de
Möbius, qui peut être pliée et dépliée de sorte à dévoiler de nouvelles faces.

Notre flexagone72 est composé de 24 triangles élémentaires se combinant pour
former 72 faces hexagonales différentes.

Organisation du dépôt
=====================

theme_XXX:
Dossier contenant le thème XXX composé principalement des triangles de base

templates:
Dossier contenant les outils pour créer les fichiers de sortie

build_XXX:
Dossier pour stocker les fichiers intermédiaires servant à la construction des
fichiers de sortie pour le thème XXX

out:
Dossier où sont créés les fichiers de sortie

Makefile:
Le Makefile pour construire le tout !

Fabriquer
=========

Pour construire les fichiers de sortie, il faut avoir quel utilitaires de base
unix (mkdir, cp...) ainsi que le logiciel Inkscape.

$ make THEME=XXX

Fichiers de sortie
==================

Les fichiers de sortie contiennent notamment le patron à découper pour le
thème choisi ainsi que la carte pour passer d'une face à une autre. Au moment
où ce document est écrit, la carte est partielle.

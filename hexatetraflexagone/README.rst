==================
Hexatétraflexagone
==================

Qu'est-ce que c'est ?
=====================

Le flexagone est une forme géométrique, topologiquement analogue à un ruban de
Möbius, qui peut être pliée et dépliée de sorte à dévoiler de nouvelles faces.

L'hexatétraflexagone a une forme carrée et comporte 6 faces (avec de multiple combinaisons).

Organisation du dossier
=======================

theme_XXX:
Dossier contenant le thème XXX composé principalement des images de base

templates:
Dossier contenant les outils pour créer les fichiers de sortie

build/XXX:
Dossier pour stocker les fichiers intermédiaires servant à la construction des
fichiers de sortie pour le thème XXX

out:
Dossier où sont créés les fichiers de sortie

generate.sh:
Le script pour construire le tout !

Fabriquer
=========

Pour construire les fichiers de sortie, il faut avoir convert de imagemagick
ainsi que le logiciel Inkscape.

$ ./generate.sh XXX # avec XXX le thème voulu

Fichiers de sortie
==================

Les fichiers de sortie contiennent le patron à découper pour le thème choisi.

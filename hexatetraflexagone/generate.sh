#!/bin/sh

THEME=$1
[ "$THEME" == "" ] && THEME=simple

mkdir -p build/$THEME
for i in 1 2 3 4 5 6
do
	convert -crop 50%x50% theme_$THEME/face$i.png build/$THEME/face$i.png
done
cp templates/patron.svg build/$THEME/

mkdir -p out
inkscape -z -e out/patron_$THEME.png build/$THEME/patron.svg

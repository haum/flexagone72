#!/bin/sh

THEME=$1
[ "$THEME" == "" ] && THEME=simple

mkdir -p build/$THEME
for i in 1 2 3 4 5 6
do
	convert -crop 50%x50% theme_$THEME/face$i.png build/$THEME/face$i.png
done
cp templates/patron_p1.svg build/$THEME/
cp templates/patron_p2.svg build/$THEME/

mkdir -p out
inkscape -z -e out/patron_p1_$THEME.png build/$THEME/patron_p1.svg
inkscape -z -e out/patron_p2_$THEME.png build/$THEME/patron_p2.svg

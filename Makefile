THEME?=study

T=build/triangles/triangle

all: patron

build/triangles:
	mkdir -p build/triangles

$T%.svg: build/triangles theme_${THEME}/triangle%.svg
	cp $(word 2,$^) $@

triangles: $T01.svg $T02.svg $T03.svg $T04.svg $T05.svg $T06.svg $T07.svg $T08.svg $T09.svg $T10.svg $T11.svg $T12.svg $T13.svg $T14.svg $T15.svg $T16.svg $T17.svg $T18.svg $T19.svg $T20.svg $T21.svg $T22.svg $T23.svg $T24.svg

out:
	mkdir -p out

patron: out/patron.pdf

build/patron.svg: templates/patron.svg
	cp $^ $@

out/patron.pdf: triangles out build/patron.svg
	inkscape -z -A $@ $(word 3,$^)

clean:
	rm -rf build

distclean: clean
	rm -rf out

.PHONY: clean distclean all triangles patron

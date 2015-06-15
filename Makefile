THEME?=study

T=build/triangles/triangle
F=build/faces/face

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

build/faces:
	mkdir -p build/faces

$F%.svg: build/faces templates/faces/face%.svg
	cp $(word 2,$^) $@

$F%.png: triangles $F%.svg
	inkscape -z -e $@ $(word 2,$^)

faces: $F01.png $F02.png $F03.png $F04.png $F05.png $F06.png $F07.png $F08.png $F09.png $F10.png $F11.png $F12.png $F13.png $F14.png $F15.png $F16.png $F17.png $F18.png $F19.png $F20.png $F21.png $F22.png $F23.png $F24.png $F25.png $F26.png $F27.png $F28.png $F29.png $F30.png $F31.png $F32.png $F33.png $F34.png $F35.png $F36.png

clean:
	rm -rf build

distclean: clean
	rm -rf out

.PRECIOUS: $F01.svg $F02.svg $F03.svg $F04.svg $F05.svg $F06.svg $F07.svg $F08.svg $F09.svg $F10.svg $F11.svg $F12.svg $F13.svg $F14.svg $F15.svg $F16.svg $F17.svg $F18.svg $F19.svg $F20.svg $F21.svg $F22.svg $F23.svg $F24.svg $F25.svg $F26.svg $F27.svg $F28.svg $F29.svg $F30.svg $F31.svg $F32.svg $F33.svg $F34.svg $F35.svg $F36.svg

.PHONY: clean distclean all triangles patron faces

THEME?=study

T=build/triangles/triangle
TS=$T01.svg $T02.svg $T03.svg $T04.svg $T05.svg $T06.svg $T07.svg $T08.svg $T09.svg $T10.svg $T11.svg $T12.svg $T13.svg $T14.svg $T15.svg $T16.svg $T17.svg $T18.svg $T19.svg $T20.svg $T21.svg $T22.svg $T23.svg $T24.svg
F=build/faces/face
FS=$F01.png $F02.png $F03.png $F04.png $F05.png $F06.png $F07.png $F08.png $F09.png $F10.png $F11.png $F12.png $F13.png $F14.png $F15.png $F16.png $F17.png $F18.png $F19.png $F20.png $F21.png $F22.png $F23.png $F24.png $F25.png $F26.png $F27.png $F28.png $F29.png $F30.png $F31.png $F32.png $F33.png $F34.png $F35.png $F36.png $F37.png $F38.png $F39.png $F40.png $F41.png $F42.png $F43.png $F44.png $F45.png $F46.png $F47.png $F48.png $F49.png $F50.png $F51.png $F52.png $F53.png $F54.png $F55.png $F56.png $F57.png $F58.png $F59.png $F60.png $F61.png $F62.png $F63.png $F64.png $F65.png $F66.png $F67.png $F68.png $F69.png $F70.png $F71.png $F72.png

all: patron map

build/triangles:
	mkdir -p build/triangles

$T%.svg: theme_${THEME}/triangle%.svg | build/triangles
	cp $(word 1,$^) $@

triangles: ${TS}

build:
	mkdir -p build

out:
	mkdir -p out

patron: out/patron.pdf

build/patron.svg: templates/patron.svg | build
	cp $(word 1,$^) $@

out/patron.pdf: build/patron.svg ${TS} | out
	inkscape -z -A $@ $(word 1,$^)

build/faces:
	mkdir -p build/faces

$F%.svg: templates/faces/face%.svg | build/faces
	cp $(word 1,$^) $@

$F%.png: $F%.svg ${TS}
	inkscape -z -e $@ $(word 1,$^)

faces: ${FS}

build/map.svg: | build
	cp templates/map.svg build/

out/map.pdf: build/map.svg ${FS} | out
	inkscape -z -A $@ $(word 1,$^)

map: out/map.pdf

clean:
	rm -rf build

distclean: clean
	rm -rf out

.PRECIOUS: $F01.svg $F02.svg $F03.svg $F04.svg $F05.svg $F06.svg $F07.svg $F08.svg $F09.svg $F10.svg $F11.svg $F12.svg $F13.svg $F14.svg $F15.svg $F16.svg $F17.svg $F18.svg $F19.svg $F20.svg $F21.svg $F22.svg $F23.svg $F24.svg $F25.svg $F26.svg $F27.svg $F28.svg $F29.svg $F30.svg $F31.svg $F32.svg $F33.svg $F34.svg $F35.svg $F36.svg $F37.svg $F38.svg $F39.svg $F40.svg $F41.svg $F42.svg $F43.svg $F44.svg $F45.svg $F46.svg $F47.svg $F48.svg $F49.svg $F50.svg $F51.svg $F52.svg $F53.svg $F54.svg $F55.svg $F56.svg $F57.svg $F58.svg $F59.svg $F60.svg $F61.svg $F62.svg $F63.svg $F64.svg $F65.svg $F66.svg $F67.svg $F68.svg $F69.svg $F70.svg $F71.svg $F72.svg

.PHONY: clean distclean all triangles patron faces

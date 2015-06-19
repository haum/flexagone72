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

faces: ${FS}

build/map.svg: | build
	cp templates/map.svg build/

out/map.pdf: build/map.svg ${FS} | out
	inkscape -z -A $@ $(word 1,$^)

map: out/map.pdf

build/faces/face01.png: build/faces/face01.svg $T03.svg $T18.svg $T19.svg $T08.svg $T09.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face02.png: build/faces/face02.svg $T06.svg $T17.svg $T16.svg $T23.svg $T22.svg $T07.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face03.png: build/faces/face03.svg $T06.svg $T07.svg $T22.svg $T23.svg $T16.svg $T17.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face04.png: build/faces/face04.svg $T01.svg $T10.svg $T21.svg $T20.svg $T05.svg $T04.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face05.png: build/faces/face05.svg $T03.svg $T12.svg $T09.svg $T08.svg $T19.svg $T18.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face06.png: build/faces/face06.svg $T01.svg $T04.svg $T05.svg $T20.svg $T21.svg $T10.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face07.png: build/faces/face07.svg $T01.svg $T16.svg $T17.svg $T06.svg $T07.svg $T10.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face08.png: build/faces/face08.svg $T04.svg $T15.svg $T14.svg $T21.svg $T20.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face09.png: build/faces/face09.svg $T04.svg $T05.svg $T20.svg $T21.svg $T14.svg $T15.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face10.png: build/faces/face10.svg $T02.svg $T11.svg $T08.svg $T19.svg $T18.svg $T03.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face11.png: build/faces/face11.svg $T01.svg $T10.svg $T07.svg $T06.svg $T17.svg $T16.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face12.png: build/faces/face12.svg $T02.svg $T03.svg $T18.svg $T19.svg $T08.svg $T11.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face13.png: build/faces/face13.svg $T04.svg $T05.svg $T08.svg $T11.svg $T14.svg $T15.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face14.png: build/faces/face14.svg $T02.svg $T13.svg $T24.svg $T19.svg $T18.svg $T03.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face15.png: build/faces/face15.svg $T02.svg $T03.svg $T18.svg $T19.svg $T24.svg $T13.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face16.png: build/faces/face16.svg $T01.svg $T12.svg $T09.svg $T06.svg $T17.svg $T16.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face17.png: build/faces/face17.svg $T04.svg $T15.svg $T14.svg $T11.svg $T08.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face18.png: build/faces/face18.svg $T01.svg $T16.svg $T17.svg $T06.svg $T09.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face19.png: build/faces/face19.svg $T02.svg $T03.svg $T06.svg $T09.svg $T24.svg $T13.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face20.png: build/faces/face20.svg $T01.svg $T12.svg $T23.svg $T22.svg $T17.svg $T16.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face21.png: build/faces/face21.svg $T01.svg $T16.svg $T17.svg $T22.svg $T23.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face22.png: build/faces/face22.svg $T04.svg $T15.svg $T14.svg $T11.svg $T10.svg $T07.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face23.png: build/faces/face23.svg $T02.svg $T13.svg $T24.svg $T09.svg $T06.svg $T03.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face24.png: build/faces/face24.svg $T04.svg $T07.svg $T10.svg $T11.svg $T14.svg $T15.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face25.png: build/faces/face25.svg $T01.svg $T04.svg $T07.svg $T22.svg $T23.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face26.png: build/faces/face26.svg $T10.svg $T21.svg $T20.svg $T15.svg $T14.svg $T11.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face27.png: build/faces/face27.svg $T10.svg $T11.svg $T14.svg $T15.svg $T20.svg $T21.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face28.png: build/faces/face28.svg $T02.svg $T13.svg $T24.svg $T09.svg $T08.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face29.png: build/faces/face29.svg $T01.svg $T12.svg $T23.svg $T22.svg $T07.svg $T04.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face30.png: build/faces/face30.svg $T02.svg $T05.svg $T08.svg $T09.svg $T24.svg $T13.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face31.png: build/faces/face31.svg $T02.svg $T05.svg $T20.svg $T21.svg $T10.svg $T11.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face32.png: build/faces/face32.svg $T08.svg $T19.svg $T18.svg $T13.svg $T24.svg $T09.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face33.png: build/faces/face33.svg $T08.svg $T09.svg $T24.svg $T13.svg $T18.svg $T19.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face34.png: build/faces/face34.svg $T03.svg $T12.svg $T23.svg $T22.svg $T07.svg $T06.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face35.png: build/faces/face35.svg $T02.svg $T11.svg $T10.svg $T21.svg $T20.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face36.png: build/faces/face36.svg $T03.svg $T06.svg $T07.svg $T22.svg $T23.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face37.png: build/faces/face37.svg $T02.svg $T13.svg $T24.svg $T21.svg $T18.svg $T03.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face38.png: build/faces/face38.svg $T04.svg $T05.svg $T10.svg $T11.svg $T14.svg $T15.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face39.png: build/faces/face39.svg $T04.svg $T15.svg $T14.svg $T11.svg $T10.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face40.png: build/faces/face40.svg $T01.svg $T16.svg $T17.svg $T20.svg $T23.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face41.png: build/faces/face41.svg $T02.svg $T03.svg $T18.svg $T21.svg $T24.svg $T13.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face42.png: build/faces/face42.svg $T01.svg $T12.svg $T23.svg $T20.svg $T17.svg $T16.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face43.png: build/faces/face43.svg $T04.svg $T15.svg $T14.svg $T23.svg $T20.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face44.png: build/faces/face44.svg $T01.svg $T16.svg $T17.svg $T06.svg $T07.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face45.png: build/faces/face45.svg $T01.svg $T12.svg $T07.svg $T06.svg $T17.svg $T16.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face46.png: build/faces/face46.svg $T02.svg $T03.svg $T18.svg $T19.svg $T22.svg $T13.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face47.png: build/faces/face47.svg $T04.svg $T05.svg $T20.svg $T23.svg $T14.svg $T15.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face48.png: build/faces/face48.svg $T02.svg $T13.svg $T22.svg $T19.svg $T18.svg $T03.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face49.png: build/faces/face49.svg $T06.svg $T17.svg $T16.svg $T13.svg $T22.svg $T07.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face50.png: build/faces/face50.svg $T02.svg $T03.svg $T18.svg $T19.svg $T08.svg $T09.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face51.png: build/faces/face51.svg $T02.svg $T09.svg $T08.svg $T19.svg $T18.svg $T03.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face52.png: build/faces/face52.svg $T04.svg $T05.svg $T20.svg $T21.svg $T24.svg $T15.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face53.png: build/faces/face53.svg $T06.svg $T07.svg $T22.svg $T13.svg $T16.svg $T17.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face54.png: build/faces/face54.svg $T04.svg $T15.svg $T24.svg $T21.svg $T20.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face55.png: build/faces/face55.svg $T08.svg $T19.svg $T18.svg $T15.svg $T24.svg $T09.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face56.png: build/faces/face56.svg $T04.svg $T05.svg $T20.svg $T21.svg $T10.svg $T11.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face57.png: build/faces/face57.svg $T04.svg $T11.svg $T10.svg $T21.svg $T20.svg $T05.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face58.png: build/faces/face58.svg $T06.svg $T07.svg $T22.svg $T23.svg $T14.svg $T17.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face59.png: build/faces/face59.svg $T08.svg $T09.svg $T24.svg $T15.svg $T18.svg $T19.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face60.png: build/faces/face60.svg $T06.svg $T17.svg $T14.svg $T23.svg $T22.svg $T07.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face61.png: build/faces/face61.svg $T10.svg $T21.svg $T20.svg $T17.svg $T14.svg $T11.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face62.png: build/faces/face62.svg $T01.svg $T06.svg $T07.svg $T22.svg $T23.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face63.png: build/faces/face63.svg $T01.svg $T12.svg $T23.svg $T22.svg $T07.svg $T06.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face64.png: build/faces/face64.svg $T08.svg $T09.svg $T24.svg $T13.svg $T16.svg $T19.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face65.png: build/faces/face65.svg $T10.svg $T11.svg $T14.svg $T17.svg $T20.svg $T21.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face66.png: build/faces/face66.svg $T08.svg $T19.svg $T16.svg $T13.svg $T24.svg $T09.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face67.png: build/faces/face67.svg $T01.svg $T12.svg $T23.svg $T22.svg $T19.svg $T16.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face68.png: build/faces/face68.svg $T02.svg $T03.svg $T08.svg $T09.svg $T24.svg $T13.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face69.png: build/faces/face69.svg $T02.svg $T13.svg $T24.svg $T09.svg $T08.svg $T03.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face70.png: build/faces/face70.svg $T10.svg $T11.svg $T14.svg $T15.svg $T18.svg $T21.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face71.png: build/faces/face71.svg $T01.svg $T16.svg $T19.svg $T22.svg $T23.svg $T12.svg
	inkscape -z -e $@ $(word 1,$^)

build/faces/face72.png: build/faces/face72.svg $T10.svg $T21.svg $T18.svg $T15.svg $T14.svg $T11.svg
	inkscape -z -e $@ $(word 1,$^)

clean:
	rm -rf build

distclean: clean
	rm -rf out

.PRECIOUS: $F01.svg $F02.svg $F03.svg $F04.svg $F05.svg $F06.svg $F07.svg $F08.svg $F09.svg $F10.svg $F11.svg $F12.svg $F13.svg $F14.svg $F15.svg $F16.svg $F17.svg $F18.svg $F19.svg $F20.svg $F21.svg $F22.svg $F23.svg $F24.svg $F25.svg $F26.svg $F27.svg $F28.svg $F29.svg $F30.svg $F31.svg $F32.svg $F33.svg $F34.svg $F35.svg $F36.svg $F37.svg $F38.svg $F39.svg $F40.svg $F41.svg $F42.svg $F43.svg $F44.svg $F45.svg $F46.svg $F47.svg $F48.svg $F49.svg $F50.svg $F51.svg $F52.svg $F53.svg $F54.svg $F55.svg $F56.svg $F57.svg $F58.svg $F59.svg $F60.svg $F61.svg $F62.svg $F63.svg $F64.svg $F65.svg $F66.svg $F67.svg $F68.svg $F69.svg $F70.svg $F71.svg $F72.svg

.PHONY: clean distclean all triangles patron faces

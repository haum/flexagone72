#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from generate import faces, Triangle

def name(tri, sens):
    ori = ('G', 'W', 'R')[int((tri.orient + 2)/2) - sens]
    return ori + tri.nb_str()

paires = {}
for f in faces:
    tris = f.triangles()
    for i in range(6):
        key = name(tris[i], 2) + ',' + name(tris[i-1], 1)
        if tris[i].number > tris[i-1].number:
            key = name(tris[i-1], 1) + ',' + name(tris[i], 2)
        if not key in paires.keys():
            paires[key] = 1
        else:
            paires[key] += 1

print('graph {')
print('mincross = 2.0')
for k in paires.keys():
    a, b = k.split(',')
    print('\t' + a + ' -- ' + b + ' [label=' + str(paires[k]) + ',waight=' + str(paires[k]) + ']')
print('}')

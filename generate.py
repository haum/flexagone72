#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from PIL import Image
from shutil import copyfile
import os, math, sys

THEME='game_dots'
if len(sys.argv) > 1:
    THEME = sys.argv[1]

def should_be_remade(file_old, file_new):
    if not os.path.isfile(file_new):
        return True
    omtime = os.path.getmtime(file_old)
    nmtime = os.path.getmtime(file_new)
    return omtime > nmtime

############
# Triangle #
############
# Triangle is one of the element that will compose an hexagon
class Triangle:
    WIDTH = 800
    HEIGHT = 693
    REGENERATED = list(False for i in range(72))
    
    @classmethod
    def resetUpdates(cls):
        cls.REGENERATED = list(False for i in range(72))

    def __init__(self, nb):
        if nb < 1 or nb > 24:
            raise IndexError('Triangle accepts only number from 1 to 24')
        self.number = nb

    def nb_str(self):
        if self.number < 10:
            return '0' + str(self.number)
        return str(self.number)

####################
# OrientedTriangle #
####################
# OrientedTriangle is a Triangle that have an orientation inside a face
class OrientedTriangle(Triangle):
    NORMAL = 0
    LEFT = -2
    RIGHT = 2

    OFFSETS = (
        (-Triangle.WIDTH/2, -Triangle.HEIGHT/3),
        (-3*Triangle.WIDTH/4, -2*Triangle.HEIGHT/3),
        (-3*Triangle.WIDTH/4, -5*Triangle.HEIGHT/6),
        (-Triangle.WIDTH/2, -2*Triangle.HEIGHT/3),
        (-Triangle.WIDTH/2, -5*Triangle.HEIGHT/6),
        (-Triangle.WIDTH/2, -2*Triangle.HEIGHT/3),
    )

    def __init__(self, nb, orient=NORMAL):
        Triangle.__init__(self, nb)
        self.orient = orient

    def generate(self, theme):
        # Create build directory if needed
        buildpath = './build/' + theme
        if not os.path.exists(buildpath):
                os.makedirs(buildpath)

        # Check if built file is recent
        if Triangle.REGENERATED[self.number-1]:
            return True
        buildfile = buildpath + '/triangle' + self.nb_str() + '.png'
        srcfileprefix = 'theme_' + theme + '/triangle' + self.nb_str()
        if os.path.isfile(srcfileprefix + '.png'):
            if not should_be_remade(srcfileprefix + '.png', buildfile):
                return False
        elif os.path.isfile(srcfileprefix + '.svg'):
            if not should_be_remade(srcfileprefix + '.svg', buildfile):
                return False

        # Build
        Triangle.REGENERATED[self.number-1] = True
        if os.path.isfile(srcfileprefix + '.png'):
            copyfile(srcfileprefix + '.png', buildfile)
        else:
            os.system('inkscape -z -e ' + buildfile + ' ' + srcfileprefix + '.svg')
        print('Triangle ' + self.nb_str() + ' generated.')
        return True

########
# Face #
########
# Face is a set of 6 OrientedTriangle
class Face:
    def __init__(self, nb, t1, t2, t3, t4, t5, t6):
        if nb < 1 or nb > 72:
            raise IndexError('Face accepts only number from 1 to 72')
        self.number = nb
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.t5 = t5
        self.t6 = t6

    def nb_str(self):
        if self.number < 10:
            return '0' + str(self.number)
        return str(self.number)

    def triangles(self):
        return (self.t1, self.t2, self.t3, self.t4, self.t5, self.t6)    

    def generate(self, theme):
        # Generate triangles
        triangles_regenerated = False
        for t in self.triangles():
            triangles_regenerated = triangles_regenerated or t.generate(theme)

        # Check if build is needed
        buildpath = './build/' + theme
        buildfile = buildpath + '/face' + self.nb_str() + '.png'
        if not triangles_regenerated and os.path.isfile(buildfile):
            return False

        # Build
        img = Image.new('RGBA', (2*Triangle.WIDTH, 2*Triangle.HEIGHT), (255, 255, 255, 0))
        angle = 0
        for t in self.triangles():
            rot = (angle + t.orient) % 6
            imgtri = Image.open(buildpath + '/triangle' + t.nb_str() + '.png')
            if rot != 0:
                imgtri = imgtri.rotate(rot * -60, Image.BICUBIC, 1)
            img.paste(imgtri, (int(round(Triangle.WIDTH + math.sin(angle * math.pi / 3) * 2*Triangle.HEIGHT/3 + OrientedTriangle.OFFSETS[rot][0])), int(round(Triangle.HEIGHT - math.cos(angle * math.pi / 3) * 2*Triangle.HEIGHT/3 + OrientedTriangle.OFFSETS[rot][1]))), imgtri)
            angle += 1
        img.save(buildfile)
        print('Face ' + self.nb_str() + ' generated.')
        return True

##########
# Patron #
##########
# Patron of flexagon
class Patron:
    def generate(self, theme):
        # Generate triangles
        triangles_regenerated = False
        for i in range(24):
            t = OrientedTriangle(i + 1, OrientedTriangle.NORMAL)
            triangles_regenerated = t.generate(theme) or triangles_regenerated

        # Build
        rebuild = False
        buildpath = './build/' + theme
        buildfile = buildpath + '/patron_inner.png'
        img = Image.new('RGBA', (7*Triangle.WIDTH, 2*Triangle.HEIGHT), (255, 255, 255, 0))
        if triangles_regenerated or not os.path.isfile(buildfile):
            for i in range(12):
                t = OrientedTriangle(i + 1, OrientedTriangle.NORMAL)
                t.generate(theme)
                imgtri = Image.open(buildpath + '/triangle' + t.nb_str() + '.png')
                if (i+1) & 1 == 0:
                    imgtri = imgtri.rotate(180, Image.BICUBIC, 1)
                img.paste(imgtri, (int(round(Triangle.WIDTH/2 + Triangle.WIDTH/2*i)), 0), imgtri)
                t = OrientedTriangle(i + 13, OrientedTriangle.NORMAL)
                t.generate(theme)
                imgtri = Image.open(buildpath + '/triangle' + t.nb_str() + '.png')
                if (i+1) & 1 == 0:
                    imgtri = imgtri.rotate(180, Image.BICUBIC, 1)
                img.paste(imgtri, (int(round(Triangle.WIDTH/2*i)), Triangle.HEIGHT), imgtri)
            img.save(buildfile)
            rebuild = True

        # Infos
        buildfile = buildpath + '/patron_infos.png'
        srcfile = 'theme_' + theme + '/infos.svg'
        if should_be_remade(srcfile, buildfile):
            os.system('inkscape -z -e ' + buildfile + ' ' + srcfile)
            rebuild = True

        # Background
        buildfile = buildpath + '/patron_outter.png'
        srcfile = 'templates/patron.svg'
        if should_be_remade(srcfile, buildfile):
            os.system('inkscape -z -e ' + buildfile + ' ' + srcfile)
            rebuild = True

        # Build final
        buildfile2 = 'out/patron_' + theme + '.jpg'
        if not os.path.exists('out'):
                os.makedirs('out')
        if not os.path.exists(buildfile2) or rebuild:
            imgout = Image.open(buildfile)
            img = Image.open(buildpath + '/patron_inner.png')
            imgout.paste(img, (106, 1359), img)
            img = Image.open(buildpath + '/patron_infos.png')
            imgout.paste(img, (200, 2901), img)
            imgout.save(buildfile2)
            print('Paton generated.')

        return True

#######
# Map #
#######
# Map of flexagon
class Map:
    def generate(self, theme):
        # Generate faces
        faces_regenerated = False
        for f in faces:
            faces_regenerated = f.generate(theme) or faces_regenerated

        # Template
        buildpath = './build/' + theme
        buildfile = buildpath + '/map.svg'
        srcfile = 'templates/map.svg'
        if should_be_remade(srcfile, buildfile):
            copyfile(srcfile, buildfile)

        # Build
        buildfile = 'out/map_' + theme + '.png'
        if not os.path.exists('out'):
                os.makedirs('out')
        if faces_regenerated or should_be_remade(buildpath + '/map.svg', buildfile):
            os.system('inkscape -z -e ' + buildfile + ' ' + buildpath + '/map.svg')


#############
# All faces #
#############
# Inventory of all possible faces
faces = (
    Face(
        1,
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.NORMAL),
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.NORMAL)
    ),
    Face(
        2,
        OrientedTriangle(6, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.LEFT)
    ),
    Face(
        3,
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.NORMAL)
    ),
    Face(
        4,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.LEFT),
        OrientedTriangle(4, OrientedTriangle.NORMAL)
    ),
    Face(
        5,
        OrientedTriangle(3, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.RIGHT),
        OrientedTriangle(9, OrientedTriangle.LEFT),
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.NORMAL)
    ),
    Face(
        6,
        OrientedTriangle(1, OrientedTriangle.RIGHT),
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.NORMAL),
        OrientedTriangle(10, OrientedTriangle.LEFT)
    ),
    Face(
        7,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.NORMAL),
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(10, OrientedTriangle.NORMAL)
    ),
    Face(
        8,
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.LEFT)
    ),
    Face(
        9,
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.NORMAL)
    ),
    Face(
        10,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.NORMAL),
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(3, OrientedTriangle.LEFT)
    ),
    Face(
        11,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(10, OrientedTriangle.RIGHT),
        OrientedTriangle(7, OrientedTriangle.LEFT),
        OrientedTriangle(6, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.NORMAL)
    ),
    Face(
        12,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.NORMAL),
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.RIGHT)
    ),
    Face(
        13,
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.NORMAL)
    ),
    Face(
        14,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(3, OrientedTriangle.LEFT)
    ),
    Face(
        15,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.NORMAL)
    ),
    Face(
        16,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(6, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.NORMAL)
    ),
    Face(
        17,
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.LEFT),
        OrientedTriangle(8, OrientedTriangle.RIGHT),
        OrientedTriangle(5, OrientedTriangle.LEFT)
    ),
    Face(
        18,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.NORMAL),
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.RIGHT),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        19,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(6, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.NORMAL)
    ),
    Face(
        20,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.NORMAL)
    ),
    Face(
        21,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        22,
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.LEFT),
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.NORMAL)
    ),
    Face(
        23,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.LEFT),
        OrientedTriangle(6, OrientedTriangle.RIGHT),
        OrientedTriangle(3, OrientedTriangle.LEFT)
    ),
    Face(
        24,
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.RIGHT),
        OrientedTriangle(10, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.NORMAL)
    ),
    Face(
        25,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        26,
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.LEFT)
    ),
    Face(
        27,
        OrientedTriangle(10, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.NORMAL)
    ),
    Face(
        28,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.LEFT),
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.NORMAL)
    ),
    Face(
        29,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.LEFT),
        OrientedTriangle(4, OrientedTriangle.RIGHT)
    ),
    Face(
        30,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.RIGHT),
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.NORMAL)
    ),
    Face(
        31,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.NORMAL),
        OrientedTriangle(10, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.NORMAL)
    ),
    Face(
        32,
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.LEFT)
    ),
    Face(
        33,
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.NORMAL)
    ),
    Face(
        34,
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.LEFT),
        OrientedTriangle(6, OrientedTriangle.NORMAL)
    ),
    Face(
        35,
        OrientedTriangle(2, OrientedTriangle.RIGHT),
        OrientedTriangle(11, OrientedTriangle.LEFT),
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.LEFT)
    ),
    Face(
        36,
        OrientedTriangle(3, OrientedTriangle.RIGHT),
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        37,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(3, OrientedTriangle.LEFT)
    ),
    Face(
        38,
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(10, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.NORMAL)
    ),
    Face(
        39,
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.LEFT),
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.LEFT)
    ),
    Face(
        40,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        41,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.RIGHT),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.NORMAL)
    ),
    Face(
        42,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.RIGHT),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.NORMAL)
    ),
    Face(
        43,
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.LEFT)
    ),
    Face(
        44,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.NORMAL),
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        45,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.LEFT),
        OrientedTriangle(6, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.NORMAL)
    ),
    Face(
        46,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.NORMAL)
    ),
    Face(
        47,
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.RIGHT),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.NORMAL)
    ),
    Face(
        48,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.RIGHT),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(3, OrientedTriangle.LEFT)
    ),
    Face(
        49,
        OrientedTriangle(6, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.LEFT)
    ),
    Face(
        50,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.NORMAL),
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.NORMAL)
    ),
    Face(
        51,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.LEFT),
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(3, OrientedTriangle.LEFT)
    ),
    Face(
        52,
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.NORMAL)
    ),
    Face(
        53,
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.RIGHT),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.NORMAL)
    ),
    Face(
        54,
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.RIGHT),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.LEFT)
    ),
    Face(
        55,
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(15, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.LEFT)
    ),
    Face(
        56,
        OrientedTriangle(4, OrientedTriangle.LEFT),
        OrientedTriangle(5, OrientedTriangle.NORMAL),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.NORMAL),
        OrientedTriangle(10, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.NORMAL)
    ),
    Face(
        57,
        OrientedTriangle(4, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.LEFT),
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(5, OrientedTriangle.LEFT)
    ),
    Face(
        58,
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.NORMAL)
    ),
    Face(
        59,
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.RIGHT),
        OrientedTriangle(18, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.NORMAL)
    ),
    Face(
        60,
        OrientedTriangle(6, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.RIGHT),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.LEFT)
    ),
    Face(
        61,
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(20, OrientedTriangle.NORMAL),
        OrientedTriangle(17, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.LEFT)
    ),
    Face(
        62,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(6, OrientedTriangle.LEFT),
        OrientedTriangle(7, OrientedTriangle.NORMAL),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        63,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(7, OrientedTriangle.LEFT),
        OrientedTriangle(6, OrientedTriangle.NORMAL)
    ),
    Face(
        64,
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.NORMAL)
    ),
    Face(
        65,
        OrientedTriangle(10, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(17, OrientedTriangle.RIGHT),
        OrientedTriangle(20, OrientedTriangle.LEFT),
        OrientedTriangle(21, OrientedTriangle.NORMAL)
    ),
    Face(
        66,
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.LEFT),
        OrientedTriangle(16, OrientedTriangle.RIGHT),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.LEFT)
    ),
    Face(
        67,
        OrientedTriangle(1, OrientedTriangle.LEFT),
        OrientedTriangle(12, OrientedTriangle.NORMAL),
        OrientedTriangle(23, OrientedTriangle.LEFT),
        OrientedTriangle(22, OrientedTriangle.NORMAL),
        OrientedTriangle(19, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.NORMAL)
    ),
    Face(
        68,
        OrientedTriangle(2, OrientedTriangle.LEFT),
        OrientedTriangle(3, OrientedTriangle.NORMAL),
        OrientedTriangle(8, OrientedTriangle.LEFT),
        OrientedTriangle(9, OrientedTriangle.NORMAL),
        OrientedTriangle(24, OrientedTriangle.LEFT),
        OrientedTriangle(13, OrientedTriangle.NORMAL)
    ),
    Face(
        69,
        OrientedTriangle(2, OrientedTriangle.NORMAL),
        OrientedTriangle(13, OrientedTriangle.LEFT),
        OrientedTriangle(24, OrientedTriangle.NORMAL),
        OrientedTriangle(9, OrientedTriangle.LEFT),
        OrientedTriangle(8, OrientedTriangle.NORMAL),
        OrientedTriangle(3, OrientedTriangle.LEFT)
    ),
    Face(
        70,
        OrientedTriangle(10, OrientedTriangle.LEFT),
        OrientedTriangle(11, OrientedTriangle.NORMAL),
        OrientedTriangle(14, OrientedTriangle.LEFT),
        OrientedTriangle(15, OrientedTriangle.NORMAL),
        OrientedTriangle(18, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.NORMAL)
    ),
    Face(
        71,
        OrientedTriangle(1, OrientedTriangle.NORMAL),
        OrientedTriangle(16, OrientedTriangle.LEFT),
        OrientedTriangle(19, OrientedTriangle.RIGHT),
        OrientedTriangle(22, OrientedTriangle.LEFT),
        OrientedTriangle(23, OrientedTriangle.NORMAL),
        OrientedTriangle(12, OrientedTriangle.LEFT)
    ),
    Face(
        72,
        OrientedTriangle(10, OrientedTriangle.NORMAL),
        OrientedTriangle(21, OrientedTriangle.LEFT),
        OrientedTriangle(18, OrientedTriangle.RIGHT),
        OrientedTriangle(15, OrientedTriangle.LEFT),
        OrientedTriangle(14, OrientedTriangle.NORMAL),
        OrientedTriangle(11, OrientedTriangle.LEFT)
    )
)

########
# Main #
########
# Generate files
if __name__ == "__main__":
    Triangle.resetUpdates()
    Patron().generate(THEME)
    Map().generate(THEME)

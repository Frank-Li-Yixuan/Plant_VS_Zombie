import objectBase
import sunshine
import peaBullet
import time
import pygame as py
from const import *
class SunFlower(objectBase.ObjectBase):
    def __init__(self, id, pos):
        super(SunFlower, self).__init__(id, pos)
        self.sunShines = []
        self.hasSunshine = False
    def preSummon(self):

        self.hasSunshine = True
    def hasSummon(self):
        return self.hasSunshine
    def doSummon(self):
        if self.hasSunshine:
            self.hasSunshine = False
            return sunshine.Sunshine(2, (self.pos[0] + 20, self.pos[1] - 10))

    def update(self):
        super(SunFlower, self).update()
        for s1 in self.sunShines:
            s1.update()
    def draw(self, Win):
        super(SunFlower, self).draw(Win)
        for s1 in self.sunShines:
            s1.draw(Win)




class PeaShooter(objectBase.ObjectBase):
    def __init__(self, id, pos):
        super(PeaShooter, self).__init__(id, pos)
        self.hasShoot = False
        self.hasBullet = False
    def preSummon(self):
        if self.status == 0:
            return
        elif self.status == 1:
            self.pathIndex = 0
            self.hasBullet = True
    def hasSummon(self):
        return self.hasBullet
    def doSummon(self):
        if self.hasBullet:
            self.hasShoot = True
            self.hasBullet = False
            sound1 = py.mixer.Sound(PATH_SHOOT)
            sound1.play()
            return peaBullet.PeaBullet(0, (self.pos[0] + 3, self.pos[1]))

    def update(self):
        super(PeaShooter, self).update()

    def draw(self, Win):
        super(PeaShooter, self).draw(Win)
    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getIndexCD():
            return
        self.preIndexTime = time.time()

        index = self.pathIndex + 1
        if index == 5 and self.hasShoot:
            self.hasShoot = False
        if index >= self.pathIndexCount:
            index = 0
        self.updateIndex(index)


class WallNut(objectBase.ObjectBase):
    def __init__(self, id, pos):
        super(WallNut, self).__init__(id, pos)
        self.crack1hp = self.hp * 0.6
        self.crack2hp = self.hp * 0.3
        self.crack1 = False
        self.crack2 = False

    def update(self):
        super(WallNut, self).update()

    def draw(self, Win):
        super(WallNut, self).draw(Win)
    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getIndexCD():
            return
        self.preIndexTime = time.time()

        index = self.pathIndex + 1
        if self.hp < self.crack1hp:
            self.crack1 = True
        elif self.hp < self.crack2hp:
            self.crack2 = True

        if self.crack1 == True:
            self.status = 1

        if self.crack2 == True:
            self.status = 2

        if index >= self.pathIndexCount:
            index = 0
        self.updateIndex(index)
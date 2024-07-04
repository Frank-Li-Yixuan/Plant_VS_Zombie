import image
import time
import data_object
import pygame as py
from const import *
class ObjectBase(image.Image):
    def __init__(self, id, pos):
        self.id = id
        self.status = 0
        self.existTime = time.time()
        self.preIndexTime = 0
        self.prePositionTime = 0
        self.preSummonTime = 0
        self.preAttackTime = 0

        self.hp = self.getData()['HP']
        self.atk = self.getData()['ATK']
        super(ObjectBase, self).__init__(
            self.status,
            self.getData()['PATH'],
            self.getData()['PATH_STATUS_ONE'],
            self.getData()['PATH_STATUS_TWO'],
            0,
            pos,
            self.getData()['SIZE'],
            self.getData()['IMAGE_INDEX_MAX']
        )
    def getData(self):
        return data_object.data[self.id]
    def update(self):
        self.checkSummon()
        self.checkImageIndex()
        self.checkPosition()
    def summonSound(self):
        if self.id == 0:
            sound1 = py.mixer.Sound(self.getData()['SUMMON_SOUND_PATH'])
            sound1.play()
    def summonBurst(self, Win):
        if self.id == 0:
            Win.blit(py.image.load(PATH_PEA_BULLET_BURST), self.getRect(0, 0, (52, 46)))
            return 5

    def isCollide(self, other):
        if self.getRect(self.getCollideDeviation(), self.getCollideDeviationY(), self.getCollideSize()).colliderect(other.getRect(other.getCollideDeviation(), other.getCollideDeviationY(), other.getCollideSize())):
            return True
    def getCollideDeviation(self):
        return self.getData()['COLLIDE_DEVIATION']
    def getCollideDeviationY(self):
        return self.getData()['COLLIDE_DEVIATION_Y']
    def getPositionCD(self):
        return self.getData()['POSITION_CD']
    def getCollideSize(self):
        return self.getData()['COLLIDE_SIZE']
    def getSummonCD(self):
        return self.getData()['SUMMON_CD']

    def getAttackCD(self):
        return self.getData()['ATTACK_CD']
    def canPick(self):
        return self.getData()['CANPICK']
    def canFight(self):
        return self.getData()['CANFIGHT']
    def getPrice(self):
        return self.getData()['PRICE']
    def getIndexCD(self):
        return self.getData()['IMAGE_INDEX_CD']
    def getSpeed(self):
        return self.getData()['SPEED']

    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getIndexCD():
            return
        self.preIndexTime = time.time()

        index = self.pathIndex + 1
        if self.id ==5:
            if index >= self.pathIndexCount:
                self.status = -100
                return
        if index >= self.pathIndexCount:
            index = 0
        self.updateIndex(index)

    def checkSummon(self):
        if time.time() - self.preSummonTime <= self.getSummonCD():
            return False
        self.preSummonTime = time.time()
        self.preSummon()
    def getIndexByPos(self, pos):
        x = (pos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (pos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x, y
    def checkPosition(self):
        if time.time() - self.prePositionTime <= self.getPositionCD():
            return False
        self.prePositionTime = time.time()
        speed = self.getSpeed()
        if self.status == 0:
            self.pos = (self.pos[0] + speed[0], self.pos[1] + speed[1])
        elif self.status == 1:
            return True
        return True

    def preSummon(self):
        pass
    def hasSummon(self):
        pass
    def doSummon(self):
        pass
import pygame as py
import data_object
from const import *
class Image(py.sprite.Sprite):
    def __init__(self, status, pathFmt, pathStatus1, pathStatus2, pathIndex, pos, size, pathIndexCount):
        self.status = status
        self.pathFmt = pathFmt
        self.pathStatus1 = pathStatus1
        self.pathStatus2 = pathStatus2
        self.pathIndex = pathIndex
        self.size = size
        self.pathIndexCount = pathIndexCount
        self.pos = list(pos)
        self.updateImage()
    def getRect(self, collide_deviation = 0, collide_deviation_y = 0, collide_size = (0,0)):
        rect = self.image.get_rect()
        rect.x, rect.y = (self.pos[0] + collide_deviation, self.pos[1] + collide_deviation_y)
        if collide_size != (0,0):
            rect.width, rect.height = collide_size
        return rect

    def updateImage(self):
        if self.status == 0:
            path = self.pathFmt
        elif self.status == 1:
            path = self.pathStatus1
        elif self.status == -1:
            path = PATH_NORMAL_ZOMBIE_LOST_HEAD
        elif self.status == -2:
            path = PATH_NORMAL_ZOMBIE_DIE

        if self.pathIndexCount !=0:
            path = path % self.pathIndex
        self.image = py.image.load(path)
        if self.size:
            self.image = py.transform.scale(self.image, self.size)

    def updateSize(self, size):
        self.size = size
        self.updateImage()
    def updateIndex(self, pathIndex):
        self.pathIndex = pathIndex
        self.updateImage()
    def draw(self, Win):
        Win.blit(self.image, self.getRect())


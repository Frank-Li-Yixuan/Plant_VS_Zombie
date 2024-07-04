import objectBase
import time
class ZombieBase(objectBase.ObjectBase):
    # def __init__(self, pathFmt, pathIndex, pos, size = None, pathIndexCount = 0):
    #     super(ZombieBase, self).__init__(pathFmt, pathIndex, pos, size, pathIndexCount)
    #
    # def getIndexCD(self):
    #     return 0.1
    # def getPositionCD(self):
    #
    #     return 0.01
    # def checkPosition(self):
    #     b = super(ZombieBase, self).checkPosition()
    #     if b:
    #         self.pos[0] -= 0.1
    #     return b
    def fight(self, other):
        self.hp -= other.atk
        other.hp -= self.atk
        if self.hp <= 0:
            return True
        if other.hp <= 0:
            return False
        return
    pass
    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getIndexCD():
            return
        self.preIndexTime = time.time()
        if self.id ==1 and self.status==-1:
            index = self.pathIndex + 1
            if index >= 22:
                self.status = -2
                index = 0
                self.updateIndex(index)
                return
            self.updateIndex(index)
            return
        elif self.id == 1 and self.status == -2:
            index = self.pathIndex + 1

            if index >= 10:
                self.status = -100
                return
            self.updateIndex(index)
            return

        index = self.pathIndex + 1

        if self.id ==5:
            if index >= self.pathIndexCount:
                self.status = -100
                return
        if index >= self.pathIndexCount:
            index = 0
        self.updateIndex(index)


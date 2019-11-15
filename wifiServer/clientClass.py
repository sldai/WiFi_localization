from particleFilterClass import particleFilter
import math
import numpy as np
class client:
    def __init__(self,ip,apNum, type, path, theta0):
        self.ip=ip
        self.apNum=apNum
        self.type = type
        self.path = path
        self.theta0 = theta0
        self.pF=particleFilter(apNum,type,path)

        self.ifIni = False

    def update(self, data):
        if data[0] == 0:
            observe = data[1:(1 + self.apNum)]
            self.pF.particleUpdate(observe)

        elif data[0] == 1:
            move = [data[1] * math.cos(math.radians(-data[2] + self.theta0)),
                    data[1] * math.sin(math.radians(-data[2] + self.theta0))]
            self.pF.particleMove(np.array(move))

        if self.pF.ifResample(50) == 1:
            self.pF.particleResample()

    def clientIni(self, data):
        self.pF.particleInitial(self.pF.knn(data[1:(1 + self.apNum)],11),100)
        self.ifIni = True

    def getMean(self):
        return self.pF.getMean()


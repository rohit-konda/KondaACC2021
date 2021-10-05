from limcomorder import *
import numpy as np


def getRanges(x1, x2, y1, y2, dx, dy):
    from itertools import product
    rangeX = np.arange(x1, x2 + dx, dx)
    rangeY = np.arange(y1, y2 + dy, dy)
    return list(product(rangeX, rangeY))


class Arena():
    def __init__(self, dim, gaussians):
        self.gaussians = gaussians
        self.x = dim[0]
        self.y = dim[1]

    def getRangeXY(self):
        DXY = .2
        return getRanges(0, self.x, 0, self.y, DXY, DXY)

    def evalGauss(self, gauss, point):
        A = gauss[0]
        dx = (point[0] - gauss[0][0])**2
        dy = (point[1] - gauss[0][1])**2
        sigx = 2 * gauss[1][0]**2
        sigy = 2 * gauss[1][1]**2
        return A * np.exp(-dx / sigx - dy / sigy)

    def evalP(self, point):
        if 0 <= point[0] <= self.x and 0 <= point[1] <= self.y:
            sumGauss = 1
            for gauss in self.gaussians:
                sumGauss += self.evalGauss(gauss, point)
            return sumGauss
        else:
            return 0


class Triangle():
    ''' class for defining a Triangle '''
    def __init__(self, p1, p2, p3):
        self.vertices = (p1, p2, p3)

    def pointIn(self, point):
        ''' check if given point is in the Triangle '''
        v = self.vertices
        boolIn = [False] * 3
        for i in range(3):
            if v[i][0] - v[i - 1][0] != 0:
                m = (v[i][1] - v[i - 1][1]) / (v[i][0] - v[i - 1][0])
                b = v[i][1] - m * v[i][0]
                dirP = np.sign(point[1] - m * point[0] - b)
                dirV = np.sign(v[i - 2][1] - m * v[i - 2][0] - b)
                boolIn[i] = dirV == dirP or dirP == 0
            else:
                dirP = np.sign(point[0] - v[i][0])
                dirV = np.sign(v[i - 2][0] - v[i][0])
                boolIn[i] = dirV == dirP or dirP == 0
        return all(boolIn)


def makeErdosGraph(n, p):
    ''' fill neighborList based on Erdos-graph (p probability of edge existing) '''
    from itertools import combinations
    edges = combinations(range(n), 2)
    neighborList = [[] for _ in range(n)]
    for e in edges:
        if np.random.rand() <= p:
            neighborList[e[0]].append(e[1])
            neighborList[e[1]].append(e[0])
    return neighborList


def welfare(arena, triangles, rangeXY):
    def inAnyTri(p):
        return float(any([tri.pointIn(p) for tri in triangles]))
    w = np.mean([arena.evalP(p) * inAnyTri(p) for p in rangeXY])
    return w * arena.x * arena.y


class TowerParam():
    def __init__(self, x, y, ang, dist, spread):
        self.x = x
        self.y = y
        self.ang = ang
        self.dist = dist
        self.spread = spread
        self.DXY = .1

    def getTriangle(self, ang):
        p1 = (self.x, self.y)
        ang1rad = (ang - self.spread) * np.pi / 180
        p2x = self.dist * np.cos(ang1rad)
        p2y = self.dist * np.sin(ang1rad)
        p2 = (self.x + p2x, self.y + p2y)
        ang2rad = (ang + self.spread) * np.pi / 180
        p3x = self.dist * np.cos(ang2rad)
        p3y = self.dist * np.sin(ang2rad)
        p3 = (self.x + p3x, self.y + p3y)
        return Triangle(p1, p2, p3)

    def getRangeXY(self):
        DXY = .1
        x1 = self.x - self.dist
        x2 = self.x + self.dist
        y1 = self.y - self.dist
        y2 = self.y + self.dist
        return getRanges(x1, x2, y1, y2, DXY, DXY)


class SensorTower(LimComAgent):
    def __init__(self, par, arena, iD=None):
        LimComAgent.__init__(self, iD)
        self.par = par
        self.arena = arena
        self.Ai = list(range(0, 360, 10))
        self.rangeXY = self.par.getRangeXY()

    def getBR(self, actionSet):
        ang = np.max([self.util(ang, actionSet) for ang in self.Ai])
        return self.getAct(ang)

    def util(self, ang, actionSet):
        triangles = list(actionSet.values()) + [self.getAct(ang)]
        return welfare(self.arena, triangles, self.rangeXY)

    def getAct(self, ang):
        return self.par.getTriangle(ang)


class SensorScenario(LimComScenario):
    def __init__(self, agents, neighborList, arena):
        LimComScenario.__init__(self, agents, neighborList)
        self.arena = arena
        DXY = .1
        self.rangeXY = getRanges(0, arena.x, 0, arena.y, DXY, DXY)

    def getOpt(self):
        from itertools import product
        actions = product([a.Ai for a in self.agents])
        maxWelf = 0
        for jact in actions:
            triangles = [self.agents[i].getAct(ang) for i, ang in enumerate(jact)]
            welf = welfare(arena, triangles, self.rangeXY)
            if welf > maxWelf:
                maxWelf = welf
        return maxWelf

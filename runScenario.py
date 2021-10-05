import numpy as np
from sensorScenario import *


def makeLGauss():
    pos = (np.random.rand() * x, np.random.rand() * y)
    var = (np.random.norm(1), np.random.normal(1))
    A = np.random.normal(1)
    return [(pos, var, A) for _ in num]


def makeArena():
    arenaDim = (5, 5)
    gaussians = []  # makeLGauss()
    return Arena(arenaDim, gaussians)


def makeAgent(i, arena):
    x = np.random.rand() * arena.x
    y = np.random.rand() * arena.y
    ang = 0
    dist = 1
    spread = 30
    tp = TowerParam(x, y, ang, dist, spread)
    return SensorTower(tp, arena, i)


def makeScenario():
    n = 5
    p = .2
    arena = makeArena()
    graph = makeErdosGraph(n, p)
    agents = [makeAgent(i, arena) for i in range(n)]
    senS = SensorScenario(agents, graph, arena)
    return senS


def main():
    senS = makeScenario()
    senS.runSim()


if __name__ == '__main__':
    main()

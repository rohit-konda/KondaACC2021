from sensorScenario import *
from runScenario import *
import unittest


def plotTriangles(triangles):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    _, ax = plt.subplots()
    for tri in triangles:
        p = Polygon(np.array(tri.vertices), alpha=0.2, color='red')
        ax.add_patch(p)
    plt.show()

print(25*.75)

arena = makeArena()
rxy = getRanges(0, 5, 0, 5, .5, .5)
triangles = [Triangle((5, 0), (0, 0), (0, 5)), Triangle((5, 5), (0, 0), (0, 5))]
print(welfare(arena, triangles, rxy))








class ErdosTest(unittest.TestCase):
    def testCorner(self):
        self.assertEqual(makeErdosGraph(3, 0), [[], [], []])
        self.assertEqual(makeErdosGraph(3, 1), [[1, 2], [0, 2], [0, 1]])

    def testUndirected(self):
        for _ in range(10):
            self.assertEqual(len(makeErdosGraph(3, .2)), 3)
            self.assertIn(0)


class TriangleTest(unittest.TestCase):
    def test(self):
        pass






if __name__ == '__main__':
    #unittest.main()
    pass
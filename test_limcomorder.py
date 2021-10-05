from limcomorder import *
import unittest


class AgentTester(LimComAgent):
    def __init__(self, iD):
        LimComAgent.__init__(self, iD)

    def getBR(self, actionSet):
        return list(self.actionSet.keys())


class CommunicationTest(unittest.TestCase):

    def testMethods(self):
        pass




if __name__ == '__main__':
    unittest.main()

# if __name__ == '__main__':
#     neighborList = [[1], [0], [3], [2]]
#     agents = [LimComAgent(1), LimComAgent(2), LimComAgent(3), LimComAgent(4)]
#     LCS = LimComScenario(agents, neighborList)
#     for i in range(10):
#         LCS.step()
#         # for m in LCS.messageList:
#         #     print(m)
#         # print()
#         print([a.actionSet for a in LCS.agents], LCS.checkDone())
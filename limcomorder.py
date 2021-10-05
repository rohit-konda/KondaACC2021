class LimComAgent():
    def __init__(self, iD):
        self.iD = iD  # agent-specific tag that may be assigned to an agent
        self.lowest = self.iD  # lowest agent tag that has been viewed
        self.ord = 1  # ordering when algorithm is finished
        self.parent = None  # parent when executing depth-first search
        self.children = []  # possible children when executing the depth-first search
        self.childrenComp = []  # children that have completed best response (and their all of their children)
        self.neighbors = []  # neighborhood set
        self.actionSet = {}  # keeps track of best responses of other agents
        self.complete = False  # tracks if all children have performed a best response in order

    def bestResponse(self):
        ''' perform best response and update self.actionSet '''
        Br = self.getBR(self.actionSet)
        self.actionSet[str(self.iD)] = Br

    def getBR(self, actionSet):
        ''' calculate the best response given an actionSet'''
        raise NotImplementedError

    def message(self):
        ''' message that is sent to neighbors'''
        return {
            'iD': self.iD,
            'lowest': self.lowest,
            'actionSet': dict(self.actionSet),  # copy of self.actionSet
            'child': self.children[0] if self.children else None,  # the child is the first in the list
            'complete': self.complete
        }

    def update(self, messages):
        ''' agent update after receiving messages from neighbors'''
        if not self.neighbors:
            # initialize neighborhood set based on initial messages recieved
            self.neighbors = [m['iD'] for m in messages]
            # initialize children set
            self.children = [m['iD'] for m in messages if m['lowest'] > self.lowest]
            self.bestResponse()
        else:
            lower = None
            # get lowest 'lowest' from messages and see if self is selected in the depth-first search
            for i, m in enumerate(messages):
                if m['lowest'] < self.lowest and m['child'] == self.iD:
                    self.lowest = m['lowest']
                    lower = i
            if lower is not None:  # if there is a message with lower 'lowest' (reset info)
                self.parent = messages[lower]['iD']  # switch parent to relevant neighbor
                self.actionSet = messages[lower]['actionSet']  # update action ledger
                self.ord = len(messages[lower]['actionSet']) + 1  # update order in the greedy algorithm
                self.complete = False  # make sure that self is not complete
                self.bestResponse()  # perform best response

            for m in messages:
                # if lowest is higher : add neighbor to children
                if m['iD'] in self.children and m['lowest'] < self.lowest:
                    self.children.pop(self.children.index(m['iD']))
                # if lowest is lower : remove neighbor from children
                elif m['iD'] not in self.children and m['lowest'] > self.lowest:
                    self.children.append(m['iD'])
                elif m['lowest'] == self.lowest:
                    # check if child is completed
                    if self.children and m['iD'] == self.children[0] and m['complete']:
                        self.actionSet.update(m['actionSet'])
                        child = self.children.pop(0)
                        self.childrenComp.append(child)
            # if depth first search ends, update to complete
            if not self.children:
                self.complete = True


class LimComScenario():
    def __init__(self, agents, neighborList):
        self.agents = agents  # list of agents in the scenario
        self.neighborList = neighborList  # list of list of agents that are in the neighborhood for each agent
        self.t = 0  # time
        self.messageList = None  # messages that are passed

    def step(self):
        ''' perform one communication step for every agent'''
        messageList = [[self.agents[j].message() for j in nL] for nL in self.neighborList]
        self.messageList = [a.message() for a in self.agents]
        for i, agent in enumerate(self.agents):
            agent.update(messageList[i])
        self.t += 1

    def checkDone(self):
        ''' terminate condition if all agents have completed '''
        completedAll = all([agent.complete for agent in self.agents])
        return completedAll

    def runSim(self, T=100):
        ''' run step function until terminated condition is reached or T steps have been performed. '''
        c = 0
        while not self.checkDone() or c < T:
            self.step()
            c += 1
        print('SIMULATION COMPLETE')

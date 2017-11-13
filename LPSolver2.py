import os

import pickle

from pulp import pulp, LpVariable, LpProblem, LpMaximize, lpSum


class monad:
    def __init__(self):
        self.region_idx = 0
        self.time_idx = 0
        self.tech_idx = 0
        self.costs = 0
        self.revenus = 0

class monads(list):
    def __init__(self):
        list.__init__(self)

    def getMonadsByYear(self,i):
        tmp = monads()
        for mn in self:
            if mn.time_idx == i:
                tmp.append(mn)
        return tmp



class LP:
    def __init__(self):
        self.monads = monads()
        self.tempH = 0

    def objective(self,tab):

        self.tempH = len(tab[0])
        for i in range(len(tab)):
            for j in range(len(tab[i])):
                for k in range(len(tab[i][j])):
                    mn = monad()
                    mn.region_idx = i
                    mn.time_idx = j
                    mn.tech_idx = k
                    mn.costs = tab[i][j][k][1]
                    mn.revenus = tab[i][j][k][0]
                    self.monads.append(mn)

    def localPL(self,timeStamp):
        prob = LpProblem("Maximize monads", LpMaximize)
        vars_ = ["X" + str(c) for c in range(len(self.monads.getMonadsByYear(timeStamp)))]
        vars = LpVariable.dicts("Number of monads", vars_, lowBound=0)
        ["X" + str(c) for c in range(len(self.monads.getMonadsByYear(timeStamp)))]

        prob += lpSum([rois[c] * vars[c] for c in Chairs])






if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    tab = pickle.load(open(path + "/save.p", "rb"))

    lp = LP()
    lp.objective(tab)
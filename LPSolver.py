import random
import pickle
from pulp import LpProblem, LpMaximize, pulp, LpConstraint, lpSum
import os
class LPResult:
    def __init__(self):
        self.region_idx = 0
        self.time_idx = 0
        self.tech_idx = 0
        self.checked = False
        self.costs = 0
        self.revenus = 0
        self.roi = 0

class LPResults(list):
    def __init__(self):
        list.__init__(self)
    def getChecked(self):
        tmp = LPResults()
        for i in self:
            if i.checked == True:
                tmp.append(i)
        return tmp
    def prints(self):
        for i in self:
            print i.__dict__


class LP():
    def __init__(self):
        self.prob = LpProblem("NEST Optics", LpMaximize)

    def objective(self,tab):
        """Define and create the objective function from the data set and assign this function
                   to a linear problem (prob).

                   Keyword arguments:
                   tab -- (3D list) the data set
                   prob -- (LinearProblem) the linear problem
                """
        dictionary = {}
        for i in range(len(tab)):
            for j in range(len(tab[i])):
                for k in range(len(tab[i][j])):
                    varNameX = 'X' + str(i) + "_" + str(j) + "_" + str(k)
                    varNameD = 'D' + str(i) + "_" + str(j) + "_" + str(k)
                    varNameC = 'C' + str(i) + "_" + str(j) + "_" + str(k)
                    varNameR = 'R' + str(i) + "_" + str(j) + "_" + str(k)

                    self.macroDynamic(varNameX, pulp.LpVariable(varNameX, upBound=1, lowBound=0, cat='LpInteger'))

                    R = tab[i][j][k][0]
                    C = tab[i][j][k][1]

                    # print R,C,R-C
                    globals()[varNameR] = R
                    globals()[varNameC] = C
                    self.macroDynamic(varNameD, R - C)
                    dictionary.update({globals()[varNameX]: globals()[varNameD]})
                    # print globals()[varNameD], globals()[varNameX]

        self.prob += pulp.LpAffineExpression(dictionary)

    def constraint1(self,tab):
        """Create the first family of constraints and assign them to the linear problem.

                   Keyword arguments:
                   tab -- (3D list) the data set
                   prob -- (LinearProblem) the linear problem
                """
        for row in range(len(tab)):
            #w =  [tab[row][j][k] for j in range(len(tab[0])) for k in range(len(tab[0][0]))]
            w = [1 for j in range(len(tab[0])) for k in range(len(tab[0][0]))]
            x_ = ['X' + str(row) + "_" + str(j) + "_" + str(k) for j in range(len(tab[0])) for k in range(len(tab[0][0]))]
            x = self.prob.variablesDict()
            x = self.extract(x, x_).values()
            self.prob += lpSum([w[c] * x[c] for c in range(len(w))]) <= 1, "C_1_" + str(row)


    def constraint2(self,tab,Yb):
        """Create the second family of constraints and assign them to the linear problem.

                   Keyword arguments:
                   tab -- (3D list) the data set
                   prob -- (LinearProblem) the linear problem
        """
        for row in range(len(tab[0])):
            w = [tab[i][row][k][1] for i in range(len(tab)) for k in range(len(tab[0][0]))]
            x_ = ['X' + str(i) + "_" + str(row) + "_" + str(k) for i in range(len(tab)) for k in range(len(tab[0][0]))]
            x = self.prob.variablesDict()
            x = self.extract(x, x_).values()
            self.prob += lpSum([w[c] * x[c] for c in range(len(w))]) <= Yb[row], "C_2_" + str(row)

    def constraint3(self,tab,PpY):
        """Create the third family of constraints andd assign them to the linear problem.

                   Keyword arguments:
                   tab -- (3D list) the data set
                   prob -- (LinearProblem) the linear problem
                """
        for row in range(len(tab[0])):
            w = [1 for i in range(len(tab)) for k in range(len(tab[0][0]))]
            x_ = ['X' + str(i) + "_" + str(row) + "_" + str(k) for i in range(len(tab)) for k in range(len(tab[0][0]))]
            x = self.prob.variablesDict()
            x = self.extract(x, x_).values()
            self.prob += lpSum([w[c] * x[c] for c in range(len(w))]) <= PpY[row], "C_3_" + str(row)

    def constraint4(self,tab):
        """Create the fourth family of constraints andd assign them to the linear problem.

                   Keyword arguments:
                   tab -- (3D list) the data set
                   prob -- (LinearProblem) the linear problem
        """
        idx = 0
        for row in range(len(tab)):
            for row2 in range(len(tab[0][0])):
                w = [1 for j in range(len(tab[0])) ]
                x_ = ['X' + str(row) + "_" + str(j) + "_" + str(row2) for j in range(len(tab[0]))]
                x = self.prob.variablesDict()
                x = self.extract(x, x_).values()
                self.prob += lpSum([w[c] * x[c] for c in range(len(w))]) <= 1, "C_4_" + str(row) + "_" + str(row2)

    def solve(self):
        results = LPResults()
        self.prob.solve()
        print(pulp.LpStatus[lp.prob.status])
        s = []
        selected = []
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                for k in range(len(tab[0][0])):
                    res = LPResult()
                    res.region_idx = i
                    res.time_idx = j
                    res.tech_idx = k
                    varNameX = 'X' + str(i) + "_" + str(j) + "_" + str(k)

                    if globals()[varNameX].varValue < 1:
                        res.checked = False
                    else:
                        res.checked = True

                    res.costs = tab[i][j][k][1]
                    res.revenus = tab[i][j][k][0]
                    res.roi = res.revenus - res.costs
                    results.append(res)
        return results

    @staticmethod
    def macroDynamic(varName, value):
        """Dynamically create variables.

            Keyword arguments:
            varName -- a string to define the variable name
            value -- the value of the variable
            """

        globals()[varName] = value

    @staticmethod
    def extract(dict_,list_):
        tmp = {}
        for i in dict_.keys():
            if i in list_:
                tmp.update({i:dict_[i]})
        return tmp

    @staticmethod
    def generateValues(reg, tim, tech):
        """Generate simulation set for testing purposes.

                Keyword arguments:
                reg -- (Integer) the number of regions
                tim -- (Integer) the temporal horizon
                tech -- (Integer) the number of technologies
        """
        tab = []
        tab_ = []

        for i in range(reg):
            tab_ = []
            for j in range(tim):
                tab__ = []
                for k in range(tech):
                    tab__.append([(1 - j * 0.8) * random.randint(20000, 30000), random.randint(20000, 30000)])
                tab_.append(tab__)
            tab.append(tab_)
        #print len(tab), len(tab[0]), len(tab[0][0])
        return tab

if __name__ == '__main__':
    lp = LP()
    #tab = lp.generateValues(5, 2, 2)
    #pickle.dump(tab, open("save.p", "wb"))
    path = os.path.dirname(os.path.realpath(__file__))
    print path
    tab = pickle.load( open( path + "/save.p", "rb" ))
    Yb = [150000 for i in range(len(tab[0]))]
    PpY = [4 for i in range(len(tab[0]))]
    lp.objective(tab)
    lp.constraint1(tab)
    lp.constraint2(tab,Yb)
    lp.constraint3(tab, PpY)
    lp.constraint4(tab)
    res = lp.solve()
    res.getChecked().prints()


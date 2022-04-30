from pulp import *


def lpsolver(stations,tracks,choicepoints,choicetracks,length,costs,A,B):
    model = LpProblem("Minimize_costs_or_length", LpMinimize)
    nrstations = len(stations)

    P = LpVariable.dicts("points",range(nrstations),0,1,cat='Integer')
    T = LpVariable.dicts("tracks",((i,j) for i in range(nrstations) for j in range(nrstations)), 0, 1,cat='Integer')

    ###objective function
    model += lpSum(A*length[i][j]*T[i,j] + B*costs[i][j]*T[i,j] for i in range(nrstations) for j in range(nrstations))

    for i in range(nrstations):
        for j in range(nrstations):
            if i==j:
                model += T[i,j] == 0                        #can't go from station to itself
            else:
                model += P[i] >= T[i,j]                     #a point is passed if a track incident to it is used
                model += T[i,j] >= choicetracks[i][j]        #use a track if it's in the user's preferences
                model += T[i,j] <= tracks[i][j]              #if a track doesn't exist don't use it

        model += lpSum(T[i,j] for j in range(nrstations)) >= P[i]       #if a point is passed, at least one track incident to it has to be used
        model += P[i] >= choicepoints[i]                                #pass a point if it's in the user's preferences

    model.solve()

    print(pulp.value(model.objective))
    print(LpStatus[model.status])
    for i in range(nrstations):
        print("P_{} = ".format(i), P[i].varValue)
        for j in range(nrstations):
            print("T_{}{} = ".format(i,j), T[i,j].varValue)


stations = ['a','b','c']

tracks = [[0,1,1],[1,0,1],[1,1,0]]

choicepoints = [0,0,0]

choicetracks = [[0,1,0],[1,0,0],[0,0,0]]

length = [[0,8,2],[8,0,1],[2,1,0]]

costs = [[0,1,1],[1,0,1],[1,1,0]]
A, B = 1, 0

sol = lpsolver(stations,tracks,choicepoints,choicetracks,length,costs,A,B)

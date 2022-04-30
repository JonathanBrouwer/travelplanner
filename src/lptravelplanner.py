from pulp import *


def lpsolver(stations,start,end,tracks,choicepoints,choicetracks,length,costs,A,B):
    model = LpProblem("Minimize_costs_or_length", LpMinimize)
    nrstations = len(stations)
    start = stations.index(start)
    end = stations.index(end)
    loop = start == end

    P = LpVariable.dicts("points",range(nrstations),0,None,cat='Integer')
    T = LpVariable.dicts("tracks",((i,j) for i in range(nrstations) for j in range(nrstations)), 0, 1,cat='Integer')

    ###objective function
    model += lpSum(A*length[i][j]*T[i,j] + B*costs[i][j]*T[i,j] for i in range(nrstations) for j in range(nrstations))
    
    for i in range(nrstations):
        if i == start or i == end and loop==False:
            model += lpSum(T[i,j] for j in range(nrstations)) == 1          #the end and start points only have one used edge incident to it
        else:
            model += lpSum(T[i,j] for j in range(nrstations)) >= 2*P[i]     #if it passes through a point, it needs to go out again
        for j in range(nrstations):
            if i == j:
                model+= T[i,j] == 0
            model += P[i] >= T[i,j]                     #a point is passed if a track incident to it is used
            model += T[i,j] >= choicetracks[i][j]        #use a track if it's in the user's preferences
            model += T[i,j] <= tracks[i][j]              #if a track doesn't exist don't use it
            model += T[i,j] == T[j,i]
            
        model += lpSum(T[i,j] for j in range(nrstations)) >= P[i]       #if a point is passed, at least one track incident to it has to be used
        model += P[i] >= choicepoints[i]                                #pass a point if it's in the user's preferences
        
    #print(model)

    model.solve(GUROBI_CMD())

    print(pulp.value(model.objective))
    print(LpStatus[model.status])
    for i in range(nrstations):
        print("P_{} = ".format(i), P[i].varValue)
        for j in range(nrstations):
            print("T_{}{} = ".format(i,j), T[i,j].varValue)

    route = getRoute(T,start,end,nrstations)
    print(route)
    return route

def getNext(T,here,prev,nrstations):
    for nxt in range(nrstations):
        if T[here,nxt].varValue and prev != nxt:
            return "T_{}{}".format(here,nxt), here, nxt

def getRoute(T,start,end,nrstations):
    for nxt in range(nrstations):
        if T[start,nxt].varValue:
            route = ["T_{}{}".format(start,nxt)]
            break
    if nxt == end:
        return route
    else:
        track, prev, here = getNext(T,nxt,start,nrstations)
        route.append(track)
        while here != end:
            track, prev, here = getNext(T,here,prev,nrstations)
            route.append(track)
        return route
        


stations = ['a','b','c','d']

start = 'c'
end = 'a'

tracks = [[0,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,0]]

choicepoints = [0,1,0,1]

choicetracks = [[0,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

length = [[0,8,2,1],[8,0,1,2],[2,1,0,3],[0,2,3,1]]

costs = [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
A, B = 1, 0

sol = lpsolver(stations,start,end,tracks,choicepoints,choicetracks,length,costs,A,B)

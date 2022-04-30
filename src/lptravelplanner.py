import pulp as *


def lpsolver(input_data):
    model = LpProblem("Minimize costs or length", LpMinimize)

    P = LpVariable.dicts("points",range(nrstations),0,1,cat='Integer')
    T = LpVariable.dicts("tracks",((i,j) for i in range(nrstations) for j in range(nrstations)), 0, 1,cat='Integer')

    ###objective function
    model += lpSum(A*length[i,j]*T[i,j] + B*costs[i,j]*T[i,j] for i in range(nrstations) for j in range(nrstations))

    for i in range(nrstations):
        for j in range(nrstations):
            if i==j:
                model += T[i,j] == 0
            else:
                model += P[i] >= T[i,j]
                if choicetracks[i,j] == 1:
                    model += T[i,j] == 1
        model += lpSum(T[i,j] for j in range(nrstations)) >= P[i]
        if choicepoints[i] == 1:
            model += P[i] == 1

    model.solve()




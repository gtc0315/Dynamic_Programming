import numpy as np


class PathPlanning:
    def __init__(self,name):
        self.n,self.start, self.goal, self.C = self.__read_txt(name)
        self.state_space = np.array(range(self.n))
        self.T = self.n-1
        self.policy = [{} for _ in range(self.T)]
        self.value = [{} for _ in range(self.T+1)]

    def __read_txt(self, name):
        print 'reading txt...'
        with open(name,'r') as f:
            n = int(f.readline().strip()) # number of vertices
            start = int(f.readline().strip()) -1 # starting vertex (from 0 to n-1)
            goal = int(f.readline().strip()) -1 # goal vertex (from 0 to n-1)
            c = np.ones((n, n), dtype=float) * 999 # initial cost map
            for q in range(n):
                c[q, q] = 0 # vertex q to q cost 0
            for line in f:
                i, j, wij = line.strip().split(' ')
                c[int(i)-1, int(j)-1] = float(wij) # assign cost on the edge
        return n,start,goal,c

    def cost(self,state,move=-1):
        if move==-1: # gT(x)
            if state==self.goal:
                return 0 # cost score of goal is 0
            else:
                return 999 #  cost score of others is 999
        else: # gt(x,u)
            return self.C[state,move]

    def dynamic_programming(self):
        print 'dynamic programming...'
        for i in self.state_space:
            self.value[self.T][i] = self.cost(i) # VT(x) = gT(x), for all x
        for t in range(self.T - 1, -1, -1): # for t = 0 to T-1

            # Qt(x,u) = gt(x,u) + Ex'~p(|x,u)Vt+1(x'), for all x, all u
            Q = np.zeros((self.n, self.n))
            for i in self.state_space:  # for all x in X
                for u in self.state_space:  # for all u in U
                    Q[i, u] = self.cost(i, u) + self.value[t+1][u]

            # Vt(x) = max Qt(x,u), for all x
            for i in self.state_space:
                self.value[t][i] = np.amin(Q[i, :])

            # pi_t(x) = argmax Qt(x,u), for all x
            for i in self.state_space:
                self.policy[t][i] = np.argmin(Q[i, :])

    def generate_path(self,name):
        print 'writing txt...'
        x = self.start

        # path from t=0 to T
        path = [x]
        pathvalue = [self.value[0][x]]

        # shortest path
        shortest_path = []
        optimal_value = []

        # generate path and value with policy
        for t in range(self.T):
            x = self.policy[t][x]
            path.append(x)
            pathvalue.append(self.value[t + 1][x])

        # remove non-moving steps
        for i in range(len(path) - 1):
            if path[i] != path[i + 1]:
                shortest_path.append(path[i])
                optimal_value.append(pathvalue[i])
        shortest_path.append(path[-1])
        optimal_value.append(pathvalue[-1])

        # convert index 0 - n-1 to 1 - n
        for i in range(len(shortest_path)):
            shortest_path[i] += 1

        # write to file
        with open(name, "w") as out_f:
            out_f.write(' '.join(map(str, shortest_path)) + '\n')
            out_f.write(' '.join(map(str, optimal_value)))


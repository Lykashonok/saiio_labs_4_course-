import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce
opt = __import__("5")

class vertex:
    directs, enters = [], []
    def __init__(self, cost, flow):
        self.cost, self.flow = cost, flow
    def direct(self, destination_vector):
        if destination_vector not in self.directs:
            self.directs.append(destination_vector)
            if self not in destination_vector.enters:
                destination_vector.enters.append(self)
    def getMatrix(self, vertexes):
        M = [[0 for _ in vertexes] for _ in vertexes]
        for vertex in vertexes:
            i = vertexes.index(vertex)
            for direct in vertex.directs:
                j = vertexes.index(direct)
                M[i][j] = direct

def getReadablePath(path):
    """Passing path to dictionary"""
    return [d[i] for i in path]

def get_col(M, col):
    res = []
    for i in range(len(M)):
        for j in range(len(M)):
            if j == col:
                res.append(M[i][j])
    return res

def get_matrix(M, type_of_matrix):
    C = [[0 for _ in M] for _ in M]
    for i in range(len(M)):
        for j in range(len(M)):
            C[i][j] = M[i][j][type_of_matrix]
    return C

def _minCostMaxFlow(M):
    v, v_cur, path = len(M) - 1, 0, None
    while v_cur < v:
        # Residual cost graph
        C = [[M[i][j][0] for j in range(len(M))] for i in range(len(M))]
        
        if path is not None:
            for i in range(len(path)):
                next_index = i + 1
                if next_index < len(path):
                    edge_cost = M[path[i]][path[next_index]][0]
                    edge_p = M[path[i]][path[next_index]][1]
                    edge_cur_p = M[path[i]][path[next_index]][2]
                    if edge_cur_p == 0:
                        C[path[i]][path[next_index]] = edge_cost
                    elif edge_p == edge_cur_p:
                        C[path[next_index]][path[i]] -= edge_cost
                        C[path[i]][path[next_index]] = 0
                    elif edge_cur_p > 0 and edge_cur_p < edge_p:
                        C[path[i]][path[next_index]] = edge_cost
                        C[path[next_index]][path[i]] = -edge_cost

        # Find path with minimal cost
        # path = opt.getAnyPath(C, 0, len(C) - 1)
        path = opt.dijkstra(C, 0, len(C) - 1)[2]
        
        # Go through every edge
        # e1 (straight) = min(c(i, j) - p(i, j))
        # e2 (reverse) = min(p(i, j))
        # e = min(e1, e2, v - v_cur)
        e1, e2 = [np.inf], [np.inf]
        for i in range(len(path)):
            next_index = i + 1
            if next_index < len(path):
                edge_cost = M[path[i]][path[next_index]][0]
                edge_p = M[path[i]][path[next_index]][1]
                edge_cur_p = M[path[i]][path[next_index]][2]
                if edge_cost > 0:
                    new_value = edge_p - edge_cur_p
                    e1.append(new_value)
                elif edge_cost < 0:
                    e1.append(edge_cur_p)
        e = min(min(e1), min(e2), v - v_cur)
        
        for i in range(len(path)):
            next_index = i + 1
            if next_index < len(path):
                if M[path[i]][path[next_index]][0] < 0:
                    M[path[i]][path[next_index]][2] -= e
                elif M[path[i]][path[next_index]][0] > 0:
                    M[path[i]][path[next_index]][2] += e
        v_cur += e
    total = 0
    for i in range(len(M)):
        for j in range(len(M)):
            total += M[i][j][2] * M[i][j][0]
    return total, M

def minCostMaxFlow(C, P):
    M = [[0 for _ in C] for _ in C]
    for i in range(len(C)):
        for j in range(len(C)):
            M[i][j] = [C[i][j], P[i][j], 0]
    return _minCostMaxFlow(M)

C =[#S  A  B  T
    [0, 5, 1, 0],
    [0, 0, 0, 1],
    [0, 1, 0, 6],
    [0, 0, 0, 0],
]
P = [
    [0, 4, 2, 0],
    [0, 0, 0, 2],
    [0, 3, 0, 3],
    [0, 0, 0, 0],
]

total, M = minCostMaxFlow(C, P)
print(total)
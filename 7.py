import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce

M=[# A    B   C    D    E
    [0,   10, 30  ,50,  10], #A
    [0,   0,  0   ,0,   0 ], #B
    [0,   0,  0   ,0,   10], #C
    [0,   40, 20  ,0,   0 ], #D
    [10,  0,  10  ,30,  0 ], #E
]
d = {
  0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",
  "A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,
}

# M=[# A B C D E F G
#     [0,2,3,4,0,0,0], #A
#     [0,0,2,0,3,0,0], #B
#     [0,0,0,0,4,0,0], #C
#     [0,0,1,0,0,5,0], #D
#     [0,0,0,0,0,3,7], #E
#     [0,0,0,0,0,0,3], #F
#     [0,0,0,0,0,0,0], #G
# ]
# d = {
#   0:"1",1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",
#   "1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,
# }

M=[# A B C D E F
    [0,7,4,0,0,0 ], #A
    [0,0,4,0,2,0 ], #B
    [0,0,0,4,8,0 ], #C
    [0,0,0,0,0,12], #D
    [0,0,0,4,0,5 ], #E
    [0,0,0,0,0,0 ], #F
]

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

def show_graph_with_labels(M):
    G = nx.DiGraph(directed=True)
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0:
                G.add_edge(d[i], d[j], weight=M[i][j])
    edge_labels = dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
    pos = nx.spring_layout(G, seed=1)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=3, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels, label_pos=0.3)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def getAnyPath(M, origin, destination, ignore = []):
    """Returns passable path from origin to destination"""
    path, current_destination, visited = [(destination, np.inf)], destination, []
    while current_destination != origin:
        visited.append(current_destination)
        for i in range(len(M)):
            if M[i][current_destination] != 0 and i not in visited and i not in ignore:
                path.append((i, M[i][current_destination]))
                current_destination = i
                break
        else:
            if current_destination not in ignore:
                ignore.append(current_destination)
                return getAnyPath(M, origin, destination, ignore)
            else:
                return []
    return list(reversed(path))
    
def getResidualNetWithFlow(M, path):
    current_flow = reduce(lambda a, b: a if a[1] < b[1] else b, path)[1]
    for i, p in enumerate(path):
        next_vertex = i + 1
        if next_vertex >= len(path):
            break
        i, j = path[i][0], path[next_vertex][0]
        M[i][j] -= current_flow
        M[j][i] += current_flow
    return M, current_flow
            

def ford(M):
    origin, destination = 0, len(M) - 1
    path, max_flow = getAnyPath(M, origin, destination), 0
    while len(path) > 0:
        M, flow = getResidualNetWithFlow(M, path)
        # show_graph_with_labels(M)
        path = getAnyPath(M, origin, destination)
        max_flow += flow
    return M, max_flow

M, max_flow = ford(M)
print(M)
print(max_flow)
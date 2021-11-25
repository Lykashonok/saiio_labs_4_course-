import numpy as np
from functools import reduce

M=[# A B C D E F G
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
# d = {
#   0:"1",1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",
#   "1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,
# }

def getReadablePath(path):
  """Passing path to dictionary"""
  return [d[i] for i in path]

def getPassableVertexes(M, i):
  """Returns vertexes passable from i"""
  result = []
  for j in range(len(M)):
    if M[i][j] != 0:
      result.append(j)
  return result

def dijkstra(M, source, destination = None):
  vertexes = [[np.inf, False, []] for _ in M]
  currentVertex = source
  while True:
    vertexes[currentVertex][1] = True
    passableVertexes = getPassableVertexes(M, currentVertex)
    print("current vertex", getReadablePath([currentVertex]))
    print("passable to", getReadablePath(passableVertexes))
    # value, seen, path
    for index in passableVertexes:
      if vertexes[currentVertex][0] + M[currentVertex][index] <= vertexes[index][0] and not vertexes[index][1]:
        if vertexes[currentVertex][0] == np.inf:
          vertexes[currentVertex][0] = 0
        # print(f"assigning {getReadablePath([index])}, {vertexes[index][0]} => {vertexes[currentVertex][0] + M[currentVertex][index]}")
        vertexes[index][0] = vertexes[currentVertex][0] + M[currentVertex][index]
        vertexes[index][2] = [*vertexes[currentVertex][2], currentVertex]
        

    min_value, min_vertex = np.inf, source
    for index in range(len(vertexes)):
      if vertexes[index][0] < min_value and not vertexes[index][1]:
        min_value, min_vertex = vertexes[index][0], index

    print("min path to vertex ", getReadablePath([min_vertex]))
    if not vertexes[min_vertex][1]:
      currentVertex = min_vertex
    else:
      break
  
  for index in range(len(vertexes)):
    vertexes[index][2].append(index)
    print(getReadablePath([index]), vertexes[index][0], getReadablePath(vertexes[index][2]))
  
  if destination is not None and destination >= 0:
    return vertexes[destination]
  print("raw result", vertexes)
  return vertexes


M=[# A B C D E F G
    [0,2,3,4,0,0,0], #A
    [0,0,2,0,3,0,0], #B
    [0,0,0,0,4,0,0], #C
    [0,0,1,0,0,5,0], #D
    [0,0,0,0,0,3,7], #E
    [0,0,0,0,0,0,3], #F
    [0,0,0,0,0,0,0], #G
]

dijkstra(M, 0)
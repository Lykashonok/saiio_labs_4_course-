import numpy as np

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
d = {
  0:"1",1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",
  "1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,
}

M = [
  [0, 8, 5],
  [3, 0, 0],
  [0, 2, 0],
]

def getReadablePath(path):
  """Passing path to dictionary"""
  return [d[i] for i in path]

def get_col(M, col):
  res = []
  for i in range(len(M)):
    for j in range(len(M)):
      if j == col:
        res.append(M[j][i])
  return res

def getPathFromPathMatrix(P, source, destination):
  path, P = [destination], np.array(P)
  while destination != source:
    col = get_col(P, destination)
    for i in range(len(col)):
      if col[i] != None:
        path.append(i)
        destination = i
        break
  return list(reversed(path))
    
def getReadablePathMatrix(M, P):
  for i in range(len(M)):
    print(f"Vertex {d[i]}")
    for j in range(len(M)):
      if i != j:
        print(f"\tTo vertex {d[j]} - {getReadablePath(getPathFromPathMatrix(P, i, j))} - {M[i][j]}")

def _floid(M):
  P = [[None for _ in M] for _ in M]
  for k in range(len(M)):
    for i in range(len(M)):
      for j in range(len(M)):
        if M[i][k] + M[k][j] < M[i][j]:
          M[i][j], P[i][j] = M[i][k] + M[k][j], k
  return M, P

def floid(M):
  for i in range(len(M)):
    for j in range(len(M)):
      if i != j and M[i][j] == 0:
        M[i][j] = np.inf
  return _floid(M)

M, P = floid(M)
print(M)
print(P)
getReadablePathMatrix(M, P)
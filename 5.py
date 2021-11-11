import numpy as np

M=[# A B C D E F G
    [0,2,3,4,0,0,0], #A
    [0,0,2,0,3,0,0], #B
    [0,0,0,0,4,0,0], #C
    [0,0,1,0,0,5,0], #D
    [0,0,0,0,0,3,7], #E
    [0,0,0,0,0,0,3], #F
    [0,0,0,0,0,0,0], #G
]
d = {
  0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",
  "A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,
}

def getReadablePath(path):
  """Passing path to dictionary"""
  return [d[i] for i in path]

def getIndexesByEnterPoint(M, i):
  """Returns indexes of matrix where enter in vertex with index i exists"""
  result = []
  for j in range(len(M)):
    if M[j][i] != 0:
      result.append(j)
  return result

def getMinPath(M, i, j):
  """Returns min price and path from i to j"""
  vertex_from, price, path = M[i], np.inf, [i]
  price = min(price, M[i][j])

  for index, cur_price in enumerate(vertex_from):
    # if branch points from current vertex
    # and not in destination, calc minPathValue for it
    if index != j and cur_price != 0:
      newPrice, newPath = getMinPath(M, index, j)
      newMinPathPrice = cur_price + newPrice
      if (newMinPathPrice <= price and newMinPathPrice > 0) or M[i][j] == 0:
        price = newMinPathPrice
        path+=newPath
  return price, path

def getLayerMinPath(M, layer, destination):
  """
  Returns price and path of current layer
  By getMinPath though every vertex
  """
  price_and_path = []
  for vertex_index in layer:
    # Finding path and price from current vertex to destination
    cur_price, path = getMinPath(M, vertex_index, destination)
    price_and_path.append(getMinPath(M, vertex_index, destination))
  return price_and_path

def getNewLayer(M, layer_prices_paths):
  """
  Returns new layer after passing
  (layer - vertex array)
  through entered layer to destinatin vertex
  (at first iteration it's last vertex)
  """
  price_and_path, stop_flags = [], []
  for cur_price, path in layer_prices_paths:
    # Getting vertexes connected to last passed vertex
    destination = path[0]
    a = getIndexesByEnterPoint(M, destination)
    b = list(map(lambda p: p[1][0], layer_prices_paths))
    currentLayerIndeces = a
    if len(currentLayerIndeces) == 0:
      stop_flags.append(True)
      price_and_path.append((cur_price, path))
    else:
      stop_flags.append(False)
    price_and_path_array = getLayerMinPath(M, currentLayerIndeces, destination)
    print('current path is ', getReadablePath(path), cur_price)
    if len(currentLayerIndeces) == 0:
      print('path is finished')
    else:
      print('path reachable from vertexes ', getReadablePath(currentLayerIndeces))
    for i in range(len(price_and_path_array)):
      new_price_and_path = (price_and_path_array[i][0] + cur_price, price_and_path_array[i][1] + path)
      print('new price and path is', new_price_and_path[0], getReadablePath(new_price_and_path[1]))
      price_and_path.append(new_price_and_path)
  if False not in stop_flags:
    return layer_prices_paths, True
  return price_and_path, False
  


def getOptimalPath(M, is_max = False):
  if is_max:
    M = list(np.array(M) * -1)
  destination = len(M) - 1
  currentLayerIndeces = getIndexesByEnterPoint(M, destination)
  price_and_path_array = getLayerMinPath(M, currentLayerIndeces, destination)
  price_and_path_array, stop_flag = getNewLayer(M, price_and_path_array)
  while stop_flag == False:
    price_and_path_array, stop_flag = getNewLayer(M, price_and_path_array)
  min_value, result_path = np.inf, []
  for price_and_path in price_and_path_array:
    if price_and_path[0] < min_value:
      min_value, result_path = price_and_path[0], price_and_path[1]
  result_path.append(destination)
  print("result", min_value, getReadablePath(result_path))


getOptimalPath(M, True)
from scipy.optimize import linprog
import numpy as np
from math import trunc, ceil

def fract_part(a):
  return 1 - (ceil(a) - a)
  # return a + 1 - ceil(a)

def isBaseline(baselineIndeces, scalesVector, conditionsMatrix, x):
  baselineMatrix = getBaselineMatrix(baselineIndeces, conditionsMatrix)
  nonBaselineIndeces = [i for i in range(len(x)) if i not in baselineIndeces]
  if len(baselineIndeces) != len(baselineMatrix[0]):
    return False
  if next((i for i in nonBaselineIndeces if x[i] != 0), None) != None:
    return False
  if np.linalg.det(baselineMatrix) == 0:
    return False

  return True

def findNonIntergerValue(haystack):
  max_fract_part, x_to_return = 0, None
  for x in haystack:
    if abs(round(x) - x) > 10 ** -6:  
      current_fract_part = fract_part(x)
      if current_fract_part >= max_fract_part:
        max_fract_part, x_to_return = current_fract_part, x
  return x_to_return

def getBaselineMatrix(baselineIndeces, conditionsMatrix):
  return np.array([np.copy(conditionsMatrix[:,i]) for i in baselineIndeces]).transpose()

def gomori(objective, ineq_left=(), ineq_right=()):
  mainLength = len(objective)
  def gomoriIteration(scalesVector, conditionsMatrix, freeVector):
    bounds = [[0, None] for _ in range(len(scalesVector))]
    res = linprog(scalesVector, conditionsMatrix, freeVector, bounds = bounds, method = 'simplex')
    
    if res.success == False:
      print(res.message)
      return None

    x = res.x
    # Creating baseline indeces
    baselineIndeces = []
    for i in range(len(x)):
      if x[i] != 0:
        baselineIndeces.append(i)
    while len(baselineIndeces) < len(conditionsMatrix):
      for i in range(len(conditionsMatrix[0])):
        if i not in baselineIndeces:
          baselineIndeces.append(i)
          break

    if not isBaseline(baselineIndeces, scalesVector, conditionsMatrix, x):
      raise "Indeces are not baseline!"

    nonIntegerValue = findNonIntergerValue(x)
    if nonIntegerValue == None:
      x_ = [round(x) for x in x]
      return (x[0:mainLength], x_[0:mainLength])
    k = list(x).index(nonIntegerValue)

    nonBaselineIndeces = [i for i in range(len(x)) if i not in baselineIndeces]

    baselineMatrix = np.array([np.copy(conditionsMatrix[:,i]) for i in baselineIndeces]).transpose() # getBaselineMatrix(baselineIndeces, conditionsMatrix)
    nonBaselineMatrix = getBaselineMatrix(nonBaselineIndeces, conditionsMatrix)

    baselineMatrixInv = np.linalg.inv(baselineMatrix)

    l = [0 for i in range(len(baselineIndeces))]
    l[k] = 1
    y = np.dot(l, baselineMatrixInv)
    subConditionsMatrix = []
    for i in range(len(conditionsMatrix[0])):
      subConditionsMatrix.append(np.dot(y, conditionsMatrix[:,i]))
    
    subFreeVector = np.dot(y, freeVector)
    
    newConditionsMatrix = [0 for _ in range(len(conditionsMatrix[0]))]
    for i in range(len(nonBaselineIndeces)):
      newConditionsMatrix[nonBaselineIndeces[i]] = -fract_part(subConditionsMatrix[nonBaselineIndeces[i]])
    newConditionsMatrix += [1]
    temp = conditionsMatrix.tolist()
    for i in temp:
      i += [0]
    temp.append(newConditionsMatrix)
    conditionsMatrix = np.array(temp)
    temp = scalesVector.tolist()
    temp += [0]
    scalesVector = np.array(temp)
    temp = freeVector.tolist()
    temp += [-fract_part(subFreeVector)]
    freeVector = np.array(temp)
    bounds.append((0, None))

    return gomoriIteration(scalesVector, conditionsMatrix, freeVector)
  return gomoriIteration(scalesVector, conditionsMatrix, freeVector)


# scalesVector = np.array([-1, -2])
# conditionsMatrix = np.array([
#     [0, 1],
#     [1, 2],
# ])
# freeVector = np.array([1, 5])

scalesVector = np.array([1, -2, 0, 0])
conditionsMatrix = np.array([
    [-4, 6, 1, 0],
    [1, 1, 0, 1],
])
freeVector = np.array([9, 4])
print('scalesVector', scalesVector)
print('conditionsMatrix', conditionsMatrix)
print('freeVector', freeVector)
print('Result', gomori(scalesVector, conditionsMatrix, freeVector))
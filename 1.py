import numpy as np
import json
from scipy.optimize import linprog
scalesVector = np.array([-1, -1]) # your original c for maximization
conditionsMatrix = [
    [2, 11], 
    [1, 1],
    [4, -5],
]
freeVector = [38, 7, 5]

# scalesVector = np.array([7, 9]) # your original c for maximization
# scalesVector *= -1 # negate the objective coefficients
# conditionsMatrix = [
#     [-1, 3], 
#     [7, 1],
# ]
# freeVector = [6, 35]

# scalesVector = np.array([2, 3]) # your original c for maximization
# scalesVector *= -1 # negate the objective coefficients
# conditionsMatrix = [
#     [3, 5], 
#     [3, 4],
#     [0, 1],
# ]
# freeVector = [60, 34, 8]

# scalesVector = np.array([2, 3]) # your original c for maximization
# scalesVector *= -1 # negate the objective coefficients
# conditionsMatrix = [
#     [3, 4], 
#     [2, 5],
# ]
# freeVector = [24, 22]

# scalesVector = np.array([11, 5, 4]) # your original c for maximization
# scalesVector *= -1 # negate the objective coefficients
# conditionsMatrix = [
#     [3, 2, 8], 
#     [2, 0, 1],
#     [3, 3, 1],
# ]
# freeVector = [11, 5, 13]


def findNonIntergerValue(haystack):
    return next((x for x in haystack if not abs(x-round(x)) < 0.0001), None)

# Brunch and bonds method
def bbm(scalesVector, conditionsMatrix, freeVector):
    def bbmIteration(scalesVector, conditionsMatrix, freeVector, bounds, x_current, non_integer_value):
        non_integer_value_index = list(x_current).index(non_integer_value)
        
        boundsLeft, boundsRight = bounds.copy(), bounds.copy()
        boundsLeft[non_integer_value_index] = (0, int(non_integer_value))
        boundsRight[non_integer_value_index] = (int(non_integer_value+1), None)

        options = {}
        resLeft = linprog(scalesVector, conditionsMatrix, freeVector, bounds=boundsLeft, options=options)
        resRight = linprog(scalesVector, conditionsMatrix, freeVector, bounds=boundsRight, options=options)
        
        if resLeft.success:
            non_integer_value = findNonIntergerValue(resLeft.x)
            if non_integer_value == None:
                resLeft.fun *= -1
                # for i in range(len(resRight.x)):
                #     resRight.x[i] = round(resRight.x[i])
                results[resLeft.fun] = list(resLeft.x)
            else:
                bbmIteration(scalesVector, conditionsMatrix, freeVector, boundsLeft, resLeft.x, non_integer_value)
        if resRight.success:
            non_integer_value = findNonIntergerValue(resRight.x)
            if non_integer_value == None:
                resRight.fun *= -1
                # for i in range(len(resRight.x)):
                #     resRight.x[i] = round(resRight.x[i])
                results[resLeft.fun] = list(resRight.x)
            else:
                bbmIteration(scalesVector, conditionsMatrix, freeVector, boundsRight, resRight.x, non_integer_value)

    bounds, results = [], {}
    for c in scalesVector:
        bounds.append((0, None))
    res = linprog(scalesVector, conditionsMatrix, freeVector, bounds=bounds)
    non_integer_value = findNonIntergerValue(res.x)
    if non_integer_value != None:
        bbmIteration(scalesVector, conditionsMatrix, freeVector, bounds, res.x, non_integer_value)
    print('results')
    print(json.dumps(results, indent = 4))
    if len(results) != 0:
        return results[max(results, key=results.get('fun.x'))]    
    return None


print('scales vector')
print(scalesVector)
print('conditions matrix')
print(conditionsMatrix)
print('free vector')
print(freeVector)
a = bbm(scalesVector, conditionsMatrix, freeVector)
print('integer result is')
print(a)
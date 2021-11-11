import numpy as np

def investorProblem(A, K):
  step = int(K / (len(A[0]) - 1))
  u = list(range(0, K + step, step))
  Q = max(u)
  result = []
  x_list = [u]
  currentElement = len(A) - 1
  max_incomes = [[A[currentElement][i] for i in range(len(u))]]
  currentElement -= 1
  while currentElement >= 0:
    current_income = [A[currentElement][i] for i in range(len(u))]
    last_income = list(reversed(max_incomes[-1]))
    u, remain = x_list[-1], []
    new_income = [0]
    for i, v in enumerate(u):
      if i == 0: continue
      f = current_income[:i+1]
      s = last_income[len(last_income) - i - 1:len(last_income)]
      max_sum = list(np.array(s) + np.array(f))
      max_value = max(max_sum)
      new_income.append(max_value)
      if i == len(u) - 1 - currentElement:
        result.append(u[max_sum.index(max_value)])
    max_incomes.append(new_income)    
    currentElement-=1
  result = list(reversed(result))
  result.append(u[u.index(Q - sum(result))])
  return result

A = [
  [0, 8, 15, 21],
  [0, 6, 17, 20],
  [0, 7, 18, 21]
]
K = 60

print(investorProblem(A, K))
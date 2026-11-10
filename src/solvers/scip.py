from pyscipopt import Model
from src.common import * 

model = Model("コンチ")

const_c = float(input())
c_squared = const_c * const_c

m = [][]

# adiciona variáveis das mochilas no modelo
for i in range(len(backpacks)):
    for j in range(backpacks[i][0]):
        m[i][j] = model.addVar(name=f"m{i}{j}", vtype="B")


# daqui pra baixo copiei de exer do runcodes
x2 = model.addVar(name="x2", vtype="I")

model.setObjective(c_squared * x1 + const_c * x2)

model.addCons(5 * x1 + x2 <= 100)
model.addCons(x1 + -1 * x2 <= 15)
model.addCons(-1 * x1 + 12 * x2 <= 225)
model.addCons(-1 * x1 + -1 * x2 <= -10)
model.addCons(x1 <= 20)
model.addCons(x2 <= 20)

model.addCons(x1 >= 0)
model.addCons(x2 >= 0)

model.hideOutput()
# model.setMaximize()
model.optimize()

solution = model.getObjVal()
x1_sol = model.getVal(x1)
x2_sol = model.getVal(x2)
print("{:}".format(round(solution, 2)))
print("{:}".format(round(x1_sol, 2)))
print("{:}".format(round(x2_sol, 2)))

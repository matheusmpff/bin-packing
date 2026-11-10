from pyscipopt import Model
from src.common import * 

model = Model("コンチ")

m = []

# adiciona variáveis das mochilas no modelo
for k in range(len(backpacks)):
    bag_num = []
    for j in range(backpacks[i][0]):
        bag_tipe[j] = model.addVar(name=f"m{j}{k}", vtype="B")
    m[k] = bag_num


x = []
for i in range(len(relics)):
    bag_type = []
    for k in range(len(backpacks)):
        bag_num = []
        for j in range(backpacks[i][0]):
            bag_num[j] = model.addVar(name=f"x{i}{j}{k}", vtype="I")
        bag_type[k] = bag_num
    x[i] = bag_type

y = model.addVar(name="y", vtype="B")

model.setObjective(m[0][0] + m[0][1] + m[0][2] + m[0][3] + m[0][4] + m[0][5] + m[0][6] + m[0][7] + m[0][8] + m[0][9] + m[1][0] + m[1][1] + m[1][2] + m[1][3] + m[1][4] + m[1][5] + m[2][0] + m[2][1] + m[2][2] + m[2][3] + m[3][0] + m[3][1] + m[3][2] + m[3][3] + m[3][4] + m[3][5] + m[3][6] + m[3][7] + m[3][8] + m[3][9] + m[3][10] + m[3][11] + m[4][0] + m[4][1] + m[4][2] + m[4][3] + m[4][4] + m[4][5] + m[4][6] + m[4][7])

# daqui pra baixo copiei de exer do runcodes


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

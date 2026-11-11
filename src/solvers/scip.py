from pyscipopt import Model, quicksum
from src.common import * 

model = Model("コンチ")

# number of types of backpacks
backpack_tnum = len(backpacks)
j_limits = backpacks[:, QUANTITY]
backpack_weights = backpacks[:,WEIGHT]
backpack_volumes = backpacks[:,VOLUME]
backpack_costs = backpacks[:,COST]

relic_tnum = len(relics)
relic_weights = relics[:,WEIGHT]
relic_volumes = relics[:,VOLUME]
relic_costs = relics[:,COST]

m = []

# variáveis das mochilas no modelo
# note que a ordem das listas é tipo da mochila e depois número da mochila

for k in range(backpack_tnum):
    bag_num = []
    for j in range(backpacks[k][0]):
        bag_num.append(model.addVar(name=f"m_{j}{k}", vtype="B"))
    m.append(bag_num)

# variáveis das relíquias
# note que a ordem em que coloquei as listas foi: tipo, tipo da mochila e número (j-ésima) da mochila

x = []
for i in range(relic_tnum):
    bag_type = []
    for k in range(backpack_tnum):
        bag_num = []
        for j in range(backpacks[k][0]):
            bag_num.append(model.addVar(name=f"x_{i}{j}{k}", vtype="I"))
        bag_type.append(bag_num)
    x.append(bag_type)

y = model.addVar(name="y", vtype="B")

model.setObjective(m[0][0] + m[0][1] + m[0][2] + m[0][3] + m[0][4] + m[1][0] + m[1][1] + m[1][2] + m[2][0] + m[2][1] + m[3][0] + m[3][1] + m[3][2] + m[3][3] + m[3][4] + m[3][5] + m[4][0] + m[4][1] + m[4][2] + m[4][3])

# restrição de peso
for k in range(backpack_tnum):
    for j in range(backpacks[k][0]):
        model.addCons(quicksum(relic_weights[i] * x[i][k][j] for i in range(relic_tnum)) <= backpack_weights[k] * m[k][j])

# restrição volume
for k in range(backpack_tnum):
    for j in range(backpacks[k][0]):
        model.addCons(quicksum(relic_volumes[i] * x[i][k][j] for i in range(relic_tnum)) <= backpack_volumes[k] * m[k][j])

#Restrições para quantidade de reliquias
for i in range(relic_tnum):
    terms = []
    for k in range(backpack_tnum):
        for j in range(j_limits[k]):
            terms.append(x[i][k][j])
    model.addCons(quicksum(terms) == 4)

# Restrições de custo máximo
multiplied_m = []
for k in range(backpack_tnum):
    for j in range(j_limits[k]):
        multiplied_m.append(backpack_costs[k] * m[k][j])

model.addCons(quicksum(multiplied_m) <= C_MAX)

# Restrições para o valor dentro da mochila
for k in range(backpack_tnum):
    for j in range(j_limits[k]):
        multiplied_x = []
        for i in range(5):
            multiplied_x.append(relic_costs[i] * x[i][k][j])
        model.addCons(quicksum(multiplied_x) <= 45000 * m[k][j]) 


# restrição destinatário
num_relics_Muzza = [1, 1, 0, 2, 0]
for i in range(5):
    if num_relics_Muzza[i] != 0:
        model.addCons(x[i][3][0] <= num_relics_Muzza[i] + 10000 * y)
        model.addCons(-1 * x[i][3][0] <= -1 * num_relics_Muzza[i] + 10000 * y)

        model.addCons(x[i][4][0] <= num_relics_Muzza[i] + 10000 * (1 - y))
        model.addCons(-1 * x[i][4][0] <= -1 * num_relics_Muzza[i] + 10000 * (1 - y))
    else:
        model.addCons(x[i][3][0] <= 10000 * y)

        model.addCons(x[i][4][0] <= 10000 * (1 - y))


# variáveis das relíquias: garantir positividade
for i in range(relic_tnum):
    for k in range(len(backpacks)):
        for j in range(j_limits[k]):
            model.addCons(x[i][k][j] >= 0)

# model.hideOutput()
# model.setMaximize()
model.optimize()

solution = model.getObjVal()
print(f"Solução: {solution} mochilas")

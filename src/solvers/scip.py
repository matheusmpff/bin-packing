from pyscipopt import Model, quicksum
from src.common import * 

model = Model("コンチ")

m = []

# variáveis das mochilas no modelo
# note que a ordem das listas é tipo da mochila e depois número da mochila

for k in range(len(backpacks)):
    bag_num = []
    for j in range(backpacks[k][0]):
        bag_num.append(model.addVar(name=f"m_{j}{k}", vtype="B"))
        print(f"Adicionei m{j}{k}")
    m.append(bag_num)

# variáveis das relíquias
# note que a ordem em que coloquei as listas foi: tipo, tipo da mochila e número (j-ésima) da mochila

x = []
for i in range(len(relics)):
    bag_type = []
    for k in range(len(backpacks)):
        bag_num = []
        for j in range(backpacks[k][0]):
            bag_num.append(model.addVar(name=f"x_{i}{j}{k}", vtype="I"))
            print(f"Adicionei x{i}{j}{k}")
        bag_type.append(bag_num)
    x.append(bag_type)

y = model.addVar(name="y", vtype="B")

model.setObjective(m[0][0] + m[0][1] + m[0][2] + m[0][3] + m[0][4] + m[1][0] + m[1][1] + m[1][2] + m[2][0] + m[2][1] + m[3][0] + m[3][1] + m[3][2] + m[3][3] + m[3][4] + m[3][5] + m[4][0] + m[4][1] + m[4][2] + m[4][3])

# restrição de peso

for k in range(len(backpacks)):
    for j in range(backpacks[k][0]):
        model.addCons(quicksum(relics[i][1] * x[i][k][j] for i in range(len(relics))) <= backpacks[k][1] * m[k][j])


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
for i in range(len(relics)):
    for k in range(len(backpacks)):
        for j in range(backpacks[k][0]):
            model.addCons(x[i][k][j] >= 0)

# model.hideOutput()
# model.setMaximize()
model.optimize()

solution = model.getObjVal()
print("{:}".format(round(solution, 2)))

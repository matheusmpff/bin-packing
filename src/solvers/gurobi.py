import gurobipy as gp
from src.common import * 
from gurobipy import GRB

model = gp.Model("model")

j_limits = backpacks[:, QUANTITY]
backpack_weights = backpacks[:,WEIGHT]
backpack_volumes = backpacks[:,VOLUME]
backpack_costs = backpacks[:,COST]

relic_weights = relics[:,WEIGHT]
relic_volumes = relics[:,VOLUME]
relic_costs = relics[:,COST]

#Cria as variáveis binárias m_jk
m = []
for j in range (6):
    aux = []
    for k in range(5):
        if(j >= j_limits[k]):
            aux.append(None)
        else:
            aux.append(model.addVar(lb=0,vtype=GRB.BINARY,name=f"m_{j}{k}"))
    m.append(aux)

#Cria as variáveis inteiras x_ijk
x = []
for i in range(5):
    aux = []
    for j in range(6):
        linha = []
        for k in range(5):
            if(j >= j_limits[k]):
                linha.append(None)
            else:
                linha.append(model.addVar(lb=0,vtype=GRB.INTEGER,name=f"x_{i}{j}{k}"))
        aux.append(linha)
    x.append(aux)
    
# Restrições de peso da mochila
for k in range(5):
    for j in range(j_limits[k]):
        multiplied_x = []
        for i in range(5):
            multiplied_x.append(relic_weights[k]*x[i][j][k])
        model.addConstr(gp.quicksum(multiplied_x)<= backpack_weights[k]*m[j][k])

# Restrições de volume
for k in range(5):
    for j in range(j_limits[k]):
        multiplied_x = []
        for i in range(5):
            multiplied_x.append(relic_volumes[k]*x[i][j][k])
        model.addConstr(gp.quicksum(multiplied_x)<= backpack_volumes[k]*m[j][k])

# Restrições de custo máximo
multiplied_m = []
for k in range(5):
    for j in range(j_limits[k]):
        multiplied_m.append(relic_costs[k]*m[j][k])

model.addConstr(gp.quicksum(multiplied_m)<= C_MAX)

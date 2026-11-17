import gurobipy as gp
from gurobipy import GRB
import json
import numpy as np

# Colunas das mochilas
QUANTITY = 0
WEIGHT = 1
VOLUME = 2
COST = 3

def backpack_gurobi(backpacks, relics):
    C_MAX = 1100 # Caso em que fazemos com 20 reliquias apenas
    total_relics = relics[:,QUANTITY].sum()
    if total_relics != 20:
        C_MAX = (backpacks[:,COST]*backpacks[:,QUANTITY]).sum()*0.6 
    
    #Configura o modelo para limite de 10 segundos e 1 thread
    
    model = gp.Model("model")
    model.Params.TimeLimit = 60
    model.Params.Threads = 1

    # Dados das caixas e reliquias
    
    j_limits = backpacks[:, QUANTITY]
    backpack_weights = backpacks[:,WEIGHT]
    backpack_volumes = backpacks[:,VOLUME]
    backpack_costs = backpacks[:,COST]

    relic_weights = relics[:,WEIGHT]
    relic_volumes = relics[:,VOLUME]
    relic_costs = relics[:,COST]

    #Cria as variáveis binárias m_jk
    
    m = []
    for j in range (np.max(j_limits)):
        aux = []
        for k in range(5):
            if(j >= j_limits[k]):
                aux.append(None)
            else:
                aux.append(model.addVar(lb=0,vtype=GRB.BINARY,name=f"m_{j}_{k}"))
        m.append(aux)
    
    #Cria as variáveis inteiras x_ijk
    
    x = []
    for i in range(5):
        aux = []
        for j in range(np.max(j_limits)):
            linha = []
            for k in range(5):
                if(j >= j_limits[k]):
                    linha.append(None)
                else:
                    linha.append(model.addVar(lb=0,vtype=GRB.INTEGER,name=f"x_{i}_{j}_{k}"))
            aux.append(linha)
        x.append(aux)
        
    # Restrições de peso
    
    for k in range(5):
        for j in range(j_limits[k]):
            multiplied_x = []
            for i in range(5):
                multiplied_x.append(relic_weights[i]*x[i][j][k])
            model.addConstr(gp.quicksum(multiplied_x)<= backpack_weights[k]*m[j][k])

    # Restrições de volume
    
    for k in range(5):
        for j in range(j_limits[k]):
            multiplied_x = []
            for i in range(5):
                multiplied_x.append(relic_volumes[i]*x[i][j][k])
            model.addConstr(gp.quicksum(multiplied_x)<= backpack_volumes[k]*m[j][k])

    #Restrições para quantidade de reliquias
    
    for i in range(5):
        terms= []
        for k in range(5):
            for j in range(j_limits[k]):
                terms.append(x[i][j][k])
        model.addConstr(gp.quicksum(terms) == relics[i,QUANTITY])

    # Restrições de custo máximo
    
    multiplied_m = []
    for k in range(5):
        for j in range(j_limits[k]):
            multiplied_m.append(backpack_costs[k]*m[j][k])
    model.addConstr(gp.quicksum(multiplied_m)<= C_MAX)

    # Restrições para o valor dentro da mochila
    
    for k in range(5):
        for j in range(j_limits[k]):
            multiplied_x = []
            for i in range(5):
                multiplied_x.append(relic_costs[i]*x[i][j][k])
            model.addConstr(gp.quicksum(multiplied_x)<= 45000* m[j][k])
    
    #Define função objetivo
         
    all_ms = gp.quicksum(
        m[j][k]
        for k in range(5)
        for j in range(j_limits[k])
    )
    model.setObjective(all_ms,GRB.MINIMIZE)

    #Executa Otimização
    
    model.optimize()

    #Estrutura do resultado da otimização
    
    resultado = {
        "caixas_utilizadas": [],
        "tempo": 0.0
    }
    
    #Caso o modelo encontre solução otima ou time limit
    
    if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
        print(f"Encontramos uma solução = {model.objVal} caixa(s) utilizada(s)")

        #Caso seja o caso de 20 pegamos as caixas e as reliquias dentro delas
    
        if total_relics == 20:
            for k in range(5):
                for j in range(j_limits[k]):
                    m_jk = model.getVarByName(f"m_{j}_{k}")
                    if m_jk.X !=0:
                        caixa = {
                            "numero":j +1,
                            "tipo": k + 1,
                            "reliquias":{
                            }
                        }
                        for i in range(5):
                            x_ijk = model.getVarByName(f"x_{i}_{j}_{k}")
                            if x_ijk.X !=0:
                                caixa["reliquias"][i+1] = x_ijk.X 
                                
                        resultado["caixas_utilizadas"].append(caixa)   

        # Dados importantes para analise do modelo
        
        resultado["iteracoes_simplex"] = model.IterCount
        resultado["num_caixas"] = model.ObjVal
        resultado["status"] = model.status 
        resultado["gap"] = model.MIPGap
        resultado["tempo"] = model.Runtime
        
        #Escreve o resultado no arquivo JSON
        
        with open(f"resultado_gurobi_{total_relics}.json","w",encoding="utf-8") as arquivo:
            json.dump(resultado,arquivo,indent=4,ensure_ascii=False)
              
    if model.status == GRB.INFEASIBLE:
        print("solução inviável")
    
    if model.status == GRB.UNBOUNDED:
        print("Função objetivo decresce indefinidamente")

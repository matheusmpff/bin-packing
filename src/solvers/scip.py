from pyscipopt import Model, quicksum
import json

# Colunas das mochilas
QUANTITY = 0
WEIGHT = 1
VOLUME = 2
COST = 3

def backpack_scip(backpacks, relics):
    C_MAX = 1100 # Caso em que fazemos com 20 reliquias apenas
    total_relics = relics[:,QUANTITY].sum()
    if total_relics != 20:
        C_MAX = (backpacks[:,COST]*backpacks[:,QUANTITY]).sum()*0.6 
    
    model = Model("コンチ")

    # number of types of backpacks
    backpack_tnum = len(backpacks)
    j_limits = backpacks[:, QUANTITY]
    backpack_weights = backpacks[:,WEIGHT]
    backpack_volumes = backpacks[:,VOLUME]
    backpack_costs = backpacks[:,COST]

    relic_tnum = len(relics)
    relic_quantity = relics[:, QUANTITY]
    relic_weights = relics[:,WEIGHT]
    relic_volumes = relics[:,VOLUME]
    relic_costs = relics[:,COST]

    m = []
    obj_sum = []

    # variáveis das mochilas no modelo
    # note que a ordem das listas é tipo da mochila e depois número da mochila

    for k in range(backpack_tnum):
        bag_num = []
        for j in range(backpacks[k][0]):
            bag_num.append(model.addVar(name=f"m_{j}_{k}", vtype="B"))
            obj_sum.append(bag_num[j])
        m.append(bag_num)

    # variáveis das relíquias
    # note que a ordem em que coloquei as listas foi: tipo, tipo da mochila e número (j-ésima) da mochila

    x = []
    for i in range(relic_tnum):
        bag_type = []
        for k in range(backpack_tnum):
            bag_num = []
            for j in range(backpacks[k][0]):
                bag_num.append(model.addVar(name=f"x_{i}_{j}_{k}", vtype="I"))
            bag_type.append(bag_num)
        x.append(bag_type)

    y = model.addVar(name="y", vtype="B")

    model.setObjective(quicksum(obj_sum))

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
        model.addCons(quicksum(terms) == relic_quantity[i])

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
    # num_relics_Muzza = [1, 1, 0, 2, 0]
    # for i in range(5):
    #     if num_relics_Muzza[i] != 0:
    #         model.addCons(x[i][3][0] <= num_relics_Muzza[i] + 10000 * y)
    #         model.addCons(-1 * x[i][3][0] <= -1 * num_relics_Muzza[i] + 10000 * y)

    #         model.addCons(x[i][4][0] <= num_relics_Muzza[i] + 10000 * (1 - y))
    #         model.addCons(-1 * x[i][4][0] <= -1 * num_relics_Muzza[i] + 10000 * (1 - y))
    #     else:
    #         model.addCons(x[i][3][0] <= 10000 * y)

    #         model.addCons(x[i][4][0] <= 10000 * (1 - y))


    # variáveis das relíquias: garantir positividade
    for i in range(relic_tnum):
        for k in range(len(backpacks)):
            for j in range(j_limits[k]):
                model.addCons(x[i][k][j] >= 0)

    # model.hideOutput()
    # model.setMaximize()
    model.setParam('limits/time', 60)
    model.optimize()
    # solution = model.getObjVal()

    resultado = {
        "caixas_utilizadas": [],
        "tempo": 0.0,
        "iteracoes_simplex": 0
    }
    if model.getStatus() == "optimal" or model.getStatus() == "timelimit":
        print(f"Encontramos uma solução otima = {model.getObjVal()} mochila(s) utilizada(s)")
        varDict = model.getVarDict()
        for scip_var_name, scip_var_value in varDict.items():
            print(f"{scip_var_name} = {scip_var_value}") if scip_var_value != 0 else None
    
        for k in range(backpack_tnum):
            for j in range(j_limits[k]):
                backpack_value = varDict[f"m_{j}_{k}"]
                if backpack_value !=0:
                    caixa = {
                        "numero":j +1,
                        "tipo": k + 1,
                        "reliquias":{
                        }
                    }
                    for i in range(relic_tnum):
                        relic_value = varDict[f"x_{i}_{j}_{k}"]
                        if relic_value !=0:
                            caixa["reliquias"][i+1] = relic_value 
                        
                    resultado["caixas_utilizadas"].append(caixa)   
    
        resultado["num_caixas"] = model.getObjVal()
        resultado["iteracoes_simplex"] = model.getNLPIterations()
        resultado["status"] = model.getStatus()
        resultado["gap"] = model.getGap()
        resultado["tempo"] = model.getSolvingTime()

        # model.hideOutput()
        # tempo_soma = 0.0
        # for i in range(10):
        #     model.freeTransform()
        #     model.optimize()
        #     tempo_soma += model.getSolvingTime()

        # resultado["tempo"] = tempo_soma / 10

        with open("resultado_scip.json","w",encoding="utf-8") as arquivo:
            json.dump(resultado,arquivo,indent=4,ensure_ascii=False)
    
          
    if model.getStatus() == "infeasible":
        print("solução inviável")
    
    if model.getStatus() == "unbounded":
        print("Função objetivo decresce indefinidamente")

import numpy as np
import random

from src.solvers.scip import backpack_scip
#Custo máximo para gastar com mochilas
C_MAX = 1100

# Colunas das mochilas
QUANTITY = 0
WEIGHT = 1
VOLUME = 2
COST = 3

"""
Armazena os dados dos 5 tipos de mochilas.

Colunas:
quantidade | Peso Máx (Kg) | Volume Max (L) | Preço (R$)
"""
backpacks =np.array( [
    [5,20,25,120],
    [3,25,10,135],
    [2,40,30,240],
    [6,30,15,180],
    [4,15,8,105]
])

"""
Armazena os dados dos 5 tipos de Relíquias.

Colunas:
quantidade | Peso Máx (Kg) | Volume Max (L) | Preço (R$)
"""
relics = np.array([
    [4,4,2,1000],
    [4,6,3,1200],
    [4,1,1,24000],
    [4,10,5,18000],
    [4,15,4,30000]
])

def split_random(limit, n_elements):
    result = [1] * n_elements
    
    for i in range(limit-n_elements):
        index = random.randrange(n_elements)
        result[index]+=1
    
    return result
      
# sed is the seed, for the randomness to be reproducible
# num is the number of backpacks
def create_attr(sed, num):
    random.seed(sed)

    """
    Armazena os dados dos 5 tipos de mochilas.

    Colunas:
    quantidade | Peso Máx (Kg) | Volume Max (L) | Preço (R$)
    """
    backpack_quants = split_random(num, 5)
    backpacks =np.array( [
        [backpack_quants[0],20,25,120],
        [backpack_quants[1],25,10,135],
        [backpack_quants[2],40,30,240],
        [backpack_quants[3],30,15,180],
        [backpack_quants[4],15,8,105]
    ])

    """
    Armazena os dados dos 5 tipos de Relíquias.

    Colunas:
    quantidade | Peso Máx (Kg) | Volume Max (L) | Preço (R$)
    """
    relic_quants = split_random(num, 5)
    relics = np.array([
        [relic_quants[0],4,2,1000],
        [relic_quants[1],6,3,1200],
        [relic_quants[2],1,1,24000],
        [relic_quants[3],10,5,18000],
        [relic_quants[4],15,4,30000]
    ])

    return (backpacks, relics)

#backpack_scip(backpacks,relics)
backpack_scip(*create_attr(1, 40))

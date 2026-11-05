import numpy as np

#Custo máximo para gastar com mochilas
C_MAX = 1100

# Colunas das mochilas
QUANTITY = 0
MAX_WEIGHT = 1
MAX_VOLUME = 2
COST = 3

# Colunas das relíquias
RELIC_QUANTITY = 0
RELIC_WEIGHT = 1
RELIC_VOLUME = 2
RELIC_VALUE =3

"""
Armazena os dados dos 5 tipos de mochilas.

Colunas:
quantidade | Peso Máx (Kg) | Volume Max (L) | Preço (R$)
"""
backpacks = np.array([
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


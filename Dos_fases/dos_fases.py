from fase1 import estado_primal 
from fase2 import get_S_columns,get_estado_primal
from matrizSimplex import crearMatriz,actualizar_matriz
import fase2 as f2
# z = {
#     "x1": 4,
#     "x2": 3
# }

# s_a = [
#     {"x1": 1, "x2": 2, "sign": "<=", "value": 8},
#     {"x1": 2, "x2": 1, "sign": ">=", "value": 10},
#     {"x1": 1, "x2": 1, "sign": "==", "value": 6}
# ]



# z = {
#     "x1": 5, "x2": 3, "x3": 2, "x4": 7, "x5": 1,
#     "x6": 4, "x7": 6, "x8": 2, "x9": 3, "x10": 5,
#     "x11": 2, "x12": 6, "x13": 4
# }
# s_a = [
#     {
#         "x1": 2, "x2": 1, "x3": 1, "x4": 0, "x5": 3,
#         "x6": 0, "x7": 2, "x8": 1, "x9": 1, "x10": 0,
#         "x11": 0, "x12": 1, "x13": 2,
#         "sign": "<=", "value": 10
#     },
#     {
#         "x1": 1, "x2": 2, "x3": 0, "x4": 1, "x5": 1,
#         "x6": 2, "x7": 0, "x8": 1, "x9": 0, "x10": 1,
#         "x11": 1, "x12": 0, "x13": 1,
#         "sign": ">=", "value": 8
#     },
#     {
#         "x1": 0, "x2": 0, "x3": 1, "x4": 1, "x5": 2,
#         "x6": 3, "x7": 1, "x8": 0, "x9": 2, "x10": 1,
#         "x11": 1, "x12": 1, "x13": 0,
#         "sign": "==", "value": 12
#     }
# ]

# z = {
#     "x1": 2,
#     "x2": 1,
#     "x3": 3
# }

# s_a = [
#     {"x1": 5, "x2": 2, "x3": 7, "sign": "==", "value": 420},
#     {"x1": 3, "x2": 2, "x3": 5, "sign": ">=", "value": 280},
#     {"x1": 1, "x2": 0, "x3": 1, "sign": "<=", "value": 100}
# ]

# z = {  #basico
#     "x1": 4,
#     "x2": 1,}

# s_a = [
#     {"x1": 3, "x2": 1, "sign": "==", "value": 3},
#     {"x1": 4, "x2": 3, "sign": ">=", "value": 6},
#     {"x1": 1, "x2": 2, "sign": "<=", "value": 4}
# ]

z = {  #basico
    "x1": 2,
    "x2": 1
    }

s_a = [
    {"x1": 3, "x2": 1, "sign": "==", "value": 3},
    {"x1": 4, "x2": 3, "sign": ">=", "value": 6},
    {"x1": 1, "x2": 2, "sign": "<=", "value": 4}
]
# z = {
#     "x1": 5,
#     "x2": 2
# }

# s_a = [
#     {"x1": 1, "x2": 3, "sign": ">=", "value": 9},
#     {"x1": 2, "x2": 1, "sign": "<=", "value": 8}
# ]
# z = {
#     "x1": 2000,
#     "x2": 2000
# }

# s_a = [
#     {"x1": 1, "x2": 2, "sign": ">=", "value": 80},
#     {"x1": 3, "x2": 2, "sign": ">=", "value": 160},
#     {"x1": 5, "x2": 2, "sign": ">=", "value": 200}
# ]
## fase 1
s_a_fase1, min_r = estado_primal(s_a)

print(s_a_fase1)
print(min_r)
matriz,fila_p,columna_p,zj_cj = crearMatriz(min_r,s_a_fase1)

print("Matriz actualizada:")
for fila in matriz:
    print(fila)

r = 0 
for fila in matriz:
    cx = min_r[fila[-1]]
    bi = fila[-2]
    r += cx*bi

print("zj-cj",zj_cj)
print("z",r)
print("fila_pivote:",matriz[fila_p])
print("columna pivote")
for i in range(len(matriz)):
    print(matriz[i][columna_p])

while r>0:
    matriz,fila_p,columna_p,zj_cj = actualizar_matriz(matriz,fila_p,columna_p,min_r)
    print("Matriz actualizada:")
    for fila in matriz:
        print(fila)

    r = 0 
    for fila in matriz:
        cx = min_r[fila[-1]]
        bi = fila[-2]
        r += cx*bi

    if r == 0 or all(valor <= 0 for valor in zj_cj): 
        break

    print("zj-cj",zj_cj)
    print("z",r)
    print("fila_pivote:",matriz[fila_p])
    print("columna pivote")
    for i in range(len(matriz)):
        print(matriz[i][columna_p])



##fase 2
print("fase2")
S_colums = f2.get_S_columns(min_r)
s_a_fase2, z = f2.get_estado_primal(S_colums, matriz, z, min_r)
print(s_a_fase2)

matriz, fila_p, columna_p, zj_cj = f2.crearMatriz(z, s_a_fase2)

print("Matriz actualizada:")
for fila in matriz:
    print(fila)

Z = 0
for fila in matriz:
    cx = z[fila[-1]]
    bi = fila[-2]
    Z += cx * bi

print("zj-cj",zj_cj)
print("Z", Z)
if(columna_p>0 and fila_p>0):
    print("fila_pivote:", matriz[fila_p])
    print("columna pivote")
    for i in range(len(matriz)):
        print(matriz[i][columna_p])

while any(valor > 0 for valor in zj_cj):
    matriz, fila_p, columna_p, zj_cj = f2.actualizar_matriz(matriz, fila_p, columna_p, z)
    print("Matriz actualizada:")
    for fila in matriz:
        print(fila)

    Z = 0
    for fila in matriz:
        cx = z[fila[-1]]
        bi = fila[-2]
        Z += cx * bi

    print("zj-cj",zj_cj)
    print("z", Z)

    if all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
        break

    print("fila_pivote:", matriz[fila_p])
    print("columna pivote")
    for i in range(len(matriz)):
        print(matriz[i][columna_p])
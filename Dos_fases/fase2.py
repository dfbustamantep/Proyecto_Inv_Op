def get_S_columns(func_z):
    keys = list(func_z.keys())
    S_columns = []
    for j in range(len(keys)):
        if keys[j].startswith("S"):
            S_columns.append(j)
    return S_columns

def get_estado_primal(S_column,matriz,func_z,z_fase1):
    s_a = []
    keys = list(z_fase1.keys())
    
    for k in keys:
        if k.startswith("x"):
            continue
        func_z[k] = 0

    for i in range(len(matriz)):
        fila = {}
        fila[matriz[i][-1]] = 1
        for j in range(len(S_column)):
            fila[f"S{j+1}"] = matriz[i][S_column[j]]
        fila["sign"] = "=="
        fila["value"] = matriz[i][-2]
        s_a.append(fila)
    return s_a,func_z

import sys
from fractions import Fraction

def crearMatriz(func_z,s_a):
    n = len(s_a)
    m = len(func_z)
    keys = list(func_z.keys())
    matriz = []
    for i in range(n):  # 각 제약조건 (행)
        keys_s = list(s_a[i].keys())
        fila_vals = []
        for j in range(m):  # 각 키 (열)
            fila_vals.append(s_a[i].get(keys[j], 0))
        
        fila_vals.append(s_a[i]["value"])
        for k in keys_s:
            if k.startswith(("x", "H", "R")):
                fila_vals.append(k)
        for k in keys_s:
            if k.startswith(("S")) and not isinstance(fila_vals[-1], str):
                fila_vals.append(k)

        matriz.append(fila_vals)

    fila_pivote, columna_pivote, zj_cj = pivotear(func_z,matriz,n,m)

    return matriz,fila_pivote,columna_pivote,zj_cj

def actualizar_matriz(matriz, fila_p, columna_p, func_z):
    puntos = puntos_coeficientes(matriz, columna_p)
    ##if(puntos[fila_p]==)
    n = len(matriz)
    m = len(matriz[0])
    # Normalizar fila pivote
    fila_pivote_normalizada = []
    for j in range(m-1):
        valor = Fraction(matriz[fila_p][j], puntos[fila_p])
        fila_pivote_normalizada.append(valor)
    
    xb = list(func_z.keys())[columna_p]
    fila_pivote_normalizada.append(xb)
    matriz_nuevo = [[0 for _ in range(m-1)] for _ in range(n)]

    # Asignar fila pivote normalizada
    matriz_nuevo[fila_p] = fila_pivote_normalizada

    # Calcular nuevas filas para el resto
    for i in range(n):
        if i == fila_p:
            continue
        fila_nueva = []
        for j in range(m-1):
            valor = matriz[i][j] + puntos[i] * -1 * fila_pivote_normalizada[j]
            fila_nueva.append(valor)
        xb = matriz[i][-1] # xb de cada pila
        fila_nueva.append(xb)
        matriz_nuevo[i] = fila_nueva

    fila_pivote, columna_pivote,zj_cj = pivotear(func_z,matriz_nuevo,n,m-2)

    return matriz_nuevo,fila_pivote,columna_pivote,zj_cj

def pivotear(func_z,matriz,n,m):
    # print("prueba matriz",matriz[0])
    # print("prueba matriz",matriz[1])
    # print("prueba matriz",matriz[2])
    # print("prueba matriz",matriz[3])
    # print("prueba matriz",matriz[4])
    # print("prueba matriz",matriz[5])
    # print("prueba matriz",matriz[6])
    # print("prueba matriz",matriz[7])
    # print("prueba matriz",matriz[8])
    # print("prueba matriz",matriz[9])
    # print("prueba matriz",matriz[10])
    # print("prueba matriz",matriz[11])
    # print("prueba matriz",matriz[12])
    keys = list(func_z.keys())
    columna_pivote = -1
    max_val = -1000
    zj_cj = []
    for j in range(m):
        zj = 0
        cj = func_z[keys[j]]
        for i in range(n):
            xb = matriz[i][-1]
            cx = func_z[xb]
            zj +=matriz[i][j] * cx
        
        zj_cj.append(zj-cj)
        if max_val<(zj-cj and zj-cj>0):
            max_val = zj - cj
            columna_pivote=j
    
    min_val = sys.float_info.max
    fila_pivote = -1
    if columna_pivote == -1:
        return fila_pivote,columna_pivote,zj_cj
    for i in range(n):
        bi = matriz[i][-2]
        xi = matriz[i][columna_pivote]
        if xi>0 and min_val>(bi/xi):
            min_val = bi/xi
            fila_pivote = i
    return fila_pivote,columna_pivote,zj_cj

def puntos_coeficientes(matriz, columna_p):
    puntos = []
    for i in range(len(matriz)):
        puntos.append(matriz[i][columna_p])
    return puntos

def get_Z(matriz,func_z):
    r = 0 
    for fila in matriz:
        cx = func_z[fila[-1]]
        bi = fila[-2]
        r += cx*bi
    return r

def get_Cx(matriz,func_z):
    cx = [] 
    for fila in matriz:
        cx.append(func_z[fila[-1]])
    return cx

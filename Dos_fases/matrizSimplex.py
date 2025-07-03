import sys
from fractions import Fraction

def crearMatriz(min_r,s_a):
    n = len(s_a)
    m = len(min_r)
    keys = list(min_r.keys())
    matriz = []
    for i in range(n):  # 각 제약조건 (행)
        keys_s = list(s_a[i].keys())
        fila_vals = []
        for j in range(m):  # 각 키 (열)
            fila_vals.append(s_a[i].get(keys[j], 0))
        
        fila_vals.append(s_a[i]["value"])
        for k in keys_s:
            if k.startswith("R"):
                fila_vals.append(k)
        for k in keys_s:
            if k.startswith("H"):
                fila_vals.append(k)
        matriz.append(fila_vals)

    fila_pivote, columna_pivote, zj_cj = pivotear(min_r,matriz,n,m)

    return matriz,fila_pivote,columna_pivote,zj_cj

def actualizar_matriz(matriz, fila_p, columna_p, min_r):
    puntos = puntos_coeficientes(matriz, columna_p)

    n = len(matriz)
    m = len(matriz[0])
    # Normalizar fila pivote
    fila_pivote_normalizada = []
    for j in range(m-1):
        valor = Fraction(matriz[fila_p][j], puntos[fila_p])
        fila_pivote_normalizada.append(valor)
    
    xb = list(min_r.keys())[columna_p]
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
        xb = matriz[i][-1]
        fila_nueva.append(xb)
        matriz_nuevo[i] = fila_nueva

    fila_pivote, columna_pivote,zj_cj = pivotear(min_r,matriz_nuevo,n,m-2)

    return matriz_nuevo,fila_pivote,columna_pivote,zj_cj

def pivotear(min_r,matriz,n,m):
    keys = list(min_r.keys())
    columna_pivote = 0
    max_val = 0
    zj_cj = []
    for j in range(m):
        zj = 0
        cj = min_r[keys[j]]
        for i in range(n):
            xb = matriz[i][-1]
            cx = min_r[xb]
            zj +=matriz[i][j] * cx
        zj_cj.append(zj-cj)
        if max_val<(zj-cj):
            max_val = zj - cj
            columna_pivote=j
    min_val = sys.float_info.max
    fila_pivote = 0
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

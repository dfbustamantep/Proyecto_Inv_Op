from . import fase1 as f1
from . import fase2 as f2

def mostrar_fase1(s_a, imprimir=print):
    s_a_fase1, func_z = f1.estado_primal(s_a)
    imprimir("estado inicio primal")
    imprimir(f"min_z: {convertir_a_fraccion(func_z)}")
    for fila in s_a_fase1:
        imprimir(str(convertir_a_fraccion(fila)))

    imprimir(f"cj: {convertir_a_fraccion(list(func_z.values()))}")
    imprimir(f": {list(func_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = f1.crearMatriz(func_z, s_a_fase1)
    cx = f1.get_Cx(matriz, func_z)

    imprimir(f"cx: {convertir_a_fraccion(cx)}")
    imprimir("Matriz actualizada:")
    imprimir(f": {list(func_z.keys())} Bi Xb")
    for fila in matriz:
        imprimir(str(convertir_a_fraccion(fila)))

    Z = f1.get_Z(matriz, func_z)
    imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
    imprimir(f"z: {convertir_a_fraccion(Z)}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {fila_p} {convertir_a_fraccion(matriz[fila_p])}")
        imprimir(f"columna pivote: {columna_p}")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))

    while Z > 0:
        matriz, fila_p, columna_p, zj_cj = f1.actualizar_matriz(matriz, fila_p, columna_p, func_z)
        cx = f1.get_Cx(matriz, func_z)

        imprimir(f"cx: {convertir_a_fraccion(cx)}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(convertir_a_fraccion(fila)))

        Z = f1.get_Z(matriz, func_z)
        imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
        imprimir(f"z: {convertir_a_fraccion(Z)}")

        if Z == 0 or all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {fila_p} {convertir_a_fraccion(matriz[fila_p])}")
        imprimir(f"columna pivote: {columna_p}")
        imprimir("")

    return func_z, matriz

def minimizar(fun_z_f1, fun_z, matriz, imprimir=print):
    S_colums = f2.get_S_columns(fun_z_f1)
    s_a_fase2, fun_z = f2.get_estado_primal(S_colums, matriz, fun_z, fun_z_f1)

    imprimir("estado inicio primal")
    imprimir(f"func_z: {convertir_a_fraccion(fun_z)}")
    for fila in s_a_fase2:
        imprimir(str(convertir_a_fraccion(fila)))

    imprimir(f"cj: {convertir_a_fraccion(list(fun_z.values()))}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = f2.crearMatriz(fun_z, s_a_fase2, objetivo="minimizar")
    cx = f2.get_Cx(matriz, fun_z)

    imprimir(f"cx: {convertir_a_fraccion(cx)}")
    imprimir("Matriz actualizada:")
    for fila in matriz:
        imprimir(str(convertir_a_fraccion(fila)))

    Z = f2.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
    imprimir(f"Z: {convertir_a_fraccion(Z)}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))

    while any(valor > 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = f2.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="minimizar")
        cx = f2.get_Cx(matriz, fun_z)

        imprimir(f"cx: {convertir_a_fraccion(cx)}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(convertir_a_fraccion(fila)))

        Z = f2.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
        imprimir(f"Z: {convertir_a_fraccion(Z)}")

        if all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))
        imprimir("")

def maximizar(fun_z_f1, fun_z, matriz, imprimir=print):
    S_colums = f2.get_S_columns(fun_z_f1)
    s_a_fase2, fun_z = f2.get_estado_primal(S_colums, matriz, fun_z, fun_z_f1)

    imprimir("estado inicio primal")
    imprimir(f"func_z: {convertir_a_fraccion(fun_z)}")
    for fila in s_a_fase2:
        imprimir(str(convertir_a_fraccion(fila)))

    imprimir(f"cj: {convertir_a_fraccion(list(fun_z.values()))}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = f2.crearMatriz(fun_z, s_a_fase2, objetivo="maximizar")
    cx = f2.get_Cx(matriz, fun_z)

    imprimir(f"cx: {convertir_a_fraccion(cx)}")
    imprimir("Matriz actualizada:")
    for fila in matriz:
        imprimir(str(convertir_a_fraccion(fila)))

    Z = f2.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
    imprimir(f"Z: {convertir_a_fraccion(Z)}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))

    while any(valor < 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = f2.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="maximizar")
        cx = f2.get_Cx(matriz, fun_z)

        imprimir(f"cx: {convertir_a_fraccion(cx)}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(convertir_a_fraccion(fila)))

        Z = f2.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
        imprimir(f"Z: {convertir_a_fraccion(Z)}")

        if all(valor >= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))
        imprimir("")

from fractions import Fraction

def convertir_a_fraccion(valor):
    if isinstance(valor, float):
        return str(Fraction(valor).limit_denominator())
    elif isinstance(valor, Fraction):
        return str(valor)  # 이미 Fraction이면 문자열로 변환
    elif isinstance(valor, list):
        return [convertir_a_fraccion(v) for v in valor]
    else:
        return valor
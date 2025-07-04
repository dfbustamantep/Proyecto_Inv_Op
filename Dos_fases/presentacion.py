from . import fase1 as f1
from . import fase2 as f2

def mostrar_fase1(s_a, imprimir=print):
    s_a_fase1, func_z = f1.estado_primal(s_a)
    imprimir("estado inicio primal")
    imprimir(f"min_z: {func_z}")
    for fila in s_a_fase1:
        imprimir(str(fila))

    imprimir(f"cj: {list(func_z.values())}")
    imprimir(f": {list(func_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = f1.crearMatriz(func_z, s_a_fase1)
    cx = f1.get_Cx(matriz, func_z)

    imprimir(f"cx: {cx}")
    imprimir("Matriz actualizada:")
    imprimir(f": {list(func_z.keys())} Bi Xb")
    for fila in matriz:
        imprimir(str(fila))

    Z = f1.get_Z(matriz, func_z)
    imprimir(f"zj-cj: {zj_cj}")
    imprimir(f"z: {Z}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {fila_p} {matriz[fila_p]}")
        imprimir(f"columna pivote: {columna_p}")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))

    while Z > 0:
        matriz, fila_p, columna_p, zj_cj = f1.actualizar_matriz(matriz, fila_p, columna_p, func_z)
        cx = f1.get_Cx(matriz, func_z)

        imprimir(f"cx: {cx}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(fila))

        Z = f1.get_Z(matriz, func_z)
        imprimir(f"zj-cj: {zj_cj}")
        imprimir(f"z: {Z}")

        if Z == 0 or all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {fila_p} {matriz[fila_p]}")
        imprimir(f"columna pivote: {columna_p}")
        imprimir("")

    return func_z, matriz

def minimizar(fun_z_f1, fun_z, matriz, imprimir=print):
    S_colums = f2.get_S_columns(fun_z_f1)
    s_a_fase2, fun_z = f2.get_estado_primal(S_colums, matriz, fun_z, fun_z_f1)

    imprimir("estado inicio primal")
    imprimir(f"func_z: {fun_z}")
    for fila in s_a_fase2:
        imprimir(str(fila))

    imprimir(f"cj: {list(fun_z.values())}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = f2.crearMatriz(fun_z, s_a_fase2, objetivo="minimizar")
    cx = f2.get_Cx(matriz, fun_z)

    imprimir(f"cx: {cx}")
    imprimir("Matriz actualizada:")
    for fila in matriz:
        imprimir(str(fila))

    Z = f2.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {zj_cj}")
    imprimir(f"Z: {Z}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))

    while any(valor > 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = f2.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="minimizar")
        cx = f2.get_Cx(matriz, fun_z)

        imprimir(f"cx: {cx}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(fila))

        Z = f2.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {zj_cj}")
        imprimir(f"Z: {Z}")

        if all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))
        imprimir("")

def maximizar(fun_z_f1, fun_z, matriz, imprimir=print):
    S_colums = f2.get_S_columns(fun_z_f1)
    s_a_fase2, fun_z = f2.get_estado_primal(S_colums, matriz, fun_z, fun_z_f1)

    imprimir("estado inicio primal")
    imprimir(f"func_z: {fun_z}")
    for fila in s_a_fase2:
        imprimir(str(fila))

    imprimir(f"cj: {list(fun_z.values())}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = f2.crearMatriz(fun_z, s_a_fase2, objetivo="maximizar")
    cx = f2.get_Cx(matriz, fun_z)

    imprimir(f"cx: {cx}")
    imprimir("Matriz actualizada:")
    for fila in matriz:
        imprimir(str(fila))

    Z = f2.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {zj_cj}")
    imprimir(f"Z: {Z}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))

    while any(valor < 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = f2.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="maximizar")
        cx = f2.get_Cx(matriz, fun_z)

        imprimir(f"cx: {cx}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(fila))

        Z = f2.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {zj_cj}")
        imprimir(f"Z: {Z}")

        if all(valor >= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote:")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))
        imprimir("")

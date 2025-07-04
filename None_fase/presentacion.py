from None_fase import none_fase as nf

def minimizar(func_z_orig, s_a, imprimir=print):
    s_a_nf, fun_z = nf.estado_primal(s_a, func_z_orig)
    imprimir("estado inicio primal")
    imprimir(f"func_z: {fun_z}")
    for fila in s_a_nf:
        imprimir(str(fila))

    imprimir(f"cj: {list(fun_z.values())}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = nf.crearMatriz(fun_z, s_a_nf, objetivo="minimizar")
    cx = nf.get_Cx(matriz, fun_z)

    imprimir(f"cx: {cx}")
    imprimir("Matriz actualizada:")
    imprimir(f": {list(fun_z.keys())} Bi Xb")
    for fila in matriz:
        imprimir(str(fila))

    Z = nf.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {zj_cj}")
    imprimir(f"Z: {Z}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))

    while any(valor > 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = nf.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="minimizar")
        cx = nf.get_Cx(matriz, fun_z)

        imprimir(f"cx: {cx}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(fila))

        Z = nf.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {zj_cj}")
        imprimir(f"Z: {Z}")

        if all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))
        imprimir("")


def maximizar(func_z_orig, s_a, imprimir=print):
    s_a_nf, fun_z = nf.estado_primal(s_a, func_z_orig)

    imprimir("estado inicio primal")
    imprimir(f"func_z: {fun_z}")
    for fila in s_a_nf:
        imprimir(str(fila))

    imprimir(f"cj: {list(fun_z.values())}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = nf.crearMatriz(fun_z, s_a_nf, objetivo="maximizar")
    cx = nf.get_Cx(matriz, fun_z)

    imprimir(f"cx: {cx}")
    imprimir("Matriz actualizada:")
    for fila in matriz:
        imprimir(str(fila))

    Z = nf.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {zj_cj}")
    imprimir(f"Z: {Z}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))

    while any(valor < 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = nf.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="maximizar")
        cx = nf.get_Cx(matriz, fun_z)

        imprimir(f"cx: {cx}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(fila))

        Z = nf.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {zj_cj}")
        imprimir(f"Z: {Z}")

        if all(valor >= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {matriz[fila_p]}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(matriz[i][columna_p]))
        imprimir("")

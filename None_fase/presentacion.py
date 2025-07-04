from None_fase import none_fase as nf
from fractions import Fraction

def convertir_a_fraccion(valor):
    if isinstance(valor, float):
        return str(Fraction(valor).limit_denominator())
    elif isinstance(valor, Fraction):
        return str(valor)
    elif isinstance(valor, list):
        return [convertir_a_fraccion(v) for v in valor]
    elif isinstance(valor, dict):
        return {k: convertir_a_fraccion(v) for k, v in valor.items()}
    else:
        return valor

def minimizar(func_z_orig, s_a, imprimir=print):
    s_a_nf, fun_z = nf.estado_primal(s_a, func_z_orig)

    imprimir("estado inicio primal")
    imprimir(f"func_z: {convertir_a_fraccion(fun_z)}")
    for fila in s_a_nf:
        imprimir(str(convertir_a_fraccion(fila)))

    imprimir(f"cj: {convertir_a_fraccion(list(fun_z.values()))}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = nf.crearMatriz(fun_z, s_a_nf, objetivo="minimizar")
    cx = nf.get_Cx(matriz, fun_z)

    imprimir(f"cx: {convertir_a_fraccion(cx)}")
    imprimir("Matriz actualizada:")
    imprimir(f": {list(fun_z.keys())} Bi Xb")
    for fila in matriz:
        imprimir(str(convertir_a_fraccion(fila)))

    Z = nf.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
    imprimir(f"Z: {convertir_a_fraccion(Z)}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))

    while any(valor > 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = nf.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="minimizar")
        cx = nf.get_Cx(matriz, fun_z)

        imprimir(f"cx: {convertir_a_fraccion(cx)}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(convertir_a_fraccion(fila)))

        Z = nf.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
        imprimir(f"Z: {convertir_a_fraccion(Z)}")

        if all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))
        imprimir("")


def maximizar(func_z_orig, s_a, imprimir=print):
    s_a_nf, fun_z = nf.estado_primal(s_a, func_z_orig)

    imprimir("estado inicio primal")
    imprimir(f"func_z: {convertir_a_fraccion(fun_z)}")
    for fila in s_a_nf:
        imprimir(str(convertir_a_fraccion(fila)))

    imprimir(f"cj: {convertir_a_fraccion(list(fun_z.values()))}")
    imprimir(f": {list(fun_z.keys())}")

    matriz, fila_p, columna_p, zj_cj = nf.crearMatriz(fun_z, s_a_nf, objetivo="maximizar")
    cx = nf.get_Cx(matriz, fun_z)

    imprimir(f"cx: {convertir_a_fraccion(cx)}")
    imprimir("Matriz actualizada:")
    for fila in matriz:
        imprimir(str(convertir_a_fraccion(fila)))

    Z = nf.get_Z(matriz, fun_z)
    imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
    imprimir(f"Z: {convertir_a_fraccion(Z)}")

    if columna_p > -1 and fila_p > -1:
        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))

    while any(valor < 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = nf.actualizar_matriz(matriz, fila_p, columna_p, fun_z, objetivo="maximizar")
        cx = nf.get_Cx(matriz, fun_z)

        imprimir(f"cx: {convertir_a_fraccion(cx)}")
        imprimir("Matriz actualizada:")
        for fila in matriz:
            imprimir(str(convertir_a_fraccion(fila)))

        Z = nf.get_Z(matriz, fun_z)
        imprimir(f"zj-cj: {convertir_a_fraccion(zj_cj)}")
        imprimir(f"Z: {convertir_a_fraccion(Z)}")

        if all(valor >= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            break

        imprimir(f"fila_pivote: {convertir_a_fraccion(matriz[fila_p])}")
        imprimir("columna pivote")
        for i in range(len(matriz)):
            imprimir(str(convertir_a_fraccion(matriz[i][columna_p])))
        imprimir("")

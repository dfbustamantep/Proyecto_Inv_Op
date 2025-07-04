import fase2 as f2
import fase1 as f1
def mostrar_fase1(s_a):
    s_a_fase1, func_z = f1.estado_primal(s_a)
    print("estado inicio primal")
    print("min_z",func_z)
    for fila in s_a_fase1:
        print(fila)

    print("cj:", list(func_z.values()))
    print(":", list(func_z.keys()))

    matriz,fila_p,columna_p,zj_cj = f1.crearMatriz(func_z,s_a_fase1)

    cx = f1.get_Cx(matriz,func_z)

    print("cx",cx)
    print("Matriz actualizada:")
    print(":", list(func_z.keys()), "Bi","Xb")
    for fila in matriz:
        print(fila)

    Z = f1.get_Z(matriz,func_z)

    print("zj-cj",zj_cj)
    print("z",Z)
    if(columna_p>-1 and fila_p>-1):
        print("fila_pivote:", fila_p,matriz[fila_p])
        print("columna pivote: ", columna_p)
        print()
        for i in range(len(matriz)):
            print(matriz[i][columna_p])

    while Z>0:
        matriz,fila_p,columna_p,zj_cj = f1.actualizar_matriz(matriz,fila_p,columna_p,func_z)

        cx = f1.get_Cx(matriz,func_z)

        print("cx",cx)
        print("Matriz actualizada:")
        print(":", list(func_z.keys()), "Bi","Xb")
        for fila in matriz:
            print(fila)

        Z = f1.get_Z(matriz,func_z)

        print("zj-cj",zj_cj)
        print("z",Z)

        if Z == 0 or all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            print()
            break

        print("fila_pivote:", fila_p,matriz[fila_p])
        print("columna pivote: ", columna_p)
        print()
    return func_z,matriz

def minimizar(fun_z_f1,fun_z,matriz):
    S_colums = f2.get_S_columns(fun_z_f1)
    s_a_fase2, fun_z = f2.get_estado_primal(S_colums, matriz, fun_z, fun_z_f1)

    print("estado inicio primal")
    print("func_z",fun_z)
    for fila in s_a_fase2:
        print(fila)

    print("cj:", list(fun_z.values()))
    print(":", list(fun_z.keys()))

    matriz, fila_p, columna_p, zj_cj = f2.crearMatriz(fun_z, s_a_fase2,objetivo="minimizar")
    cx = f2.get_Cx(matriz,fun_z)

    print("cx",cx)
    print("Matriz actualizada:")
    print(":", list(fun_z.keys()), "Bi","Xb")
    for fila in matriz:
        print(fila)

    Z = f2.get_Z(matriz,fun_z)

    print("zj-cj",zj_cj)
    print("Z", Z)
    if(columna_p>0 and fila_p>0):
        print("fila_pivote:", matriz[fila_p])
        print("columna pivote")
        for i in range(len(matriz)):
            print(matriz[i][columna_p])
    
    print()

    while any(valor > 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = f2.actualizar_matriz(matriz, fila_p, columna_p, fun_z,objetivo="minimizar")
        cx = f2.get_Cx(matriz,fun_z)

        print("cx",cx)
        print("Matriz actualizada:")
        print(":", list(fun_z.keys()), "Bi","Xb")
        for fila in matriz:
            print(fila)

        Z = f2.get_Z(matriz,fun_z)

        print("zj-cj",zj_cj)
        print("Z", Z)

        if all(valor <= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            print("termina minimizacion")
            break

        print("fila_pivote:", matriz[fila_p])
        print("columna pivote")
        for i in range(len(matriz)):
            print(matriz[i][columna_p])
            print()

def maximizar(fun_z_f1,fun_z,matriz):
    S_colums = f2.get_S_columns(fun_z_f1)
    s_a_fase2, fun_z = f2.get_estado_primal(S_colums, matriz, fun_z, fun_z_f1)

    print("estado inicio primal")
    print("func_z",fun_z)
    for fila in s_a_fase2:
        print(fila)

    print("cj:", list(fun_z.values()))
    print(":", list(fun_z.keys()))

    matriz, fila_p, columna_p, zj_cj = f2.crearMatriz(fun_z, s_a_fase2,objetivo="maximizar")
    cx = f2.get_Cx(matriz,fun_z)

    print("cx",cx)
    print("Matriz actualizada:")
    print(":", list(fun_z.keys()), "Bi","Xb")
    for fila in matriz:
        print(fila)

    Z = f2.get_Z(matriz,fun_z)

    print("zj-cj",zj_cj)
    print("Z", Z)
    if(columna_p>-1 and fila_p>-1):
        print("fila_pivote:", matriz[fila_p])
        print("columna pivote")
        for i in range(len(matriz)):
            print(matriz[i][columna_p])

    while any(valor < 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = f2.actualizar_matriz(matriz, fila_p, columna_p, fun_z,objetivo="maximizar")
        cx = f2.get_Cx(matriz,fun_z)

        print("cx",cx)
        print("Matriz actualizada:")
        print(":", list(fun_z.keys()), "Bi","Xb")
        for fila in matriz:
            print(fila)

        Z = f2.get_Z(matriz,fun_z)

        print("zj-cj",zj_cj)
        print("Z", Z)

        if all(valor >= 0 for valor in zj_cj) or fila_p < 0 or columna_p < 0:
            print("termina maximizacion")
            break

        print("fila_pivote:", matriz[fila_p])
        print("columna pivote")
        for i in range(len(matriz)):
            print(matriz[i][columna_p])
            print()
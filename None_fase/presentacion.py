from None_fase import none_fase as nf

def minimizar(func_z_orig,s_a):
    s_a_nf, fun_z = nf.estado_primal(s_a,func_z_orig)
    print("estado inicio primal")
    print("func_z",fun_z)
    for fila in s_a_nf:
        print(fila)

    print("cj:", list(fun_z.values()))
    print(":", list(fun_z.keys()))

    matriz, fila_p, columna_p, zj_cj = nf.crearMatriz(fun_z, s_a_nf,objetivo="minimizar")
    cx = nf.get_Cx(matriz,fun_z)

    print("cx",cx)
    print("Matriz actualizada:")
    print(":", list(fun_z.keys()), "Bi","Xb")
    for fila in matriz:
        print(fila)

    Z = nf.get_Z(matriz,fun_z)

    print("zj-cj",zj_cj)
    print("Z", Z)
    if(columna_p>0 and fila_p>0):
        print("fila_pivote:", matriz[fila_p])
        print("columna pivote")
        for i in range(len(matriz)):
            print(matriz[i][columna_p])
    
    print()

    while any(valor > 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = nf.actualizar_matriz(matriz, fila_p, columna_p, fun_z,objetivo="minimizar")
        cx = nf.get_Cx(matriz,fun_z)

        print("cx",cx)
        print("Matriz actualizada:")
        print(":", list(fun_z.keys()), "Bi","Xb")
        for fila in matriz:
            print(fila)

        Z = nf.get_Z(matriz,fun_z)

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

def maximizar(func_z_orig,s_a):
    s_a_nf, fun_z = nf.estado_primal(s_a,func_z_orig)

    print("estado inicio primal")
    print("func_z",fun_z)
    for fila in s_a_nf:
        print(fila)

    print("cj:", list(fun_z.values()))
    print(":", list(fun_z.keys()))

    matriz, fila_p, columna_p, zj_cj = nf.crearMatriz(fun_z, s_a_nf,objetivo="maximizar")
    cx = nf.get_Cx(matriz,fun_z)

    print("cx",cx)
    print("Matriz actualizada:")
    print(":", list(fun_z.keys()), "Bi","Xb")
    for fila in matriz:
        print(fila)

    Z = nf.get_Z(matriz,fun_z)

    print("zj-cj",zj_cj)
    print("Z", Z)
    if(columna_p>-1 and fila_p>-1):
        print("fila_pivote:", matriz[fila_p])
        print("columna pivote")
        for i in range(len(matriz)):
            print(matriz[i][columna_p])

    while any(valor < 0 for valor in zj_cj):
        matriz, fila_p, columna_p, zj_cj = nf.actualizar_matriz(matriz, fila_p, columna_p, fun_z,objetivo="maximizar")
        cx = nf.get_Cx(matriz,fun_z)

        print("cx",cx)
        print("Matriz actualizada:")
        print(":", list(fun_z.keys()), "Bi","Xb")
        for fila in matriz:
            print(fila)

        Z = nf.get_Z(matriz,fun_z)

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
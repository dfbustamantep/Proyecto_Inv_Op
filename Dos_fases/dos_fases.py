from fase1 import estado_primal 
from fase2 import get_S_columns,get_estado_primal
import fase1 as f1
import fase2 as f2
from presentacion import minimizar,maximizar, mostrar_fase1
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from None_fase import none_fase as nf, presentacion as prN

# func_z = {
#     "x1": 4,
#     "x2": 3
# }

# s_a = [
#     {"x1": 1, "x2": 2, "sign": "<=", "value": 8},
#     {"x1": 2, "x2": 1, "sign": ">=", "value": 10},
#     {"x1": 1, "x2": 1, "sign": "==", "value": 6}
# ]



# func_z = {
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

# func_z = {
#     "x1": 2,
#     "x2": 1,
#     "x3": 3
# }

# s_a = [
#     {"x1": 5, "x2": 2, "x3": 7, "sign": "==", "value": 420},
#     {"x1": 3, "x2": 2, "x3": 5, "sign": ">=", "value": 280},
#     {"x1": 1, "x2": 0, "x3": 1, "sign": "<=", "value": 100}
# ]

# func_z = {  #basico
#     "x1": 4,
#     "x2": 1,}

# s_a = [
#     {"x1": 3, "x2": 1, "sign": "==", "value": 3},
#     {"x1": 4, "x2": 3, "sign": ">=", "value": 6},
#     {"x1": 1, "x2": 2, "sign": "<=", "value": 4}
# ]

# objetivo = "minimizacion"
# func_z = {  #basico
#     "x1": 4,
#     "x2": 1
#     }

# s_a = [
#     {"x1": 3, "x2": 1, "sign": "==", "value": 3},
#     {"x1": 4, "x2": 3, "sign": ">=", "value": 6},
#     {"x1": 1, "x2": 2, "sign": "<=", "value": 4}
# ]
# objetivo = "maximizacion"
# func_z = {  #basico
#     "x1": 10,
#     "x2": 20
#     }

# s_a = [
#     {"x1": 3, "x2": 1, "sign": "<=", "value": 90},
#     {"x1": 1, "x2": 1, "sign": "<=", "value": 50},
#     {"x1": 0, "x2": 1, "sign": "<=", "value": 35}
# ]
# func_z = {
#     "x1": 5,
#     "x2": 2
# }

# s_a = [
#     {"x1": 1, "x2": 3, "sign": ">=", "value": 9},
#     {"x1": 2, "x2": 1, "sign": "<=", "value": 8}
# ]


# objetivo = "maximizar" # funciona
# func_z = { 
#     "x1": 250,
#     "x2": 400
# }

# s_a = [
#     {"x1": 0.25, "x2": 0.5, "sign": "<=", "value": 50},
#     {"x1": 1, "x2": 1, "sign": "<=", "value": 150},
#     {"x1": 1, "x2": 0, "sign": "<=", "value": 125},
#     {"x1": 0, "x2": 1, "sign": "<=", "value": 125}
# ]

# objetivo = "maximizar" # funciona
# func_z = { 
#     "x1": 10,
#     "x2": 20
# }

# s_a = [
#     {"x1": 3, "x2": 1, "sign": "<=", "value": 90},
#     {"x1": 1, "x2": 1, "sign": "<=", "value": 50},
#     {"x1": 0, "x2": 1, "sign": "<=", "value": 35}
# ]
# objetivo = "maximizar" # si da
# func_z = { 
#     "x1": 2,
#     "x2": 1
# }

# s_a = [
#     {"x1": 1, "x2": 1, "sign": "==", "value": 2},
#     {"x1": 2, "x2": 3, "sign": ">=", "value": 5},
#     {"x1": 1, "x2": 2, "sign": "<=", "value": 3}
# ]

# objetivo = "maximizar" #no da
# func_z = { 
#     "x1": 0.1,
#     "x2": 0.08
# }

# s_a = [
#     {"x1": 1, "x2": 1, "sign": "<=", "value": 210000},
#     {"x1": 1, "x2": 0, "sign": "<=", "value": 130000},
#     {"x1": 0, "x2": 1, "sign": ">=", "value": 60000},
#     {"x1": 1, "x2": -2, "sign": "<=", "value": 0}
# ]

# objetivo = "minimizar" #da
# func_z = { 
#     "x1": 60,
#     "x2": 80
# }

# s_a = [
#     {"x1": 40, "x2": 50, "sign": ">=", "value": 400},
#     {"x1": 1, "x2": 1, "sign": "<=", "value": 9},
#     {"x1": 1, "x2": 0, "sign": "<=", "value": 8},
#     {"x1": 0, "x2": 1, "sign": "<=", "value": 10}
# ]

# objetivo = "minimizar" # si da
# func_z = {
#     "x1": 2000,
#     "x2": 2000
# }
# s_a = [
#     {"x1": 1, "x2": 2, "sign": ">=", "value": 80},    # R1
#     {"x1": 3, "x2": 2, "sign": ">=", "value": 160},   # R2
#     {"x1": 5, "x2": 2, "sign": ">=", "value": 200}    # R3
# ]

objetivo = "minimizar"
func_z = { # funciona
    "x1": 2000,"x2": 2000
}

s_a = [
    {"x1": 1, "x2": 2, "sign": ">=", "value": 80},
    {"x1": 3, "x2": 2, "sign": ">=", "value": 160},
    {"x1": 5, "x2": 2, "sign": ">=", "value": 200}
]

sin_dos_fases = all(restriccion["sign"] == "<=" for restriccion in s_a)

if sin_dos_fases: #todavia esta hasta maximizacion
    if(objetivo == "maximizar"):
        prN.maximizar(func_z,s_a)
    # else:
    #     prN.minimizar(func_z,s_a)

else:
    print("fase 1")

    func_z_fase1,matriz = mostrar_fase1(s_a)

    print("fase2")
    if(objetivo == "minimizar"):
        print("minimizacion")
        minimizar(func_z_fase1,func_z,matriz)
    else:
        print("maximizacion")
        maximizar(func_z_fase1,func_z,matriz)
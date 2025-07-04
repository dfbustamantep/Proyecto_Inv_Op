import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

def graficar(z1, z2, restricciones, tipo_optimizacion):
    plt.style.use('default')
    plt.figure(figsize=(12, 9))

    max_x_intercepts = []
    max_y_intercepts = []

    for a1, a2, op, b in restricciones:
        if a1 != 0:
            x_intercept = b / a1
            if x_intercept > 0:
                max_x_intercepts.append(x_intercept)
        if a2 != 0:
            y_intercept = b / a2
            if y_intercept > 0:
                max_y_intercepts.append(y_intercept)

    x_max = max(max_x_intercepts + [10]) * 1.3
    y_max = max(max_y_intercepts + [10]) * 1.3
    x_max = min(x_max, 200)
    y_max = min(y_max, 200)

    x = np.linspace(-2, x_max, 1000)
    vertices = []

    # Ampliado para 13 o más restricciones con colores extra
    colores = [
        'red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray',
        'olive', 'cyan', 'magenta', 'teal', 'navy', 'coral', 'darkgreen', 'lime', 'indigo'
    ]

    for i, (a1, a2, operador, b) in enumerate(restricciones):
        color = colores[i % len(colores)]
        if a2 != 0:
            y = (b - a1 * x) / a2
            mask = (y >= -2) & (y <= y_max) & (x >= -2) & (x <= x_max)
            x_valid = x[mask]
            y_valid = y[mask]
            if len(x_valid) > 0:
                plt.plot(x_valid, y_valid, color=color, linewidth=3,
                         label=f"R{i+1}: {a1}x₁ + {a2}x₂ {operador} {b}")
                if operador == "<=" and len(x_valid[x_valid >= 0]) > 0:
                    plt.fill_between(x_valid[x_valid >= 0],
                                     np.maximum(0, y_valid[x_valid >= 0]), 0,
                                     alpha=0.15, color=color)
                elif operador == ">=" and len(x_valid[x_valid >= 0]) > 0:
                    plt.fill_between(x_valid[x_valid >= 0],
                                     np.maximum(0, y_valid[x_valid >= 0]), y_max,
                                     alpha=0.15, color=color)
        elif a1 != 0:
            x_line = b / a1
            if -2 <= x_line <= x_max:
                plt.axvline(x=x_line, color=color, linewidth=3,
                            label=f"R{i+1}: {a1}x₁ + {a2}x₂ {operador} {b}")
                if operador == "<=" and x_line >= 0:
                    plt.axvspan(0, x_line, alpha=0.15, color=color)
                elif operador == ">=" and x_line <= x_max:
                    plt.axvspan(max(0, x_line), x_max, alpha=0.15, color=color)

        if a1 != 0:
            x_intercept = b / a1
            if x_intercept >= 0:
                vertices.append((x_intercept, 0))
        if a2 != 0:
            y_intercept = b / a2
            if y_intercept >= 0:
                vertices.append((0, y_intercept))

    for i, (a1_i, a2_i, _, b_i) in enumerate(restricciones):
        for j, (a1_j, a2_j, _, b_j) in enumerate(restricciones):
            if i < j:
                det = a1_i * a2_j - a1_j * a2_i
                if abs(det) > 1e-10:
                    x_intersect = (b_i * a2_j - b_j * a2_i) / det
                    y_intersect = (a1_i * b_j - a1_j * b_i) / det
                    if x_intersect >= -1e-10 and y_intersect >= -1e-10:
                        vertices.append((max(0, x_intersect), max(0, y_intersect)))

    vertices.append((0, 0))
    vertices_factibles = []
    for x_v, y_v in vertices:
        factible = True
        if x_v < -1e-10 or y_v < -1e-10:
            continue
        for a1, a2, operador, b in restricciones:
            valor = a1 * x_v + a2 * y_v
            if operador == "<=" and valor > b + 1e-8:
                factible = False
                break
            elif operador == ">=" and valor < b - 1e-8:
                factible = False
                break
            elif operador == "==" and abs(valor - b) > 1e-8:
                factible = False
                break
        if factible:
            vertices_factibles.append((x_v, y_v))

    vertices_unicos = []
    for vertex in vertices_factibles:
        if all(abs(vertex[0] - v[0]) > 1e-6 or abs(vertex[1] - v[1]) > 1e-6 for v in vertices_unicos):
            vertices_unicos.append(vertex)

    mejor_vertice = None
    mejor_valor = None

    if len(vertices_unicos) >= 3:
        try:
            vertices_array = np.array(vertices_unicos)
            hull = ConvexHull(vertices_array)
            hull_vertices = vertices_array[hull.vertices]
            plt.fill(hull_vertices[:, 0], hull_vertices[:, 1], color='lightgreen', alpha=0.5,
                     label='Región factible', edgecolor='darkgreen', linewidth=3)
            for i, vertex in enumerate(hull_vertices):
                plt.plot(vertex[0], vertex[1], 'o', markersize=10, color='red')
                plt.annotate(f'V{i+1} ({vertex[0]:.2f}, {vertex[1]:.2f})', (vertex[0], vertex[1]),
                             xytext=(10, 10), textcoords='offset points', fontsize=10)
            if tipo_optimizacion == "maximizacion":
                mejor_valor = float('-inf')
                for vertex in hull_vertices:
                    valor = z1 * vertex[0] + z2 * vertex[1]
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_vertice = vertex
            else:
                mejor_valor = float('inf')
                for vertex in hull_vertices:
                    valor = z1 * vertex[0] + z2 * vertex[1]
                    if valor < mejor_valor:
                        mejor_valor = valor
                        mejor_vertice = vertex
            if mejor_vertice is not None:
                plt.plot(mejor_vertice[0], mejor_vertice[1], '*', markersize=20, color='gold',
                         label=f'Óptimo: Z = {mejor_valor:.2f}')
        except Exception as e:
            print("Error en ConvexHull:", e)

    plt.xlim(-1, x_max)
    plt.ylim(-1, y_max)
    plt.xlabel("x₁")
    plt.ylabel("x₂")
    plt.title(f"Método gráfico - Z = {z1}x₁ + {z2}x₂ ({tipo_optimizacion})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return mejor_vertice, mejor_valor, vertices_unicos
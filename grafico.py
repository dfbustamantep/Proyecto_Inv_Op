import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

def graficar(z1, z2, restricciones, tipo_optimizacion):
    plt.figure(figsize=(12, 8))
    
    # Configurar límites del gráfico
    x_max = 100
    y_max = 100
    
    # Crear puntos para graficar las líneas de restricción
    x = np.linspace(0, x_max, 1000)
    
    # Lista para almacenar los puntos de intersección (vértices de la región factible)
    vertices = []
    
    # Agregar restricciones de no negatividad
    restricciones_completas = [(1, 0, ">=", 0), (0, 1, ">=", 0)] + restricciones
    
    # Graficar cada restricción
    for i, (a1, a2, operador, b) in enumerate(restricciones):
        if a2 != 0:
            # Calcular y para la línea de restricción
            y = (b - a1 * x) / a2
            
            # Filtrar valores válidos
            mask = (y >= 0) & (y <= y_max)
            x_valid = x[mask]
            y_valid = y[mask]
            
            # Graficar la línea de restricción
            plt.plot(x_valid, y_valid, linewidth=2, 
                    label=f"Restricción {i+1}: {a1}x1 + {a2}x2 {operador} {b}")
            
        elif a1 != 0:
            # Línea vertical
            x_line = b / a1
            if 0 <= x_line <= x_max:
                plt.axvline(x=x_line, linewidth=2, 
                           label=f"Restricción {i+1}: {a1}x1 + {a2}x2 {operador} {b}")
        
        # Encontrar intersecciones con los ejes
        if a1 != 0:
            x_intercept = b / a1
            if x_intercept >= 0:
                vertices.append((x_intercept, 0))
        
        if a2 != 0:
            y_intercept = b / a2
            if y_intercept >= 0:
                vertices.append((0, y_intercept))
    
    # Encontrar intersecciones entre restricciones
    for i, (a1_i, a2_i, op_i, b_i) in enumerate(restricciones):
        for j, (a1_j, a2_j, op_j, b_j) in enumerate(restricciones):
            if i < j:
                # Resolver sistema de ecuaciones 2x2
                det = a1_i * a2_j - a1_j * a2_i
                if abs(det) > 1e-10:  # Evitar división por cero
                    x_intersect = (b_i * a2_j - b_j * a2_i) / det
                    y_intersect = (a1_i * b_j - a1_j * b_i) / det
                    
                    if x_intersect >= 0 and y_intersect >= 0:
                        vertices.append((x_intersect, y_intersect))
    
    # Agregar origen y puntos en los ejes
    vertices.append((0, 0))
    
    # Filtrar vértices que satisfacen todas las restricciones
    vertices_factibles = []
    for vertex in vertices:
        x_v, y_v = vertex
        factible = True
        
        # Verificar restricciones de no negatividad
        if x_v < 0 or y_v < 0:
            factible = False
        
        # Verificar cada restricción
        for a1, a2, operador, b in restricciones:
            valor = a1 * x_v + a2 * y_v
            
            if operador == "<=" and valor > b + 1e-10:
                factible = False
                break
            elif operador == ">=" and valor < b - 1e-10:
                factible = False
                break
            elif operador == "=" and abs(valor - b) > 1e-10:
                factible = False
                break
        
        if factible:
            vertices_factibles.append(vertex)
    
    # Eliminar duplicados
    vertices_unicos = []
    for vertex in vertices_factibles:
        es_duplicado = False
        for v_unico in vertices_unicos:
            if abs(vertex[0] - v_unico[0]) < 1e-8 and abs(vertex[1] - v_unico[1]) < 1e-8:
                es_duplicado = True
                break
        if not es_duplicado:
            vertices_unicos.append(vertex)
    
    # Graficar la región factible
    if len(vertices_unicos) >= 3:
        try:
            # Ordenar vértices para formar un polígono
            vertices_array = np.array(vertices_unicos)
            hull = ConvexHull(vertices_array)
            
            # Crear polígono de la región factible
            for simplex in hull.simplices:
                plt.plot(vertices_array[simplex, 0], vertices_array[simplex, 1], 'k-', alpha=0.5)
            
            # Rellenar la región factible
            hull_vertices = vertices_array[hull.vertices]
            plt.fill(hull_vertices[:, 0], hull_vertices[:, 1], 
                    color='lightgreen', alpha=0.3, label='Región factible')
            
            # Marcar vértices
            for vertex in hull_vertices:
                plt.plot(vertex[0], vertex[1], 'ro', markersize=8)
                plt.annotate(f'({vertex[0]:.1f}, {vertex[1]:.1f})', 
                           (vertex[0], vertex[1]), xytext=(5, 5), 
                           textcoords='offset points', fontsize=10)
            
            # Encontrar el vértice óptimo
            if tipo_optimizacion == "maximizacion":
                mejor_valor = float('-inf')
                mejor_vertice = None
                for vertex in hull_vertices:
                    valor = z1 * vertex[0] + z2 * vertex[1]
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_vertice = vertex
            else:  # minimización
                mejor_valor = float('inf')
                mejor_vertice = None
                for vertex in hull_vertices:
                    valor = z1 * vertex[0] + z2 * vertex[1]
                    if valor < mejor_valor:
                        mejor_valor = valor
                        mejor_vertice = vertex
            
            if mejor_vertice is not None:
                plt.plot(mejor_vertice[0], mejor_vertice[1], 'b*', markersize=15, 
                        label=f'Óptimo: ({mejor_vertice[0]:.2f}, {mejor_vertice[1]:.2f})\nZ = {mejor_valor:.2f}')
                
                # Graficar algunas líneas iso-beneficio/iso-costo
                if z2 != 0:
                    for k in range(1, 4):
                        z_value = mejor_valor * k * 0.5
                        y_iso = (z_value - z1 * x) / z2
                        mask = (y_iso >= 0) & (y_iso <= y_max)
                        if np.any(mask):
                            plt.plot(x[mask], y_iso[mask], '--', alpha=0.7, 
                                   label=f'Z = {z_value:.0f}' if k == 1 else '')
        
        except Exception as e:
            print(f"Error al crear la región factible: {e}")
            # Graficar puntos individualmente si falla ConvexHull
            for vertex in vertices_unicos:
                plt.plot(vertex[0], vertex[1], 'ro', markersize=8)
                plt.annotate(f'({vertex[0]:.1f}, {vertex[1]:.1f})', 
                           (vertex[0], vertex[1]), xytext=(5, 5), 
                           textcoords='offset points', fontsize=10)
    
    elif len(vertices_unicos) > 0:
        # Graficar puntos si hay pocos vértices
        for vertex in vertices_unicos:
            plt.plot(vertex[0], vertex[1], 'ro', markersize=8)
            plt.annotate(f'({vertex[0]:.1f}, {vertex[1]:.1f})', 
                       (vertex[0], vertex[1]), xytext=(5, 5), 
                       textcoords='offset points', fontsize=10)
    
    # Configurar el gráfico
    plt.xlim(0, x_max)
    plt.ylim(0, y_max)
    plt.xlabel("X1", fontsize=12)
    plt.ylabel("X2", fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.title(f"Gráfico del modelo ({tipo_optimizacion.capitalize()})\nZ = {z1}X1 + {z2}X2", fontsize=14)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Mostrar información adicional
    print(f"\nResultados del {tipo_optimizacion}:")
    print(f"Función objetivo: Z = {z1}X1 + {z2}X2")
    print(f"Vértices de la región factible:")
    for i, vertex in enumerate(vertices_unicos):
        valor_z = z1 * vertex[0] + z2 * vertex[1]
        print(f"  Vértice {i+1}: ({vertex[0]:.2f}, {vertex[1]:.2f}) -> Z = {valor_z:.2f}")
    
    plt.tight_layout()
    plt.show()

# Función auxiliar para pruebas
def test_graficar():
    # Ejemplo de prueba
    z1, z2 = 10000, 30000
    restricciones = [
        (5, 5, "<=", 250),
        (3, 7, "<=", 210),
        (0, 1, "<=", 20)
    ]
    graficar(z1, z2, restricciones, "maximizacion")

if __name__ == "__main__":
    test_graficar()
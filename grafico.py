import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.patches as patches

def graficar(z1, z2, restricciones, tipo_optimizacion):
    """
    Función mejorada para graficar problemas de programación lineal
    
    Args:
        z1, z2: Coeficientes de la función objetivo
        restricciones: Lista de tuplas (a1, a2, operador, b)
        tipo_optimizacion: "maximizacion" o "minimizacion"
    """
    # Configurar estilo
    plt.style.use('default')
    plt.figure(figsize=(10, 7))
    
    # Calcular límites inteligentes del gráfico
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
    
    # Establecer límites con margen
    x_max = max(max_x_intercepts) * 1.2 if max_x_intercepts else 20
    y_max = max(max_y_intercepts) * 1.2 if max_y_intercepts else 20
    
    # Límites mínimos y máximos
    x_max = max(min(x_max, 100), 10)
    y_max = max(min(y_max, 100), 10)
    
    # Crear array de puntos
    x = np.linspace(0, x_max, 1000)
    
    # Colores para restricciones
    colores = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']
    
    # Lista para vértices candidatos
    vertices_candidatos = [(0, 0)]  # Siempre incluir el origen
    
    # Graficar restricciones
    for i, (a1, a2, operador, b) in enumerate(restricciones):
        color = colores[i % len(colores)]
        
        if a2 != 0:
            # Línea de restricción: a1*x + a2*y = b
            y_line = (b - a1 * x) / a2
            
            # Filtrar puntos válidos
            mask = (y_line >= 0) & (y_line <= y_max) & (x >= 0) & (x <= x_max)
            x_valid = x[mask]
            y_valid = y_line[mask]
            
            if len(x_valid) > 0:
                # Graficar línea
                plt.plot(x_valid, y_valid, color=color, linewidth=3, 
                        label=f"R{i+1}: {a1}x₁ + {a2}x₂ {operador} {b}")
                
                # Encontrar intersecciones con ejes
                if a1 != 0:
                    x_int = b / a1
                    if x_int >= 0:
                        vertices_candidatos.append((x_int, 0))
                
                if a2 != 0:
                    y_int = b / a2
                    if y_int >= 0:
                        vertices_candidatos.append((0, y_int))
        
        elif a1 != 0:  # Línea vertical
            x_line = b / a1
            if 0 <= x_line <= x_max:
                plt.axvline(x=x_line, color=color, linewidth=3,
                           label=f"R{i+1}: {a1}x₁ {operador} {b}")
                vertices_candidatos.append((x_line, 0))
    
    # Encontrar intersecciones entre restricciones
    for i in range(len(restricciones)):
        for j in range(i + 1, len(restricciones)):
            a1_i, a2_i, _, b_i = restricciones[i]
            a1_j, a2_j, _, b_j = restricciones[j]
            
            # Resolver sistema 2x2
            det = a1_i * a2_j - a1_j * a2_i
            if abs(det) > 1e-10:
                x_int = (b_i * a2_j - b_j * a2_i) / det
                y_int = (a1_i * b_j - a1_j * b_i) / det
                
                if x_int >= -1e-10 and y_int >= -1e-10:
                    vertices_candidatos.append((max(0, x_int), max(0, y_int)))
    
    # Filtrar vértices factibles
    vertices_factibles = []
    for vertex in vertices_candidatos:
        x_v, y_v = vertex
        es_factible = True
        
        # Verificar no negatividad
        if x_v < -1e-10 or y_v < -1e-10:
            es_factible = False
        
        # Verificar restricciones
        for a1, a2, operador, b in restricciones:
            valor = a1 * x_v + a2 * y_v
            
            if operador == "<=" and valor > b + 1e-8:
                es_factible = False
                break
            elif operador == ">=" and valor < b - 1e-8:
                es_factible = False
                break
            elif operador == "=" and abs(valor - b) > 1e-8:
                es_factible = False
                break
        
        if es_factible:
            vertices_factibles.append((max(0, x_v), max(0, y_v)))
    
    # Eliminar duplicados
    vertices_unicos = []
    for vertex in vertices_factibles:
        es_duplicado = False
        for v_unico in vertices_unicos:
            if abs(vertex[0] - v_unico[0]) < 1e-6 and abs(vertex[1] - v_unico[1]) < 1e-6:
                es_duplicado = True
                break
        if not es_duplicado:
            vertices_unicos.append(vertex)
    
    # Variables para el óptimo
    mejor_vertice = None
    mejor_valor = None
    
    # Crear y mostrar región factible
    if len(vertices_unicos) >= 3:
        try:
            vertices_array = np.array(vertices_unicos)
            hull = ConvexHull(vertices_array)
            hull_vertices = vertices_array[hull.vertices]
            
            # Rellenar región factible (solo el área, más limpio)
            plt.fill(hull_vertices[:, 0], hull_vertices[:, 1], 
                    color='lightgreen', alpha=0.3, label='Región factible',
                    edgecolor='darkgreen', linewidth=2)
            
            # Marcar vértices
            for i, vertex in enumerate(hull_vertices):
                plt.plot(vertex[0], vertex[1], 'o', markersize=10, 
                        markerfacecolor='darkred', markeredgecolor='black', markeredgewidth=2)
                plt.annotate(f'({vertex[0]:.2f}, {vertex[1]:.2f})', 
                           (vertex[0], vertex[1]), xytext=(15, 15), 
                           textcoords='offset points', fontsize=10, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            
            # Encontrar óptimo
            if tipo_optimizacion == "maximizacion":
                mejor_valor = float('-inf')
                for vertex in hull_vertices:
                    valor = z1 * vertex[0] + z2 * vertex[1]
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_vertice = vertex
            else:  # minimización
                mejor_valor = float('inf')
                for vertex in hull_vertices:
                    valor = z1 * vertex[0] + z2 * vertex[1]
                    if valor < mejor_valor:
                        mejor_valor = valor
                        mejor_vertice = vertex
            
            # Marcar punto óptimo
            if mejor_vertice is not None:
                plt.plot(mejor_vertice[0], mejor_vertice[1], '*', markersize=20, 
                        color='gold', markeredgecolor='black', markeredgewidth=2,
                        label=f'Óptimo: ({mejor_vertice[0]:.2f}, {mejor_vertice[1]:.2f})')
                
                # Línea iso-beneficio/iso-costo óptima
                if z2 != 0:
                    y_optimo = (mejor_valor - z1 * x) / z2
                    mask = (y_optimo >= 0) & (y_optimo <= y_max) & (x >= 0) & (x <= x_max)
                    if np.any(mask):
                        plt.plot(x[mask], y_optimo[mask], '--', color='gold', linewidth=3, 
                               label=f'Z* = {mejor_valor:.2f}')
        
        except Exception as e:
            print(f"Error en ConvexHull: {e}")
    
    # Configurar gráfico
    plt.xlim(-1, x_max * 1.05)
    plt.ylim(-1, y_max * 1.05)
    plt.xlabel("x₁ (Variable 1)", fontsize=14, fontweight='bold')
    plt.ylabel("x₂ (Variable 2)", fontsize=14, fontweight='bold')
    
    # Ejes
    plt.axhline(0, color='black', linewidth=1.5)
    plt.axvline(0, color='black', linewidth=1.5)
    
    # Título
    titulo = f"Programación Lineal - Método Gráfico\n"
    titulo += f"Z = {z1}x₁ + {z2}x₂ ({tipo_optimizacion.capitalize()})"
    plt.title(titulo, fontsize=16, fontweight='bold', pad=20)
    
    # Leyenda
    plt.legend(loc='upper right', fontsize=10, framealpha=0.9)
    
    # Grilla
    plt.grid(True, alpha=0.3)
    
    # Información del resultado
    if mejor_vertice is not None:
        info_text = f"Solución Óptima:\n"
        info_text += f"x₁* = {mejor_vertice[0]:.3f}\n"
        info_text += f"x₂* = {mejor_vertice[1]:.3f}\n"
        info_text += f"Z* = {mejor_valor:.3f}"
        
        plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
                 fontsize=12, verticalalignment='top', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.9))
    
    plt.tight_layout()
    plt.show()
    
    # Imprimir resultados detallados
    print("\n" + "="*80)
    print(f"MÉTODO GRÁFICO - {tipo_optimizacion.upper()}")
    print("="*80)
    print(f"Función objetivo: Z = {z1}x₁ + {z2}x₂")
    print(f"\nRestricciones:")
    for i, (a1, a2, op, b) in enumerate(restricciones):
        print(f"  R{i+1}: {a1}x₁ + {a2}x₂ {op} {b}")
    print(f"  No negatividad: x₁, x₂ ≥ 0")
    
    print(f"\nVértices de la región factible:")
    valores_z = []
    for i, vertex in enumerate(vertices_unicos):
        valor_z = z1 * vertex[0] + z2 * vertex[1]
        valores_z.append(valor_z)
        print(f"  V{i+1}: ({vertex[0]:.4f}, {vertex[1]:.4f}) → Z = {valor_z:.4f}")
    
    if mejor_vertice is not None:
        print(f"\n{'='*40}")
        print(f"SOLUCIÓN ÓPTIMA:")
        print(f"{'='*40}")
        print(f"Punto óptimo: ({mejor_vertice[0]:.4f}, {mejor_vertice[1]:.4f})")
        print(f"Valor óptimo: Z* = {mejor_valor:.4f}")
        print(f"Tipo: {tipo_optimizacion}")
        print(f"{'='*40}")
    
    return mejor_vertice, mejor_valor, vertices_unicos

# Ejemplo de uso con tu problema
if __name__ == "__main__":
    # Ejemplo: Maximizar Z = 10000x1 + 30000x2
    z1 = 10000
    z2 = 30000
    
    restricciones = [
        (5, 5, "<=", 250),   # 5x1 + 5x2 <= 250
        (3, 7, "<=", 210),   # 3x1 + 7x2 <= 210
        (0, 1, "<=", 20),    # x2 <= 20 (corrigiendo la restricción)
    ]
    
    tipo = "maximizacion"
    
    # Llamar a la función
    optimo, valor_optimo, vertices = graficar(z1, z2, restricciones, tipo)
    
    print(f"\nVerificación manual:")
    print(f"En el punto óptimo ({optimo[0]:.3f}, {optimo[1]:.3f}):")
    print(f"Z = {z1}*{optimo[0]:.3f} + {z2}*{optimo[1]:.3f} = {valor_optimo:.3f}")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.patches as patches

def graficar(z1, z2, restricciones, tipo_optimizacion):
    # Configurar el estilo de matplotlib para mejor visualización
    plt.style.use('default')
    plt.figure(figsize=(12, 9))  # Aumentar tamaño de figura
    
    # Configurar límites del gráfico de manera más inteligente
    # Calcular intersecciones con los ejes para determinar mejor rango
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
    
    # Determinar límites más inteligentes
    if max_x_intercepts:
        x_max = max(max_x_intercepts) * 1.3  # 30% más de margen
    else:
        x_max = 20
    
    if max_y_intercepts:
        y_max = max(max_y_intercepts) * 1.3  # 30% más de margen
    else:
        y_max = 20
    
    # Establecer límites mínimos para evitar gráficos muy pequeños
    x_max = max(x_max, 10)
    y_max = max(y_max, 10)
    
    # Limitar para evitar gráficos extremadamente grandes
    x_max = min(x_max, 100)
    y_max = min(y_max, 100)
    
    # Crear puntos para graficar las líneas de restricción
    x = np.linspace(-2, x_max, 1000)
    
    # Lista para almacenar los puntos de intersección
    vertices = []
    
    # Colores para las restricciones
    colores = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    # Graficar cada restricción con información más clara
    for i, (a1, a2, operador, b) in enumerate(restricciones):
        color = colores[i % len(colores)]
        
        if a2 != 0:
            # Calcular y para la línea de restricción
            y = (b - a1 * x) / a2
            
            # Filtrar valores válidos (expandir rango para mejor visualización)
            mask = (y >= -2) & (y <= y_max) & (x >= -2) & (x <= x_max)
            x_valid = x[mask]
            y_valid = y[mask]
            
            if len(x_valid) > 0:
                # Graficar la línea de restricción
                plt.plot(x_valid, y_valid, color=color, linewidth=3, 
                        label=f"R{i+1}: {a1}x₁ + {a2}x₂ {operador} {b}")
                
                # Sombrear la región que satisface la restricción
                if operador == "<=":
                    # Para x₁, x₂ ≥ 0, solo sombrear en el primer cuadrante
                    x_shade = x_valid[x_valid >= 0]
                    y_shade = y_valid[x_valid >= 0]
                    if len(x_shade) > 0:
                        plt.fill_between(x_shade, np.maximum(0, y_shade), 0, alpha=0.15, color=color)
                elif operador == ">=":
                    x_shade = x_valid[x_valid >= 0]
                    y_shade = y_valid[x_valid >= 0]
                    if len(x_shade) > 0:
                        plt.fill_between(x_shade, np.maximum(0, y_shade), y_max, alpha=0.15, color=color)
                
                # Agregar etiqueta de la restricción en la línea
                if len(x_valid) > 10:
                    # Encontrar un buen punto para la etiqueta
                    valid_indices = np.where((x_valid >= 0) & (y_valid >= 0))[0]
                    if len(valid_indices) > 0:
                        mid_idx = valid_indices[len(valid_indices) // 2]
                        plt.annotate(f'R{i+1}', 
                                   xy=(x_valid[mid_idx], y_valid[mid_idx]),
                                   xytext=(12, 12), textcoords='offset points',
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor=color, alpha=0.8),
                                   fontsize=12, fontweight='bold', color='white')
        
        elif a1 != 0:
            # Línea vertical
            x_line = b / a1
            if -2 <= x_line <= x_max:
                plt.axvline(x=x_line, color=color, linewidth=3, 
                           label=f"R{i+1}: {a1}x₁ + {a2}x₂ {operador} {b}")
                
                # Sombrear región
                if operador == "<=":
                    if x_line >= 0:
                        plt.axvspan(0, x_line, alpha=0.15, color=color)
                elif operador == ">=":
                    if x_line <= x_max:
                        plt.axvspan(max(0, x_line), x_max, alpha=0.15, color=color)
        
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
                if abs(det) > 1e-10:
                    x_intersect = (b_i * a2_j - b_j * a2_i) / det
                    y_intersect = (a1_i * b_j - a1_j * b_i) / det
                    
                    if x_intersect >= -1e-10 and y_intersect >= -1e-10:
                        vertices.append((max(0, x_intersect), max(0, y_intersect)))
    
    # Agregar origen
    vertices.append((0, 0))
    
    # Filtrar vértices que satisfacen todas las restricciones
    vertices_factibles = []
    for vertex in vertices:
        x_v, y_v = vertex
        factible = True
        
        # Verificar restricciones de no negatividad
        if x_v < -1e-10 or y_v < -1e-10:
            factible = False
        
        # Verificar cada restricción
        for a1, a2, operador, b in restricciones:
            valor = a1 * x_v + a2 * y_v
            
            if operador == "<=" and valor > b + 1e-8:
                factible = False
                break
            elif operador == ">=" and valor < b - 1e-8:
                factible = False
                break
            elif operador == "=" and abs(valor - b) > 1e-8:
                factible = False
                break
        
        if factible:
            vertices_factibles.append((max(0, x_v), max(0, y_v)))
    
    # Eliminar duplicados con mayor tolerancia
    vertices_unicos = []
    for vertex in vertices_factibles:
        es_duplicado = False
        for v_unico in vertices_unicos:
            if abs(vertex[0] - v_unico[0]) < 1e-6 and abs(vertex[1] - v_unico[1]) < 1e-6:
                es_duplicado = True
                break
        if not es_duplicado:
            vertices_unicos.append(vertex)
    
    # Variables para almacenar información del óptimo
    mejor_vertice = None
    mejor_valor = None
    
    # Graficar la región factible
    if len(vertices_unicos) >= 3:
        try:
            # Ordenar vértices para formar un polígono
            vertices_array = np.array(vertices_unicos)
            hull = ConvexHull(vertices_array)
            
            # Crear polígono de la región factible con mejor visualización
            hull_vertices = vertices_array[hull.vertices]
            
            # Rellenar la región factible
            plt.fill(hull_vertices[:, 0], hull_vertices[:, 1], 
                    color='lightgreen', alpha=0.5, label='Región factible', 
                    edgecolor='darkgreen', linewidth=3)
            
            # Marcar vértices con mejor formato
            for i, vertex in enumerate(hull_vertices):
                plt.plot(vertex[0], vertex[1], 'o', markersize=12, markerfacecolor='red', 
                        markeredgecolor='black', markeredgewidth=2)
                plt.annotate(f'V{i+1}({vertex[0]:.2f}, {vertex[1]:.2f})', 
                           (vertex[0], vertex[1]), xytext=(18, 18), 
                           textcoords='offset points', fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                                   edgecolor='black', alpha=0.9))
            
            # Encontrar el vértice óptimo
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
            
            if mejor_vertice is not None:
                plt.plot(mejor_vertice[0], mejor_vertice[1], '*', markersize=25, 
                        color='gold', markeredgecolor='black', markeredgewidth=3,
                        label=f'Óptimo: ({mejor_vertice[0]:.2f}, {mejor_vertice[1]:.2f})')
                
                # Graficar líneas iso-beneficio/iso-costo
                if z2 != 0:
                    # Línea que pasa por el punto óptimo
                    y_optimo = (mejor_valor - z1 * x) / z2
                    mask = (y_optimo >= -2) & (y_optimo <= y_max) & (x >= -2) & (x <= x_max)
                    if np.any(mask):
                        plt.plot(x[mask], y_optimo[mask], '--', color='gold', linewidth=4, 
                               label=f'Z* = {mejor_valor:.2f}')
                    
                    # Líneas adicionales para mostrar dirección de optimización
                    for k in [0.5, 1.5]:
                        z_value = mejor_valor * k
                        y_iso = (z_value - z1 * x) / z2
                        mask = (y_iso >= -2) & (y_iso <= y_max) & (x >= -2) & (x <= x_max)
                        if np.any(mask):
                            plt.plot(x[mask], y_iso[mask], ':', alpha=0.7, color='orange', linewidth=2,
                                   label=f'Z = {z_value:.1f}' if k == 0.5 else '')
        
        except Exception as e:
            print(f"Error al crear la región factible: {e}")
            # Graficar puntos individualmente si falla ConvexHull
            for i, vertex in enumerate(vertices_unicos):
                plt.plot(vertex[0], vertex[1], 'ro', markersize=12)
                plt.annotate(f'V{i+1}({vertex[0]:.2f}, {vertex[1]:.2f})', 
                           (vertex[0], vertex[1]), xytext=(18, 18), 
                           textcoords='offset points', fontsize=12)
    
    elif len(vertices_unicos) > 0:
        # Graficar puntos si hay pocos vértices
        for i, vertex in enumerate(vertices_unicos):
            plt.plot(vertex[0], vertex[1], 'ro', markersize=12)
            plt.annotate(f'V{i+1}({vertex[0]:.2f}, {vertex[1]:.2f})', 
                       (vertex[0], vertex[1]), xytext=(18, 18), 
                       textcoords='offset points', fontsize=12)
    
    # Configurar el gráfico con mejor formato y límites más apropiados
    plt.xlim(-1, x_max * 1.05)
    plt.ylim(-1, y_max * 1.05)
    plt.xlabel("x₁ (Variable 1)", fontsize=16, fontweight='bold')
    plt.ylabel("x₂ (Variable 2)", fontsize=16, fontweight='bold')
    
    # Líneas de ejes más visibles
    plt.axhline(0, color='black', linewidth=2)
    plt.axvline(0, color='black', linewidth=2)
    
    # Título más informativo
    titulo = f"Programación Lineal - Método Gráfico\n"
    titulo += f"Función Objetivo: Z = {z1}x₁ + {z2}x₂ ({tipo_optimizacion.capitalize()})"
    plt.title(titulo, fontsize=18, fontweight='bold', pad=25)
    
    # Leyenda mejorada
    plt.legend(loc='upper right', fontsize=12, framealpha=0.95, 
              fancybox=True, shadow=True)
    
    # Grilla más visible
    plt.grid(True, alpha=0.4, linestyle='-', linewidth=0.8)
    
    # Agregar información de texto en el gráfico
    info_text = f"Restricciones: {len(restricciones)}\n"
    info_text += f"Vértices factibles: {len(vertices_unicos)}\n"
    if mejor_vertice is not None:
        info_text += f"Solución óptima: Z* = {mejor_valor:.2f}\n"
        info_text += f"En punto: ({mejor_vertice[0]:.2f}, {mejor_vertice[1]:.2f})"
    
    plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
             fontsize=13, verticalalignment='top', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.6', facecolor='lightblue', alpha=0.9))
    
    # Mejorar el formato de los números en los ejes
    plt.gca().tick_params(axis='both', which='major', labelsize=12)
    
    # Mostrar información detallada en consola
    print("\n" + "="*60)
    print(f"RESULTADOS DEL MÉTODO GRÁFICO - {tipo_optimizacion.upper()}")
    print("="*60)
    print(f"Función objetivo: Z = {z1}x₁ + {z2}x₂")
    print(f"\nRestricciones:")
    for i, (a1, a2, op, b) in enumerate(restricciones):
        print(f"  R{i+1}: {a1}x₁ + {a2}x₂ {op} {b}")
    print(f"  Restricciones de no negatividad: x₁, x₂ ≥ 0")
    
    print(f"\nVértices de la región factible:")
    if len(vertices_unicos) > 0:
        for i, vertex in enumerate(vertices_unicos):
            valor_z = z1 * vertex[0] + z2 * vertex[1]
            print(f"  V{i+1}: ({vertex[0]:.4f}, {vertex[1]:.4f}) → Z = {valor_z:.4f}")
    else:
        print("  No se encontraron vértices factibles")
    
    if mejor_vertice is not None:
        print(f"\nSOLUCIÓN ÓPTIMA:")
        print(f"  Punto óptimo: ({mejor_vertice[0]:.4f}, {mejor_vertice[1]:.4f})")
        print(f"  Valor óptimo: Z* = {mejor_valor:.4f}")
        print(f"  Tipo de optimización: {tipo_optimizacion}")
    else:
        print(f"\nNo se pudo determinar una solución óptima")
    
    print("="*60)
    
    plt.tight_layout()
    plt.show()
    
    return mejor_vertice, mejor_valor, vertices_unicos
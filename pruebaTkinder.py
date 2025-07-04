import tkinter as tk
from tkinter import ttk
import re
from Dos_fases.presentacion import minimizar, maximizar, mostrar_fase1
from None_fase import none_fase as nf, presentacion as prN
from tkinter import Label

class SimplexVentana(tk.Toplevel):
    def __init__(self, master, tipo_optimizacion):
        super().__init__(master)
        self.title("Método Simplex - Dos Fases")
        self.geometry("1100x800")
        self.tipo_optimizacion = tipo_optimizacion
        self.configure(bg="#ffffff")
        
        
        titulo_label = tk.Label(self, text="Método Simplex - Dos Fases", font=("Arial", 14, "bold"),bg="#ffffff").pack(pady=10)
        tipo_label=tk.Label(self, text=f"Tipo: {tipo_optimizacion.capitalize()}", font=("Arial", 10),bg="#ffffff").pack(pady=5)
        
        # Entrada función objetivo
        frame_obj = ttk.LabelFrame(self, text="Función Objetivo (ej: 4x1 + 1x2)")
        frame_obj.pack(fill="x", padx=10, pady=5)
        self.entry_objetivo = ttk.Entry(frame_obj)
        self.entry_objetivo.pack(fill="x", padx=5, pady=5)

        # Restricciones
        frame_rest = ttk.LabelFrame(self, text="Restricciones (una por línea, ej: 3x1 + 1x2 >= 3)")
        frame_rest.pack(fill="both", padx=10, pady=5)
        self.text_restricciones = tk.Text(frame_rest, height=5)
        self.text_restricciones.pack(fill="both", padx=5, pady=5)

        # Botón ejecutar
        self.btn_start = ttk.Button(self, text="Ejecutar Simplex", command=self.ejecutar_simplex)
        self.btn_start.pack(pady=10)

        # Frame para mostrar tabla del método simplex
        self.frame_tabla = ttk.Frame(self)
        self.frame_tabla.pack(fill="both", expand=False, padx=10, pady=5)
        self.tree = None  # Tabla inicial vacía

        # Output
        self.output = tk.Text(self, height=15, width=100)
        self.output.pack(padx=10, pady=10)

    def imprimir(self, texto):
        self.output.insert(tk.END, texto + '\n')
        self.output.see(tk.END)

    def mostrar_tabla_simplex(self, columnas, filas, titulo="Tabla Simplex"):
        # Borra tabla anterior si existe
        if self.tree:
            self.tree.destroy()

        # Crear nueva tabla
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=len(filas))
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor='center')
        for fila in filas:
            self.tree.insert("", "end", values=fila)
        self.tree.pack(fill="x", expand=True)

    def parse_func_z(self, texto):
        texto = texto.replace(" ", "")
        partes = re.findall(r'([+-]?\d*\.?\d*)x(\d+)', texto)
        func_z = {}
        for coef, varnum in partes:
            if coef in ['', '+']: coef = 1
            elif coef == '-': coef = -1
            func_z[f"x{varnum}"] = float(coef)
        return func_z

    def parse_restricciones(self, texto):
        restricciones = []
        lineas = texto.strip().split('\n')
        for linea in lineas:
            match = re.match(r'(.+?)(<=|>=|==)(.+)', linea.replace(" ", ""))
            if not match:
                continue
            lhs, signo, rhs = match.groups()
            partes = re.findall(r'([+-]?\d*\.?\d*)x(\d+)', lhs)
            restriccion = {}
            for coef, varnum in partes:
                if coef in ['', '+']: coef = 1
                elif coef == '-': coef = -1
                restriccion[f"x{varnum}"] = float(coef)
            restriccion['sign'] = signo
            restriccion['value'] = float(rhs)
            restricciones.append(restriccion)
        return restricciones

    def ejecutar_simplex(self):
        self.output.delete("1.0", tk.END)
        raw_func_z = self.entry_objetivo.get()
        raw_restricciones = self.text_restricciones.get("1.0", tk.END)

        try:
            func_z = self.parse_func_z(raw_func_z)
            restricciones = self.parse_restricciones(raw_restricciones)

            if not func_z or not restricciones:
                self.imprimir("⚠️ Error: debes ingresar función objetivo y restricciones válidas.")
                return

            sin_dos_fases = all(r["sign"] == "<=" for r in restricciones)

            if sin_dos_fases:
                if self.tipo_optimizacion == "maximizacion":
                    prN.maximizar(func_z, restricciones, imprimir=self.imprimir)
                else:
                    prN.minimizar(func_z, restricciones, imprimir=self.imprimir)
            else:
                self.imprimir("✅ Fase 1")
                func_z_fase1, matriz = mostrar_fase1(restricciones, imprimir=self.imprimir)

                # Mostrar tabla con base en una iteración ejemplo
                columnas = list(matriz[0].keys())
                filas = [[fila[col] for col in columnas] for fila in matriz]
                self.mostrar_tabla_simplex(columnas + ["Bi", "Base"], filas)

                self.imprimir("✅ Fase 2")
                if self.tipo_optimizacion == "minimizacion":
                    minimizar(func_z_fase1, func_z, matriz, imprimir=self.imprimir)
                else:
                    maximizar(func_z_fase1, func_z, matriz, imprimir=self.imprimir)

        except Exception as e:
            self.imprimir(f"❌ Error al ejecutar: {str(e)}")
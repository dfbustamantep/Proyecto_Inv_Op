import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from Dos_fases.presentacion import minimizar, maximizar, mostrar_fase1
from None_fase import none_fase as nf, presentacion as prN
import re

class SimplexApp(Toplevel):
    def __init__(self, master,tipo_optimizacion, num_restricciones=0, num_variables=0):
        super().__init__(master)
        self.master = master
        self.objetivo=tipo_optimizacion
        self.title("Método Simplex - Dos Fases")
        frame_objetivo = tk.LabelFrame(self, text=f"Tipo: {self.objetivo.capitalize()}", font=("Arial", 10), bg="#ffffff")
        frame_objetivo.pack(fill="x", padx=10, pady=5)
        
        # --- Entrada de la función objetivo ---
        frame_obj = ttk.LabelFrame(self, text="Función Objetivo (ej: 4x1 + 1x2)")
        frame_obj.pack(fill="x", padx=10, pady=5)
        self.entry_objetivo = ttk.Entry(frame_obj)
        self.entry_objetivo.pack(fill="x", padx=5, pady=5)

        # --- Entrada de restricciones ---
        frame_rest = ttk.LabelFrame(self, text="Restricciones (una por línea, ej: 3x1 + 1x2 >= 3)")
        frame_rest.pack(fill="both", padx=10, pady=5)
        self.text_restricciones = tk.Text(frame_rest, height=5)
        self.text_restricciones.pack(fill="both", padx=5, pady=5)

        # --- Selección de objetivo ---
        #frame_objetivo = ttk.LabelFrame(self, text="Tipo de Optimización")
        #frame_objetivo.pack(fill="x", padx=10, pady=5)
        #self.objetivo = tk.StringVar(value="minimizar")
        #ttk.Radiobutton(frame_objetivo, text="Minimizar", variable=self.objetivo, value="minimizar").pack(side="left", padx=10)
        #ttk.Radiobutton(frame_objetivo, text="Maximizar", variable=self.objetivo, value="maximizar").pack(side="left", padx=10)

        # --- Botón de ejecución ---
        self.btn_start = ttk.Button(self, text="Ejecutar Simplex", command=self.ejecutar_simplex)
        self.btn_start.pack(pady=10)

        # --- Salida ---
        self.output = tk.Text(self, height=30, width=100)
        self.output.pack(padx=10, pady=10)

    def imprimir(self, texto):
        self.output.insert(tk.END, texto + '\n')
        self.output.see(tk.END)

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
                if self.objetivo == "maximizar":
                    prN.maximizar(func_z, restricciones, imprimir=self.imprimir)
                else:
                    prN.minimizar(func_z, restricciones, imprimir=self.imprimir)
            else:
                self.imprimir("✅ Fase 1")
                func_z_fase1, matriz = mostrar_fase1(restricciones, imprimir=self.imprimir)

                self.imprimir("✅ Fase 2")
                if self.objetivo == "minimizar":
                    self.imprimir("minimizacion")
                    minimizar(func_z_fase1, func_z, matriz, imprimir=self.imprimir)
                else:
                    self.imprimir("maximizacion")
                    maximizar(func_z_fase1, func_z, matriz, imprimir=self.imprimir)

        except Exception as e:
            self.imprimir(f"❌ Error al ejecutar: {str(e)}")

""" 
if __name__ == "__main__":
    root = tk.Tk()
    app = SimplexApp(root)
    root.mainloop() """
from tkinter import *
from tkinter import messagebox
from grafico import graficar
from pruebaTkinder import SimplexApp

class VentanaPrincipal(Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto investigación de operaciones")
        #ancho x alto
        self.geometry("500x450")
        self.configure(bg="#ffffff")
        
        self.tipo_optimizacion = StringVar(value=" Ninguno")
        
        # Etiqueta
        self.label_titulo = Label(self, text="Proyecto investigación de operaciones",font=("Arial",12,"bold"),bg="#ffffff")
        self.label_titulo.pack(pady=10)

        #Frame para seleccionar si es maxximizacion o minimizacion
        self.frame_optimizacion = Frame(self,bg="#ffffff")
        self.frame_optimizacion.pack(pady=10)
        
        self.label_opt =Label(self.frame_optimizacion, text="Seleccione el tipo de optimización:",font=("Arial", 12),bg="#ffffff")
        self.label_opt.pack(pady=5)
        
        # Radiobuttons para seleccionar tipo de optimización
        self.radio_max = Radiobutton(self.frame_optimizacion, text="Maximización",variable=self.tipo_optimizacion, value="maximizacion",command=self.actualizar_botones,bg="#ffffff",font=("Arial", 11),)
        self.radio_max.pack(pady=2)
        
        self.radio_min = Radiobutton(self.frame_optimizacion, text="Minimización",variable=self.tipo_optimizacion, value="minimizacion",command=self.actualizar_botones,bg="#ffffff",font=("Arial", 11))
        self.radio_min.pack(pady=2)
        
        self.frmae_metodos= Frame(self,bg="#ffffff")
        self.frmae_metodos.pack(pady=5)
        
        # Etiqueta
        self.label1 = Label(self, text="Seleccione la opción que desea:",font=("Arial", 12),bg="#ffffff")
        self.label1.pack(pady=5)
        
        # Boton
        self.button_dos_fases = Button(self, text="Metodo de dos fases", command=self.solicitar_datos_dos_fases,state="disabled",bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2)
        self.button_dos_fases.pack(pady=5)

        self.button_grafico = Button(self, text="Metodo gráfico", command=self.solicitar_restricciones,state="disabled",bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2)
        self.button_grafico.pack(pady=5)

        self.button_credtios = Button(self, text="Creditos", command=self.creditos,bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2)
        self.button_credtios.pack(pady=5)
        
        # Etiqueta para mostrar resultado
        self.credito = Label(self, text="",bg="#ffffff")
        self.credito.pack(pady=10)
        
    def actualizar_botones(self):
        """Habilita los botones de los metodos cuando se eslecciona el tipo de optimizacion"""
        if self.tipo_optimizacion.get():
            self.button_dos_fases.config(state='normal')
            self.button_grafico.config(state='normal')
            # Limpiar créditos si están mostrados
            self.credito.config(text="")
        
    def creditos(self):
        mensaje="Aplicación realizada por: \nDonghe Do\nCrithian Prieto\nDavid Guaba\nDaniel Bustamante"
        messagebox.showinfo("Créditos", mensaje)
    
    def solicitar_datos_dos_fases(self):
        """Solicita el número de restricciones y variables antes de abrir el método de dos fases"""
        ventana_datos = VentanaDatosDosFases(self, self.tipo_optimizacion.get())
        
    def abrir_dos_fases(self,num_restricciones,num_variables):
        """ tipo_optimizacion =self.tipo_optimizacion.get()
        print(f"Abriendo Método Dos fases...{tipo_optimizacion}")
        VentanaDosFases(self,tipo_optimizacion,num_restricciones,num_variables) """
        tipo_optimizacion = self.tipo_optimizacion.get()
        print(f"Abriendo Método Dos fases... {tipo_optimizacion}")
        SimplexApp(self, tipo_optimizacion)

    def solicitar_restricciones(self):
        """Solicita el numero de restricciones antes de abrir el metodo grafico"""
        ventana_restricciones = VentanaRestricciones(self, self.tipo_optimizacion.get())
        
    def abrir_grafico(self,num_restricciones):
        tipo_optimizacion =self.tipo_optimizacion.get()
        print(f"Abriendo Método grafico...{tipo_optimizacion}")
        VentanaGrafico(self,tipo_optimizacion,num_restricciones)

class VentanaDatosDosFases(Toplevel):
    def __init__(self, master, tipo_optimizacion):
        super().__init__(master)
        self.master = master
        self.tipo_optimizacion = tipo_optimizacion
        self.title("Configuración Método Dos Fases")
        self.geometry("450x350")
        self.configure(bg="#ffffff")
        
        # Centrar la ventana
        self.transient(master)
        self.grab_set()
        
        # Contenido de la ventana
        Label(self, text="Método de Dos Fases", font=("Arial", 14, "bold"),bg="#ffffff").pack(pady=10)
        Label(self, text=f"Tipo: {tipo_optimizacion.capitalize()}", font=("Arial", 10),bg="#ffffff").pack(pady=5)
        
        # Frame para número de variables
        frame_variables = Frame(self,bg="#ffffff")
        frame_variables.pack(pady=15)
        
        Label(frame_variables, text="Número de variables:", font=("Arial", 10),bg="#ffffff").pack(anchor='w')
        self.entry_variables = Entry(frame_variables, width=10, font=("Arial", 12), justify="center")
        self.entry_variables.pack(pady=5)
        
        # Frame para número de restricciones
        frame_restricciones = Frame(self,bg="#ffffff")
        frame_restricciones.pack(pady=15)
        
        Label(frame_restricciones, text="Número de restricciones:", font=("Arial", 10),bg="#ffffff").pack(anchor='w')
        self.entry_restricciones = Entry(frame_restricciones, width=10, font=("Arial", 12), justify="center")
        self.entry_restricciones.pack(pady=5)
        
        # Validar que solo se ingresen números
        vcmd = (self.register(self.validar_numero), '%P')
        self.entry_variables.config(validate='key', validatecommand=vcmd)
        self.entry_restricciones.config(validate='key', validatecommand=vcmd)
        
        # Establecer foco en el primer entry
        self.entry_variables.focus()
        
        # Botones
        frame_botones = Frame(self,bg="#ffffff")
        frame_botones.pack(pady=20)
        
        Button(frame_botones, text="Aceptar", command=self.aceptar, 
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Cancelar", command=self.destroy, 
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
        
        # Permitir Enter para aceptar
        self.bind('<Return>', lambda event: self.aceptar())
        
    def validar_numero(self, valor):
        """Valida que solo se ingresen números"""
        if valor == "":
            return True
        try:
            int(valor)
            return True
        except ValueError:
            return False
    
    def aceptar(self):
        """Procesa la entrada del usuario"""
        try:
            num_variables = int(self.entry_variables.get())
            num_restricciones = int(self.entry_restricciones.get())
            
            if num_variables <= 0:
                messagebox.showerror("Error", "El número de variables debe ser mayor que 0")
                return
            if num_restricciones <= 0:
                messagebox.showerror("Error", "El número de restricciones debe ser mayor que 0")
                return
            if num_variables > 20:
                messagebox.showwarning("Advertencia", "Un número muy alto de variables puede hacer complejo el cálculo")
            if num_restricciones > 20:
                messagebox.showwarning("Advertencia", "Un número muy alto de restricciones puede hacer complejo el cálculo")
            
            # Cerrar esta ventana y abrir el método de dos fases
            self.destroy()
            self.master.abrir_dos_fases(num_restricciones, num_variables)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos en ambos campos")


class VentanaRestricciones(Toplevel):
    def __init__(self, master, tipo_optimizacion):
        super().__init__(master)
        self.master = master
        self.tipo_optimizacion = tipo_optimizacion
        self.title("Número de restricciones")
        self.geometry("450x300")
        self.configure(bg="#ffffff")
        
        # Centrar la ventana
        self.transient(master)
        self.grab_set()
        
        # Contenido de la ventana
        Label(self, text="Método Gráfico", font=("Arial", 14, "bold"),bg="#ffffff").pack(pady=10)
        Label(self, text=f"Tipo: {tipo_optimizacion.capitalize()}", font=("Arial", 10),bg="#ffffff").pack(pady=5)
        
        Label(self, text="Ingrese el número de restricciones:", font=("Arial", 10),bg="#ffffff").pack(pady=10)
        
        # Frame para el entry y validación
        frame_entrada = Frame(self,bg="#ffffff")
        frame_entrada.pack(pady=10)
        
        self.entry_restricciones = Entry(frame_entrada, width=10, font=("Arial", 12), justify="center")
        self.entry_restricciones.pack(side=LEFT, padx=5)
        self.entry_restricciones.focus()
        
        # Validar que solo se ingresen números
        vcmd = (self.register(self.validar_numero), '%P')
        self.entry_restricciones.config(validate='key', validatecommand=vcmd)
        
        # Botones
        frame_botones = Frame(self,bg="#ffffff")
        frame_botones.pack(pady=20)
        
        Button(frame_botones, text="Aceptar", command=self.aceptar, 
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Cancelar", command=self.destroy, 
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
        
        # Permitir Enter para aceptar
        self.bind('<Return>', lambda event: self.aceptar())
        
    def validar_numero(self, valor):
        """Valida que solo se ingresen números"""
        if valor == "":
            return True
        try:
            int(valor)
            return True
        except ValueError:
            return False
    
    def aceptar(self):
        """Procesa la entrada del usuario"""
        try:
            num_restricciones = int(self.entry_restricciones.get())
            if num_restricciones <= 0:
                messagebox.showerror("Error", "El número de restricciones debe ser mayor que 0")
                return
            if num_restricciones > 12:
                messagebox.showwarning("Advertencia", "Un número muy alto de restricciones puede hacer complejo el método gráfico")
            
            # Cerrar esta ventana y abrir el método gráfico
            self.destroy()
            self.master.abrir_grafico(num_restricciones)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")

class VentanaGrafico(Toplevel):
    def __init__(self,master=None,tipo_optimizacion="",num_restricciones=0):
        super().__init__(master)
        self.master = master
        self.title(f"Método gráfico - {tipo_optimizacion}")
        self.geometry("600x700")
        self.configure(bg="#ffffff")
        
        # Título y información
        Label(self, text="Método Gráfico", font=("Arial", 14, "bold"),bg="#ffffff").pack(pady=10)
        Label(self, text=f"Tipo: {tipo_optimizacion.capitalize()}", font=("Arial", 10),bg="#ffffff").pack(pady=5)
        Label(self, text=f"Número de restricciones: {num_restricciones}", font=("Arial", 10),bg="#ffffff").pack(pady=5)
        
        # Función objetivo
        Label(self, text="Función objetivo Z:", font=("Arial", 12, "bold"),bg="#ffffff").pack(pady=10)
        
        # Frame para la función objetivo
        frame_z = Frame(self,bg="#ffffff")
        frame_z.pack(pady=5)
        
        Label(frame_z, text="Z = ", font=("Arial", 10),bg="#ffffff").pack(side=LEFT)
        self.z_x1 = Entry(frame_z, width=8, justify="center")
        self.z_x1.pack(side=LEFT, padx=2)
        Label(frame_z, text="x1 + ", font=("Arial", 10),bg="#ffffff").pack(side=LEFT)
        self.z_x2 = Entry(frame_z, width=8, justify="center")
        self.z_x2.pack(side=LEFT, padx=2)
        Label(frame_z, text="x2", font=("Arial", 10),bg="#ffffff").pack(side=LEFT)

        # Restricciones
        Label(self, text="Restricciones:", font=("Arial", 12, "bold"),bg="#ffffff").pack(pady=(15,5))
        
        self.restricciones = []
        for i in range(num_restricciones):
            frame = Frame(self,bg="#ffffff")
            frame.pack(pady=2)

            x1 = Entry(frame, width=5)
            x1.pack(side=LEFT)
            Label(frame, text="x1 + ",bg="#ffffff").pack(side=LEFT)

            x2 = Entry(frame, width=5)
            x2.pack(side=LEFT)
            Label(frame, text="x2",bg="#ffffff").pack(side=LEFT)

            operador = StringVar()
            operador.set("<=")
            menu_operador = OptionMenu(frame, operador, "<=", ">=", "=")
            menu_operador.config(bg="#ffffff", fg="black")
            menu_operador.pack(side=LEFT)

            b = Entry(frame, width=5)
            b.pack(side=LEFT)

            self.restricciones.append((x1, x2, operador, b))

        # Restricciones de no negatividad
        self.r_label = Label(self, text="X1, X2 >= 0",bg="#ffffff")
        self.r_label.pack(pady=5)

        # Botones
        frame_botones = Frame(self,bg="#ffffff")
        frame_botones.pack(pady=20)
        
        Button(frame_botones, text="Resolver", command=self.resolver,
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Cerrar", command=self.destroy,
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
    
    def resolver(self):
        try:
            z1 = float(self.z_x1.get())
            z2 = float(self.z_x2.get())
            restricciones = []
            for x1, x2, op, b in self.restricciones:
                coef_x1 = float(x1.get())
                coef_x2 = float(x2.get())
                operador = op.get()
                lado_derecho = float(b.get())
                restricciones.append((coef_x1, coef_x2, operador, lado_derecho))

            print("Función objetivo: Z =", z1, "x1 +", z2, "x2")
            print("Restricciones:", restricciones)
            
            graficar(z1, z2, restricciones, tipo_optimizacion=self.master.tipo_optimizacion.get())

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos en todos los campos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver:\n{str(e)}")
        
class VentanaDosFases(Toplevel):
    def __init__(self,master=None,tipo_optimizacion="",num_restricciones=0, num_variables=0):
        super().__init__(master)
        self.master = master
        self.tipo_optimizacion = tipo_optimizacion
        self.num_restricciones = num_restricciones
        self.num_variables = num_variables
        
        self.title(f"Método dos fases - {tipo_optimizacion}")
        
        # Ajustar tamaño según el número de variables y restricciones
        altura = min(600 + (num_restricciones * 25) + (num_variables * 5), 800)
        self.geometry(f"700x{altura}")
        self.configure(bg="#ffffff")
        
        # Título
        Label(self, text="Método de Dos Fases", font=("Arial", 14, "bold"),bg="#ffffff").pack(pady=10)
        
        # Información del problema
        info_frame = Frame(self,bg="#ffffff")
        info_frame.pack(pady=5)
        Label(info_frame, text=f"Tipo: {tipo_optimizacion.capitalize()}", font=("Arial", 10),bg="#ffffff").pack(side=LEFT, padx=10)
        Label(info_frame, text=f"Variables: {num_variables}", font=("Arial", 10),bg="#ffffff").pack(side=LEFT, padx=10)
        Label(info_frame, text=f"Restricciones: {num_restricciones}", font=("Arial", 10),bg="#ffffff").pack(side=LEFT, padx=10)
        
        # Función objetivo
        Label(self, text="Función objetivo Z:", font=("Arial", 12, "bold"),bg="#ffffff").pack(pady=10)
        
        # Frame para la función objetivo
        z_frame = Frame(self,bg="#ffffff")
        z_frame.pack(pady=5)
        
        Label(z_frame, text="Z = ", font=("Arial", 10, "bold"),bg="#ffffff").pack(side=LEFT)
        
        # Crear entries para los coeficientes de cada variable
        self.coeficientes_objetivo = []
        for i in range(num_variables):
            if i > 0:
                Label(z_frame, text=" + ", font=("Arial", 10),bg="#ffffff").pack(side=LEFT)
            
            # Entry para el coeficiente
            coef_entry = Entry(z_frame, width=6, justify="center")
            coef_entry.pack(side=LEFT, padx=2)
            coef_entry.insert(0, "0")  # Valor por defecto
            
            # Label para la variable
            Label(z_frame, text=f"x{i+1}", font=("Arial", 10),bg="#ffffff").pack(side=LEFT)
            
            self.coeficientes_objetivo.append(coef_entry)
        
        # Restricciones
        Label(self, text="Restricciones:", font=("Arial", 12, "bold"),bg="#ffffff").pack(pady=(15,5))
        
        self.restricciones = []
        for i in range(num_restricciones):
            frame = Frame(self,bg="#ffffff")
            frame.pack(pady=2)
            
            # Crear entries para cada variable en la restricción
            variables_entries = []
            for j in range(num_variables):
                if j > 0:
                    Label(frame, text=" + ",bg="#ffffff").pack(side=LEFT)
                
                var_entry = Entry(frame, width=5)
                var_entry.pack(side=LEFT)
                var_entry.insert(0, "0")  # Valor por defecto
                
                Label(frame, text=f"x{j+1}",bg="#ffffff").pack(side=LEFT)
                variables_entries.append(var_entry)
            
            # Operador
            operador = StringVar()
            operador.set("<=")
            menu_operador = OptionMenu(frame, operador, "<=", ">=", "=")
            menu_operador.config(bg="#ffffff", fg="black")
            menu_operador.pack(side=LEFT)
            
            # Lado derecho
            b = Entry(frame, width=5)
            b.pack(side=LEFT)
            b.insert(0, "0")  # Valor por defecto
            
            self.restricciones.append((variables_entries, operador, b))

        # Restricciones de no negatividad
        restricciones_text = ", ".join([f"x{i+1}" for i in range(num_variables)])
        self.r_label = Label(self, text=f"{restricciones_text} >= 0",bg="#ffffff")
        self.r_label.pack(pady=5)

        # Botones
        frame_botones = Frame(self,bg="#ffffff")
        frame_botones.pack(pady=20)
        
        Button(frame_botones, text="Resolver", command=self.resolver,
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Cerrar", command=self.destroy,
               bg="#ffffff",fg="black",font=("Arial",11,"bold"),width=16,height=2).pack(side=LEFT, padx=5)
        
    def resolver(self):
        try:
            # Obtener coeficientes de la función objetivo
            coeficientes_z = []
            for entry in self.coeficientes_objetivo:
                coeficientes_z.append(float(entry.get()))
            
            # Obtener restricciones
            restricciones = []
            for variables_entries, operador, b in self.restricciones:
                coeficientes = []
                for entry in variables_entries:
                    coeficientes.append(float(entry.get()))
                
                restricciones.append((coeficientes, operador.get(), float(b.get())))
            
            print("Función objetivo Z =", coeficientes_z)
            print("Restricciones:", restricciones)
            
            # Aquí puedes agregar la lógica para resolver por el método de dos fases
            messagebox.showinfo("Método de Dos Fases", 
                              "Datos capturados correctamente.\nImplementar lógica de resolución.")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos en todos los campos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver:\n{str(e)}")
        
def main():
    app= VentanaPrincipal()
    app.mainloop()

# if __name__=="__main__":
main()
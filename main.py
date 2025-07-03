from tkinter import *
from tkinter import messagebox
from grafico import graficar


class VentanaPrincipal(Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto investigación de operaciones")
        self.geometry("400x400")

        self.tipo_optimizacion = StringVar(value="")
        # Etiqueta
        self.label_titulo = Label(self, text="Proyecto ingestigación de operaciones",font=("Arial",12,"bold"))
        self.label_titulo.pack(pady=10)

        #Frame para seleccionar si es maxximizacion o minimizacion
        self.frame_optimizacion = Frame(self)
        self.frame_optimizacion.pack(pady=10)
        
        self.label_opt =Label(self.frame_optimizacion, text="Seleccione el tipo de optimización:",font=("Arial", 10))
        self.label_opt.pack(pady=5)
        
        # Radiobuttons para seleccionar tipo de optimización
        self.radio_max = Radiobutton(self.frame_optimizacion, text="Maximización",variable=self.tipo_optimizacion, value="maximizacion",command=self.actualizar_botones)
        self.radio_max.pack(pady=2)
        
        self.radio_min = Radiobutton(self.frame_optimizacion, text="Minimización",variable=self.tipo_optimizacion, value="minimizacion",command=self.actualizar_botones)
        self.radio_min.pack(pady=2)
        
        self.frmae_metodos= Frame(self)
        self.frmae_metodos.pack(pady=10)
        
        # Etiqueta
        self.label1 = Label(self, text="Selccione la opción que desea:")
        self.label1.pack(pady=5)
        
        # Boton
        self.button_dos_fases = Button(self, text="Metodo de dos fases", command=self.abrir_dos_fases,state="disabled")
        self.button_dos_fases.pack(pady=5)

        self.button_grafico = Button(self, text="Metodo gráfico", command=self.solicitar_restricciones,state="disabled")
        self.button_grafico.pack(pady=5)

        self.button_credtios = Button(self, text="Creditos", command=self.creditos)
        self.button_credtios.pack(pady=5)
        
        # Etiqueta para mostrar resultado
        self.credito = Label(self, text="")
        self.credito.pack(pady=10)
        
    def actualizar_botones(self):
        """Habilita los botones de los metodos cuando se eslecciona el tipo de optimizacion"""
        if self.tipo_optimizacion.get():
            self.button_dos_fases.config(state='normal')
            self.button_grafico.config(state='normal')
            # Limpiar créditos si están mostrados
            self.credito.config(text="")
        
    def creditos(self):
        self.credito.config(text=f"Aplicación realizada por: \nDonghe Do\nCrithian Prieto\nDavid Guaba\nDaniel Bustamante")
    
    def abrir_dos_fases(self):
        tipo_optimizacion =self.tipo_optimizacion.get()
        print(f"Abriendo Método Dos fases...{tipo_optimizacion}")
        VentanaDosFases(self,tipo_optimizacion)

    def solicitar_restricciones(self):
        """Solicita el numero de restricciones antes de abrir el metodo grafico"""
        ventana_restricciones = VentanaRestricciones(self, self.tipo_optimizacion.get())
        
    def abrir_grafico(self,num_restricciones):
        tipo_optimizacion =self.tipo_optimizacion.get()
        print(f"Abriendo Método grafico...{tipo_optimizacion}")
        VentanaGrafico(self,tipo_optimizacion,num_restricciones)

class VentanaRestricciones(Toplevel):
    def __init__(self, master, tipo_optimizacion):
        super().__init__(master)
        self.master = master
        self.tipo_optimizacion = tipo_optimizacion
        self.title("Número de restricciones")
        self.geometry("450x300")
        
        # Centrar la ventana
        self.transient(master)
        self.grab_set()
        
        # Contenido de la ventana
        Label(self, text="Método Gráfico", font=("Arial", 14, "bold")).pack(pady=10)
        Label(self, text=f"Tipo: {tipo_optimizacion.capitalize()}", font=("Arial", 10)).pack(pady=5)
        
        Label(self, text="Ingrese el número de restricciones:", font=("Arial", 10)).pack(pady=10)
        
        # Frame para el entry y validación
        frame_entrada = Frame(self)
        frame_entrada.pack(pady=10)
        
        self.entry_restricciones = Entry(frame_entrada, width=10, font=("Arial", 12), justify="center")
        self.entry_restricciones.pack(side=LEFT, padx=5)
        self.entry_restricciones.focus()
        
        # Validar que solo se ingresen números
        vcmd = (self.register(self.validar_numero), '%P')
        self.entry_restricciones.config(validate='key', validatecommand=vcmd)
        
        # Botones
        frame_botones = Frame(self)
        frame_botones.pack(pady=20)
        
        Button(frame_botones, text="Aceptar", command=self.aceptar, 
               width=10).pack(side=LEFT, padx=5)
        Button(frame_botones, text="Cancelar", command=self.destroy, 
               width=10).pack(side=LEFT, padx=5)
        
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
            if num_restricciones > 10:
                messagebox.showwarning("Advertencia", "Un número muy alto de restricciones puede hacer complejo el método gráfico")
            
            # Cerrar esta ventana y abrir el método gráfico
            self.destroy()
            self.master.abrir_grafico(num_restricciones)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")

class VentanaGrafico(Toplevel):
    def __init__(self,master=None,tipo_optimizacion="",num_restricciones=0):
        super().__init__(master)
        self.title(f"Metodo grafico -{tipo_optimizacion}")
        self.geometry("600x600")
        
        
        Label(self, text="Interfaz del Método Gráfico").pack(pady=10)
        Label(self, text=f"Tipo: {tipo_optimizacion}").pack(pady=5)
        Label(self, text=f"Número de restricciones: {num_restricciones}").pack(pady=5)
        #Z es la funcion objetivo
        Label(self, text="Función objetivo Z:").pack(pady=5)
        #Datos de la funcion objetivo
        frame_z = Frame(self)
        frame_z.pack()
        self.z_x1 = Entry(frame_z, width=5)
        self.z_x1.pack(side=LEFT)
        Label(frame_z, text="x1 + ").pack(side=LEFT)
        self.z_x2 = Entry(frame_z, width=5)
        self.z_x2.pack(side=LEFT)
        Label(frame_z, text="x2").pack(side=LEFT)

        Label(self, text="Restricciones:").pack(pady=10)
        self.restricciones = []

        for i in range(num_restricciones):
            frame = Frame(self)
            frame.pack(pady=2)

            x1 = Entry(frame, width=5)
            x1.pack(side=LEFT)
            Label(frame, text="x1 + ").pack(side=LEFT)

            x2 = Entry(frame, width=5)
            x2.pack(side=LEFT)
            Label(frame, text="x2").pack(side=LEFT)

            operador = StringVar()
            operador.set("<=")
            OptionMenu(frame, operador, "<=", ">=", "=").pack(side=LEFT)

            b = Entry(frame, width=5)
            b.pack(side=LEFT)

            self.restricciones.append((x1, x2, operador, b))

        self.r_label = Label(self, text="X1, X2 >= 0")
        self.r_label.pack(pady=5)

        Button(self, text="Resolver", command=self.resolver).pack(pady=10)
        Button(self, text="Cerrar", command=self.destroy).pack(pady=5)
    
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

            graficar(z1, z2, restricciones, tipo_optimizacion=self.master.tipo_optimizacion.get())

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Verifica los campos ingresados.\n\n{str(e)}")
        print("Resolver")
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
        
class VentanaDosFases(Toplevel):
    def __init__(self,master=None,tipo_optimizacion=""):
        super().__init__(master)
        self.title(f"Metodo dos fases -{tipo_optimizacion}")
        self.geometry("450x350")
        
        Label(self, text="Interfaz del Método de Dos Fases").pack(pady=20)
        Button(self, text="Cerrar esta ventana", command=self.destroy).pack(pady=10)
        
def main():
    app= VentanaPrincipal()
    app.mainloop()

# if __name__=="__main__":
main()
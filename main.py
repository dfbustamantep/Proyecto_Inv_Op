from tkinter import *

class Ventana(Tk):
    def __init__(self):
        super().__init__()
        
def main():
    app= Ventana()
    app.title("Proyecto fianl investigación de operaciones")
    app.state("zoomed")
    app.mainloop()

if __name__=="__main__":
    main()
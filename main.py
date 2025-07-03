from tkinter import *

class Ventana(Tk):
    def __init__(self):
        super().__init__()
        self.title("입력 예제")
        self.geometry("400x200")

        # 라벨
        self.label = Label(self, text="이름을 입력하세요:")
        self.label.pack(pady=10)

        # 입력창
        self.entry = Entry(self)
        self.entry.pack(pady=5)

        # 버튼
        self.button = Button(self, text="확인", command=self.mostrar_nombre)
        self.button.pack(pady=5)

        # 결과 표시 라벨
        self.resultado = Label(self, text="")
        self.resultado.pack(pady=10)

    def mostrar_nombre(self):
        nombre = self.entry.get()
        self.resultado.config(text=f"안녕하세요, {nombre}님!")
        
def main():
    app= Ventana()
    app.mainloop()

# if __name__=="__main__":
main()
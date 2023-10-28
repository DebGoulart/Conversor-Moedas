from tkinter import * 

window = Tk()
window.title("Cotação Atual das Moedas")

inicial_text = Label(window, text="Clique no botão para ver as cotações")
inicial_text.grid(column=0, row=0)

button = Button = Label(window, text="Buscar Cotações")
button.grid(column=0, row=1)


window.mainloop()
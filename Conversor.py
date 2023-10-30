import requests
from datetime import datetime
from tkinter import *
from tkinter import ttk

# Função para obter cotações
def cotacoes():
    request = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL,JPY-BRL,CAD-BRL,AUD-BRL")

    data = request.json()

    cotacoes = {}

    for moeda in ['USD', 'CAD', 'AUD', 'EUR', 'GBP', 'JPY']:
        if f'{moeda}BRL' in data:
            cotacao = data[f'{moeda}BRL']
            compra = float(cotacao['bid'])
            venda = float(cotacao['ask'])
            variacao = float(cotacao['varBid'])
            maximo = float(cotacao['high'])
            minimo = float(cotacao['low'])

            if maximo != 0:
                porcentagem_variacao = (variacao / maximo) * 100
            else:
                porcentagem_variacao = 0.0

            cotacoes[moeda] = {
                'compra': compra,
                'venda': venda,
                'variacao': variacao,
                'porcentagem_variacao': porcentagem_variacao,
                'maximo': maximo,
                'minimo': minimo,
            }

    return cotacoes

# Função para converter moedas
def converter_moedas(valor, moeda_origem, moeda_destino, cotacoes):
    if moeda_origem in cotacoes and moeda_destino in cotacoes:
        taxa_origem = cotacoes[moeda_origem]['compra']
        taxa_destino = cotacoes[moeda_destino]['venda']
        valor_convertido = valor / taxa_origem * taxa_destino
        return valor_convertido
    else:
        return None

# Função para abrir janela de aviso
def abrir_janela_aviso():
    aviso = Toplevel()
    aviso.title("Aviso")
    
    aviso_label = Label(aviso, text="A moeda Real (BRL) ainda não está disponível no programa.\nAguarde as próximas atualizações")
    aviso_label.pack(padx=20, pady=20)
    
    ok_button = Button(aviso, text="OK", command=aviso.destroy)
    ok_button.pack(pady=10)

    aviso.geometry("400x150+400+300")

# Função para atualizar a tabela de cotações
def atualizar_tabela(cotacoes_atualizadas):
    for moeda, cotacao in cotacoes_atualizadas.items():
        compra = cotacao['compra']
        venda = cotacao['venda']
        variacao = cotacao['variacao']
        porcentagem_variacao = cotacao['porcentagem_variacao']
        maximo = cotacao['maximo']
        minimo = cotacao['minimo']

        treeview.insert(
            "", "end",
            values=(moeda, f"{compra:.2f}", f"{venda:.2f}", f"{variacao:.2f}", f"{porcentagem_variacao:.2f}%", f"{maximo:.2f}", f"{minimo:.2f}")
        )

# Função para atualizar as cotações
def atualizar_cotacoes():
    cotacao_label.config(text=f"Cotação Atualizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    cotacoes_atualizadas = cotacoes()
    treeview.delete(*treeview.get_children())
    if cotacoes_atualizadas:
        atualizar_tabela(cotacoes_atualizadas)
    else:
        resultado_label.config(text="Erro ao obter cotações")
    root.after(15000, atualizar_cotacoes)

# Função para calcular conversão
def calcular_conversao():
    valor = float(valor_entry.get())
    moeda_origem = moeda_origem_var.get()
    moeda_destino = moeda_destino_var.get()
    valor_convertido = converter_moedas(valor, moeda_origem, moeda_destino, cotacoes())
    if valor_convertido is not None:
        resultado_label.config(text=f"{valor:.2f} {moeda_origem} = {valor_convertido:.2f} {moeda_destino}")
    else:
        resultado_label.config(text="Moedas inválidas")

# Interface gráfica
root = Tk()
root.title("Conversor de Moedas")

largura_maxima = 1400

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela - largura_maxima) // 2
y = (altura_tela - 800) // 2

frame = Frame(root)
frame.pack()

root.geometry(f"{largura_maxima}x400+{x}+{y}")

moedas = ['USD', 'CAD', 'AUD', 'EUR', 'GBP', 'JPY']

frame_entrada = Frame(root)
frame_entrada.pack()

valor_label = Label(frame, text="Valor:")
valor_label.pack(side=LEFT)

valor_entry = Entry(frame)
valor_entry.pack(side=LEFT)

moeda_origem_label = Label(frame, text="Moeda de Origem:")
moeda_origem_label.pack(side=LEFT)

moeda_origem_var = StringVar(value='USD')
moeda_origem_menu = OptionMenu(frame, moeda_origem_var, 'USD', 'CAD', 'AUD', 'EUR', 'GBP', 'JPY')
moeda_origem_menu.pack(side=LEFT)

moeda_destino_label = Label(frame, text="Moeda de Destino:")
moeda_destino_label.pack(side=LEFT)

moeda_destino_var = StringVar(value='EUR')
moeda_destino_menu = OptionMenu(frame, moeda_destino_var, 'USD', 'CAD', 'AUD', 'EUR', 'GBP', 'JPY')
moeda_destino_menu.pack(side=LEFT)

converter_button = Button(frame, text="Converter", command=calcular_conversao)
converter_button.pack(side=LEFT)

resultado_label = Label(root, text="")
resultado_label.pack()

cotacao_label = Label(root, text="")
cotacao_label.pack()

treeview = ttk.Treeview(root, columns=("Moeda", "Compra", "Venda", "Variação", "Variação (%)", "Máximo", "Mínimo"), show="headings")
treeview.heading("Moeda", text="Moeda")
treeview.heading("Compra", text="Compra")
treeview.heading("Venda", text="Venda")
treeview.heading("Variação", text="Variação")
treeview.heading("Variação (%)", text="Variação (%)")
treeview.heading("Máximo", text="Máximo")
treeview.heading("Mínimo", text="Mínimo")
treeview.pack()

abrir_janela_aviso()

atualizar_cotacoes()

root.mainloop()

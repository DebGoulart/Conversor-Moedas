import requests
from datetime import datetime
import time as t
from tkinter import *
from tkinter import ttk 

def cotacoes():
    request = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL,GBP-BRL,JPY-BRL,CAD-BRL,AUD-BRL")
    data = request.json()
    
    cotacao_dolarAm = float(data['USDBRL']['bid'])
    cotacao_dolarCan = float(data['CADBRL']['bid'])
    cotacao_dolarAus = float(data['AUDBRL']['bid'])
    cotacao_euro = float(data['EURBRL']['bid'])
    cotacao_libra = float(data['GBPBRL']['bid'])
    cotacao_iene = float(data['JPYBRL']['bid'])
    cotacao_bitcoin = float(data['BTCBRL']['bid'])
    
    return {
        'USD': cotacao_dolarAm,
        'CAD': cotacao_dolarCan,
        'AUD': cotacao_dolarAus,
        'EUR': cotacao_euro,
        'GBP': cotacao_libra,
        'JPY': cotacao_iene,
        'BTC': cotacao_bitcoin,
        'BRL': 1.0
    }

def atualizar_tabela(cotacoes_atualizadas):
    for moeda, cotacao in cotacoes_atualizadas.items():
        treeview.insert("", "end", values=(moeda, f"{cotacao:.2f}"))

def converter_moedas(valor, moeda_origem, moeda_destino, cotacoes):
    if moeda_origem in cotacoes and moeda_destino in cotacoes:
        taxa_origem = cotacoes[moeda_origem]
        taxa_destino = cotacoes[moeda_destino]
        valor_convertido = valor * (1 / taxa_origem) * taxa_destino
        return valor_convertido
    else:
        return None

def atualizar_cotacoes():
    cotacao_label.config(text=f"Cotação Atualizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    cotacoes_atualizadas = cotacoes()
    converter_button['state'] = 'normal'
    treeview.delete(*treeview.get_children())
    if cotacoes_atualizadas:
        atualizar_tabela(cotacoes_atualizadas)
    else:
        resultado_label.config(text="Erro ao obter cotações")

def calcular_conversao():
    valor = float(valor_entry.get())
    moeda_origem = moeda_origem_var.get()
    moeda_destino = moeda_destino_var.get()
    cotacoes_atualizadas = atualizar_cotacoes()
    
    if cotacoes_atualizadas:
        valor_convertido = converter_moedas(valor, moeda_origem, moeda_destino, cotacoes_atualizadas)
        if valor_convertido is not None:
            resultado_label.config(text=f"{valor:.2f} {moeda_origem} = {valor_convertido:.2f} {moeda_destino}")
        else:
            resultado_label.config(text="Moedas inválidas")
    else:
        resultado_label.config(text="Erro ao obter cotações")

root = Tk()
root.title("Conversor de Moedas")

moedas = ['USD', 'CAD', 'AUD', 'EUR', 'GBP', 'JPY', 'BTC', 'BRL']

valor_label = Label(root, text="Valor:")
valor_label.pack()

valor_entry = Entry(root)
valor_entry.pack()

moeda_origem_label = Label(root, text="Moeda de Origem:")
moeda_origem_label.pack()

moeda_origem_var = StringVar(value=moedas[0])
moeda_origem_menu = OptionMenu(root, moeda_origem_var, *moedas)
moeda_origem_menu.pack()

moeda_destino_label = Label(root, text="Moeda de Destino:")
moeda_destino_label.pack()

moeda_destino_var = StringVar(value=moedas[1])
moeda_destino_menu = OptionMenu(root, moeda_destino_var, *moedas)
moeda_destino_menu.pack()

converter_button = Button(root, text="Converter", command=calcular_conversao)
converter_button.pack()

resultado_label = Label(root, text="")
resultado_label.pack()

cotacao_label = Label(root, text="")
cotacao_label.pack()

treeview = ttk.Treeview(root, columns=("Moeda", "Cotação"), show="headings")
treeview.heading("Moeda", text="Moeda")
treeview.heading("Cotação", text="Cotação")
treeview.pack()

atualizar_cotacoes()

root.mainloop()

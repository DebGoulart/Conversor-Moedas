import requests
from datetime import datetime
import time as t
from tkinter import *


def cotacoes():
    request = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL,GBP-BRL,JPY-BRL,CAD-BRL,AUD-BRL")

    data = request.json()

    cotacao_dolarAm = data['USDBRL']['bid']
    cotacao_dolarCan = data['CADBRL']['bid']
    cotacao_dolarAus = data['AUDBRL']['bid']
    cotacao_euro = data['EURBRL']['bid']
    cotacao_libra = data['GBPBRL']['bid']
    cotacao_iene = data['JPYBRL']['bid']
    cotacao_bitcoin = data['BTCBRL']['bid']

    print(f"Cotação Dólar Americano (USD): {cotacao_dolarAm}")
    print(f"Cotação Dólar Canadense (CAD): {cotacao_dolarCan}")
    print(f"Cotação Dólar Australiano (AUD): {cotacao_dolarAus}")
    print(f"Cotação Euro (EUR): {cotacao_euro}")
    print(f"Cotação Libra Esterlina (GBP): {cotacao_libra}")
    print(f"Cotação Iene Japonês (JPY): {cotacao_iene}")
    print(f"Cotação Bitcoin (BTC): {cotacao_bitcoin}")
    print(f"Cotação Atualizada. {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

while True:
    cotacoes()
    t.sleep(30)


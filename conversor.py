import requests

def obter_cambio():
    url = " "

    response = requests.get(url)
    data = response.json()
    return data['rates']

def converter_cambios(valor, moeda1, moeda2, taxa):
    if moeda1 in taxa and moeda2 in taxa:
        taxa1 = taxa[moeda1]
        taxa2 = taxa[moeda2]

        valor_dolar = valor / taxa1
        valor_convertido = valor_dolar * taxa2

        return valor_convertido
    else:
        print("Erro! Não consegui obter a taxa de câmbio.")

        return None
    
taxa_cambio = obter_cambio()
valor = float(input('Digite o valor a ser convertido: '))
moeda1 = input('Digite a moeda de origem: ').upper() 
moeda2 = input('Digite a moeda que será convertida: ').upper()

valor_convertido = converter_cambios(
    valor, moeda1, moeda2, taxa_cambio)

if valor_convertido is not None:
    print(f'\n{valor:.2f} {moeda1} é equivalente a {valor_convertido:.2f} {moeda2}')
else:
    print('Moedas inválidas')
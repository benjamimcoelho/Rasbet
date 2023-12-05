import requests
from apostas.models import Cambio,Utilizador

def requestCambio(tipo):
    ret = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + tipo)
    if ret.status_code == 200:
        return ret.json()['price']
    else:
        raise 

def checkCambio():
    matrix = dict()
    for moeda in Utilizador.getMetodosPagamento():
        lista = dict()
        for m in Utilizador.getMetodosPagamento():
            if m != moeda:
                lista[m] = None
        matrix[moeda] = lista

    def newCambio(moeda_origem,moeda_destino,string):
        rate = float(requestCambio(string))
        matrix[moeda_origem][moeda_destino] = rate
        matrix[moeda_destino][moeda_origem] = 1/rate
        Cambio.update_taxa_cambio(moeda_origem,moeda_destino,rate)
    
    def recursive(moeda_origem,moeda_destino):
        calc = 1.0
        # elemento da matrix que é do tipo matriz[*][moeda_destino] xx pertence a *
        for xx in [x[0] for x in matrix.items() for y in x[1].items()  if y[0] == moeda_destino if y[1] != None]:
            ## verifica se faz parte de matriz[moeda_origem][*]
            if xx in [x[0] for x in matrix[moeda_origem].items() if x[1] != None]:
                calc = calc * matrix[moeda_origem][xx] * matrix[xx][moeda_destino]
                matrix[moeda_origem][moeda_destino] = calc
                matrix[moeda_destino][moeda_origem] = 1/calc
                Cambio.update_taxa_cambio(moeda_origem,moeda_destino,calc)
                return calc
        #senao fizer parte ver de matriz[moeda_origem][xx]
        for xx in [x[0] for x in matrix.items() for y in x[1].items()  if y[0] == moeda_destino if y[1] != None]:
            a = recursive(moeda_origem,xx)
            if a != 0:
                calc = a * matrix[xx][moeda_destino]
                matrix[moeda_origem][moeda_destino] = calc
                matrix[moeda_destino][moeda_origem] = 1/calc
                Cambio.update_taxa_cambio(moeda_origem,moeda_destino,calc)
                return calc
        return 0

    try:
        newCambio("Euro","Dolar","EURUSDT")
        newCambio("Bitcoin","Dolar","BTCUSDT")
        newCambio("Dogecoin","Bitcoin","DOGEBTC")
        newCambio("Libra","Dolar","GBPUSDT")
        newCambio("Cardano","Dolar","ADAUSDT")

        for moeda_origem,lista in matrix.items():
            for moeda_destino,rate in lista.items():
                if rate == None:
                    recursive(moeda_origem,moeda_destino)
    except:
        print("Couldn't get Cambio")
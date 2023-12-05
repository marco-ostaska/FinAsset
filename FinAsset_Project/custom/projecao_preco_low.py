#Importando as bibliotecas necessárias
from tqdm import tqdm
from custom import projecaoAtivosLib


def forecast(ativo):
    dias_projecao = 3

    forecast = ativo.forecast(dias_projecao, 10)

    projetado = round(forecast.mean(), 2)
    minimo = round(forecast.min(), 2)

    return {
        "ativo": ativo.ticker,
        "fechamento": round(ativo.historico[-1], 2),
        "projecao": f"R$ {minimo} - R$ {projetado}"
    }


def gerar_lista_ativos(ativos,anos_historico):
    return [projecaoAtivosLib.Ativo(a, anos_historico, "Low") for a in ativos]

def retorna(tickers):
    ativos = [t.upper() for t in tickers]
    anos_historico=5
    lista_ativos = gerar_lista_ativos(ativos,anos_historico)

    results = []
    for ativo in lista_ativos:
        try:
            print("Processando atvo:", ativo.ticker)
            print(forecast(ativo))
            results.append(forecast(ativo))
        except:
            pass

    return results


# Função principal
def main():
    ativos = input("Entre os ativos separado por virgula: ")
    ativos = [a.strip() for  a in ativos.split(",")]
    anos_historico=5
    lista_ativos = gerar_lista_ativos(ativos,anos_historico)

    results = []
    for ativo in lista_ativos:
        try:
            results.append(forecast(ativo))
        except:
            pass

    print(results)


# Iniciando o programa
if __name__ == "__main__":
    main()

#Importando as bibliotecas necessárias
from tqdm import tqdm
from custom import projecaoAtivosLib


def print_cabecalho(ativo):
    print("-----------------------------------------------------------------------------")
    print(f"{ativo.ticker.upper()} - Preço fechamento: R$ {round(ativo.historico[-1],2)}")
    print("-----------------------------------------------------------------------------")

def print_cabecalho_projecao(i, dias_projecao):
    if i == dias_projecao[-2]:
        print("Projeção até final do ano")
    elif i== dias_projecao[-1]:
        print("Projeção em cinco anos")
    else:
        print(f"Projeção para os proximos {i} dias")


# Função para exibir a Projeção
def print_forecast(ativo):
    dias_projecao=[7,30,90,projecaoAtivosLib.dias_ate_final_ano(), 5*365]
    print_cabecalho(ativo)

    for dp in dias_projecao:
        print_cabecalho_projecao(dp, dias_projecao)

        forecast=ativo.forecast(dp, 10)
        maximo = round(forecast.max(),2)
        maximo_pct = round(((maximo - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        projetado = round(forecast.mean(),2)
        projetado_pct = round(((projetado - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        minimo= round(forecast.min(),2)
        minimo_pct = round(((minimo - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        print(f"Preço Otimista     : R$ {maximo} ({maximo_pct}%)")
        print(f"Preço Projetado    : R$ {projetado} ({projetado_pct}%)")
        print(f"Preço Pessimista   : R$ {minimo} ({minimo_pct}%)")
        print()


def forecast(ativo):
    dias_projecao = [7, 30, 90, projecaoAtivosLib.dias_ate_final_ano(), 5 * 365]

    dias_projecao_resultado = []

    for dp in dias_projecao:
        forecast = ativo.forecast(dp, 10)
        maximo = round(forecast.max(), 2)
        maximo_pct = round(((maximo - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        projetado = round(forecast.mean(), 2)
        projetado_pct = round(((projetado - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        minimo = round(forecast.min(), 2)
        minimo_pct = round(((minimo - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        dias_projecao_resultado.append({
            "ativo": ativo.ticker,
            "dias": dp,
            "fechamento": round(ativo.historico[-1],2),
            "projecoes": {
                "otimista": {"valor": maximo, "percentual": maximo_pct},
                "projetado": {"valor": projetado, "percentual": projetado_pct},
                "pessimista": {"valor": minimo, "percentual": minimo_pct}
            }
        })

    return dias_projecao_resultado



def gerar_lista_ativos(ativos,anos_historico):
    lista_ativos = []

    for a in ativos:
        lista_ativos.append(projecaoAtivosLib.Ativo(a, anos_historico))

    return lista_ativos

def retorna(tickers):
    ativos = [t.upper() for t in tickers]
    anos_historico=5
    lista_ativos = gerar_lista_ativos(ativos,anos_historico)

    results = []
    for ativo in lista_ativos:
        try:
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


    for ativo in lista_ativos:

        print_forecast(ativo)



# Iniciando o programa
if __name__ == "__main__":
    main()

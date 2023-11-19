from matplotlib.pyplot import tick_params
from custom import bancoCentral, fundamentusData, investidor10
from tabulate import tabulate

def taxa_livre_risco():
    selic = bancoCentral.SELIC(5)
    ipca = bancoCentral.IPCA(5)

    if ipca.media_ganho_real() > selic.media_anual():
        return ipca.media_ganho_real()

    return selic.media_anual()


def get_tickers(tickers):
    return [t.upper().strip() for t in tickers]



def process_acoes(ticker, free_risk):
    ativo = fundamentusData.Acao(ticker)
    df = [
        ["Cotação",f"R$ {ativo.cotacao}"],
        ["P/L", f"{ativo.pl}"],
        ["P/VP", f"{ativo.pvp}"],
        ["DY", f"{ativo.div_yield}%"],
        ["Teto", f"R$ {ativo.graham}"],
        ["Teto Div", f"R$ {ativo.bazin(free_risk)}"]

        ]

    print()
    print(tabulate(df, headers=[ativo.ticker, "Valores"], tablefmt='simple'))

    desconto = round(((ativo.cotacao-ativo.graham)/ativo.graham)*100,2) if ativo.graham < 0 else round(((ativo.graham-ativo.cotacao)/ativo.graham)*100,2)

    return {
            'ticker': ativo.ticker,
            'desconto': desconto,
            'df': df
        }



def process_fi_infra(ticker, free_risk):
    ativo = investidor10.FI_INFRA(ticker)
    df = [
        ["Cotação", f"R$ {ativo.cotacao}"],
        ["P/VP", f"{ativo.pvp}"],
        ["DY", f"{ativo.div_yield}%"],
        ["Teto", f"R$ {ativo.graham}"],
        ["Teto Div", f"R$ {ativo.bazin(free_risk)}"]

    ]

    return {
            'ticker': ativo.ticker,
            'desconto': round((1-ativo.pvp)*100,2),
            'df': df
        }

def process_ticker(t, risk_free, function):
    try:
        return function(t, risk_free)
    except Exception as e:
        print()
        print("Error Processing ticker:", t)
        return None
    
def retorna(tipo, tickers):
    tickers = [t.upper() for t in tickers]
    risk_free = taxa_livre_risco()
    results = []
    
    functions_map = {
        "1": process_acoes,
        "2": process_fi_infra
        }

    for t in tickers:
        process_function = process_function = functions_map.get(tipo)
        result = process_ticker(t, risk_free, process_function)
        if result: results.append(result) 

    print()
    print("----------------------------------------")
    print("Ordenados por desconto")
    print("----------------------------------------")

    return results
    
#   # Ordena os resultados pelo desconto Bazin
    sorted_results = sorted(results, key=lambda x: x['desconto'],reverse=True)

#     # Agora imprime os ativos ordenados
    for result in sorted_results:
        print(f"Ticker: {result['ticker']} | {result['desconto']}%")


    

def main():
    retorna("process_fi_infra", ['hsml11'])




if __name__ == "__main__":
    main()

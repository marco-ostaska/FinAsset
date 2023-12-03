# Importando as bibliotecas necessárias
import numpy as np
from tqdm import tqdm
from pathlib import Path
from custom import projecaoAtivosLib


def calcula_projetado(ativo,dias):
    forecast= ativo.forecast(dias,10)
    projetado = round(forecast.mean(),2)
    projetado_pct = round(((projetado - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

    return projetado_pct

def print_melhores(retornos):
    rtn = []
    #Ordena a lista retornos baseado no retorno_anual_estimado (decrescente)
    retornos_ordenados = sorted(retornos, key=lambda x: x[1] if x[1] is not None else -np.inf, reverse=True)
    # Pega os 10 primeiros ou todos se tiver menos de 10
    top_10_retornos = retornos_ordenados[:10]

    for ticker, retorno in top_10_retornos:
        if retorno is not None:
            print(f"{ticker}: {retorno:.2f}%")


    return top_10_retornos

    print()

def print_cabecalho(i, dias_previsoes):
    print("------------------------------------------------------------------")
    if i == dias_previsoes[-2]:
        print("Ativos com melhores projeção até final do ano")
    elif i == dias_previsoes[-1]:
        print("Ativos com melhores projeção para 5 anos")
    else:
        print(f"melhores projeção para os proximos {i} dias")
    print("------------------------------------------------------------------")


def ler_tickers(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            # Lê as linhas, retira os espaços em branco e adiciona à lista
            tickers = [linha.strip() for linha in arquivo.readlines()]
        return tickers
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None



def gerar_lista_ativos(ativos,anos_historico):
    lista_ativos = []
    pbar = tqdm(ativos)

    for a in pbar:
        pbar.set_description(f"Coletando dados para: {a}")
        lista_ativos.append(projecaoAtivosLib.Ativo(a, anos_historico))

    return lista_ativos




def get_sel(selecao):
    selecao = int(selecao)
    print("achando arquivo correspondente para:", selecao)
    base_dir = Path(__file__).resolve().parent
    
    paths = {
        1: base_dir / "etc" / "ibov.txt",
        2: base_dir / "etc" / "idiv.txt",
        3: base_dir / "etc" / "small.txt",
        4: base_dir / "etc" / "ifix.txt",
        5: base_dir / "etc" / "ibrx50.txt",
        6: base_dir / "etc" / "ibrx100.txt",
        7: base_dir / "etc" / "setores" / "saneamento.txt",
        8: base_dir / "etc" / "setores" / "eletricas.txt",
        9: base_dir / "etc" / "setores" / "bancos.txt",
        10: base_dir / "etc" / "setores" / "seguros.txt",
        11: base_dir / "etc" / "setores" / "saude.txt",
        11: base_dir / "etc" / "valor.txt",
    }

    print("basedir",base_dir, paths[selecao] )

    print(paths[selecao])
    return paths[selecao]

def retorna(opt):

    print(get_sel(opt))
    ativos = ler_tickers(get_sel(opt))
    anos_historico = 5
    dias_previsoes = [7, 30, 90, projecaoAtivosLib.dias_ate_final_ano(), 5*365]

    lista_ativos = gerar_lista_ativos(ativos,anos_historico)
    ret = {}
    c = 0
    for dp in dias_previsoes:
        c += 1
        print_cabecalho(dp, dias_previsoes)

        retornos = [
            (ativo.ticker, calcula_projetado(ativo, dp))
            for ativo in lista_ativos
        ]
        rtrn = print_melhores(retornos)
        for r in rtrn:
            print(r)

        if c == 4:
            chave = "Até final do ano"
        elif c == 5:
            chave = "para os próximos 5 Anos"
        else:
            chave = f"para os próximos {dp} Dias"

        if chave not in ret:
            ret[chave] = []

        for r in rtrn:
            ret[chave].append({"ticker": r[0], "pct": r[1]})


    return ret



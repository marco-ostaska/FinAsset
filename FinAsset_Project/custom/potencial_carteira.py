from custom import bancoCentral
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from tabulate import tabulate

class Carteira:
    ANO_DIAS_UTEIS = 252
    retorno = []
    peso_ativos = []
    volatilidade = []
    volatilidade_ajustada = []
    sharpe_ratio = []
    sortino_ratio = []

    def __init__(self, data, selic):
        self.data = data
        self.numero_ativos = len(data.columns)
        self.selic = selic/100

    def retorno_diario(self):
        return self.data.pct_change().dropna()
    
    def retorno_anual(self):
        return self.retorno_diario().mean() * self.ANO_DIAS_UTEIS


    def cov_anual(self):
        retorno_diario = self.retorno_diario()
        cov_diaria = retorno_diario.cov()
        return cov_diaria * self.ANO_DIAS_UTEIS

    def semi_cov_anual(self):
        retorno_diario = self.retorno_diario()
        rd = retorno_diario[retorno_diario < 0]
        cov_diaria_neg = rd.cov()
        return  cov_diaria_neg * self.ANO_DIAS_UTEIS

    def get_pesos(self, numero_ativos):
        pesos = np.random.random(numero_ativos)
        pesos /= np.sum(pesos)
        return pesos

    def retorno_portfolio(self, pesos):
        return np.dot(pesos, self.retorno_anual())


    def volatilidade_portfolio(self,pesos):
        return np.sqrt(np.dot(pesos.T, np.dot(self.cov_anual(), pesos)))


    def volatilidade_ajustada_portifolio(self, pesos):
        return  np.sqrt(
            np.dot(pesos.T, np.dot(self.semi_cov_anual(), pesos)))

    def calcular_pesos_carteira(self, pesos):
        taxa_livre_risco = self.selic
        retorno_portfolio = self.retorno_portfolio(pesos)
        volatilidade_portfolio = self.volatilidade_portfolio(pesos)
        volatilidade_ajustada = self.volatilidade_ajustada_portifolio(pesos)
        sharpe = (retorno_portfolio - taxa_livre_risco) / \
            volatilidade_portfolio
        sortino = (retorno_portfolio - taxa_livre_risco) / \
            volatilidade_ajustada

        self.retorno.append(retorno_portfolio)
        self.volatilidade.append(volatilidade_portfolio)
        self.volatilidade_ajustada.append(volatilidade_ajustada)

        self.sharpe_ratio.append(sharpe)
        self.sortino_ratio.append(sortino)

        self.peso_ativos.append(pesos)


    def df_carteira(self):

        carteira = {'Retorno': self.retorno,
                    'Risco': self.volatilidade,
                    'Risco Ajustado': self.volatilidade_ajustada,
                    'Sharpe Ratio': self.sharpe_ratio,
                    'Sortino Ratio': self.sortino_ratio}

        for contar,a in enumerate(self.data):
            carteira[a] = [Peso[contar] for Peso in self.peso_ativos]

        # vamos transformar nosso dicionário em um dataframe
        df = pd.DataFrame(carteira)

        # vamos nomear as colunas do novo dataframe
        colunas = ['Retorno', 'Risco', 'Risco Ajustado', 'Sharpe Ratio' , 'Sortino Ratio'] + [a for a in self.data]
        df = df[colunas]

        return df,[a for a in self.data]




def format_values(value, is_percentage):
    return f"{value * 100:.2f}%" if is_percentage else f"{value:.2f}"

def format_dataframe(df):
    formatted_df = df.copy()
    for col in formatted_df.columns:
        if "Sharpe Ratio" in col or "Sortino Ratio" in col:
            formatted_df[col] = formatted_df[col].apply(format_values, args=(False,))
        else:
            formatted_df[col] = formatted_df[col].apply(format_values, args=(True,))
    return formatted_df.T   

def format_carteira(df):
    return tabulate(format_dataframe(df), tablefmt='simple')


def get_tickers(tickers):
    tickers = [t.upper().strip() for t in tickers]
    return [f"{t}.SA" for t in tickers]

def get_pesos(pesos):
    return np.array([float(p.strip())/100 for p in pesos])


def download_data(tickers, anos_hist):
    hoje = datetime.now()
    start_date = f"{hoje.year-anos_hist}-{datetime.now().month}-{datetime.now().day}"
    df = yf.download(tickers, start=start_date)['Adj Close'].dropna()
    df = df[tickers]  # Reordenar as colunas de acordo com a ordem dos tickers fornecidos
    return df



def retorna(tickers, pesos):
    tickers=get_tickers(tickers) 
    pesos=(get_pesos(pesos))
    print(tickers)
    print(pesos)


    anos_hist=5
    data=download_data(tickers,anos_hist)
    taxa_livre_risco = bancoCentral.taxa_livre_risco(anos_hist)

    
    carteira = Carteira(data,taxa_livre_risco)
    carteira.calcular_pesos_carteira(pesos)
    df, tt = carteira.df_carteira()

    a = {
    "Retorno": df["Retorno"].iloc[0] *100,
    "Risco": df["Risco"].iloc[0] *100,
    "RiscoAjustado": df["Risco Ajustado"].iloc[0] *100,
    "Sharpe": df["Sharpe Ratio"].iloc[0],
    "Sortino": df["Sortino Ratio"].iloc[0],
    "Tickers": []
}
    for t in tt:
        a["Tickers"].append({t:df[t].iloc[0] *100} )

    return a
   

   # return format_dataframe(carteira.df_carteira())



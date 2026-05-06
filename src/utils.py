"""
utils.py — Funções utilitárias reutilizáveis
Financial Behavior Intelligence
"""

import pandas as pd
import numpy as np


def calcular_saldo_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o saldo mensal por usuário.

    Parâmetros
    ----------
    df : DataFrame com colunas [User_ID, Date, Amount, Transaction Type]

    Retorna
    -------
    DataFrame com colunas [User_ID, Period, Receita, Despesa, Saldo]
    """
    df = df.copy()
    df['Period'] = pd.to_datetime(df['Date']).dt.to_period('M')

    result = df.pivot_table(
        index=['User_ID', 'Period'],
        columns='Transaction Type',
        values='Amount',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    result.columns.name = None
    result['Receita'] = result.get('credit', 0)
    result['Despesa'] = result.get('debit', 0)
    result['Saldo']   = result['Receita'] - result['Despesa']

    return result[['User_ID', 'Period', 'Receita', 'Despesa', 'Saldo']]


def calcular_taxa_poupanca(receita: float, despesa: float) -> float:
    """
    Calcula a taxa de poupança: (Receita - Despesa) / Receita.
    Retorna NaN se receita for zero.
    """
    if receita == 0:
        return np.nan
    return round((receita - despesa) / receita, 4)


def variacao_mom(serie: pd.Series) -> pd.Series:
    """
    Calcula a variação percentual mês a mês (MoM%).

    Parâmetros
    ----------
    serie : Série temporal ordenada com valores mensais

    Retorna
    -------
    Série com variação percentual (NaN no primeiro período)
    """
    return serie.pct_change().mul(100).round(2)


def padronizar_account_name(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza a coluna 'Account Name' para dois valores:
    'checking' e 'credit card'.
    """
    df = df.copy()
    df['Account Name'] = df['Account Name'].str.lower().str.strip()
    df['Account Name'] = df['Account Name'].replace({
        'platinum card': 'credit card',
        'silver card':   'credit card'
    })
    return df


# ADD: adicionar novas funções conforme necessário

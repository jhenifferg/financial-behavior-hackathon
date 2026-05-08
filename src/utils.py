"""
utils.py — Funções utilitárias reutilizáveis
Financial Behavior Intelligence
"""

import pandas as pd
import numpy as np


# ─────────────────────────────────────────────────────────────
# CONSTANTES DO PROJETO
# ─────────────────────────────────────────────────────────────

# Categorias excluídas do cálculo de gasto real
# (movimentações financeiras internas, não representam consumo)
CATEGORIAS_NAO_GASTO = [
    'Credit Card Payment',
    'Savings Transfer',
    'Transfer',
    'Investment',
]

# Categorias de despesas fixas mensais
CATEGORIAS_FIXAS = [
    'Rent',
    'Mortgage & Rent',
    'Phone Bill',
    'Mobile Phone',
    'Internet Bill',
    'Internet',
    'Insurance',
    'Auto Insurance',
    'Utilities',
    'Loan Payment',
]

# Categorias de lazer e entretenimento
CATEGORIAS_LAZER = [
    'Restaurants',
    'Fast Food',
    'Coffee Shops',
    'Alcohol & Bars',
    'Entertainment',
    'Movies & DVDs',
    'Travel',
    'Music',
    'Streaming Services',
    'Rideshare',
    'Gifts',
]


# ─────────────────────────────────────────────────────────────
# FUNÇÕES DE CÁLCULO FINANCEIRO
# ─────────────────────────────────────────────────────────────

def calcular_saldo_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o saldo mensal real por usuário.

    Usa apenas receita real (créditos excluindo pagamento de fatura)
    e gasto real (débitos excluindo movimentações financeiras internas),
    alinhado com a lógica do notebook 03_feature_engineering.

    Parâmetros
    ----------
    df : DataFrame com colunas [User_ID, Date, Amount, Transaction Type,
                                 Category, Description]

    Retorna
    -------
    DataFrame com colunas [User_ID, Period, Total_Receita, Total_Gasto,
                            Saldo_Mensal_Real]
    """
    df = df.copy()
    df['Period'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)

    # receita real = créditos excluindo pagamento de fatura
    receita = (
        df[
            (df['Transaction Type'] == 'credit') &
            (df['Description'] != 'Credit Card Payment')
        ]
        .groupby(['User_ID', 'Period'])['Amount']
        .sum()
        .rename('Total_Receita')
        .reset_index()
    )

    # gasto real = débitos excluindo movimentações financeiras
    gasto = (
        df[
            (df['Transaction Type'] == 'debit') &
            (~df['Category'].isin(CATEGORIAS_NAO_GASTO))
        ]
        .groupby(['User_ID', 'Period'])['Amount']
        .sum()
        .rename('Total_Gasto')
        .reset_index()
    )

    result = receita.merge(gasto, on=['User_ID', 'Period'], how='outer').fillna(0)
    result['Saldo_Mensal_Real'] = (result['Total_Receita'] - result['Total_Gasto']).round(2)

    return result.sort_values(['User_ID', 'Period']).reset_index(drop=True)


def calcular_taxa_poupanca(receita: float, despesa: float) -> float:
    """
    Calcula a taxa de poupança mensal: (Receita - Despesa) / Receita.

    Parâmetros
    ----------
    receita : float — renda real do mês
    despesa : float — gasto real do mês

    Retorna
    -------
    float — taxa de poupança (ex: 0.25 = 25%) ou NaN se receita for zero
    """
    if receita == 0:
        return np.nan
    return round((receita - despesa) / receita, 4)


def variacao_mom(serie: pd.Series) -> pd.Series:
    """
    Calcula a variação percentual mês a mês (MoM%).

    Parâmetros
    ----------
    serie : pd.Series — série temporal ordenada com valores mensais

    Retorna
    -------
    pd.Series — variação percentual (NaN no primeiro período)
    """
    return serie.pct_change().mul(100).round(2)


def padronizar_account_name(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza a coluna 'Account Name' para dois valores:
    'checking' e 'credit card'.

    Agrupa variações como 'Platinum Card' e 'Silver Card'
    sob o label único 'credit card'.

    Parâmetros
    ----------
    df : DataFrame com coluna 'Account Name'

    Retorna
    -------
    DataFrame com coluna 'Account Name' padronizada
    """
    df = df.copy()
    df['Account Name'] = df['Account Name'].str.lower().str.strip()
    df['Account Name'] = df['Account Name'].replace({
        'platinum card': 'credit card',
        'silver card':   'credit card',
    })
    return df


# ─────────────────────────────────────────────────────────────
# FUNÇÕES DE FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────

def calcular_taxa_categoria(df_debits: pd.DataFrame,
                             categorias: list,
                             nome_feature: str) -> pd.DataFrame:
    """
    Calcula a proporção do gasto total de um usuário
    em um conjunto de categorias específicas.

    Parâmetros
    ----------
    df_debits   : DataFrame filtrado para Transaction Type == 'debit'
    categorias  : lista de categorias a somar
    nome_feature: nome da coluna de saída

    Retorna
    -------
    DataFrame com colunas [User_ID, nome_feature]
    """
    total_user = df_debits.groupby('User_ID')['Amount'].sum().rename('total')

    gasto_cats = (
        df_debits[df_debits['Category'].isin(categorias)]
        .groupby('User_ID')['Amount']
        .sum()
        .rename('parcela')
    )

    result = pd.concat([total_user, gasto_cats], axis=1).fillna(0)
    result[nome_feature] = (result['parcela'] / result['total']).round(3)

    return result[[nome_feature]].reset_index()


def pct_meses_negativos(saldo_serie: pd.Series) -> float:
    """
    Calcula a proporção de meses com saldo negativo.

    Parâmetros
    ----------
    saldo_serie : pd.Series — série de saldos mensais de um usuário

    Retorna
    -------
    float — proporção de meses negativos (0.0 a 1.0)
    """
    return round((saldo_serie < 0).mean(), 3)

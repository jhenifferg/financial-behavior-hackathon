"""
data_generator.py — Script de Incremento do Dataset
Financial Behavior Intelligence

Descrição:
    Este script parte do dataset original do Kaggle
    (personal_transactions.csv) e gera uma versão expandida com
    múltiplos usuários, adicionando a coluna User_ID para
    permitir análise comparativa de comportamento financeiro.

    O dataset original recebe o ID USER_0051.
    Os 50 usuários sintéticos recebem USER_0001 a USER_0050.
    Total: 51 usuários.

Uso:
    python src/data_generator.py

Saída:
    data/raw/personal_transactions_padronizado_v2.csv
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime
import os
import sys

fake = Faker("en_US")
np.random.seed(42)
random.seed(42)

# ─────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────

INPUT_FILE  = "personal_transactions.csv"
OUTPUT_FILE = "personal_transactions_padronizado_v2.csv"

N_NOVOS_USUARIOS = 50      # usuários sintéticos a adicionar

# ─────────────────────────────────────────────
# PASSO 1 — LEITURA E DIAGNÓSTICO DO DATASET ORIGINAL
# ─────────────────────────────────────────────

print("=" * 60)
print("  INCREMENTO DO DATASET — personal_transactions.csv")
print("=" * 60)

if not os.path.exists(INPUT_FILE):
    print(f"\n[ERRO] Arquivo '{INPUT_FILE}' não encontrado.")
    print("       Coloque o CSV do Kaggle na mesma pasta deste script.")
    sys.exit(1)

df_original = pd.read_csv(INPUT_FILE)

print(f"\n[1] Dataset original carregado")
print(f"    Linhas       : {len(df_original):,}")
print(f"    Colunas      : {list(df_original.columns)}")
print(f"    Período      : {df_original['Date'].min()}  →  {df_original['Date'].max()}")
print(f"    Tipos únicos : {df_original['Transaction Type'].unique().tolist()}")
print(f"\n    Categorias originais ({df_original['Category'].nunique()} únicas):")
for cat in sorted(df_original["Category"].unique()):
    print(f"      - {cat}")

contas_originais = df_original["Account Name"].unique().tolist()
print(f"\n    Account Names: {contas_originais}")

# ─────────────────────────────────────────────
# PASSO 2 — DEFINIÇÃO DE CATEGORIAS
# ─────────────────────────────────────────────

# Formato: "Categoria": (transaction_type, valor_medio, desvio, account_name)
CATEGORIAS = {
    # Originais do Kaggle
    "Groceries"          : ("debit",   320,  80,  "checking"),
    "Restaurants"        : ("debit",   180,  70,  "credit card"),
    "Gas & Fuel"         : ("debit",   150,  50,  "credit card"),
    "Shopping"           : ("debit",   250, 120,  "credit card"),
    "Entertainment"      : ("debit",   120,  60,  "credit card"),
    "Travel"             : ("debit",   400, 200,  "credit card"),
    "Health & Fitness"   : ("debit",   100,  40,  "credit card"),
    "Utilities"          : ("debit",   180,  40,  "checking"),
    "Rent"               : ("debit",  1500, 300,  "checking"),
    "Insurance"          : ("debit",   250,  50,  "checking"),
    "Paycheck"           : ("credit", 4000, 800,  "checking"),
    # Educação
    "Education"          : ("debit",   350, 150,  "checking"),
    "Online Courses"     : ("debit",    80,  40,  "credit card"),
    "Books & Supplies"   : ("debit",    50,  30,  "credit card"),
    # Serviços digitais
    "Streaming Services" : ("debit",    45,  15,  "credit card"),
    "Software & Apps"    : ("debit",    35,  20,  "credit card"),
    "Phone Bill"         : ("debit",    85,  20,  "checking"),
    "Internet Bill"      : ("debit",    70,  15,  "checking"),
    # Saúde
    "Pharmacy"           : ("debit",    60,  40,  "credit card"),
    "Doctor & Dentist"   : ("debit",   150,  80,  "credit card"),
    "Mental Health"      : ("debit",   120,  50,  "credit card"),
    # Finanças pessoais
    "Savings Transfer"   : ("debit",   500, 200,  "checking"),
    "Investment"         : ("debit",   400, 200,  "checking"),
    "Credit Card Payment": ("debit",   800, 300,  "checking"),
    "Loan Payment"       : ("debit",   600, 150,  "checking"),
    # Casa e pessoal
    "Personal Care"      : ("debit",    80,  40,  "credit card"),
    "Home Improvement"   : ("debit",   200, 150,  "credit card"),
    "Pet Care"           : ("debit",    90,  50,  "credit card"),
    # Transporte
    "Rideshare"          : ("debit",    60,  30,  "credit card"),
    "Public Transit"     : ("debit",    40,  20,  "checking"),
    # Outros
    "Charity & Donations": ("debit",    50,  30,  "checking"),
    "Gifts"              : ("debit",    80,  60,  "credit card"),
    "Taxes"              : ("debit",   400, 200,  "checking"),
    "Freelance Income"   : ("credit",  600, 400,  "checking"),
    "Bonus"              : ("credit",  800, 500,  "checking"),
}

print(f"\n[2] Categorias disponíveis: {len(CATEGORIAS)}")

# ─────────────────────────────────────────────
# PASSO 3 — CATEGORIAS ESSENCIAIS (todo usuário tem)
# ─────────────────────────────────────────────

CATS_ESSENCIAIS = [
    "Groceries",
    "Utilities",
    "Rent",
    "Phone Bill",
    "Internet Bill",
    "Gas & Fuel",
    "Insurance",
]

# ─────────────────────────────────────────────
# PASSO 4 — GERAÇÃO DE NOVOS USUÁRIOS
# ─────────────────────────────────────────────

print(f"\n[3] Gerando {N_NOVOS_USUARIOS} novos usuários...")

df_original["Date"] = pd.to_datetime(df_original["Date"])
DATA_INICIO = df_original["Date"].min()
DATA_FIM    = df_original["Date"].max()

novos_registros = []

for uid in range(1, N_NOVOS_USUARIOS + 1):

    # formato padronizado USER_0001 a USER_0050
    user_id = f"USER_{uid:04d}"

    renda_base = random.uniform(2500, 7000)

    categorias_disponiveis = list(CATEGORIAS.keys())
    categorias_usuario = list(set(
        CATS_ESSENCIAIS
        + ["Paycheck"]
        + random.sample(categorias_disponiveis, k=random.randint(8, 15))
    ))

    datas_mensais = pd.date_range(start=DATA_INICIO, end=DATA_FIM, freq="MS")

    for data_base in datas_mensais:
        for categoria in categorias_usuario:

            tipo, media, desvio, conta = CATEGORIAS[categoria]

            # frequência de transações por categoria
            if categoria == "Travel":
                qtd = random.randint(1, 3) if data_base.month in [6, 7, 12] else random.randint(0, 1)
            elif categoria in ["Paycheck", "Rent", "Utilities", "Internet Bill",
                               "Phone Bill", "Insurance", "Loan Payment"]:
                qtd = 1
            elif categoria in ["Groceries", "Restaurants", "Shopping", "Gas & Fuel"]:
                qtd = random.randint(2, 8)
            else:
                qtd = random.randint(1, 3)

            for _ in range(qtd):
                # dia da transação conforme categoria
                if categoria == "Paycheck":
                    dia = random.randint(1, 5)
                elif categoria in ["Rent", "Utilities", "Internet Bill",
                                   "Phone Bill", "Insurance", "Loan Payment"]:
                    dia = random.randint(3, 10)
                elif categoria in ["Groceries", "Restaurants", "Gas & Fuel", "Shopping"]:
                    dia = random.randint(1, 28)
                elif categoria in ["Entertainment", "Travel", "Rideshare"]:
                    dia = random.randint(10, 28)
                else:
                    dia = random.randint(1, 28)

                data_transacao = datetime(
                    data_base.year, data_base.month, min(dia, 28)
                )

                valor = max(5, round(np.random.normal(media, desvio), 2))

                if categoria == "Paycheck":
                    valor = round(renda_base, 2)
                if categoria == "Gifts" and data_base.month == 12:
                    valor *= 2

                novos_registros.append({
                    "User_ID"          : user_id,
                    "Date"             : data_transacao.strftime("%Y-%m-%d"),
                    "Description"      : fake.company(),
                    "Category"         : categoria,
                    "Amount"           : valor,
                    "Transaction Type" : tipo,
                    "Account Name"     : conta,
                })

# ─────────────────────────────────────────────
# PASSO 5 — ATRIBUIR ID AO USUÁRIO ORIGINAL
# ─────────────────────────────────────────────

# O usuário original do Kaggle recebe o último ID (USER_0051)
if "User_ID" not in df_original.columns:
    df_original["User_ID"] = "USER_0051"
else:
    df_original["User_ID"] = "USER_0051"

# ─────────────────────────────────────────────
# PASSO 6 — CONCATENAÇÃO E EXPORTAÇÃO
# ─────────────────────────────────────────────

df_novos = pd.DataFrame(novos_registros)

df_final = pd.concat([df_original, df_novos], ignore_index=True)

print(f"\n[4] Concatenação concluída")
print(f"    Registros originais  : {len(df_original):,}  (USER_0051)")
print(f"    Registros sintéticos : {len(df_novos):,}  (USER_0001 a USER_0050)")
print(f"    TOTAL                : {len(df_final):,}")

# reorganizar colunas
colunas = ["User_ID"] + [c for c in df_final.columns if c != "User_ID"]
df_final = df_final[colunas].sort_values(["Date", "User_ID"]).reset_index(drop=True)

df_final.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"\n[5] Arquivo salvo: {OUTPUT_FILE}")
print(f"\n    Usuários únicos: {df_final['User_ID'].nunique()}")
print(f"    Range: {df_final['User_ID'].min()} → {df_final['User_ID'].max()}")
print(f"\n    Colunas:")
for col in df_final.columns:
    print(f"      {col:<22} | dtype: {str(df_final[col].dtype):<10} | nulos: {df_final[col].isnull().sum()}")

print("\n" + "=" * 60)
print("  PRÓXIMO PASSO: notebooks/01_eda_exploratoria.ipynb")
print("  Arquivo gerado:", OUTPUT_FILE)
print("=" * 60)

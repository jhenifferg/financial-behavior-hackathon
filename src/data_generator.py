"""
data_generator.py — Script de Incremento do Dataset
Financial Behavior Intelligence

Descrição:
    Este script parte do dataset original do Kaggle
    (personal_transactions.csv) e gera uma versão expandida com
    múltiplos usuários, adicionando a coluna User_ID para
    permitir análise comparativa de comportamento financeiro.

Uso:
    python src/data_generator.py

Saída:
    data/raw/personal_transactions_padronizado_v2.csv

ADD: Inserir implementação aqui.
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import sys

fake = Faker("en_US")   # mesmo locale do dataset original (inglês)
np.random.seed(42)
random.seed(42)

# ─────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────

INPUT_FILE  = "personal_transactions.csv"
OUTPUT_FILE = "personal_transactions_padronizado_v2.csv"

N_NOVOS_USUARIOS = 50      # usuários sintéticos a adicionar
MESES_POR_USUARIO = 24     # Jan 2023 → Dez 2024  (expande o período do dataset)

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

# Contas únicas no dataset (Account Name)
contas_originais = df_original["Account Name"].unique().tolist()
print(f"\n    Account Names: {contas_originais}")

# ─────────────────────────────────────────────
# PASSO 2 — NOVAS CATEGORIAS
# Mantemos TODAS as originais + adicionamos novas
# relevantes para análise de comportamento financeiro
# ─────────────────────────────────────────────

# Formato: "Categoria" : (transaction_type, valor_medio, desvio, account_name)
# transaction_type: "debit" ou "credit"
CATEGORIAS_NOVAS = {
    # --- Já existentes no Kaggle (mantidas para os novos usuários) ---
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

    # --- NOVAS categorias para enriquecer a análise ---
    # Educação & Desenvolvimento
    "Education"          : ("debit",   350, 150,  "checking"),
    "Online Courses"     : ("debit",    80,  40,  "credit card"),
    "Books & Supplies"   : ("debit",    50,  30,  "credit card"),

    # Serviços Digitais / Assinaturas
    "Streaming Services" : ("debit",    45,  15,  "credit card"),
    "Software & Apps"    : ("debit",    35,  20,  "credit card"),
    "Phone Bill"         : ("debit",    85,  20,  "checking"),
    "Internet Bill"      : ("debit",    70,  15,  "checking"),

    # Saúde
    "Pharmacy"           : ("debit",    60,  40,  "credit card"),
    "Doctor & Dentist"   : ("debit",   150,  80,  "credit card"),
    "Mental Health"      : ("debit",   120,  50,  "credit card"),

    # Finanças Pessoais
    "Savings Transfer"   : ("debit",   500, 200,  "checking"),   # dinheiro para poupança
    "Investment"         : ("debit",   400, 200,  "checking"),   # aportes em investimentos
    "Credit Card Payment": ("debit",   800, 300,  "checking"),   # pagamento da fatura
    "Loan Payment"       : ("debit",   600, 150,  "checking"),   # parcela de empréstimo

    # Cuidados Pessoais & Casa
    "Personal Care"      : ("debit",    80,  40,  "credit card"),
    "Home Improvement"   : ("debit",   200, 150,  "credit card"),
    "Pet Care"           : ("debit",    90,  50,  "credit card"),

    # Transporte Alternativo
    "Rideshare"          : ("debit",    60,  30,  "credit card"),  # Uber/Lyft
    "Public Transit"     : ("debit",    40,  20,  "checking"),

    # Outros
    "Charity & Donations": ("debit",    50,  30,  "checking"),
    "Gifts"              : ("debit",    80,  60,  "credit card"),
    "Taxes"              : ("debit",   400, 200,  "checking"),
    "Freelance Income"   : ("credit",  600, 400,  "checking"),   # renda extra
    "Bonus"              : ("credit",  800, 500,  "checking"),   # bônus/13º
}

print(f"\n[2] Novas categorias adicionadas: {len(CATEGORIAS_NOVAS)}")

# ─────────────────────────────────────────────
# PASSO 3 — PERFIS DE USUÁRIO
# Cada perfil define quais categorias aparecem com frequência
# e qual o multiplicador de gasto (1.0 = normal)
# ─────────────────────────────────────────────

PERFIS = {
    "saver": {
        "income_mult"      : 1.30,   # renda 30% acima da média
        "spend_mult"       : 0.60,   # gasta 60% da renda
        "has_investment"   : True,
        "has_loan"         : False,
        "extras"           : ["Investment", "Savings Transfer", "Online Courses"],
    },
    "balanced": {
        "income_mult"      : 1.00,
        "spend_mult"       : 0.88,
        "has_investment"   : False,
        "has_loan"         : False,
        "extras"           : ["Streaming Services", "Personal Care"],
    },
    "debtor": {
        "income_mult"      : 0.75,   # renda abaixo da média
        "spend_mult"       : 1.15,   # gasta mais do que ganha
        "has_investment"   : False,
        "has_loan"         : True,
        "extras"           : ["Loan Payment", "Credit Card Payment", "Rideshare"],
    },
}

# Categorias base que todo usuário tem (despesas essenciais)
CATS_ESSENCIAIS = [
    "Groceries", "Utilities", "Rent", "Phone Bill",
    "Internet Bill", "Gas & Fuel", "Insurance",
]

# ─────────────────────────────────────────────
# PASSO 4 — GERAÇÃO DE NOVOS REGISTROS
# ─────────────────────────────────────────────

print(f"\n[3] Gerando {N_NOVOS_USUARIOS} novos usuários "
      f"({MESES_POR_USUARIO} meses cada)...")

DATA_INICIO = datetime(2023, 1, 1)
novos_registros = []
nomes_usados = set(df_original.get("Account Name", pd.Series()).unique())

# Distribui perfis: 30% saver, 45% balanced, 25% debtor
perfis_lista = (
    ["saver"]    * int(N_NOVOS_USUARIOS * 0.30) +
    ["balanced"] * int(N_NOVOS_USUARIOS * 0.45) +
    ["debtor"]   * int(N_NOVOS_USUARIOS * 0.25)
)
# completa se faltar por arredondamento
while len(perfis_lista) < N_NOVOS_USUARIOS:
    perfis_lista.append("balanced")
random.shuffle(perfis_lista)

for uid in range(N_NOVOS_USUARIOS):
    perfil_nome = perfis_lista[uid]
    perfil      = PERFIS[perfil_nome]

    # Nome único para identificar o usuário (vai para Account Name)
    while True:
        nome = fake.name()
        if nome not in nomes_usados:
            nomes_usados.add(nome)
            break

    # Renda base aleatória por perfil
    renda_base = random.uniform(2500, 5500) * perfil["income_mult"]

    # Categorias que este usuário usa (essenciais + extras do perfil + aleatórias)
    cats_disponiveis = list(CATEGORIAS_NOVAS.keys())
    cats_usuais = (
        CATS_ESSENCIAIS
        + perfil["extras"]
        + random.sample(
            [c for c in cats_disponiveis if c not in CATS_ESSENCIAIS + perfil["extras"]
             and CATEGORIAS_NOVAS[c][0] == "debit"],
            k=min(5, len(cats_disponiveis))
        )
    )
    # Remove categorias que conflitam com o perfil
    if not perfil["has_loan"]:
        cats_usuais = [c for c in cats_usuais if c != "Loan Payment"]
    if not perfil["has_investment"]:
        cats_usuais = [c for c in cats_usuais if c != "Investment"]

    # Garante Paycheck (receita)
    if "Paycheck" not in cats_usuais:
        cats_usuais.append("Paycheck")

    # Gera transações mês a mês
    for mes_idx in range(MESES_POR_USUARIO):
        data_ref = DATA_INICIO + timedelta(days=30 * mes_idx)

        # Tendência: debtors ficam piores ao longo do tempo
        fator_tendencia = 1.0
        if perfil_nome == "debtor":
            fator_tendencia = 1 + (0.008 * mes_idx)
        elif perfil_nome == "saver":
            fator_tendencia = 1 - (0.002 * mes_idx)

        for cat in cats_usuais:
            if cat not in CATEGORIAS_NOVAS:
                continue

            tipo, val_medio, desvio, account = CATEGORIAS_NOVAS[cat]

            # Ajusta valor conforme renda e perfil
            if tipo == "credit":
                valor = round(abs(np.random.normal(
                    renda_base if cat == "Paycheck" else val_medio,
                    renda_base * 0.03 if cat == "Paycheck" else desvio
                )), 2)
            else:
                valor = round(abs(np.random.normal(
                    val_medio * perfil["spend_mult"] * fator_tendencia,
                    desvio * 0.5
                )), 2)
                valor = max(1.0, valor)

            # Sazonalidade: Shopping e Entertainment sobem no fim do ano
            if cat in ("Shopping", "Entertainment", "Gifts") and data_ref.month in (11, 12):
                valor = round(valor * 1.35, 2)

            # Freelance e Bonus: nem todo mês
            if cat == "Freelance Income" and random.random() > 0.40:
                continue
            if cat == "Bonus" and random.random() > 0.15:
                continue

            # Data aleatória dentro do mês
            dia = random.randint(1, 28)
            data_transacao = (data_ref + timedelta(days=dia)).strftime("%-m/%-d/%Y")

            novos_registros.append({
                "Date"            : data_transacao,
                "Description"     : fake.company()[:40],
                "Amount"          : valor,
                "Transaction Type": tipo,
                "Category"        : cat,
                "Account Name"    : account,
                # Coluna extra: identifica o usuário (útil para análise por perfil)
                "User_ID"         : f"SYN_{uid+1:04d}",
                "User_Profile"    : perfil_nome,
            })

df_novos = pd.DataFrame(novos_registros)
print(f"    Novos registros gerados: {len(df_novos):,}")

# ─────────────────────────────────────────────
# PASSO 5 — ADICIONAR User_ID E User_Profile AO DATASET ORIGINAL
# Usuário original recebe ID "ORIG_0001" e perfil "unknown"
# ─────────────────────────────────────────────

df_original["User_ID"]      = "ORIG_0001"
df_original["User_Profile"] = "unknown"

# ─────────────────────────────────────────────
# PASSO 6 — CONCATENAÇÃO
# ─────────────────────────────────────────────

df_final = pd.concat([df_original, df_novos], ignore_index=True)

print(f"\n[4] Concatenação concluída")
print(f"    Registros originais  : {len(df_original):,}")
print(f"    Registros sintéticos : {len(df_novos):,}")
print(f"    TOTAL ENRIQUECIDO    : {len(df_final):,}")

# ─────────────────────────────────────────────
# PASSO 7 — SALVAR
# ─────────────────────────────────────────────

df_final.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"\n[5] Arquivo salvo: {OUTPUT_FILE}")
print(f"\n    Colunas do dataset enriquecido:")
for col in df_final.columns:
    nulls = df_final[col].isnull().sum()
    print(f"      {col:<20} | dtype: {str(df_final[col].dtype):<10} | nulos: {nulls}")

print(f"\n    Categorias no dataset enriquecido ({df_final['Category'].nunique()} únicas):")
for cat in sorted(df_final["Category"].unique()):
    n = (df_final["Category"] == cat).sum()
    print(f"      {cat:<25} → {n:>5} registros")

print(f"\n    Distribuição por perfil:")
for perfil, count in df_final["User_Profile"].value_counts().items():
    print(f"      {perfil:<10} → {count:>6} registros")

print("\n" + "=" * 60)
print("  PRÓXIMO PASSO: tratamento e análise exploratória")
print("  Arquivo pronto:", OUTPUT_FILE)
print("=" * 60)


# 💸 Financial Behavior Intelligence

> Hackathon — Tema 1: Comportamento Financeiro  
> Sistema Inteligente de Análise de Perfil Financeiro e Geração de Insights Baseado em Dados

---

## 📌 Problema & Proposta

Usuários raramente entendem seus próprios padrões financeiros. Este projeto analisa 19.046 transações de 51 usuários ao longo de 7 anos para **descobrir automaticamente perfis de comportamento financeiro**, gerar insights acionáveis e predizer o perfil de novos usuários com base em seu histórico.

A abordagem usa clustering não supervisionado, onde os perfis **emergem dos dados**, sem regras pré-definidas, seguido de um classificador que generaliza esses perfis para novos usuários.

---

## 🏗️ Arquitetura da Solução

```
┌──────────────────────────────────────────────────────────────────┐
│                        PIPELINE DE DADOS                         │
│                                                                  │
│  [Kaggle CSV]                                                    │
│      │                                                           │
│      ▼                                                           │
│  data_generator.py  ──→  dataset multi-usuário (User_ID)        │
│  (src/)                  (data/raw/)                             │
│      │                                                           │
│      ▼                                                           │
│  01_eda_exploratoria.ipynb  ──→  Limpeza + Exploração            │
│  02_sql_queries.ipynb       ──→  Insights via SQL (SQLite)       │
│  03_feature_engineering.ipynb ─→ 20 features por usuário        │
│      │                           (data/processed/)               │
│      ▼                                                           │
│  04_ml_model.ipynb                                               │
│    ├── K-Means  ──→  3 perfis naturais descobertos               │
│    └── Random Forest  ──→  classificador para novos usuários     │
│      │                                                           │
│      ▼                                                           │
│  Power BI Dashboard  ──→  Painel                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📂 Estrutura do Repositório

```
financial-behavior-intelligence/
│
├── data/
│   ├── raw/                           # Dataset bruto (não versionado)
│   ├── processed/                     # Features processadas (não versionado)
│   └── data_dictionary.md             # Dicionário de dados
│
├── notebooks/
│   ├── 01_eda_exploratoria.ipynb      # Análise exploratória e estatística descritiva
│   ├── 02_sql_queries.ipynb           # Insights via SQLite em memória (7 queries)
│   ├── 03_feature_engineering.ipynb   # Engenharia de 20 features por usuário
│   └── 04_ml_model.ipynb              # K-Means + Random Forest
│
├── sql/
│   └── queries_financeiras.sql        # Queries standalone exportadas
│
├── src/
│   ├── data_generator.py              # Script de incremento de usuários
│   └── utils.py                       # Funções utilitárias reutilizáveis
│
├── powerbi/
│   └── painel.pbix                    # Dashboard Power BI 
│
├── docs/
│   ├── arquitetura_solucao.md         # Detalhamento da arquitetura
│   └── storytelling.md                # Narrativa executiva para apresentação
│
├── presentation/
│   └── slides_final.pdf               # Slides da apresentação ⬅ ADD
│
├── .gitignore
├── requirements.txt
└── README.md
```

> **⬅ ADD** — arquivos a serem adicionados conforme o projeto avança.

---

## 📊 Dataset

- **Fonte original:** [Personal Finance Dataset — Kaggle](https://www.kaggle.com/datasets/bukolafatunde/personal-finance?select=personal_transactions.csv)
- **Incremento:** O dataset original foi expandido via `src/data_generator.py`, adicionando 50 usuários sintéticos (`USER_0002` a `USER_0051`) ao usuário original (`USER_0001`), totalizando **51 usuários** para análise comparativa.
- **Período:** Janeiro/2018 — Dezembro/2024
- **Transações:** 19.046 registros | 46 categorias | 2 tipos de conta
- **Colunas:** `User_ID`, `Date`, `Description`, `Amount`, `Transaction Type`, `Category`, `Account Name`

> O arquivo de dados **não é versionado** no Git (`.gitignore`). Para reproduzir:
> 1. Baixe o CSV original do Kaggle (link acima)
> 2. Execute `python src/data_generator.py` na raiz do projeto

---

## 🤖 Modelo de Machine Learning

Pipeline em dois estágios implementado em `notebooks/04_ml_model.ipynb`:

**Etapa 1 — Clustering (K-Means)**
- Descobre perfis financeiros naturais sem rótulos pré-definidos
- 6 features normalizadas: `savings_rate`, `pct_meses_negativo`, `has_investment`, `spending_volatility`, `avg_perc_gasto_credito`, `avg_monthly_debit`
- k=3 escolhido via Elbow Method + Silhouette Score (0,4539)
- Perfis encontrados: **Investidor Estratégico** (15), **Perfil Equilibrado** (23), **Em Risco Financeiro** (13)

**Etapa 2 — Classificador (Random Forest)**
- Generaliza os perfis para classificar novos usuários automaticamente
- Acurácia CV-5: **98% ± 4%** | F1-Weighted: **97,76%**
- Top features: `avg_monthly_debit` (18,9%), `total_investment` (16,2%), `has_investment` (15,5%)

---

## 🚀 Como Executar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Ordem de Execução

```
1. python src/data_generator.py               ← gera data/raw/
2. notebooks/01_eda_exploratoria.ipynb        ← gera data/processed/transactions_clean.csv
3. notebooks/02_sql_queries.ipynb             ← insights SQL
4. notebooks/03_feature_engineering.ipynb    ← gera data/processed/user_features.csv
5. notebooks/04_ml_model.ipynb               ← gera data/processed/user_predictions.csv
```

---

## 👥 Time

| Nome | GitHub |
|---|---|
| Bárbara Moreira | — |
| Cintia Rodrigues | — |
| Isabelle Fischer | — |
| Jéssica Oliveira | — |
| Jheniffer Guimarães | [@jhenifferg](https://github.com/jhenifferg) |

---

## 🏆 Hackathon

**Tema:** Tema 1 — Comportamento Financeiro (Financial Behavior Intelligence)  
**Objetivo:** Sistema Inteligente de Análise de Perfil Financeiro, Consumo e Geração de Insights Baseado em Dados

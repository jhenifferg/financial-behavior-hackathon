# 💸 Financial Behavior Intelligence

> Hackathon — Tema 1: Comportamento Financeiro  
> Sistema Inteligente de Análise de Perfil Financeiro e Geração de Insights Baseado em Dados

---

## 📌 Problema & Proposta

Usuários raramente entendem seus próprios padrões financeiros. Este projeto analisa transações de múltiplos usuários para identificar perfis de comportamento financeiro (poupador, endividado, equilibrado), gerar insights acionáveis e predizer o perfil de novos usuários com base em seu histórico.

---

## 🏗️ Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────────┐
│                        PIPELINE DE DADOS                        │
│                                                                 │
│  [Kaggle CSV]                                                   │
│      │                                                          │
│      ▼                                                          │
│  data_generator.py  ──→  dataset multi-usuário (User_ID)       │
│  (src/)                  (data/raw/)                            │
│      │                                                          │
│      ▼                                                          │
│  01_eda_exploratoria.ipynb  ──→  Limpeza + Exploração           │
│  02_sql_queries.ipynb       ──→  Insights via SQL               │
│  03_feature_engineering.ipynb ─→ Features por usuário/mês      │
│      │                           (data/processed/)              │
│      ▼                                                          │
│  04_ml_model.ipynb  ──→  Modelo preditivo de perfil            │
│      │                                                          │
│      ▼                                                          │
│  Power BI Dashboard  ──→  Painel da Diretoria                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Estrutura do Repositório

```
financial-behavior-intelligence/
│
├── data/
│   ├── raw/                          # Dataset bruto 
│   ├── processed/                    # Features processadas 
│   └── data_dictionary.md            # Dicionário de dados
│
├── notebooks/
│   ├── 01_eda_exploratoria.ipynb     # Análise exploratória e estatística descritiva
│   ├── 02_sql_queries.ipynb          # Insights via SQLite em memória
│   ├── 03_feature_engineering.ipynb  # Engenharia de features para o modelo
│   └── 04_ml_model.ipynb             # Treinamento e avaliação do modelo preditivo
│
├── sql/
│   └── queries_financeiras.sql       # Queries standalone exportadas
│
├── src/
│   ├── data_generator.py             # Script de incremento de usuários ⬅ ADD
│   └── utils.py                      # Funções utilitárias reutilizáveis
│
├── powerbi/
│   └── painel_diretoria.pbix         # Dashboard Power BI ⬅ ADD
│
├── docs/
│   ├── arquitetura_solucao.md        # Detalhamento da arquitetura
│   └── storytelling.md              # Narrativa executiva para apresentação
│
├── presentation/
│   └── slides_final.pdf              # Slides da apresentação ⬅ ADD
│
├── .gitignore
├── requirements.txt
└── README.md
```

> **⬅ ADD** — arquivos a serem adicionados conforme o projeto avança.

---

## 📊 Dataset

- **Fonte original:** [Personal Finance Dataset — Kaggle](https://www.kaggle.com/datasets/bukolafatunde/personal-finance?select=personal_transactions.csv)
- **Incremento:** O dataset original foi expandido via `src/data_generator.py`, adicionando múltiplos usuários (coluna `User_ID`) para permitir análise comparativa de comportamento financeiro entre perfis distintos.
- **Período:** Janeiro/2018 — Setembro/2024
- **Colunas:** `Date`, `Description`, `Amount`, `Transaction Type`, `Category`, `Account Name`, `User_ID`

---

## 🚀 Como Executar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Ordem de Execução dos Notebooks

```
1. notebooks/01_eda_exploratoria.ipynb
2. notebooks/02_sql_queries.ipynb
3. notebooks/03_feature_engineering.ipynb     ← gera data/processed/
4. notebooks/04_ml_model.ipynb                ← consome data/processed/
```

---

## 👥 Time

Bárbara Moreira
Cintia Rodrigues
Isabelle Fischer
Jéssica Oliveira 
Jheniffer Guimarães 

---


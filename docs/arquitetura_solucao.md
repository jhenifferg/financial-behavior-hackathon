# 🏗️ Arquitetura da Solução

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PIPELINE DE DADOS                           │
│                                                                     │
│  ENTRADA                                                            │
│  ────────                                                           │
│  [personal_transactions.csv]  ←  Kaggle (dataset original)         │
│           │                                                         │
│           ▼                                                         │
│  [data_generator.py]                                                │
│   Expansão multi-usuário → adiciona coluna User_ID                 │
│   Saída: personal_transactions_padronizado_v2.csv                  │
│           │                                                         │
│           │             data/raw/                                   │
│  ─────────┼─────────────────────────────────────────────────────── │
│           │             PROCESSAMENTO                               │
│           ▼                                                         │
│  [01_eda_exploratoria.ipynb]                                        │
│   Limpeza, padronização, estatísticas descritivas                  │
│   Saída: transactions_clean.csv                                     │
│           │                                                         │
│           ▼                                                         │
│  [02_sql_queries.ipynb]                                             │
│   Insights via SQLite (saldo mensal, MoM%, categorias)             │
│           │                                                         │
│           ▼                                                         │
│  [03_feature_engineering.ipynb]                                     │
│   Agregações por usuário → features para o modelo                  │
│   Saída: user_features.csv                                         │
│           │                                                         │
│           │             data/processed/                             │
│  ─────────┼─────────────────────────────────────────────────────── │
│           │             MODELO                                      │
│           ▼                                                         │
│  [04_ml_model.ipynb]                                                │
│   Random Forest → classifica perfil financeiro                     │
│   (saver / debtor / balanced)                                      │
│   Saída: user_predictions.csv                                      │
│           │                                                         │
│  ─────────┼─────────────────────────────────────────────────────── │
│           │             VISUALIZAÇÃO                                │
│           ▼                                                         │
│  [Power BI — Painel da Diretoria]                                   │
│   Consome: transactions_clean.csv + user_predictions.csv           │
│   Exibe: KPIs, saldo mensal, categorias, score de perfil           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Componentes

### 1. Geração do Dataset (`src/data_generator.py`)
- **Entrada:** `personal_transactions.csv` (Kaggle)
- **Processo:** Replica e atribui transações a múltiplos usuários, criando a coluna `User_ID`
- **Saída:** `data/raw/personal_transactions_padronizado_v2.csv`

### 2. EDA (`notebooks/01_eda_exploratoria.ipynb`)
- Leitura do CSV bruto
- Conversão de tipos (Date → datetime)
- Padronização de `Account Name`
- Estatísticas descritivas (distribuições, outliers, sazonalidade)
- Geração de `transactions_clean.csv`

### 3. SQL (`notebooks/02_sql_queries.ipynb`)
- SQLite em memória via `sqlite3`
- Queries de negócio: saldo mensal, MoM%, taxa de poupança, categorias por usuário
- Queries exportadas standalone em `sql/queries_financeiras.sql`

### 4. Feature Engineering (`notebooks/03_feature_engineering.ipynb`)
- Agrega transações em 1 linha por usuário
- Features: saldo médio, volatilidade, taxa de poupança, uso de cartão, presença de investimentos
- Saída: `user_features.csv`

### 5. Modelo de ML (`notebooks/04_ml_model.ipynb`)
- **Algoritmo:** Random Forest Classifier
- **Target:** Perfil financeiro (saver / debtor / balanced)
- **Avaliação:** Acurácia, F1-Score, Confusion Matrix, Cross-Validation
- **Interpretabilidade:** Feature Importance

### 6. Dashboard Power BI (`powerbi/painel_diretoria.pbix`)
- **Fontes:** `transactions_clean.csv` + `user_predictions.csv`
- **Páginas:** Visão Geral, Saúde Financeira, Comportamento de Gasto, Predição ML

---

## Como Reproduzir o Pipeline

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Gerar o dataset
python src/data_generator.py

# 3. Executar notebooks em ordem
jupyter notebook notebooks/01_eda_exploratoria.ipynb
jupyter notebook notebooks/02_sql_queries.ipynb
jupyter notebook notebooks/03_feature_engineering.ipynb
jupyter notebook notebooks/04_ml_model.ipynb

# 4. Abrir dashboard
# Abrir powerbi/painel_diretoria.pbix no Power BI Desktop
# Atualizar fonte de dados para data/processed/
```

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Análise de dados | pandas, numpy |
| SQL | sqlite3 (in-memory) |
| Visualização | matplotlib, seaborn |
| Machine Learning | scikit-learn |
| Dashboard | Microsoft Power BI |
| Versionamento | Git / GitHub |

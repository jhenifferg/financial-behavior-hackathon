# 📖 Dicionário de Dados

## Contexto

O projeto utiliza **dois datasets relacionados**:

| Dataset | Origem | Localização |
|---|---|---|
| `personal_transactions.csv` | [Kaggle — Personal Finance](https://www.kaggle.com/datasets/bukolafatunde/personal-finance?select=personal_transactions.csv) | Externo (não versionado) |
| `personal_transactions_padronizado_v2.csv` | Gerado por `src/data_generator.py` | `data/raw/` |

O dataset do Kaggle é uma **dependência externa** e ponto de partida da geração. O dataset incrementado é o arquivo de trabalho do pipeline.

---

## Dataset Original — Kaggle (`personal_transactions.csv`)

Contém transações financeiras de **um único usuário anônimo**, sem identificação de usuário.

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `Date` | string | Data da transação (`MM/DD/YYYY`) | `01/15/2020` |
| `Description` | string | Estabelecimento ou tipo de transação | `Amazon`, `Netflix` |
| `Amount` | float | Valor em dólares (sempre positivo) | `124.50` |
| `Transaction Type` | string | `debit` (saída) ou `credit` (entrada) | `debit` |
| `Category` | string | Categoria financeira | `Groceries`, `Rent` |
| `Account Name` | string | Conta utilizada | `Checking`, `Platinum Card` |

> **Limitação do original:** Dataset de usuário único — não permite análise comparativa de perfis financeiros distintos.

---

## Dataset Incrementado — `personal_transactions_padronizado_v2.csv`

Gerado por `src/data_generator.py` a partir do dataset original. Este é o arquivo de trabalho do pipeline e fica em `data/raw/`.

**Colunas herdadas do original** (mantidas sem alteração de semântica):

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `Date` | string | Data da transação (`MM/DD/YYYY`) | `01/15/2020` |
| `Description` | string | Estabelecimento ou tipo de transação | `Amazon`, `Netflix` |
| `Amount` | float | Valor em dólares (sempre positivo) | `124.50` |
| `Transaction Type` | string | `debit` (saída) ou `credit` (entrada) | `debit` |
| `Category` | string | Categoria financeira da transação | `Groceries`, `Rent` |
| `Account Name` | string | Conta utilizada (padronizada no notebook 01) | `checking`, `credit card` |

**Coluna adicionada pelo `data_generator.py`:**

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `User_ID` | string | Identificador único do usuário, atribuído pelo script de geração | `USER_0001` |

> **O que o script faz:** replica e distribui as transações entre múltiplos usuários, gerando 51 perfis distintos (`USER_0001` a `USER_0051`). Isso permite análise comparativa de comportamento financeiro — núcleo analítico do projeto.

---

## Arquivo: `personal_transactions_padronizado_v2.csv`

Dataset de transações financeiras pessoais de múltiplos usuários, cobrindo o período de **janeiro de 2018 a setembro de 2024**.

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `Date` | string → datetime | Data da transação no formato `MM/DD/YYYY` | `01/15/2020` |
| `Description` | string | Descrição do estabelecimento ou tipo de transação | `Amazon`, `Netflix`, `Paycheck` |
| `Amount` | float | Valor da transação em dólares (sempre positivo) | `124.50` |
| `Transaction Type` | string | Tipo da transação: `debit` (saída) ou `credit` (entrada) | `debit` |
| `Category` | string | Categoria financeira da transação | `Groceries`, `Rent`, `Paycheck` |
| `Account Name` | string | Conta utilizada na transação | `checking`, `credit card` |
| `User_ID` | string | Identificador único do usuário, adicionado via `data_generator.py` | `USER_0001` |

---

## Categorias Presentes

| Categoria | Tipo Predominante | Descrição |
|---|---|---|
| `Paycheck` | credit | Salário recebido |
| `Groceries` | debit | Supermercado e alimentação |
| `Utilities` | debit | Contas de serviços (água, luz, gás) |
| `Gas & Fuel` | debit | Combustível e postos |
| `Rent` | debit | Aluguel |
| `Phone Bill` | debit | Conta de telefone |
| `Internet Bill` | debit | Conta de internet |
| `Insurance` | debit | Seguros em geral |
| `Restaurants` | debit | Restaurantes e alimentação fora |
| `Personal Care` | debit | Saúde, higiene e cuidados pessoais |
| `Streaming Services` | debit | Netflix, Spotify, etc. |
| `Credit Card Payment` | credit | Pagamento da fatura do cartão |
| `Savings Transfer` | debit | Transferências para poupança/investimentos |
| `Online Courses` | debit | Educação online |
| `Investment` | debit | Aportes em investimentos |
| `Rideshare` | debit | Uber, Lyft e similares |
| `Shopping` | debit | Compras em geral |
| `Movies & DVDs` | debit | Entretenimento |

---

## Contas (Account Name)

| Valor | Descrição |
|---|---|
| `checking` | Conta corrente principal |
| `credit card` | Cartão de crédito |

> **Nota:** No dataset bruto podem existir variações como `Checking`, `Platinum Card`, `Silver Card` — esses são tratados e padronizados no notebook `01_eda_exploratoria.ipynb`.

---

## Sobre o User_ID

A coluna `User_ID` foi gerada pelo script `src/data_generator.py` e não faz parte do dataset original do Kaggle. Ela permite análise comparativa de comportamento financeiro entre **51 usuários distintos**.

---

## Estatísticas Gerais do Dataset

| Métrica | Valor |
|---|---|
| Total de transações | 19.046 |
| Número de usuários | 51 |
| Período coberto | Jan/2018 — Set/2024 |
| Valor médio por transação | US$ 512,94 |
| Valor mínimo | US$ 1,00 |
| Valor máximo | US$ 9.200,00 |
| Nulos | Nenhum |

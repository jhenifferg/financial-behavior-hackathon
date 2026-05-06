-- ============================================================
-- Financial Behavior Intelligence — Queries SQL
-- Exportadas do notebook 02_sql_queries.ipynb
-- Banco: SQLite (tabela: transactions)
-- ============================================================


-- Q1: Saldo mensal por usuário (receita - despesa)
SELECT
    User_ID,
    strftime('%Y-%m', Date)                                                          AS Periodo,
    SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE 0 END)             AS Receita,
    SUM(CASE WHEN "Transaction Type" = 'debit'  THEN Amount ELSE 0 END)             AS Despesa,
    SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE 0 END) -
    SUM(CASE WHEN "Transaction Type" = 'debit'  THEN Amount ELSE 0 END)             AS Saldo
FROM transactions
GROUP BY User_ID, Periodo
ORDER BY User_ID, Periodo;


-- Q2: Total gasto por categoria (débitos), ranqueado por usuário
SELECT
    User_ID,
    Category,
    ROUND(SUM(Amount), 2)   AS Total_Gasto,
    COUNT(*)                AS Qtd_Transacoes
FROM transactions
WHERE "Transaction Type" = 'debit'
GROUP BY User_ID, Category
ORDER BY User_ID, Total_Gasto DESC;


-- Q3: Usuários com saldo negativo em mais de 50% dos meses
WITH saldo_mensal AS (
    SELECT
        User_ID,
        strftime('%Y-%m', Date) AS Periodo,
        SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE -Amount END) AS Saldo
    FROM transactions
    GROUP BY User_ID, Periodo
),
contagem AS (
    SELECT
        User_ID,
        COUNT(*)                                            AS Total_Meses,
        SUM(CASE WHEN Saldo < 0 THEN 1 ELSE 0 END)         AS Meses_Negativos
    FROM saldo_mensal
    GROUP BY User_ID
)
SELECT
    User_ID,
    Total_Meses,
    Meses_Negativos,
    ROUND(100.0 * Meses_Negativos / Total_Meses, 1)        AS Pct_Negativo
FROM contagem
WHERE ROUND(100.0 * Meses_Negativos / Total_Meses, 1) > 50
ORDER BY Pct_Negativo DESC;


-- Q4: Taxa de poupança média por usuário
WITH base AS (
    SELECT
        User_ID,
        strftime('%Y-%m', Date) AS Periodo,
        SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE 0 END) AS Receita,
        SUM(CASE WHEN "Transaction Type" = 'debit'  THEN Amount ELSE 0 END) AS Despesa
    FROM transactions
    GROUP BY User_ID, Periodo
)
SELECT
    User_ID,
    ROUND(AVG(CASE WHEN Receita > 0 THEN (Receita - Despesa) / Receita ELSE NULL END), 3) AS Taxa_Poupanca_Media
FROM base
GROUP BY User_ID
ORDER BY Taxa_Poupanca_Media DESC;


-- Q5: Gasto médio por categoria e conta (checking vs credit card)
SELECT
    "Account Name",
    Category,
    ROUND(AVG(Amount), 2)   AS Ticket_Medio,
    COUNT(*)                AS Qtd_Transacoes
FROM transactions
WHERE "Transaction Type" = 'debit'
GROUP BY "Account Name", Category
ORDER BY "Account Name", Ticket_Medio DESC;


-- ADD: Inserir novas queries conforme análise avança

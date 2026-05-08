-- Q1: Variação de despesas

SELECT
    User_ID,
    strftime('%Y-%m', Date) as Mes,
    ROUND(SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE 0 END), 2) as Entradas,
    ROUND(SUM(CASE WHEN "Transaction Type" = 'debit' THEN Amount ELSE 0 END), 2) as Saidas,
    ROUND(SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE 0 END) -
          SUM(CASE WHEN "Transaction Type" = 'debit' THEN Amount ELSE 0 END), 2) as Saldo_Mensal
FROM transacoes
GROUP BY User_ID, Mes
ORDER BY User_ID, Mes;


-- Q2: Ranking dos Gastos (Top 10 Categorias)

SELECT
    Category as Categoria,
    ROUND(SUM(Amount), 2) as Gasto_Total
FROM transacoes
WHERE "Transaction Type" = 'debit'
GROUP BY Category
ORDER BY Gasto_Total DESC
LIMIT 10;


-- Q3: Análise de Gastos Recorrentes

SELECT
    Description as Descricao,
    COUNT(DISTINCT strftime('%m', Date)) as Meses_Ativos,
    ROUND(AVG(Amount), 2) as Valor_Medio
FROM transacoes
WHERE "Transaction Type" = 'debit'
GROUP BY Description
HAVING Meses_Ativos >= 10
ORDER BY Meses_Ativos DESC;


-- Q4: Perfil de Pagamento

SELECT
    "Account Name" as Conta,
    COUNT(*) as Numero_de_Transacoes,
    ROUND(SUM(Amount), 2) as Total_Gasto
FROM transacoes
WHERE "Transaction Type" = 'debit'
GROUP BY "Account Name"
ORDER BY Total_Gasto DESC;


-- Q5: Usuários com saldo negativo recorrente

    WITH saldo_mensal AS (
        SELECT
            User_ID,
            strftime('%Y-%m', Date) AS Periodo,
            SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE -Amount END) AS Saldo
        FROM transacoes
        GROUP BY User_ID, Periodo
    ),
    contagem AS (
        SELECT
            User_ID,
            COUNT(*) AS Total_Meses,
            SUM(CASE WHEN Saldo < 0 THEN 1 ELSE 0 END) AS Meses_Negativos
        FROM saldo_mensal
        GROUP BY User_ID
    )
    SELECT
        User_ID,
        Total_Meses,
        Meses_Negativos,
        ROUND(100.0 * Meses_Negativos / Total_Meses, 1) AS Pct_Negativo
    FROM contagem
    WHERE Pct_Negativo > 50
    ORDER BY Pct_Negativo DESC


-- Q6: Taxa de Poupança Média por Usuário

    WITH base AS (
        SELECT
            User_ID,
            strftime('%Y-%m', Date) AS Periodo,
            SUM(CASE WHEN "Transaction Type" = 'credit' THEN Amount ELSE 0 END) AS Receita,
            SUM(CASE WHEN "Transaction Type" = 'debit'  THEN Amount ELSE 0 END) AS Despesa
        FROM transacoes
        GROUP BY User_ID, Periodo
    )
    SELECT
        User_ID,
        ROUND(AVG(CASE WHEN Receita > 0 THEN (Receita - Despesa) / Receita ELSE NULL END), 3) AS Taxa_Poupanca_Media
    FROM base
    GROUP BY User_ID
    ORDER BY Taxa_Poupanca_Media DESC



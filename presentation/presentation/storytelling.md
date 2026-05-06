# Storytelling - Hackathon Tema 1 (Comportamento Financeiro)

## 1. Problema
O acesso ao crédito e o comportamento financeiro das pessoas são temas centrais para entender desigualdades e riscos.  
Nosso desafio foi analisar uma base de transações pessoais (`personal_transactions_v2.csv`) e extrair padrões que ajudem a compreender hábitos e tendências.

---

## 2. Dados utilizados
- **Base principal:** `personal_transactions_v2.csv`  
  - Contém registros de transações financeiras pessoais.  
  - Inclui informações como data, valor e categoria da transação.  

---

## 3. Tratamento e Engenharia de Dados
- Limpeza e padronização dos dados.  
- Criação de banco SQLite para consultas SQL.  
- Estruturação da tabela `transactions` para permitir análises exploratórias.  
- Feature engineering inicial: agregações por período, categorias e valores médios.

---

## 4. Insights iniciais
- Identificação de padrões de consumo e movimentação financeira.  
- Distribuição das transações ao longo do tempo.  
- Primeiras visualizações que mostram comportamento agregado por categoria.  
- Ainda não realizamos correlação com variáveis externas (Selic, desemprego, inadimplência), mas o pipeline está preparado para integrar novas bases.

---

## 5. Próximos passos
- Integrar dados macroeconômicos (Selic, IBGE, Bacen).  
- Explorar relações entre comportamento individual e contexto econômico.  
- Construir modelos preditivos para identificar risco ou tendência de consumo.  

---

## 6. Impacto esperado
- Apoiar análises sobre comportamento financeiro individual.  
- Criar base sólida para futuras correlações com variáveis externas.  
- Contribuir para soluções que ampliem o entendimento sobre acesso ao crédito e hábitos de consumo.


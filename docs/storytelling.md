# 🎯 Storytelling 

> Documento de apoio para a apresentação de 8 minutos à banca avaliadora.

---

## Linha de Raciocínio

### 1. O Problema (45 seg)

> *"A maioria das pessoas sabe quanto ganha. Poucas sabem para onde esse dinheiro vai e menos ainda entendem o padrão por trás disso."*

Comportamentos financeiros não são aleatórios. Eles seguem padrões detectáveis e repetíveis: quem poupa regularmente tende a manter esse comportamento, e quem entra em ciclos de saldo negativo raramente percebe isso de forma clara, até que seja tarde demais.

**O problema de negócio:** Como identificar automaticamente o perfil financeiro de um usuário com base em seu histórico de transações sem precisar de regras manuais e usar isso para gerar insights acionáveis?

---

### 2. A Solução (1 min)

Desenvolvemos um sistema de análise de comportamento financeiro:

- **Dados:** 19.046 transações de 51 usuários 
- **Pipeline:** Da ingestão bruta até a predição de perfil, passando por limpeza, SQL, engenharia de features e Machine Learning
- **Modelo:** Clustering não supervisionado que descobre perfis naturais nos dados + classificador que generaliza esses perfis para novos usuários
- **Dashboard:** Painel interativo que comunica saúde financeira em tempo real

A escolha por clustering foi deliberada: **não definimos os perfis, deixamos os dados definirem.** Isso torna a solução mais honesta e escalável.

---

### 3. O Dado (1 min)

O dataset original ([Kaggle — Personal Finance](https://www.kaggle.com/datasets/bukolafatunde/personal-finance)) contém transações de um único usuário anônimo. **Nossa primeira contribuição técnica foi ampliar isso.**

Desenvolvemos um script Python (`data_generator.py`) que expande o dataset para 51 usuários distintos, criando uma base realista para análise comparativa entre perfis. Isso nos permite responder: *como o comportamento financeiro varia entre usuários ao longo do tempo?*

Durante o pré-processamento, filtramos movimentações que não refletem consumo real — pagamentos de fatura, transferências e aportes de investimento — para trabalhar apenas com **gasto real** e **receita real** de cada usuário. Essa decisão foi fundamental para que as features de saldo fizessem sentido analítico.

---

### 4. Os Insights (1 min 30 seg)

A análise exploratória e as queries SQL revelaram padrões claros de comportamento:

**Sobre os perfis descobertos pelo clustering:**

O K-Means identificou **3 grupos naturais** nos dados, sem nenhuma regra definida por nós:

| Perfil | Usuários | Taxa de Poupança | Meses no Vermelho | Investe? | Gasto Mensal Médio |
|---|---|---|---|---|---|
| **Investidor Estratégico** | 15 (29%) | +50,6% | 8% dos meses | ✅ Sim | US$ 2.489 |
| **Perfil Equilibrado** | 23 (45%) | +20,7% | 19,6% dos meses | ❌ Não | US$ 3.205 |
| **Em Risco Financeiro** | 13 (25%) | -108,3% | 83,1% dos meses | ❌ Não | US$ 6.070 |

**Destaques da análise:**

- O usuário **Em Risco** gasta em média **2,4x mais** do que o Investidor Estratégico, mas não necessariamente ganha mais
- O **Investidor Estratégico** guarda mais de **metade da sua renda** todos os meses e passa apenas 8% do tempo com saldo negativo
- O **Perfil Equilibrado** representa quase metade dos usuários: poupa 20,7% da renda, mas ainda não direcionou recursos para investimentos, é o perfil com maior potencial de conversão
- Usuários Em Risco passam **83% dos meses no vermelho** — um padrão consistente, não um evento pontual

---

### 5. O Modelo (1 min 30 seg)

**Etapa 1 — Clustering (K-Means):**

Utilizamos 6 features comportamentais normalizadas para encontrar os grupos naturais nos dados: taxa de poupança, frequência de meses negativos, presença de investimentos, volatilidade de gastos, dependência de crédito e volume médio de débitos.

Testamos k=2 até k=7 com Elbow Method e Silhouette Score. k=3 foi escolhido pela combinação de separação matemática e interpretabilidade de negócio.

| Métrica de Clustering | Valor |
|---|---|
| Silhouette Score (k=3) | 0,4539 |
| Variância explicada (PCA 2D) | ~77% |

**Etapa 2 — Classificador (Random Forest):**

O K-Means rotulou os 51 usuários atuais. O Random Forest aprendeu esses rótulos para **classificar qualquer usuário novo** com base em seu histórico de transações, sem precisar rodar o clustering novamente.

| Métrica do Classificador | Valor |
|---|---|
| Acurácia (CV-5 estratificado) | 98% ± 4% |
| F1-Weighted (CV-5) | 97,76% |
| F1-Macro (CV-5) | 97,17% |
| F1 — Investidor Estratégico | 1,00 |
| F1 — Perfil Equilibrado | 1,00 |
| F1 — Em Risco Financeiro | 1,00 |

**Features mais determinantes para a predição:**

| # | Feature | Importância |
|---|---|---|
| 1 | `avg_monthly_debit` — gasto mensal médio | 18,9% |
| 2 | `total_investment` — volume investido | 16,2% |
| 3 | `has_investment` — presença de investimentos | 15,5% |
| 4 | `savings_rate` — taxa de poupança | 14,2% |
| 5 | `avg_saldo` — saldo médio mensal | 13,1% |

*O modelo aprendeu que **quanto uma pessoa gasta e se ela investe** são os dois sinais mais fortes do seu perfil financeiro, o que faz sentido intuitivo e é facilmente comunicável.*

---

### 6. O Impacto (30 seg)

> *"Este sistema transforma dados brutos em comportamento compreensível e comportamento compreensível em decisões."*

Com este pipeline, uma instituição financeira ou aplicativo de finanças pessoais pode:

- **Identificar automaticamente** usuários em risco financeiro antes que o problema se agrave
- **Personalizar recomendações** de produtos: para o Investidor Estratégico, produtos de renda variável; para o Equilibrado, fundos de reserva; para o Em Risco, educação financeira e crédito consciente
- **Monitorar a evolução** do perfil ao longo do tempo, um usuário Em Risco que começa a poupar pode migrar para Equilibrado, e isso é mensurável

---

## Estrutura dos 8 Minutos

| Bloco | Tempo | Conteúdo |
|---|---|---|
| Problema + contexto | 45 seg | A dor financeira não é falta de renda — é falta de padrão reconhecível |
| O dado e o pipeline | 1 min | Dataset, expansão multi-usuário, fluxo EDA → SQL → features → ML |
| Insights do EDA + SQL | 1 min 30 seg | Tabela de perfis, diferença de gasto 2,4x, 83% meses negativos |
| Demonstração do dashboard | 1 min | Mostrar os 3 perfis no Power BI, filtros por usuário |
| Modelo de ML + resultados | 1 min 30 seg | K-Means → 3 clusters → RF → 98% CV accuracy → feature importance |
| Impacto e conclusão | 30 seg | Da transação ao perfil. Do perfil à decisão. |

---

## Frases de Impacto para a Apresentação

- *"19.046 transações. 51 usuários. 3 perfis que os dados escolheram — não nós."*
- *"Não construímos um relatório. Construímos um pipeline que pensa."*
- *"O usuário Em Risco gasta 2,4 vezes mais que o Investidor — e não percebe."*
- *"O modelo não precisa de regras. Ele aprende o comportamento."*
- *"45% dos usuários são Equilibrados: já poupam, mas ainda não investem. É o maior mercado desta análise."*

---

## Glossário dos Perfis para a Apresentação

| Perfil | Definição em uma frase |
|---|---|
| **Investidor Estratégico** | Poupa mais da metade da renda, investe ativamente e raramente fica no vermelho |
| **Perfil Equilibrado** | Mantém saldo positivo na maioria dos meses, mas ainda não direcionou recursos para investimentos |
| **Em Risco Financeiro** | Gasta mais do que ganha em 4 de cada 5 meses — padrão consistente, não pontual |

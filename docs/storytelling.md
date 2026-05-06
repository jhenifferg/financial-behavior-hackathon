# 🎯 Storytelling — Narrativa Executiva

> Documento de apoio para a apresentação de 8 minutos à banca avaliadora.

---

## Linha de Raciocínio

### 1. O Problema (30 seg)

> *"A maioria das pessoas sabe quanto ganha. Poucas sabem para onde esse dinheiro vai — e menos ainda entendem o padrão por trás disso."*

Comportamentos financeiros não são aleatórios. Eles seguem padrões detectáveis: quem poupa regularmente tende a manter esse comportamento, e quem entra em ciclos de dívida raramente percebe isso de forma clara.

**O problema de negócio:** Como identificar automaticamente o perfil financeiro de um usuário com base em seu histórico de transações — e usar isso para gerar insights acionáveis?

---

### 2. A Solução (1 min)

Desenvolvemos um sistema de análise de comportamento financeiro de ponta a ponta:

- **Dados:** 19.046 transações de 51 usuários ao longo de ~6 anos
- **Pipeline:** Da ingestão bruta até a predição de perfil, passando por limpeza, SQL e engenharia de features
- **Modelo:** Classificador que prediz se o usuário é *saver*, *debtor* ou *balanced*
- **Dashboard:** Painel interativo que comunica saúde financeira em tempo real

---

### 3. O Dado (1 min)

O dataset original ([Kaggle — Personal Finance](https://www.kaggle.com/datasets/bukolafatunde/personal-finance)) contém transações de um único usuário. **Nossa primeira contribuição técnica foi ampliar isso.**

Desenvolvemos um script Python (`data_generator.py`) que expande o dataset para múltiplos usuários com perfis distintos, criando uma base realista para análise comparativa. Isso nos permite responder: *como o comportamento de um poupador difere de um endividado ao longo do tempo?*

---

### 4. Os Insights (1 min)

> ADD: Preencher com resultados reais após EDA e SQL.

Exemplos de insights esperados:

- **Categorias críticas por perfil:** Usuários `debtor` tendem a gastar X% mais em restaurantes e compras espontâneas em relação à sua receita mensal
- **Sazonalidade:** Meses de dezembro e janeiro concentram os maiores picos de gasto para todos os perfis
- **Variação MoM:** Usuários `balanced` têm a menor volatilidade de despesas mês a mês (desvio padrão < X%)
- **Taxa de poupança:** Apenas X% dos usuários `saver` têm taxa de poupança positiva consistente em mais de 80% dos meses

---

### 5. O Modelo (1 min)

Treinamos um **Random Forest** para classificar o perfil financeiro de novos usuários.

| Métrica | Valor |
|---|---|
| Acurácia | ADD |
| F1-Score (saver) | ADD |
| F1-Score (debtor) | ADD |
| F1-Score (balanced) | ADD |

**Features mais importantes para a predição:**
1. ADD (preencher após treinar o modelo)
2. ADD
3. ADD

*Isso significa que o modelo aprendeu que [interpretação da feature mais importante] é o principal indicador de perfil financeiro.*

---

### 6. O Impacto (30 seg)

> *"Este sistema transforma dados brutos em comportamento compreensível — e comportamento compreensível em decisões."*

Com este pipeline, uma instituição financeira ou aplicativo de finanças pessoais pode:
- Identificar automaticamente usuários em risco financeiro
- Personalizar recomendações de produtos (ex: linhas de crédito, aplicações)
- Monitorar evolução do perfil ao longo do tempo via dashboard

---

## Estrutura dos 5 Minutos

| Bloco | Tempo | Responsável |
|---|---|---|
| Problema + contexto | 30 seg | ADD |
| Demonstração do pipeline (fluxo de dados) | 1 min | ADD |
| Insights do EDA + SQL | 1 min | ADD |
| Demonstração do dashboard | 1 min | ADD |
| Modelo de ML + resultados | 1 min | ADD |
| Impacto e conclusão | 30 seg | ADD |

---

## Frases de Impacto para a Apresentação

- *"19 mil transações. 51 usuários. Um padrão claro."*
- *"Não construímos um relatório. Construímos um pipeline que pensa."*
- *"O modelo não apenas descreve — ele prediz."*

---

> **Nota:** Preencher os campos ADD com dados reais após finalizar EDA, SQL e treinamento do modelo.

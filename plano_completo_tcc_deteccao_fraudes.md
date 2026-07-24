# Projeto de Machine Learning para Detecção de Fraudes em Cartão de Crédito

## Visão geral

Este documento consolida o plano oficial do TCC, estruturado para apresentar o projeto como uma solução completa de apoio à detecção de fraudes, conectando:

```text
Transações
    ↓
Modelo de machine learning
    ↓
Score de risco
    ↓
Política de decisão
    ↓
APROVAR | REVISAR | ALERTA_CRÍTICO
    ↓
Simulador operacional
    ↓
Persistência no SQLite
    ↓
Dashboard de acompanhamento
```

O diferencial do trabalho está na integração entre **modelo, decisão, operação e visualização**.

---

# 1. Problema

## Objetivo

Desenvolver e avaliar um protótipo de apoio à detecção de transações fraudulentas em cartões de crédito, considerando o forte desbalanceamento entre transações legítimas e fraudulentas.

## Pontos que devem ser apresentados

- Impacto das fraudes em cartões de crédito.
- Dificuldade de identificar uma classe extremamente rara.
- Limitações do uso da acurácia em bases desbalanceadas.
- Impactos dos falsos positivos.
- Impactos dos falsos negativos.
- Necessidade de transformar previsões em decisões operacionais.

---

# 2. Parte experimental

Esta etapa deve responder à seguinte pergunta:

> Qual modelo e qual estratégia de tratamento do desbalanceamento apresentam o melhor desempenho para o problema estudado?

## Etapas contempladas

- Análise exploratória da base.
- Divisão temporal entre treino, validação e teste.
- Pré-processamento.
- Comparação dos modelos.
- Comparação das estratégias de desbalanceamento.
- Seleção do modelo.
- Avaliação final no conjunto de teste.

## Modelos avaliados

- Regressão Logística.
- Random Forest.
- HistGradientBoosting.

## Estratégias de tratamento do desbalanceamento

- Sem tratamento.
- `class_weight`.
- RandomUnderSampler.
- SMOTE.

## Modelo selecionado

Regressão Logística com:

- `C = 0.1`
- `class_weight="balanced"`
- remoção da variável `Time`
- padronização de `Amount`
- preservação de `V1` até `V28`

## Métricas principais

- Average Precision.
- Precision.
- Recall.
- ROC-AUC.
- Matriz de confusão.

A **Average Precision** deve permanecer como métrica principal para seleção do modelo.

---

# 3. Parte decisória

Esta etapa deve responder:

> Como transformar o score gerado pelo modelo em uma ação operacional?

O modelo não retorna diretamente uma decisão como “aprovar” ou “bloquear”. Ele gera um score de risco, que será convertido em três faixas operacionais.

```text
Score abaixo do threshold de revisão
→ APROVAR

Score entre o threshold de revisão e o threshold crítico
→ REVISAR

Score igual ou acima do threshold crítico
→ ALERTA_CRÍTICO
```

## Thresholds congelados

```text
threshold_review:
0.885050705154475

threshold_critical:
0.9999575722567711
```

Esses thresholds foram definidos no conjunto de validação e permaneceram congelados antes da avaliação final no conjunto de teste.

## Significado operacional

### APROVAR

Transações consideradas de baixo risco pelo modelo.

Não são encaminhadas para análise manual.

### REVISAR

Transações com risco elevado, mas sem evidência suficiente para serem tratadas como alertas críticos.

Formam uma fila de análise.

### ALERTA_CRÍTICO

Transações com score extremamente alto.

Possuem prioridade máxima na fila de investigação.

---

# 4. Parte operacional

Esta etapa deve responder:

> Como essa política funcionaria durante o processamento individual das transações?

## Fluxo de processamento

Para cada transação, o sistema:

1. Lê a transação.
2. Executa o mesmo pré-processamento utilizado no treinamento.
3. Calcula o score de fraude.
4. Aplica os thresholds congelados.
5. Define a decisão.
6. Persiste o resultado.
7. Atualiza o estado da execução.

## Componentes

- Modelo treinado.
- Pipeline de pré-processamento.
- Thresholds congelados.
- Processador de transações.
- Banco SQLite.
- Modo WAL.
- Controle de execução.
- Fila de revisão.
- Fila de alertas críticos.

## Resultado do replay

Foram processadas sequencialmente:

```text
56.962 transações
```

Distribuição final:

| Decisão | Quantidade |
|---|---:|
| APROVAR | 56.674 |
| REVISAR | 231 |
| ALERTA_CRÍTICO | 57 |

O replay reproduziu exatamente os resultados oficiais da avaliação congelada.

## Resultado operacional: revisar ou crítico

| Métrica | Resultado |
|---|---:|
| Transações encaminhadas | 288 |
| Fraudes identificadas | 64 |
| Falsos positivos | 224 |
| Fraudes não identificadas | 11 |
| Recall | 85,33% |
| Precision | 22,22% |

Narrativa sugerida:

> O sistema encaminhou aproximadamente 0,51% das transações para algum nível de análise e identificou 85,33% das fraudes existentes no conjunto de teste.

## Resultado operacional: somente crítico

| Métrica | Resultado |
|---|---:|
| Alertas críticos | 57 |
| Fraudes identificadas | 51 |
| Falsos positivos | 6 |
| Recall | 68,00% |
| Precision | 89,47% |

Narrativa sugerida:

> Aproximadamente nove em cada dez alertas críticos correspondiam a fraudes reais.

---

# 5. Parte demonstrativa

A parte demonstrativa será composta por um dashboard para acompanhamento do simulador.

O objetivo não é construir um sistema bancário completo, mas uma interface que permita visualizar o funcionamento do protótipo.

## Tecnologia recomendada

**Streamlit**, consultando diretamente o banco SQLite.

## Componentes que não serão adicionados

- Kafka.
- Microsserviços.
- Autenticação.
- AWS.
- APIs externas.
- WebSocket.
- Banco em nuvem.
- Infraestrutura distribuída.

## Estrutura do dashboard

### 5.1 Visão geral

Cards com:

- Total de transações.
- Transações processadas.
- Percentual concluído.
- Transações aprovadas.
- Transações em revisão.
- Alertas críticos.

### 5.2 Distribuição das decisões

Gráfico com as quantidades de:

```text
APROVAR
REVISAR
ALERTA_CRÍTICO
```

### 5.3 Fila de revisão

Tabela com:

- Identificador da transação.
- `Time`.
- `Amount`.
- Score.
- Decisão.
- Momento do processamento.

### 5.4 Alertas críticos

Tabela separada contendo apenas as transações prioritárias.

### 5.5 Avaliação experimental

No modo de replay, o dashboard também poderá exibir:

- Classe real.
- Verdadeiro positivo.
- Falso positivo.
- Falso negativo.
- Matriz de confusão.
- Precision.
- Recall.
- Average Precision.
- ROC-AUC.

A classe real deve ser apresentada como uma informação disponível apenas no ambiente acadêmico de avaliação.

---

# 6. Estrutura recomendada dos capítulos

## Capítulo 1 — Introdução

- Contextualização.
- Problema.
- Justificativa.
- Objetivo geral.
- Objetivos específicos.
- Organização do trabalho.

## Capítulo 2 — Fundamentação teórica

- Fraude em cartões.
- Classificação supervisionada.
- Desbalanceamento.
- Regressão Logística.
- Random Forest.
- HistGradientBoosting.
- Undersampling.
- SMOTE.
- Métricas.
- Thresholds.
- Políticas de decisão.

## Capítulo 3 — Metodologia

- Descrição do dataset.
- Análise das variáveis.
- Separação temporal.
- Pré-processamento.
- Experimentos.
- Critérios para escolha do modelo.
- Definição dos thresholds.

## Capítulo 4 — Resultados experimentais

- Comparação dos modelos.
- Comparação dos tratamentos de desbalanceamento.
- Escolha da Regressão Logística.
- Resultados de validação.
- Resultados finais no teste.

## Capítulo 5 — Política de decisão

- Score.
- Threshold de revisão.
- Threshold crítico.
- APROVAR.
- REVISAR.
- ALERTA_CRÍTICO.
- Impacto operacional.

## Capítulo 6 — Simulador operacional

- Arquitetura.
- Processamento sequencial.
- Persistência.
- SQLite/WAL.
- Controle da execução.
- Equivalência com a avaliação oficial.

## Capítulo 7 — Dashboard

- Objetivos.
- Telas.
- Indicadores.
- Filas.
- Visualização dos alertas.
- Demonstração do replay.

## Capítulo 8 — Conclusão

- Principais resultados.
- Contribuições.
- Limitações.
- Trabalhos futuros.

---

# 7. Objetivo geral sugerido

> Desenvolver e avaliar um protótipo de apoio à detecção de fraudes em transações de cartões de crédito utilizando técnicas de aprendizado de máquina, contemplando a comparação de modelos em um cenário altamente desbalanceado, a definição de uma política operacional baseada em níveis de risco, a simulação do processamento sequencial das transações e a visualização dos resultados por meio de um dashboard.

---

# 8. Objetivos específicos

- Analisar as características e limitações do conjunto de dados utilizado.
- Comparar algoritmos de classificação.
- Avaliar estratégias para tratamento do desbalanceamento.
- Selecionar o modelo com melhor desempenho segundo métricas adequadas.
- Definir thresholds operacionais utilizando o conjunto de validação.
- Classificar as transações em `APROVAR`, `REVISAR` e `ALERTA_CRÍTICO`.
- Desenvolver um simulador de processamento sequencial.
- Persistir o estado e os resultados das transações.
- Construir um dashboard para acompanhamento da execução e dos alertas.
- Avaliar o impacto da política em termos de fraudes detectadas e carga de revisão.

---

# 9. Regra oficial de escopo

O projeto não será expandido com:

- Novos modelos sem necessidade.
- Redes neurais.
- Infraestrutura em nuvem.
- Integrações externas.
- Kafka.
- Microsserviços.
- Autenticação.
- Processamento distribuído.
- Retreinamento contínuo.
- Concept drift completo.
- Novo dataset principal.
- Alteração dos thresholds com base no conjunto de teste.

## Foco daqui em diante

1. Consolidar a documentação das fases já concluídas.
2. Implementar o dashboard.
3. Produzir os gráficos e tabelas finais.
4. Escrever o TCC seguindo esta estrutura.
5. Preparar a demonstração.
6. Preparar a apresentação.

---

# 10. Posicionamento final do projeto

O projeto deve ser apresentado como:

> Um protótipo completo de apoio à detecção de fraudes, que conecta a seleção do modelo, a definição de uma política de decisão, o processamento sequencial das transações, a persistência dos resultados e a visualização operacional por meio de um dashboard.

Evitar apresentar o trabalho apenas como:

> Um projeto que treinou alguns algoritmos em um dataset do Kaggle.

A narrativa central deve destacar que o projeto integra:

- análise experimental;
- decisão operacional;
- simulação;
- persistência;
- monitoramento visual.

Esse escopo é suficientemente completo, técnico e atraente para um TCC, sem torná-lo inviável dentro do tempo disponível.

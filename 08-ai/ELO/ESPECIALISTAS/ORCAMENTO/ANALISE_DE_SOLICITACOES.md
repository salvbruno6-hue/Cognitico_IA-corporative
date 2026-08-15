# Domínio Operacional — Análise de Solicitações

**Especialista:** Orçamento  
**Governança:** ELO  
**Status:** Oficial

## 1. Finalidade do domínio

`Análise de Solicitações` é o domínio operacional em que o Especialista de Orçamento recebe o contexto da SO, o direcionamento do ELO e executa o processo de orçamento.

O ELO atua como camada de análise, direcionamento, checklist, conferência e contestação.

O Especialista de Orçamento é responsável por toda a execução do orçamento.

## 2. Gatilhos oficiais

### Gatilho 1 — `ELO ANALISAR`

Quando acionado em **Análise de Solicitações**, o ELO deve:

1. analisar a SO e documentos válidos;
2. interpretar a necessidade do cliente;
3. identificar se é VENDA ou LOCAÇÃO;
4. identificar o escopo;
5. identificar famílias comerciais;
6. indicar taxonomias compatíveis;
7. apontar quantitativos e pontos que precisam ser conferidos;
8. identificar excedentes, customizações e itens especiais;
9. identificar serviços, materiais e necessidades de mão de obra relevantes;
10. identificar riscos, interfaces e responsabilidades;
11. gerar o **Checklist ELO**;
12. gerar o **Direcionamento ao Especialista de Orçamento**.

O resultado de `ELO ANALISAR` é uma orientação estruturada para o orçamento. O ELO não executa a composição detalhada nem a precificação.

### Gatilho 2 — `ORÇAR`

Quando acionado após a análise do ELO, o gatilho transfere a execução para o **Especialista de Orçamento**.

O Especialista deve:

1. receber o direcionamento do ELO;
2. revisar os documentos válidos e o contexto disponível;
3. executar toda a automação de orçamento;
4. alimentar 1.0 COMERCIAL;
5. alimentar 2.0 COMPOSIÇÃO;
6. executar cálculos;
7. aplicar BDI;
8. aplicar Taxa de Administração quando aplicável;
9. gerar o orçamento;
10. após gerar o orçamento, executar a fusão dos PTs TEC e dos pós-orçamento;
11. consolidar a entrega final.

## 3. Responsabilidades

### ELO

- analisar a SO;
- gerar checklist;
- direcionar o especialista;
- apontar riscos e omissões;
- conferir o orçamento produzido;
- conferir a fusão dos PTs TEC e dos pós-orçamento;
- contestar quando encontrar inconsistência;
- solicitar ajuste quando necessário.

### Especialista de Orçamento

- interpretar o direcionamento;
- executar o orçamento completo;
- selecionar e organizar itens comerciais;
- compor serviços;
- compor materiais;
- compor mão de obra interna;
- compor mão de obra externa;
- precificar;
- aplicar regras comerciais;
- calcular o fechamento;
- gerar orçamento;
- fazer a fusão dos PTs TEC;
- fazer a fusão dos pós-orçamento;
- consolidar a entrega;
- corrigir o orçamento quando o ELO contestar.

## 4. Fluxo oficial

```text
ANÁLISE DE SOLICITAÇÕES
        |
        | GATILHO: ELO ANALISAR
        v
ELO ANALISA
        |
        +-- Checklist ELO
        +-- Direcionamento
        +-- Riscos
        +-- Pendências
        +-- Taxonomias a avaliar
        |
        v
ANÁLISE CONCLUÍDA
        |
        | GATILHO: ORÇAR
        v
ESPECIALISTA DE ORÇAMENTO
        |
        +-- 1.0 Comercial
        +-- 2.1 Serviços
        +-- 2.2 Materiais
        +-- 2.3 MO Interna
        +-- 2.4 MO Externa
        +-- Cálculos
        +-- BDI
        +-- Taxa de Administração
        +-- Geração do orçamento
        |
        v
ORÇAMENTO GERADO
        |
        v
ESPECIALISTA DE ORÇAMENTO
        |
        +-- Fusão PTs TEC
        +-- Fusão Pós-Orçamento
        +-- Consolidação Final
        |
        v
ELO CONFERE
        |
        +-- OK
        |
        +-- CONTESTAÇÃO
                |
                v
        ORÇAMENTISTA AJUSTA
                |
                v
        ELO CONFERE NOVAMENTE
```

## 5. Regra de domínio

O domínio do Especialista é identificado pelo processo em que ele atua.

**Especialista em Orçamento → `Análise de Solicitações`**

A pasta do especialista pode conter as instruções e artefatos específicos do especialista, mas o processo operacional permanece nomeado como `Análise de Solicitações`.

## 6. Separação de execução e auditoria

Regra permanente:

> **ELO orienta e audita. Especialista de Orçamento executa.**

O ELO não deve assumir a execução detalhada do orçamento, cálculo de custos, montagem da planilha, fusão dos PTs TEC ou fusão dos pós-orçamento.

O Especialista não deve alterar as diretrizes oficiais do ELO. Melhorias permanentes devem ser propostas como nova diretriz, conforme a governança existente.

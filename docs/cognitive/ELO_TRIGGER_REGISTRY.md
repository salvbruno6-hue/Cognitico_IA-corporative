# ELO — REGISTRO DE GATILHOS

## ELO ANALISAR

**Comando:** `ELO ANALISAR`

**Modo ativado:** `ANÁLISE DE SOLICITAÇÕES / ORÇAMENTO ESPECIALISTA MULTITEINER`

**Arquitetura canônica:** `01-meta-architecture/cognitive-architecture/ELO_ANALISE_SOLICITACOES_ARQUITETURA_CANONICA.md`

**Diretriz operacional:** `00-core/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`

**Gatilho:** iniciar/acionar a análise de uma SO/LIC no fluxo de Análise de Solicitações.

**Escopo:** Comercial, Licitações, Planejamento e Engenharia de Orçamento.

**Regra de execução:** o gatilho é uma porta de entrada; não duplica nem reescreve o motor de orçamento. O ELO orquestra e audita; o Especialista de Orçamento executa.

**Fontes especializadas são consultadas conforme necessidade:**

- PTS Técnica;
- Especialista de Orçamento;
- camada de excedentes;
- taxonomia/SQL;
- memória de cálculo;
- PTS Pós-Orçamento;
- aprendizado validado.

**Resposta inicial obrigatória:**

> **ELO ANALISAR ATIVADO**
>
> Vou conduzir esta SO/LIC pelo fluxo de Análise de Solicitações, utilizando documentos vigentes, conhecimento validado, PTS Técnica, Especialista de Orçamento, PTS Pós e memória de aprendizado conforme aplicável.

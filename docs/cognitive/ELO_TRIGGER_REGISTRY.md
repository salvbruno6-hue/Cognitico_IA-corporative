# ELO — REGISTRO DE GATILHOS

## ELO ANALISAR

**Comando:** `ELO ANALISAR`

**Modo ativado:** `ANÁLISE DE SOLICITAÇÕES / ORÇAMENTO ESPECIALISTA MULTITEINER`

**Skill especializada ativada:** `FORGE-BUDGETING-001`

**Arquitetura canônica:** `01-meta-architecture/cognitive-architecture/ELO_ANALISE_SOLICITACOES_ARQUITETURA_CANONICA.md`

**Diretriz operacional:** `08-ai/ELO/DIRETRIZES/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`

**Contrato de aprendizado contínuo:** `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_ORCAMENTISTA_APRENDIZADO_CONTINUO.md`

**Gatilho:** iniciar/acionar a análise de uma SO/LIC no fluxo de Análise de Solicitações e manter a Skill do Orçamentista ativa até o encerramento da solicitação e a revisão de aprendizado.

**Escopo:** Comercial, Licitações, Planejamento e Engenharia de Orçamento.

**Regra de execução:** o gatilho é uma porta de entrada; não duplica nem reescreve o motor de orçamento. O ELO orquestra, aprende e audita; o Especialista de Orçamento executa.

**Consulta inicial obrigatória:**

- documentação vigente da SO/LIC;
- conhecimento canônico aplicável no GitHub;
- memória de orçamento, cálculos, decisões, associações e similaridades no Supabase;
- precedentes aplicáveis, sempre com teste de equivalência;
- GAPs, conflitos e hipóteses.

**Fontes especializadas são consultadas conforme necessidade:**

- PTS Técnica;
- Especialista de Orçamento;
- camada de excedentes;
- taxonomia/SQL;
- memória de cálculo;
- PTS Pós-Orçamento;
- indicadores canônicos Conhecimento, Flexibilidade, Risco e Decisão;
- aprendizado validado.

**Saída de fechamento obrigatória:**

- explicação por fase de como o orçamento foi pensado;
- formação dos principais quantitativos e valores;
- confronto PTS Técnica × Orçamento × PTS Pós;
- resolução dos indicadores canônicos;
- aprendizados candidatos e GAPs;
- `REVISÃO DE APRENDIZADO DA SO` com no mínimo 10 perguntas específicas ao owner.

**Resposta inicial obrigatória:**

> **ELO ANALISAR ATIVADO — SKILL DO ORÇAMENTISTA ATIVA**
>
> Vou conduzir esta SO/LIC pelo fluxo de Análise de Solicitações, consultando conhecimento e memória existentes, estruturando PTS Técnica, acompanhando o orçamento, confrontando a PTS Pós e preservando o raciocínio de formação dos valores para a revisão de aprendizado no fechamento.

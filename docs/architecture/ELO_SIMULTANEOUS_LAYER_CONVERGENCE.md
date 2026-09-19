# ELO — Convergência Simultânea das Camadas

## Status

`NORMATIVE / IMPLEMENTATION STRATEGY`

## Objetivo

Executar a evolução do ELO em paralelo entre as camadas, mantendo uma única arquitetura, uma única autoridade cognitiva e contratos compartilhados.

## Regra

As camadas evoluem simultaneamente, mas cada mudança possui um proprietário canônico. O trabalho paralelo não autoriza duplicação de Core, memória, roteador, governança ou integração.

## Frentes simultâneas

1. **Casa:** identidade, tenant, autenticação e workspace.
2. **Cognitive:** seleção de capacidade, modelo, ferramenta, decomposição, crítica e decisão.
3. **Interoperability:** adapters, gateway, provenance e providers.
4. **Learning:** experiência, evidência, candidato, validação e promoção.
5. **Agents:** execução governada e especialistas.
6. **Workflow:** automação, observação, resultado e aprendizagem.
7. **Corporate domains:** orçamento como primeiro POC real, seguido pelos demais domínios.
8. **Evolution:** métricas, evidências, regressão e evolução arquitetural.

## Loop integrado

```text
USUÁRIO
  ↓
CASA / IDENTITY / TENANT
  ↓
MISSÃO
  ↓
COGNITIVE
  ├─ decomposição
  ├─ especialista
  ├─ capacidade
  └─ Intelligence Router
        ↓
INTEROPERABILITY
  ├─ provider
  ├─ modelo
  └─ ferramenta
        ↓
CONTEXTO + EVIDÊNCIA
        ↓
EXECUÇÃO
        ↓
CRÍTICA / DECISÃO
        ↓
RESULTADO
        ↓
EXPERIENCE / LEARNING LABORATORY
        ↓
VALIDATION / EVOLUTION GATE
        ↓
MEMÓRIA / CONHECIMENTO VALIDADO
        ↓
NOVAS MISSÕES
```

## Primeira missão real

O primeiro POC integrado deve ser orçamento. O ELO deve receber uma solicitação simples, recuperar o conhecimento permitido, identificar as necessidades do orçamento, selecionar capacidade/modelo/ferramenta, produzir briefing contextualizado, executar através do adapter governado, apresentar cálculo/observações/premissas/evidências e registrar a experiência.

A arquitetura de orçamento existente contém guias, metodologia, memória de cálculo e diretrizes específicas que devem ser reutilizadas, não recriadas.

## Critério de evolução

Nenhuma frente é considerada pronta apenas porque possui arquivo ou contrato. O estado deve distinguir arquitetura, implementação, teste, evidência, POC e operação.

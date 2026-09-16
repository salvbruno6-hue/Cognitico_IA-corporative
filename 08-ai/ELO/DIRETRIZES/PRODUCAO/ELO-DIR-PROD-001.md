# ELO-DIR-PROD-001 — Governança da Estrutura de Produção

**Status:** PROPOSTA PARA VALIDAÇÃO
**Versão:** 1.0
**Domínio:** PRODUÇÃO
**Autoridade:** ELO Cognitivo
**Fonte canônica:** GitHub

## 1. Finalidade

Definir o contrato mínimo para que o ELO reconheça, analise e posteriormente opere sobre estruturas de Produção sem criar autoridade paralela ao processo corporativo.

## 2. Aplicação

Aplica-se às relações entre:

`PCP → PRODUÇÃO → QUALIDADE → LOGÍSTICA → RESULTADO/PÓS-EXECUÇÃO`

e às interfaces com:

`ORÇAMENTO → COMPRAS → PRODUÇÃO`

## 3. Validação mínima de uma Ordem de Produção

Antes de considerar uma Ordem de Produção operacionalmente válida, verificar:

| Critério | Evidência mínima |
|---|---|
| Origem | Ordem PCP identificada |
| Demanda | AF vinculada |
| Fluxo | MODULAR, CUSTOMIZADO ou RECUPERACAO conforme modelo existente |
| Materiais | Lista-Material identificada e versionada quando aplicável |
| Quantidades | Quantidades suportadas pela fonte de planejamento |
| Etapas | Etapas identificadas e sequenciadas |
| Execução | Início/fim ou apontamento equivalente quando disponível |
| Qualidade | Inspeção associável à produção/etapa quando aplicável |
| Retrabalho | Explicitamente identificado quando ocorrer |
| Rastreabilidade | Evento de processo com objeto de origem |
| Exceções | Sinais, divergências ou pendências registrados |
| Autorização | Ação que altere o processo deve possuir responsável/gate definido |

## 4. Estados

Os estados devem ser tratados como dados operacionais e não como inferências livres do modelo:

`PLANEJADA → LIBERADA → EM_PRODUCAO → INSPECAO → CONCLUIDA`

Estados de exceção devem ser explicitamente registrados, por exemplo:

`BLOQUEADA`, `AGUARDANDO_MATERIAL`, `RETRABALHO`.

A adoção definitiva desses estados requer validação do fluxo real da Multiteiner.

## 5. Proibições

O ELO não deve:

- inventar capacidade;
- inventar tempos padrão;
- inventar sequência física;
- inventar produtividade;
- marcar uma ordem como concluída sem evidência;
- transformar recomendação em ordem operacional;
- alterar produção sem autorização;
- criar uma tabela equivalente quando já existir estrutura adequada;
- promover aprendizado de um caso isolado para regra geral sem validação.

## 6. Fluxo de decisão

```text
DADO
 ↓
EVIDÊNCIA
 ↓
VALIDAÇÃO ESTRUTURAL
 ↓
ANÁLISE
 ↓
RECOMENDAÇÃO
 ↓
ARBITRAGEM / AUTORIZAÇÃO
 ↓
EXECUÇÃO
 ↓
RESULTADO
 ↓
LEARNING CANDIDATE
 ↓
GOVERNED LEARNING / EVOLUTION GATE
```

## 7. Relação com o modelo físico

Este documento não autoriza alteração imediata do banco. O modelo lógico existente deve ser auditado primeiro. Qualquer alteração física deverá demonstrar:

1. lacuna real;
2. inexistência de estrutura reutilizável;
3. contrato de dados;
4. impacto nas relações existentes;
5. migração segura;
6. testes;
7. evidência de validação;
8. Evolution Gate quando houver evolução canônica.

## 8. Relação com ELO Web

O ELO Web poderá apresentar Produção somente por dados provenientes da camada cognitiva/API governada. A interface não será autoridade para:

- criar regra canônica;
- aprovar capacidade;
- alterar ordens sem autorização;
- promover aprendizado;
- alterar Core ou Soul.

## 9. Critério de promoção

Esta diretriz permanece `PROPOSTA PARA VALIDAÇÃO` até que o fluxo real de Produção seja confrontado com evidências operacionais e arbitrado pelo responsável competente.

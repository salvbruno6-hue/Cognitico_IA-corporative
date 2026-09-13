# PTS-POS-001 — Ponto Operacional Estruturado do ELO

**Status:** DRAFT  
**Autoridade cognitiva:** ELO Cognitivo  
**Persistência:** Supabase  
**Fonte canônica de implementação:** GitHub

## Finalidade

Estruturar um ponto operacional rastreável para conectar contexto, evidência, análise, decisão e evolução governada sem criar autoridade paralela.

## Escopo

- CORE
- FORGE
- APPLICATION
- INFRASTRUCTURE

## Tipo

`GOVERNED_OPERATIONAL_POINT`

## Governança

- Autoridade: `ELO_COGNITIVO`
- Aprendizado: `DECISAO_ARBITRADA`
- Evolution Gate: obrigatório
- GitHub: autoridade canônica de implementação
- Supabase: autoridade persistente dos dados

## Integrações de domínio

- DOM
- PCP
- ORÇAMENTO
- QUALIDADE
- LOGÍSTICA
- CORPORATE_LEARNING

## Fronteira Web

`ELO_WEB -> ELO_COGNITIVE_API -> governed execution`

## Modelo operacional

```text
CONTEXTO
   ↓
EVIDÊNCIA
   ↓
ANÁLISE
   ↓
ARBITRAÇÃO
   ↓
DECISÃO
   ↓
VALIDAÇÃO
   ↓
EVOLUTION GATE
   ↓
CONHECIMENTO CANÔNICO
```

## Regra de autoridade

PTS-POS não é autoridade paralela. O registro operacional pode ser criado, analisado e atualizado dentro das permissões governadas, mas a promoção de conhecimento para o CORE depende de evidência, decisão arbitrada, validação e Evolution Gate.

## Registro Supabase

Tabela: `public.elo_pts_pos`  
Registro inicial: `PTS-POS-001`

Campos principais:

- `pts_pos_id`
- `pts_pos_code`
- `title`
- `pos_type`
- `status`
- `domain`
- `scope`
- `objective`
- `source_reference`
- `source_system`
- `evidence`
- `analysis`
- `decision`
- `governance`
- `links`
- `confidence`
- `owner_identity_id`
- `related_decision_id`
- `related_learning_id`
- `created_at`
- `updated_at`

## Estados

`DRAFT -> ANALYSIS -> EVIDENCED -> ARBITRATION -> VALIDATED -> CANONICAL -> ARCHIVED`

## Critério de promoção

Nenhum PTS-POS deve ser promovido a `CANONICAL` ou incorporado ao CORE apenas por criação do registro. A transição exige evidência suficiente, decisão arbitrada, validação e passagem pelo Evolution Gate.

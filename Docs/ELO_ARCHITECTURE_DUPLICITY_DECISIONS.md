# ELO — Architecture Duplicity Decision Register

## Objetivo
Registrar decisões verificáveis sobre candidatos a duplicidade arquitetural sem confundir especialização técnica com duplicidade semântica.

## Lote auditado

### 1. `01-meta-architecture/ELO_ARCHITECTURE_MASTER.md`
- `artifact_id`: `ELO.ARCH.01.MASTER`
- `concept_id`: `ELO.ARCHITECTURE.MASTER`
- decisão: `CANONICAL_OWNER`
- evidência: declara explicitamente Artifact ID, Concept ID, autoridade ARCHITECTURE e migração do caminho histórico.

### 2. `01-meta-arquitetura/ELO_ARCHITECTURE_MASTER.md`
- classificação: `HI/LEGACY_REPRESENTATION`
- decisão: não tratar como segunda autoridade.
- motivo: o arquivo canônico informa explicitamente esse caminho como `Legacy path`; a versão histórica não contém contrato de canonicalização.
- ação: preservar rastreabilidade até consumidores/referências serem migrados; não remover nesta etapa.

### 3. `docs/architecture/ELO_TECHNICAL_ARCHITECTURE_MASTER.md`
- classificação: `SPECIALIZED_ARCHITECTURE`
- decisão: preservar como arquitetura técnica especializada.
- motivo: define camadas técnicas, APIs, Core, agentes, memória, dados, automação e dependências de infraestrutura. Não substitui o owner de arquitetura corporativa.

### 4. `docs/architecture/ELO_AI_Ecosystem_Platform_Architecture_Exaustivo_Tecnico.md`
- classificação: `SPECIALIZED_COMPLEMENTARY`
- decisão: preservar.
- motivo: define arquitetura específica do ecossistema de IA e declara integração com a baseline técnica e outros masters. Não deve ser convertido em segundo owner da arquitetura corporativa.

## Resultado do lote

- 1 owner canônico confirmado.
- 1 representação histórica identificada.
- 2 arquiteturas especializadas preservadas por função distinta.
- Nenhuma remoção física autorizada.
- Nenhuma autoridade paralela criada.

## Próximo gate
Mapear consumidores e referências do caminho histórico antes de qualquer remoção/depreciação física.

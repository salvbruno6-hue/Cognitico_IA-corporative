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

### 5. `02-architecture-library/ELO_PR1_FILE_DECISION_REGISTER.yaml`
- classificação: `GOVERNANCE_REGISTER`
- decisão: preservar.
- motivo: é registro de governança/proveniência e não substitui o Master.

### 6. `02-architecture-library/ELO_PR1_RECONCILIATION_MATRIX.md`
- classificação: `GOVERNANCE_MATRIX`
- decisão: preservar.
- motivo: é matriz de reconciliação e controle da migração histórica, não uma segunda arquitetura.

## Resultado verificável do lote

- 1 owner canônico de arquitetura corporativa confirmado.
- 1 representação histórica do mesmo Master identificada.
- 2 arquiteturas especializadas preservadas por função distinta.
- 2 artefatos de governança/reconciliação preservados por função distinta.
- 0 autoridades paralelas autorizadas.
- 0 remoções físicas autorizadas.
- 0 conteúdos eliminados por semelhança nominal.

## Próximo gate
Mapear consumidores e referências do caminho histórico e verificar se existe outro artefato que declare a mesma autoridade/concept_id antes de qualquer depreciação ou remoção.

# ELO — Evidência Contextual da Família 00 — Enterprise Manifest

## Estado
`CONTEXTUAL_AUDIT — PARTIAL`

## Finalidade
Registrar somente relações que já possuem evidência contextual no conteúdo dos artefatos consultados. Ocorrências encontradas por busca permanecem candidatas até inspeção contextual.

## Evidência 1 — regra de autoridade e localização

`ELO_REPOSITORY_NAVIGATION_RULES.md` estabelece que a localização de uma pasta é sinal de navegação e não prova suficiente de autoridade. A ordem de autoridade começa pelo manifesto constitucional/empresarial, seguida de baseline arquitetural, ADR aprovado, contrato/schema canônico, política de governança/segurança, implementação, testes/evidência de runtime e roadmap/proposta.

### Decisão
`00-enterprise-manifest/` é uma localização operacional indicada para a camada Enterprise Manifest, mas o caminho, isoladamente, não prova que o conteúdo atual do diretório seja o artefato canônico completo.

### Evidência
O próprio documento determina que variantes paralelas, como `00-empresa-manifesto/` e `00-enterprise-manifest/`, não devem ser tratadas como arquiteturas independentes sem decisão explícita. Também determina preservar o conteúdo português até revisão e não mover grandes conjuntos sem ADR de consolidação.

## Evidência 2 — registry de capacidades

`ELO_CAPABILITY_REGISTRY.yaml` registra `ELO-CAP-ENT-001` com nome `Enterprise Manifest`, owner `enterprise-governance`, maturidade 2, `canonical_artifact: 00-enterprise-manifest/` e `evidence: []`. O próprio registro contém o gap: estabelecer explicitamente o artefato canônico caso permaneçam múltiplos manifestos históricos.

### Decisão
A entrada confirma uma **declaração de capacidade e localização proposta**, mas não confirma por si só equivalência, migração, autoridade normativa do README ou completude do conteúdo.

## Evidência 3 — inventário de migração

`docs/migration/migration_inventory.md` classifica `Enterprise Manifest` como domínio de Estratégia com status `Em consolidação`. Seu critério declara manter a versão mais completa, preservar histórico, remover duplicidade e garantir rastreabilidade.

### Decisão
O inventário confirma que o Enterprise Manifest ainda está em consolidação. Portanto, não há base para tratar a consolidação física como concluída.

## Evidência 4 — plano de migração

`docs/migration/migration_plan.md` define como objetivo oficial consolidar, versionar e evoluir a arquitetura; seus princípios incluem preservação da arquitetura original, consolidação de documentos duplicados, rastreabilidade das decisões e evolução por módulos/domínios. As etapas incluem inventário, auditoria, consolidação, definição de baseline, publicação controlada e evolução contínua.

### Decisão
A família 00 está dentro de um processo formal de consolidação. A etapa atual de auditoria deve preceder qualquer movimentação física.

## Matriz de evidência atual

| Artefato/estrutura | Relação comprovada | Tipo | Estado | Impacto |
|---|---|---|---|---|
| `ELO_REPOSITORY_NAVIGATION_RULES.md` | define autoridade e regra para variantes `00-*` | `GOVERNANCE_REFERENCE` | `CONFIRMED` | alto para decisão de endereço |
| `ELO_CAPABILITY_REGISTRY.yaml` | declara `ELO-CAP-ENT-001` e localização canônica proposta | `LOGICAL_REFERENCE` / `GOVERNANCE_REFERENCE` | `CONFIRMED` | alto para identidade/canonical owner |
| `docs/migration/migration_inventory.md` | registra Enterprise Manifest como “Em consolidação” | `HISTORICAL_REFERENCE` / `GOVERNANCE_REFERENCE` | `CONFIRMED` | alto para status |
| `docs/migration/migration_plan.md` | define processo e princípios de consolidação | `GOVERNANCE_REFERENCE` | `CONFIRMED` | alto para sequencing |
| `src/elo/integrations/enterprise/*` | ocorrência nominal encontrada anteriormente | `CONSUMER_CANDIDATE` | `PENDING_CONTEXT` | indeterminado |
| `docs/handbook/ELO_ENTERPRISE_HANDBOOK_v2.0_ENTERPRISE.md` | ocorrência nominal encontrada anteriormente | `REFERENCE_CANDIDATE` | `PENDING_CONTEXT` | indeterminado |

## O que permanece não comprovado

Ainda não há evidência contextual suficiente para afirmar que:

- `src/elo/integrations/enterprise/*` lê ou resolve diretamente os artefatos da família 00;
- o Enterprise Handbook é consumidor físico ou lógico da família;
- `README.md` e `ENTERPRISE_MANIFESTO.md` são equivalentes;
- qualquer arquivo pode ser removido;
- qualquer caminho pode ser alterado sem atualizar consumidores.

## Classificação provisória

```text
00-enterprise-manifest/README.md              = STRUCTURAL_SUMMARY / PENDING_AUTHORITY
00-empresa-manifesto/ENTERPRISE_MANIFESTO.md = AGGREGATOR / PENDING_AUTHORITY
00-empresa-manifesto/01_Missao.md             = CONTENT_ARTIFACT / PENDING
00-empresa-manifesto/MISSAO.md                = CONTENT_ARTIFACT / PENDING
00-empresa-manifesto/02_Objetivos.md          = CONTENT_ARTIFACT / PENDING
00-empresa-manifesto/03_Capacidades.md       = CONTENT_ARTIFACT / PENDING
00-empresa-manifesto/04_Cadeia_de_Valor.md  = CONTENT_ARTIFACT / PENDING
00-empresa-manifesto/05_Modelo_Operacional.md= CONTENT_ARTIFACT / PENDING
00-empresa-manifesto/06_Stakeholders.md      = CONTENT_ARTIFACT / PENDING
00-empresa-manifesto/07_Regras_Estrategicas.md= NORMATIVE_CANDIDATE / PENDING_AUTHORITY
```

Estas classificações são funcionais para a auditoria e não substituem `EQ/CP/CF/EX/HI/NR`.

## Próxima inspeção

1. inspecionar `ELO_ENTERPRISE_HANDBOOK_v2.0_ENTERPRISE.md`;
2. inspecionar os READMEs de `src/elo/integrations/enterprise/`;
3. localizar referências físicas aos dois roots `00-*`;
4. localizar referências aos nove arquivos de conteúdo;
5. registrar linhas/trechos e impacto;
6. somente então promover ou rejeitar candidatos.

## Gate

`REFERENCE_MAPPING = PARTIAL`
`CONSUMER_MAPPING = PENDING`
`MIGRATION_APPROVAL = BLOCKED`
`PHYSICAL_REMOVAL = BLOCKED`

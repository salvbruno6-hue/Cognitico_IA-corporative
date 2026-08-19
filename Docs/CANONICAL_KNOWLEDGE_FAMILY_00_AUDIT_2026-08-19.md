# ELO — Auditoria da Família 00 — Enterprise Manifest

## Estado
`AUDIT_PARTIAL — FILE_LEVEL_REQUIRED`

## Evidência estrutural

No snapshot auditado existem dois papéis distintos:

- `00-enterprise-manifest/` contém `.gitkeep` e `README.md`.
- `00-empresa-manifesto/` contém múltiplos artefatos de conteúdo, incluindo `01_Missao.md`, `MISSAO.md`, `02_Objetivos.md`, `03_Capacidades.md`, `04_Cadeia_de_Valor.md`, `05_Modelo_Operacional.md`, `06_Stakeholders.md`, `07_Regras_Estrategicas.md` e outros manifestos.

O `README.md` de `00-enterprise-manifest/` descreve a fonte estratégica e enumera Vision, Mission, Philosophy, Core Principles, Architecture Pillars, Knowledge Hierarchy, Corporate Knowledge Model, Architecture Rules, Evolution Rules e Governance.

O `ENTERPRISE_MANIFESTO.md` da árvore portuguesa descreve a missão e declara como escopo visão empresarial, objetivos estratégicos, capacidades centrais, cadeia de valor, modelo operacional, stakeholders e regras estratégicas.

## Conclusão estrutural atual

A existência de nomes correspondentes não permite classificar a família inteira como `EQ`. A estrutura observada indica assimetria de conteúdo: o diretório inglês proposto como canônico contém atualmente um README estrutural/resumido, enquanto o diretório português contém os artefatos de conteúdo detalhados.

A relação correta nesta fase é `CONCEITO ↔ MÚLTIPLOS ARTEFATOS`, e não `ARQUIVO PT ↔ ARQUIVO EN`.

### Classificação da família
`CONTENT_REVIEW_REQUIRED`

### Hipóteses permitidas para auditoria de arquivos

- `CP` pode ser aplicável quando dois artefatos possuem contribuições complementares.
- `EX` deve ser aplicado aos artefatos sem correspondente semântico comprovado.
- `EQ` somente após comparação de conteúdo, função e autoridade.
- `HI` quando a origem precisar ser preservada como histórico/proveniência.
- `CF` se versões divergentes expressarem regras incompatíveis.
- `NR` somente quando houver evidência de que o conteúdo não deve permanecer no modelo canônico.

## Evidência transversal do repositório

A auditoria não deve limitar-se às duas raízes da família 00. O repositório possui outros registros e artefatos que podem representar os mesmos conceitos, inclusive:

- `ELO_CAPABILITY_REGISTRY.yaml`, que registra `ELO-CAP-ENT-001` como `Enterprise Manifest`, aponta `00-enterprise-manifest/` como `canonical_artifact` proposto e, simultaneamente, reconhece como gap a necessidade de estabelecer explicitamente o artefato canônico caso permaneçam múltiplos manifestos históricos.
- `01-meta-architecture/ELO_ARCHITECTURE_MASTER.md` e outras estruturas de arquitetura podem referenciar princípios e regras originados no manifesto.
- `docs/migration/migration_plan.md`, `docs/migration/migration_inventory.md` e `docs/migration/architecture_mapping.md` constituem histórico/processo de migração que pode consumir ou apontar para os artefatos da família.
- `ELO_REPOSITORY_NAVIGATION_RULES.md` é consumidor potencial de caminhos e regras de navegação.

Consequentemente, a decisão final da família 00 não pode ser feita apenas comparando português e inglês. É necessário localizar consumidores e fontes concorrentes em todo o repositório.

## Auditoria em nível de arquivo

| Arquivo | Conteúdo observado | Estado | Decisão atual |
|---|---|---|---|
| `00-enterprise-manifest/README.md` | Fonte estratégica resumida; enumera visão, missão, filosofia, princípios, pilares, hierarquia de conhecimento, modelo corporativo, regras de arquitetura, evolução e governança | `PENDING` | Tratar como artefato estrutural/resumo; não presumir que seja substituto do conjunto detalhado português |
| `00-empresa-manifesto/01_Missao.md` | Missão empresarial; integração, conhecimento, execução e rastreabilidade aos demais documentos | `PENDING` | Comparar semanticamente com `MISSAO.md`, manifesto agregador e consumidores |
| `00-empresa-manifesto/MISSAO.md` | Missão; propósito institucional; valor para o negócio; planejamento/operação; ecossistema cognitivo | `PENDING` | Não tratar como duplicata de `01_Missao.md` apenas pelo nome |
| `00-empresa-manifesto/ENTERPRISE_MANIFESTO.md` | Documento agregador; missão e escopo envolvendo visão, objetivos, capacidades, cadeia de valor, modelo operacional, stakeholders e regras | `PENDING` | Comparar função e autoridade com o README inglês e os documentos componentes |
| `00-empresa-manifesto/02_Objetivos.md` | Objetivos estratégicos; decisão/operação; rastreabilidade; redução de redundância; evolução incremental | `PENDING` | Comparar com objetivos presentes no manifesto agregador e fontes transversais |
| `00-empresa-manifesto/03_Capacidades.md` | Capacidades empresariais; análise/decisão; conhecimento; integração de recursos; rastreabilidade; evolução | `PENDING` | Comparar com `ELO_CAPABILITY_REGISTRY.yaml` e demais fontes de capacidades |
| `00-empresa-manifesto/04_Cadeia_de_Valor.md` | Transformação de informação em conhecimento útil; decisão; planejamento; operação; governança; integração entre domínios | `PENDING` | Comparar função, granularidade e consumidores |
| `00-empresa-manifesto/05_Modelo_Operacional.md` | Estrutura operacional; capacidade, recursos e processos; governança, planejamento e execução | `PENDING` | Comparar com artefatos arquiteturais e operacionais transversais |
| `00-empresa-manifesto/06_Stakeholders.md` | Áreas estratégicas, engenharia, operação, governança, usuários de negócio, patrocinadores e mantenedores | `PENDING` | Comparar com consumidores, owners e estruturas de governança |
| `00-empresa-manifesto/07_Regras_Estrategicas.md` | Relações entre missão, objetivos, capacidades, recursos, cadeia de valor, operação e stakeholders; regras de rastreabilidade | `PENDING` | Comparar como fonte normativa; não presumir equivalência com qualquer resumo |

## Observações semânticas

### Missão
`01_Missao.md` e `MISSAO.md` compartilham o mesmo título, mas não são textualmente equivalentes. `01_Missao.md` enfatiza integração, conhecimento, execução e rastreabilidade; `MISSAO.md` enfatiza propósito institucional, valor ao negócio, planejamento/operação e suporte à decisão. A relação deve ser decidida como `EQ`, `CP`, `HI`, `CF`, `EX` ou outra classificação somente após comparação com os demais documentos e referências.

### Documento agregador
`ENTERPRISE_MANIFESTO.md` possui função diferente de um documento de missão isolado: seu escopo explicitamente agrega sete áreas estratégicas. Portanto, não deve ser fundido automaticamente com qualquer um dos documentos componentes.

### README inglês
`00-enterprise-manifest/README.md` não deve ser tratado como equivalente integral da árvore portuguesa. Seu conteúdo é estrutural e enumerativo, enquanto a árvore portuguesa contém documentos detalhados. A hipótese atual é de relação agregadora/estrutural, sujeita à análise de autoridade e referências.

### Capabilities registry
`ELO_CAPABILITY_REGISTRY.yaml` usa `00-enterprise-manifest/` como `canonical_artifact` proposto para `ELO-CAP-ENT-001`, mas o próprio registro declara a necessidade de estabelecer explicitamente o artefato canônico se múltiplos manifestos históricos permanecerem. Portanto, essa indicação é evidência de uma decisão proposta, não prova de que a consolidação já ocorreu.

### Cadeia de dependências conceituais
Os próprios documentos estabelecem relações entre missão, objetivos, capacidades, cadeia de valor, modelo operacional e stakeholders. Isso significa que uma futura consolidação deve preservar essas relações, e não apenas substituir arquivos por nomes canônicos.

## Modelo de relação recomendado

A entidade primária da auditoria deve ser o conceito, com múltiplos artefatos associados:

```text
concept_id
  ├── artifact_id: manifesto agregador
  ├── artifact_id: missão
  ├── artifact_id: objetivos
  ├── artifact_id: capacidades
  ├── artifact_id: cadeia de valor
  ├── artifact_id: modelo operacional
  ├── artifact_id: stakeholders
  └── artifact_id: regras estratégicas
```

O caminho físico (`canonical_path` ou `legacy_paths`) é atributo de localização e não identidade do conceito.

## Identidade

Nenhum `artifact_id` ou `concept_id` definitivo é atribuído nesta etapa. O nome da pasta, o nome do arquivo ou a tradução do título não são evidência suficiente de identidade.

Para cada artefato aprovado posteriormente, a identidade deverá ser estabelecida após evidência de conteúdo, hash, proveniência, função, autoridade e referências.

## Referências e consumidores

Ainda não consideradas completas. Devem ser levantadas transversalmente antes de qualquer movimentação física. O levantamento deverá procurar, no mínimo:

1. referências Markdown e documentação;
2. caminhos em YAML/JSON/TOML e arquivos de configuração;
3. imports e referências em Python/código;
4. workflows e scripts CI;
5. SourceResolver/SourceDiscovery e outros consumidores runtime;
6. Knowledge Engineering, RAG, Memory, agentes e Evidence;
7. índices, registries, aliases e documentação de navegação;
8. registros históricos de migração.

## Decisão operacional

1. Não remover `00-empresa-manifesto/`.
2. Não declarar equivalência da família 00.
3. Não consolidar arquivos apenas por tradução ou semelhança nominal.
4. Não criar um segundo registry para representar a mesma relação.
5. Tratar `ELO_CAPABILITY_REGISTRY.yaml` como fonte de capacidade/proposta e não como prova de migração concluída.
6. Completar a comparação de conteúdo e função de cada artefato.
7. Levantar referências e consumidores em todo o repositório antes de qualquer alteração de endereço.
8. Registrar conteúdo exclusivo antes de qualquer consolidação.
9. Preservar proveniência de cada origem.
10. Não atribuir `artifact_id` ou `concept_id` definitivo enquanto a evidência estiver `PENDING`.
11. Não alterar `src/elo/`, `SourceResolver` ou outra autoridade runtime nesta etapa.
12. Não executar migração física enquanto houver referência ou autoridade não resolvida.

## Critério de conclusão da família 00

A família somente poderá sair de `CONTENT_REVIEW_REQUIRED` quando existir, para cada artefato relevante:

- classificação semântica justificada;
- identidade estabelecida ou explicitamente descartada;
- hash/conteúdo registrado;
- proveniência preservada;
- referências mapeadas;
- consumidores avaliados;
- decisão de localização documentada;
- testes correspondentes aprovados;
- ausência de perda de conteúdo complementar.

## Próxima etapa

Concluir a análise transversal de conteúdo e referências da família 00. Somente após a família 00 possuir evidência suficiente será replicado o procedimento nas famílias `01`, `05`, `07`, `11`, `12`, `13`, `14` e `15`.

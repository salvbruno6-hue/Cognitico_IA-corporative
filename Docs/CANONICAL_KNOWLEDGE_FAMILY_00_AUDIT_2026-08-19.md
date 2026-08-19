# ELO — Auditoria da Família 00 — Enterprise Manifest

## Estado
`AUDIT_PARTIAL — FILE_LEVEL_REQUIRED`

## Evidência estrutural

No snapshot auditado existem dois papéis distintos:

- `00-enterprise-manifest/` contém `.gitkeep` e `README.md`.
- `00-empresa-manifesto/` contém múltiplos artefatos de conteúdo, incluindo `01_Missao.md`, `02_Objetivos.md`, `03_Capacidades.md`, `04_Cadeia_de_Valor.md`, `05_Modelo_Operacional.md`, `06_Stakeholders.md`, `07_Regras_Estrategicas.md` e outros manifestos.

O `README.md` de `00-enterprise-manifest/` descreve a fonte estratégica e enumera conceitos como Vision, Mission, Philosophy, Core Principles, Architecture Pillars, Knowledge Hierarchy, Corporate Knowledge Model, Architecture Rules, Evolution Rules e Governance.

## Conclusão atual

A existência de nomes correspondentes não permite classificar a família inteira como `EQ`. A estrutura observada indica, no mínimo, assimetria de conteúdo: o diretório inglês canônico proposto funciona atualmente como uma estrutura resumida/índice, enquanto o diretório português contém artefatos de conteúdo que precisam ser comparados individualmente.

### Classificação da família
`CONTENT_REVIEW_REQUIRED`

### Hipóteses permitidas para auditoria de arquivos

- `CP` pode ser aplicável quando o conteúdo inglês e português tiverem contribuições complementares.
- `EX` deve ser aplicado aos artefatos sem correspondente semântico comprovado.
- `EQ` somente após comparação do conteúdo.
- `HI` quando a origem precisar ser preservada como histórico/proveniência.
- `CF` se versões divergentes expressarem regras incompatíveis.
- `NR` somente quando houver evidência de que o conteúdo não deve permanecer no modelo canônico.

## Auditoria em nível de arquivo

| Arquivo | Conteúdo observado | Estado | Decisão atual |
|---|---|---|---|
| `01_Missao.md` | Missão empresarial; integração, conhecimento, execução; rastreabilidade aos demais documentos | `PENDING` | Comparar semanticamente com `MISSAO.md`, `ENTERPRISE_MANIFESTO.md` e demais fontes |
| `MISSAO.md` | Missão; propósito institucional; valor para o negócio; planejamento/operação; ecossistema cognitivo | `PENDING` | Não tratar como duplicata de `01_Missao.md` apenas pelo nome |
| `ENTERPRISE_MANIFESTO.md` | Documento agregador; missão e escopo envolvendo visão, objetivos, capacidades, cadeia de valor, modelo operacional, stakeholders e regras | `PENDING` | Comparar função e escopo com o `README.md` inglês e os documentos componentes |
| `02_Objetivos.md` | Objetivos estratégicos; decisão/operação; rastreabilidade; redução de redundância; evolução incremental | `PENDING` | Comparar com objetivos presentes no manifesto agregador e no lado inglês |
| `03_Capacidades.md` | Capacidades empresariais; análise/decisão; conhecimento; integração de recursos; rastreabilidade; evolução | `PENDING` | Comparar com capacidades citadas no manifesto e possíveis artefatos equivalentes |
| `04_Cadeia_de_Valor.md` | Transformação de informação em conhecimento útil; decisão; planejamento; operação; governança; integração entre domínios | `PENDING` | Comparar função e granularidade com referências do manifesto |
| `05_Modelo_Operacional.md` | Estrutura operacional; capacidade, recursos e processos; governança, planejamento e execução | `PENDING` | Comparar com o escopo operacional dos documentos agregadores |
| `06_Stakeholders.md` | Áreas estratégicas, engenharia, operação, governança, usuários de negócio, patrocinadores e mantenedores | `PENDING` | Comparar conteúdo e responsabilidade com consumidores e fontes estratégicas |
| `07_Regras_Estrategicas.md` | Relações entre missão, objetivos, capacidades, recursos, cadeia de valor, operação e stakeholders; regras de rastreabilidade | `PENDING` | Comparar como fonte normativa, sem presumir equivalência com qualquer resumo |

## Observações semânticas

### Missão
`01_Missao.md` e `MISSAO.md` compartilham o mesmo título, mas não são textualmente equivalentes. `01_Missao.md` enfatiza integração, conhecimento, execução e rastreabilidade; `MISSAO.md` enfatiza propósito institucional, valor ao negócio, planejamento/operação e suporte à decisão. A relação deve ser decidida como `EQ`, `CP`, `HI` ou outra classificação somente após comparação com os demais documentos e referências.

### Documento agregador
`ENTERPRISE_MANIFESTO.md` possui função diferente de um documento de missão isolado: seu escopo explicitamente agrega sete áreas estratégicas. Portanto, não deve ser fundido automaticamente com qualquer um dos documentos componentes.

### Cadeia de dependências conceituais
Os próprios documentos estabelecem relações entre missão, objetivos, capacidades, cadeia de valor, modelo operacional e stakeholders. Isso significa que uma futura consolidação deve preservar essas relações, e não apenas substituir arquivos por nomes canônicos.

## Identidade

Nenhum `artifact_id` ou `concept_id` definitivo é atribuído nesta etapa. O nome da pasta, o nome do arquivo ou a tradução do título não são evidência suficiente de identidade.

Para cada artefato aprovado posteriormente, a identidade deverá ser estabelecida após evidência de conteúdo, hash, proveniência e referências.

## Referências

Ainda não consideradas completas. Devem ser levantadas antes de qualquer movimentação física.

## Decisão operacional

1. Não remover `00-empresa-manifesto/`.
2. Não declarar equivalência da família 00.
3. Não consolidar arquivos apenas por tradução ou semelhança nominal.
4. Completar a comparação de conteúdo e função de cada artefato.
5. Levantar referências e consumidores antes de qualquer alteração de endereço.
6. Registrar conteúdo exclusivo antes de qualquer consolidação.
7. Preservar proveniência de cada origem.
8. Não atribuir `artifact_id` ou `concept_id` definitivo enquanto a evidência estiver `PENDING`.
9. Não alterar `src/elo/`, `SourceResolver` ou outra autoridade runtime nesta etapa.

## Próxima etapa

Concluir a análise semântica e de referências da família 00. Somente após a família 00 possuir evidência suficiente será replicado o procedimento nas famílias `01`, `05`, `07`, `11`, `12`, `13`, `14` e `15`.

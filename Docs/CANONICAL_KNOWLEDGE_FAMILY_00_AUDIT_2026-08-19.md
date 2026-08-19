# ELO — Auditoria da Família 00 — Enterprise Manifest

## Estado
`AUDIT_PARTIAL — FILE_LEVEL_REQUIRED`

## Evidência estrutural

No snapshot auditado existem dois papéis distintos:

- `00-enterprise-manifest/` contém `.gitkeep` e `README.md`.
- `00-empresa-manifesto/` contém múltiplos artefatos de conteúdo, incluindo `01_Missao.md`, `02_Objetivos.md`, `03_Capacidades.md`, `04_Cadeia_de_Valor.md`, `05_Modelo_Operacional.md`, `06_Stakeholders.md`, `07_Regras_Estrategicas.md` e outros manifestos.

O `README.md` de `00-enterprise-manifest/` descreve a fonte estratégica e enumera conceitos como Vision, Mission, Philosophy, Core Principles, Architecture Pillars, Knowledge Hierarchy, Corporate Knowledge Model, Architecture Rules, Evolution Rules e Governance.

## Conclusão atual

A existência de nomes correspondentes não permite classificar a família inteira como `EQ`. A estrutura observada indica, no mínimo, **assimetria de conteúdo**: o diretório inglês canônico proposto funciona atualmente como uma estrutura resumida/índice, enquanto o diretório português contém artefatos de conteúdo que ainda precisam ser comparados individualmente.

### Classificação da família
`CONTENT_REVIEW_REQUIRED`

### Hipóteses permitidas para auditoria de arquivos

- `CP` pode ser aplicável quando o conteúdo inglês e português tiverem contribuições complementares.
- `EX` deve ser aplicado aos artefatos portugueses sem correspondente semântico comprovado.
- `EQ` somente após comparação do conteúdo.
- `HI` quando a origem portuguesa precisar ser preservada como histórico/proveniência.
- `CF` se versões divergentes expressarem regras incompatíveis.

## Identidade

Nenhum `artifact_id` ou `concept_id` definitivo é atribuído nesta etapa. O nome da pasta não é evidência suficiente de identidade.

## Referências

Ainda não consideradas completas. Devem ser levantadas antes de qualquer movimentação física.

## Decisão operacional

1. Não remover `00-empresa-manifesto/`.
2. Não declarar equivalência da família 00.
3. Auditar cada arquivo português contra os artefatos existentes no diretório inglês e contra consumidores/referências.
4. Registrar conteúdo exclusivo antes de qualquer consolidação.
5. Preservar proveniência de cada origem.

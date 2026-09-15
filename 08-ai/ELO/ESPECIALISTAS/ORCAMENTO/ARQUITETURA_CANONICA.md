# ARQUITETURA CANÔNICA — ELO ESPECIALISTA DE ORÇAMENTO

## Finalidade

Esta é a raiz canônica do conhecimento específico do Especialista de Orçamento do ELO.

## Regra de localização

Todo novo conhecimento específico de orçamento deve ser criado em `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/`.

Todo aprendizado gerado por uma SO deve ser persistido em `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/`.

## Organização

```text
ORCAMENTO/
├── PROMPT.md
├── ANALISE_DE_SOLICITACOES.md
├── PTS_TECNICA_MATURIDADE.md
├── ARQUITETURA_CANONICA.md
├── GOVERNANCA/
├── METODOLOGIA/
├── DOCUMENTACAO/
├── MODELOS_E_TAXONOMIA/
├── MEMORIA_DE_DECISAO/
├── MEMORIA_DE_CALCULO/
├── EXCEDENTES/
├── PRECEDENTES/
└── APRENDIZADOS/
    ├── historico/
    ├── decisoes/
    ├── calculos/
    ├── precedentes/
    └── regras/
```

## Relação com outras camadas

`00-core/`, `01-meta-architecture/`, `06-knowledge-engineering/`, `docs/` e `src/` continuam como camadas corporativas, arquiteturais, documentais ou de implementação. Não são destinos alternativos para novos conhecimentos específicos do Especialista de Orçamento.

Quando uma dessas camadas contiver conhecimento específico de orçamento que precise ser usado pelo Especialista, deve existir uma referência ou versão canônica dentro desta raiz, mantendo a fonte original quando ela tiver função arquitetural ou de implementação.

## Git × Supabase

- **Git:** fonte versionada, auditável e humana dos artefatos canônicos.
- **Supabase:** memória estruturada e consultável pelo ELO.
- **Histórico da SO:** preserva o caso de origem.
- **ELO APRENDER:** extrai decisão, cálculo, precedente e regra reutilizável.

## Promoção do aprendizado

`SO → histórico → extração → memória de decisão/cálculo → precedente → validação → conhecimento reutilizável → regra validada`

Nenhum aprendizado histórico deve virar regra corporativa automaticamente.

## Código

Código executável permanece em `src/` ou na camada de implementação correspondente. Não deve ser duplicado dentro de `APRENDIZADOS`. A associação canônica ocorre por documentação, contrato, configuração ou referência operacional.

## Consulta

Para uma nova SO, o ELO deve consultar o conhecimento canônico do Especialista e a memória estruturada do Supabase, relacionando requisito, produto, modelo, equivalência, escopo, excedente, decisão, cálculo, precedente e validação.

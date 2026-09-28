# Classificação de Migrations GITHUB_ONLY

Este documento define o processo de classificação das
migrations que existem no GitHub mas ainda não foram
confirmadas em produção.

Decisão arquitetural de base:
`10-adr/ADR-0018-multi-tenant-model.md`

## Contexto

A auditoria estrutural identificou que:

- 29 migrations existem no GitHub (`supabase/migrations/`)
- 144 migrations existem em produção
- 16 migrations estão no GitHub mas **não confirmadas** em
  produção (GITHUB_ONLY)
- 131 migrations existem em produção mas não estão no GitHub
  (PROD_ONLY)

Este documento trata apenas das **16 GITHUB_ONLY**. As 131
PROD_ONLY são tratadas pelo mesmo processo, em documento
próprio, quando o Supabase estiver acessível para leitura.

## Definição

Uma migration é classificada como GITHUB_ONLY quando:

- o arquivo existe em `supabase/migrations/` no main
- não há registro de versão exata em
  `supabase_migrations.schema_migrations`

Uma migration pode estar **funcionalmente aplicada** mesmo
sem registro exato — por exemplo, quando foi aplicada com
uma versão diferente gerada pelo executor Supabase.

## Três grupos

Toda migration GITHUB_ONLY deve ser classificada em um dos
três grupos:

### Grupo 1 — Aplicar agora

A migration:

- representa estrutura que **deveria existir em produção**
- não conflita com o estado atual
- tem impacto conhecido e reversível
- não depende de decisão humana pendente

**Ação:** aplicar via SQL Editor ou via o workflow
`ELO Deploy Functions` quando aplicável (não aplicável a
migrations).

### Grupo 2 — Equivalente funcional

A migration:

- já foi aplicada em produção com versão diferente
- o efeito é observável no estado atual
- o registro exato em `schema_migrations` é diferente

**Ação:** documentar como equivalente. Não reexecutar.
Atualizar o índice com o mapeamento versão-GitHub ↔
versão-produção.

### Grupo 3 — Histórica / obsoleta

A migration:

- representa estrutura que **não existe mais** em produção
- foi superseded por outra
- não é reexecutável no estado atual

**Ação:** documentar como histórica. Não reexecutar.
Preservar como evidência.

## Regras

1. Nenhuma migration GITHUB_ONLY é reexecutada às cegas
2. Nenhuma migration é apagada do GitHub
3. Toda classificação exige **evidência** do estado atual de
   produção
4. Migrations aplicadas com versão diferente são registradas
   como equivalência, não como ausência
5. O processo é incremental: cada migration é classificada
   em PR própria ou em lote

## Fluxo

Para cada migration GITHUB_ONLY:

1. Ler o conteúdo em `supabase/migrations/`
2. Verificar em produção o efeito descrito
3. Classificar em um dos três grupos
4. Registrar no `INDEX.json`
5. Se Grupo 1: aplicar via SQL Editor
6. Se Grupo 2: registrar equivalência de versão
7. Se Grupo 3: registrar como histórica

## Fonte canônica

O GitHub permanece a fonte canônica. O Supabase é o ambiente
de execução. Divergências são documentadas, nunca corrigidas
automaticamente.

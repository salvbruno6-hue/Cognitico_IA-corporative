# Template de Classificação de Migration

Copiar este template para classificar cada migration
GITHUB_ONLY.

## Identificação

- **version_github:** (ex: 20260927000000)
- **name:** (ex: elo_read_rls_state)
- **path:** (ex: supabase/migrations/20260927000000_elo_read_rls_state.sql)
- **classification_date:** (YYYY-MM-DD)
- **classifier:** (nome ou identidade)

## Conteúdo da migration

Resumo do que a migration faz (1-3 linhas):

> ...

Operações:

- [ ] Cria tabela
- [ ] Altera tabela
- [ ] Cria índice
- [ ] Cria função
- [ ] Cria policy
- [ ] Insere dados
- [ ] Outros: ...

## Verificação em produção

Evidência do estado atual:

- Tabela/função/policy existe? (sim/não)
- Efeito é observável? (sim/não)
- Versão em `schema_migrations`:

## Classificação

Grupo:

- [ ] **Grupo 1 — Aplicar agora**
- [ ] **Grupo 2 — Equivalente funcional**
- [ ] **Grupo 3 — Histórica / obsoleta**

Justificativa:

> ...

## Ação

- [ ] Nenhuma (Grupo 3)
- [ ] Registrar equivalência (Grupo 2)
- [ ] Aplicar em produção (Grupo 1)

## Evidência

Links, comandos SQL, capturas, referências:

- ...

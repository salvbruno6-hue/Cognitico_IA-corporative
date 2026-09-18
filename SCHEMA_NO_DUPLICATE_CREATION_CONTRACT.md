# ELO — Schema No-Duplicate Creation Contract

## Regra canônica

Antes de criar qualquer tabela, o ELO deve consultar o schema canônico do Supabase e o histórico de migrations.

**É proibido criar uma nova tabela para representar uma entidade que já exista.**

Quando a entidade já existe:
- reutilizar a tabela canônica;
- usar `ALTER TABLE` somente para evolução estrutural comprovada;
- consolidar duplicações antes de introduzir nova autoridade;
- preservar FKs, índices, RLS, proveniência e histórico.

Quando a entidade não existe:
- somente então uma nova tabela pode ser proposta;
- a decisão deve registrar a justificativa semântica;
- deve ser verificado se tabelas existentes representam o mesmo conceito com outro nome.

## Caso validado nesta implementação

Existem no schema atual:
- `fornecedores`
- `fornecedor_itens_cotacao`
- `compras_fornecedor`
- `compras_fornecedor_itens`
- `mt_fornecedor_itens`
- `mt_ordens_compra`
- `mt_ordens_compra_itens`
- `lista_mae`

A implementação de cotação **reutiliza `fornecedor_itens_cotacao`** e não deve criar outra tabela para os itens da cotação.

A tabela `fornecedor_cotacoes` foi criada porque a verificação do histórico/schema não encontrou anteriormente uma entidade canônica de cabeçalho de cotação. Ela representa o conceito específico de **cotação recebida**, distinto de compra/ordem de compra.

## Preflight obrigatório

Executar:

`supabase/tests/schema_no_duplicate_table_creation.sql`

O teste é somente de leitura e falha com `CANONICAL_SCHEMA_GAP` quando uma relação que deveria ser reutilizada não estiver presente.

## Regra para futuras migrations

Não usar `CREATE TABLE` para uma entidade já existente. A presença de `IF NOT EXISTS` não substitui a investigação de autoridade: ela evita erro técnico, mas não evita duplicação semântica.

Fluxo obrigatório:

**diagnosticar → consultar schema → consultar migrations → identificar autoridade → reutilizar/ALTERar → testar → Evolution Gate**

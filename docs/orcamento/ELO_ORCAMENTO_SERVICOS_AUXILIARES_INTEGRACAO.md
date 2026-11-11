# ELO ORÇAR — Catálogo auxiliar de composição e vínculo ao orçamento

**Status:** implementação de infraestrutura com referências não homologadas; não promove aprendizado ao Core.  
**Executor:** FORGE-BUDGETING-001; **núcleo existente:** `public.elo_conhecimento_nucleos.codigo=CONHECIMENTO_ORCAMENTO`.  
**Autoridade:** GitHub para desenho/versionamento; Supabase para estado persistente.

## Diagnóstico
Investigação em `information_schema` de todos os esquemas: há `public.elo_orcamentos`, `public.elo_orcamento_associacoes`, `public.excedentes`, `public.lista_mae`, porém não foi localizada uma entidade própria de linhas de composição por orçamento nem catálogo relacional de serviços laterais. O modelo documentado em `docs/orcamento/ELO_ORCAMENTO_DATA_MODEL.md` prevê relações e composições como entidades de primeira classe.

## Associação proposta (sem autoridade paralela)
`elo_conhecimento_nucleos[CONHECIMENTO_ORCAMENTO]` → `elo_orcamento_servicos_auxiliares` → `elo_orcamento_composicao_itens` → `elo_orcamentos[orcamento_id]`.

- Catálogo registra descrição original, preço de referência informado pelo Analista, unidade (somente quando comprovada), origem, condição e status. Sem alteração da Lista-Mãe ou do catálogo EXC.
- Linha de composição aponta opcionalmente à referência lateral, ao código `lista_mae.cod_item` ou `excedentes.codigo_excedente`, e informa `secao` canônica, quantidade, custo unitário, total, decisão de inclusão e memória/evidência. Só `APLICADO` com quantidade/custo permite somar.
- Não se presume destino de seta ilegível ou condição de aplicação não demonstrada; referências sem validação ficam `REFERENCIA_NAO_HOMOLOGADA`; item fica `EM_ANALISE` até confirmação.
- Logística/Munck precisa respeitar memória da SO 203.26 (Logística → Comercial), evitando cobrança técnica e logística duplicada.
- O orçamento M05 (SO 233.26) recebe apenas registro `EM_ANALISE`; **nenhuma** referência lateral será aplicada ou computada automaticamente.
- `EXC-011` já inclui mão de obra, então não duplicar com 2.3.
- RLS habilitado e sem políticas públicas: acesso apenas por papel de backend autorizado até revisão de permissões.
- Evolução dessa infraestrutura não equivale a canonizar o aprendizado metodológico da SO, ainda pendente de validação do Analista.

## Testes de aceitação
1. As duas tabelas existem com FKs válidas para núcleo, referência auxiliar e orçamento.
2. As referências laterais exibem valores e fonte, sem lançar custo no M05.
3. Seleção de composição sem preço e quantidade fica fora da soma.
4. A consulta por `SO 233.26` retorna catálogo relacionado ao núcleo do orçamento, mas zero serviços laterais `APLICADO`.
5. Nenhuma função, trigger ou permissão `anon`/`authenticated` cria custo automaticamente.

insert into public.elo_conhecimento_fontes
  (tabela_origem, nucleo_codigo, papel, regra_direcionamento, ativo)
values
  ('estrutura_metalica_20_componentes', 'CONHECIMENTO_MATERIAIS', 'fonte física canônica da estrutura metálica modular 20 pés', 'Usar para consultar e persistir peças, COD_PRODUT, peso das peças, grupo de material, grupo funcional e fonte de associação. Alterações físicas validadas devem ser persistidas aqui; não editar a VW de perda.', true),
  ('estrutura_metalica_20_componentes', 'CONHECIMENTO_PRODUTOS', 'componentes da estrutura metálica modular 20 pés', 'Usar quando a pergunta tratar da composição física da estrutura modular 20 pés. Esta fonte descreve a estrutura transversal e não deve ser confundida com a BOM específica de um modelo.', true),
  ('vw_perda_estrutura_metalica_20', 'CONHECIMENTO_ORCAMENTO', 'visão consolidada de perda da estrutura metálica modular 20 pés', 'Usar para leitura de peso comprado, peso utilizado, saldo, percentual, custo e impacto por matéria-prima. É visão derivada: consultar aqui, mas persistir correções nas fontes físicas ou na memória de cálculo, nunca diretamente na VW.', true)
on conflict (tabela_origem, nucleo_codigo) do update
set papel = excluded.papel,
    regra_direcionamento = excluded.regra_direcionamento,
    ativo = true;

insert into public.elo_conhecimento_regras_routing
  (codigo, prioridade, condicao, destino_nucleo, destino_subnucleo, acao, evitar_duplicacao, ativo)
values
  ('ROUTE-EST-MET-20-COMPONENTES', 31,
   'Consulta trata de peças, componentes, matéria-prima, COD_PRODUT, grupo de material ou peso utilizado da estrutura metálica modular 20 pés',
   'CONHECIMENTO_MATERIAIS', 'ESTRUTURA_METALICA_20_COMPONENTES',
   'CONSULTAR public.estrutura_metalica_20_componentes COMO FONTE FISICA CANONICA. Para alteração validada de peça/peso/associação, persistir nesta tabela; não escrever em VW derivada.', true, true),
  ('ROUTE-EST-MET-20-PERDA', 32,
   'Consulta trata de perda, sobra, diferença, peso comprado, peso utilizado, percentual ou impacto financeiro da estrutura metálica modular 20 pés',
   'CONHECIMENTO_ORCAMENTO', 'ESTRUTURA_METALICA_20_PERDA',
   'CONSULTAR public.vw_perda_estrutura_metalica_20 PARA LEITURA CONSOLIDADA; validar memória em public.elo_orcamento_memoria pelo conceito PERDA_ESTRUTURA_METALICA_MODULAR_20_PES; em conflito rastrear public.estrutura_metalica_20_componentes.', true, true),
  ('ROUTE-EST-MET-20-MEMORIA', 33,
   'Consulta pede fórmula, memória de cálculo, evidência, origem, justificativa ou regra de cálculo da perda da estrutura metálica modular 20 pés',
   'CONHECIMENTO_ORCAMENTO', 'ESTRUTURA_METALICA_20_MEMORIA',
   'CONSULTAR public.elo_orcamento_memoria com conceito_key PERDA_ESTRUTURA_METALICA_MODULAR_20_PES. Novas memórias de cálculo validadas permanecem no domínio de orçamento e referenciam as tabelas físicas; não duplicar em tabela genérica.', true, true),
  ('ROUTE-EST-MET-20-CADASTRO', 34,
   'Consulta pede cadastro, descrição oficial, valor canônico, unidade, curva, obrigatoriedade ou aplicabilidade do item PERDA-EST-MET',
   'CONHECIMENTO_MATERIAIS', 'CATALOGO_PERDA_EST_MET',
   'CONSULTAR public.lista_mae pelo cod_item PERDA-EST-MET. O cadastro mestre hospeda identidade e valor canônico; memória de cálculo permanece em elo_orcamento_memoria.', true, true),
  ('ROUTE-EST-MET-20-COMPOSICAO', 35,
   'Consulta pede em quais kits ou modelos o item PERDA-EST-MET está efetivamente aplicado',
   'CONHECIMENTO_MATERIAIS', 'COMPOSICAO_APLICADA',
   'CONSULTAR public.kit_itens vinculado a public.lista_mae. Aplicabilidade geral em lista_mae não autoriza replicar automaticamente o item em todos os kits; composição concreta deve ser evidenciada.', true, true)
on conflict (codigo) do update
set prioridade = excluded.prioridade,
    condicao = excluded.condicao,
    destino_nucleo = excluded.destino_nucleo,
    destino_subnucleo = excluded.destino_subnucleo,
    acao = excluded.acao,
    evitar_duplicacao = excluded.evitar_duplicacao,
    ativo = true;

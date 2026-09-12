begin;

alter table public.fluxo_produtivo_modular
  add constraint fk_fluxo_produtivo_modelo
  foreign key (modelo_id) references public.modelos(id) not valid;

alter table public.fluxo_produtivo_modular
  add constraint fk_fluxo_produtivo_taxonomia
  foreign key (taxonomia_id) references public.taxonomia(id) not valid;

create unique index if not exists uq_compra_fornecedor_numero
  on public.compras_fornecedor(fornecedor_id, numero_compra)
  where numero_compra is not null and trim(numero_compra) <> '';

create or replace view public.vw_ultimas_compras_fornecedor as
select
  ci.id as compra_item_id,
  c.id as compra_id,
  c.fornecedor_id,
  f.nome as fornecedor_nome,
  ci.lista_mae_id,
  ci.codigo_item,
  ci.descricao,
  ci.unidade,
  ci.quantidade,
  ci.valor_unitario,
  ci.valor_total,
  c.data_compra,
  c.numero_compra,
  c.origem_so,
  row_number() over (
    partition by coalesce(ci.lista_mae_id::text, upper(trim(ci.codigo_item)), upper(trim(ci.descricao)))
    order by c.data_compra desc, ci.created_at desc
  ) as ordem_recencia
from public.compras_fornecedor_itens ci
join public.compras_fornecedor c on c.id = ci.compra_id
join public.fornecedores f on f.id = c.fornecedor_id;

insert into public.fluxo_produtivo_modular (codigo, nome, descricao, observacoes)
values (
  'MLT.PROD.PADRAO',
  'Fluxo Produtivo Modular — Referência',
  'Fluxo de referência documentado para produção modular Multiteiner.',
  'Tempos, capacidades e recursos específicos devem ser preenchidos somente com evidência operacional validada.'
)
on conflict (codigo) do nothing;

insert into public.fluxo_produtivo_modular_etapas (fluxo_id, ordem, codigo_etapa, nome, processo, observacoes)
select f.id, v.ordem, v.codigo, v.nome, v.processo, v.observacoes
from public.fluxo_produtivo_modular f
cross join (values
 (1,'TRIAGEM','Triagem','Entrada','Entrada e preparação da estrutura.'),
 (2,'CHASSI','Chassi','Fabricação','Conformação do chassi.'),
 (3,'ESCOVACAO','Escovação','Tratamento','Preparação superficial.'),
 (4,'PINTURA_TRATAMENTO','Pintura de tratamento','Pintura','Tratamento anticorrosivo.'),
 (5,'ACABAMENTO_BRANCO','Acabamento branco','Pintura','Acabamento branco.'),
 (6,'ESTOQUE_ESTRUTURAS','Estoque de estruturas','Estoque','Buffer de estruturas.'),
 (7,'MOVIMENTACAO','Movimentação','Logística interna','Movimentação para montagem.'),
 (8,'PISO','Piso','Montagem','Execução do piso.'),
 (9,'TETO','Teto','Montagem','Execução do teto.'),
 (10,'COLUNAS','Colunas','Montagem','Instalação das colunas.'),
 (11,'TRILHO','Trilho','Montagem','Instalação do trilho.'),
 (12,'PINTURA_MODULAR','Pintura modular','Pintura','Pintura do conjunto modular.'),
 (13,'PAREDES','Paredes','Montagem','Execução das paredes.'),
 (14,'INSTALACOES','Instalações','Instalações','Instalações prediais.'),
 (15,'ACABAMENTO','Acabamento','Acabamento','Acabamentos finais.'),
 (16,'TESTES','Testes','Qualidade','Testes e verificação.'),
 (17,'LIBERACAO','Liberação','Qualidade','Gate de liberação para expedição.')
) as v(ordem,codigo,nome,processo,observacoes)
where f.codigo='MLT.PROD.PADRAO'
on conflict (fluxo_id, ordem) do nothing;

commit;

-- ELO / MULTITEINER
-- Logical model: process-integrated data architecture
-- Status: conceptual/logical; physical implementation requires validation.

create schema if not exists multiteiner;

create table if not exists multiteiner.demanda (
  demanda_id bigint primary key,
  modalidade varchar(20) not null check (modalidade in ('VENDA','LOCACAO')),
  cliente_id bigint,
  local_entrega varchar(255),
  prazo date,
  status varchar(40) not null,
  origem varchar(40) not null default 'COMERCIAL',
  created_at timestamp not null default current_timestamp
);

create table if not exists multiteiner.af (
  af_id bigint primary key,
  demanda_id bigint not null references multiteiner.demanda(demanda_id),
  quantidade integer not null,
  modelo_id bigint,
  configuracao varchar(255),
  customizacao boolean not null default false,
  completa boolean,
  status varchar(40) not null,
  received_at timestamp
);

create table if not exists multiteiner.modelo_modulo (
  modelo_id bigint primary key,
  codigo varchar(80) not null unique,
  descricao varchar(255),
  tipo varchar(30) not null check (tipo in ('PADRAO','VARIACAO','CUSTOMIZADO')),
  ativo boolean not null default true
);

create table if not exists multiteiner.orcamento (
  orcamento_id bigint primary key,
  af_id bigint references multiteiner.af(af_id),
  modelo_id bigint references multiteiner.modelo_modulo(modelo_id),
  tipo varchar(30) not null default 'CUSTOMIZACAO',
  valor numeric(14,2),
  status varchar(40) not null,
  sazonalidade_ref varchar(40)
);

create table if not exists multiteiner.customizacao (
  customizacao_id bigint primary key,
  af_id bigint not null references multiteiner.af(af_id),
  orcamento_id bigint references multiteiner.orcamento(orcamento_id),
  requisito varchar(500) not null,
  material_extra boolean not null default false,
  status varchar(40) not null
);

create table if not exists multiteiner.ordem_pcp (
  ordem_pcp_id bigint primary key,
  af_id bigint not null references multiteiner.af(af_id),
  fluxo varchar(20) not null check (fluxo in ('MODULAR','CUSTOMIZADO','RECUPERACAO')),
  prioridade integer,
  janela_inicio timestamp,
  janela_fim timestamp,
  status varchar(40) not null,
  capacidade_validada boolean,
  materiais_validado boolean
);

create table if not exists multiteiner.lista_material (
  lm_id bigint primary key,
  ordem_pcp_id bigint not null references multiteiner.ordem_pcp(ordem_pcp_id),
  versao varchar(30) not null,
  status varchar(40) not null
);

create table if not exists multiteiner.lista_material_item (
  lm_item_id bigint primary key,
  lm_id bigint not null references multiteiner.lista_material(lm_id),
  material_id bigint not null,
  quantidade numeric(14,3) not null,
  origem varchar(30) not null
);

create table if not exists multiteiner.estoque (
  estoque_id bigint primary key,
  material_id bigint not null,
  localizacao varchar(100),
  quantidade_disponivel numeric(14,3) not null default 0,
  quantidade_reservada numeric(14,3) not null default 0,
  atualizado_em timestamp not null default current_timestamp
);

create table if not exists multiteiner.ordem_compra (
  ordem_compra_id bigint primary key,
  origem varchar(30) not null check (origem in ('PRODUCAO','REPARO')),
  status varchar(40) not null,
  data_prevista date
);

create table if not exists multiteiner.movimento_estoque (
  movimento_id bigint primary key,
  estoque_id bigint not null references multiteiner.estoque(estoque_id),
  tipo varchar(30) not null,
  quantidade numeric(14,3) not null,
  referencia_tipo varchar(40),
  referencia_id bigint,
  realizado_em timestamp not null default current_timestamp
);

create table if not exists multiteiner.modulo (
  modulo_id bigint primary key,
  modelo_id bigint not null references multiteiner.modelo_modulo(modelo_id),
  numero_patrimonio varchar(100) unique,
  status varchar(40) not null,
  modalidade_atual varchar(20),
  disponibilidade boolean not null default false
);

create table if not exists multiteiner.ordem_producao (
  ordem_producao_id bigint primary key,
  ordem_pcp_id bigint not null references multiteiner.ordem_pcp(ordem_pcp_id),
  modulo_id bigint references multiteiner.modulo(modulo_id),
  fluxo varchar(20) not null,
  status varchar(40) not null
);

create table if not exists multiteiner.ordem_producao_etapa (
  etapa_id bigint primary key,
  ordem_producao_id bigint not null references multiteiner.ordem_producao(ordem_producao_id),
  sequencia integer not null,
  etapa varchar(80) not null,
  inicio timestamp,
  fim timestamp,
  status varchar(40) not null,
  retrabalho boolean not null default false
);

create table if not exists multiteiner.inspecao_qualidade (
  inspecao_id bigint primary key,
  modulo_id bigint not null references multiteiner.modulo(modulo_id),
  etapa_id bigint,
  resultado varchar(20) not null check (resultado in ('APROVADO','FALHA')),
  nao_conformidade varchar(500),
  realizado_em timestamp not null default current_timestamp
);

create table if not exists multiteiner.expedicao (
  expedicao_id bigint primary key,
  demanda_id bigint not null references multiteiner.demanda(demanda_id),
  status varchar(40) not null,
  data_saida timestamp,
  local_destino varchar(255)
);

create table if not exists multiteiner.retorno_modulo (
  retorno_id bigint primary key,
  modulo_id bigint not null references multiteiner.modulo(modulo_id),
  data_retorno timestamp not null,
  motivo varchar(255),
  status varchar(40) not null
);

create table if not exists multiteiner.quarentena (
  quarentena_id bigint primary key,
  retorno_id bigint not null references multiteiner.retorno_modulo(retorno_id),
  modulo_id bigint not null references multiteiner.modulo(modulo_id),
  entrada timestamp not null,
  saida timestamp,
  condicao_inicial varchar(500),
  status varchar(40) not null
);

create table if not exists multiteiner.avaria (
  avaria_id bigint primary key,
  modulo_id bigint not null references multiteiner.modulo(modulo_id),
  quarentena_id bigint references multiteiner.quarentena(quarentena_id),
  componente varchar(120),
  tipo varchar(120),
  severidade varchar(30),
  causa_provavel varchar(255),
  descricao varchar(1000),
  prioridade integer,
  identificada_em timestamp not null default current_timestamp
);

create table if not exists multiteiner.ordem_reparo (
  ordem_reparo_id bigint primary key,
  modulo_id bigint not null references multiteiner.modulo(modulo_id),
  origem varchar(30) not null check (origem in ('QUALIDADE','RETORNO_LOCACAO','OUTRO')),
  diagnostico varchar(1000),
  oficina varchar(80),
  prioridade integer,
  status varchar(40) not null
);

create table if not exists multiteiner.reparo_etapa (
  reparo_etapa_id bigint primary key,
  ordem_reparo_id bigint not null references multiteiner.ordem_reparo(ordem_reparo_id),
  etapa varchar(80) not null,
  inicio timestamp,
  fim timestamp,
  status varchar(40) not null
);

create table if not exists multiteiner.reparo_material (
  reparo_material_id bigint primary key,
  ordem_reparo_id bigint not null references multiteiner.ordem_reparo(ordem_reparo_id),
  material_id bigint not null,
  quantidade numeric(14,3) not null,
  custo_unitario numeric(14,2)
);

create table if not exists multiteiner.apontamento_reparo (
  apontamento_id bigint primary key,
  ordem_reparo_id bigint not null references multiteiner.ordem_reparo(ordem_reparo_id),
  equipe_id bigint,
  profissional_id bigint,
  horas numeric(10,2) not null,
  apontado_em timestamp not null default current_timestamp
);

create table if not exists multiteiner.teste_reparo (
  teste_reparo_id bigint primary key,
  ordem_reparo_id bigint not null references multiteiner.ordem_reparo(ordem_reparo_id),
  resultado varchar(20) not null check (resultado in ('APROVADO','FALHA')),
  observacao varchar(1000),
  realizado_em timestamp not null default current_timestamp
);

create table if not exists multiteiner.estoque_seguranca (
  estoque_seguranca_id bigint primary key,
  modulo_id bigint not null references multiteiner.modulo(modulo_id),
  entrada timestamp not null,
  saida timestamp,
  motivo varchar(255),
  status varchar(40) not null
);

-- ELO process orchestration: every process event must point back to a source object.
create table if not exists multiteiner.elo_evento_processo (
  evento_id bigint primary key,
  processo varchar(80) not null,
  etapa varchar(120) not null,
  gate varchar(120),
  setor_responsavel varchar(80),
  objeto_tipo varchar(80) not null,
  objeto_id bigint not null,
  status varchar(40) not null,
  criado_em timestamp not null default current_timestamp
);

create table if not exists multiteiner.elo_sinal (
  sinal_id bigint primary key,
  origem_tipo varchar(80) not null,
  origem_id bigint not null,
  tipo_sinal varchar(80) not null,
  severidade varchar(20),
  indicador varchar(120),
  valor numeric(18,4),
  detectado_em timestamp not null default current_timestamp,
  status varchar(30) not null
);

create table if not exists multiteiner.elo_plano_tatico (
  plano_id bigint primary key,
  sinal_id bigint references multiteiner.elo_sinal(sinal_id),
  objetivo varchar(500) not null,
  acao varchar(1000) not null,
  responsavel_setor varchar(80),
  prazo date,
  status varchar(40) not null
);

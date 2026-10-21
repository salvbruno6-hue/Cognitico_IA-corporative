-- Registra a fonte comercial usada na baseline executiva sem hardcode de UUID.
-- O arquivo bruto nao e promovido a autoridade operacional; a referencia preserva hash e proveniencia.

insert into public.mt_referencias_fontes (
  tipo_fonte,
  referencia,
  titulo,
  origem
)
select
  'BASE_COMERCIAL_USUARIO',
  'upload://Copia-de-Relatorio-Comercial-1.csv#sha256=181cba3132f844e855fa8f846ef25b7f1b41d6d147bc33acda5bda59e4daf59a',
  'Cópia de Relatório Comercial (1).csv',
  'Arquivo fornecido pelo usuário em 2026-10-21; baseline analítica Comercial/PCP'
where not exists (
  select 1
  from public.mt_referencias_fontes
  where referencia = 'upload://Copia-de-Relatorio-Comercial-1.csv#sha256=181cba3132f844e855fa8f846ef25b7f1b41d6d147bc33acda5bda59e4daf59a'
);
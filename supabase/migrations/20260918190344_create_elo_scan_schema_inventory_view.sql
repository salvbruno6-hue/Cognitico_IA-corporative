create or replace view public.elo_scan_schema_inventory as
select
  table_name,
  table_type
from information_schema.tables
where table_schema = 'public'
  and table_type in ('BASE TABLE', 'VIEW')
order by table_name;

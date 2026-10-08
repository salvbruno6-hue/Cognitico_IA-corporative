-- Run after the migration. Catalog checks are read-only; role probes are rolled back.
BEGIN;
DO $$
DECLARE role_name text; privilege_name text;
BEGIN
  IF NOT (SELECT relrowsecurity FROM pg_class WHERE oid='public.mt_gates'::regclass)
     OR EXISTS (SELECT 1 FROM pg_policy WHERE polrelid='public.mt_gates'::regclass) THEN
    RAISE EXCEPTION 'mt_gates fail-closed RLS boundary changed';
  END IF;
  FOREACH role_name IN ARRAY ARRAY['anon','authenticated'] LOOP
    FOREACH privilege_name IN ARRAY ARRAY['SELECT','INSERT','UPDATE','DELETE','TRUNCATE','REFERENCES','TRIGGER'] LOOP
      IF has_table_privilege(role_name,'public.mt_gates',privilege_name) THEN
        RAISE EXCEPTION '% unexpectedly has % on mt_gates',role_name,privilege_name;
      END IF;
    END LOOP;
  END LOOP;
  FOREACH privilege_name IN ARRAY ARRAY['SELECT','INSERT','UPDATE','DELETE'] LOOP
    IF NOT has_table_privilege('service_role','public.mt_gates',privilege_name)
       OR NOT has_table_privilege('postgres','public.mt_gates',privilege_name) THEN
      RAISE EXCEPTION 'Existing server/admin % path was lost',privilege_name;
    END IF;
  END LOOP;
  IF NOT EXISTS(SELECT 1 FROM pg_attribute WHERE attrelid='public.mt_gates'::regclass
                AND attname='tenant_id' AND attnotnull AND NOT attisdropped) THEN
    RAISE EXCEPTION 'Tenant identifier contract was lost';
  END IF;
END $$;
SET LOCAL ROLE anon;
DO $$ BEGIN
  BEGIN PERFORM 1 FROM public.mt_gates LIMIT 1;
    RAISE EXCEPTION 'Anonymous read unexpectedly succeeded';
  EXCEPTION WHEN insufficient_privilege THEN NULL; END;
END $$;
RESET ROLE;
SET LOCAL ROLE authenticated;
DO $$ BEGIN
  BEGIN PERFORM 1 FROM public.mt_gates LIMIT 1;
    RAISE EXCEPTION 'Authenticated direct read unexpectedly succeeded';
  EXCEPTION WHEN insufficient_privilege THEN NULL; END;
END $$;
RESET ROLE;
SET LOCAL ROLE service_role;
SELECT count(*) AS server_readable_rows FROM public.mt_gates;
RESET ROLE;
ROLLBACK;

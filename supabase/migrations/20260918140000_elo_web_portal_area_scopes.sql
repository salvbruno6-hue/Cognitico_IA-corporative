-- Canonical operational area scopes used by the ELO Web portal.
-- Scopes identify governed areas; capabilities identify permitted operations.

UPDATE public.elo_scopes
SET scope_type = 'DOMAIN',
    description = 'PCP — Lista-Mãe: concepção, composição, quantidades e valores unitários.',
    active = true
WHERE scope_key = 'PCP-LISTA-MAE';

INSERT INTO public.elo_scopes (scope_type, scope_key, description, active)
SELECT 'DOMAIN', 'PCP-LISTA-MAE', 'PCP — Lista-Mãe: concepção, composição, quantidades e valores unitários.', true
WHERE NOT EXISTS (
  SELECT 1 FROM public.elo_scopes WHERE scope_key = 'PCP-LISTA-MAE'
);

UPDATE public.elo_scopes
SET scope_type = 'DOMAIN',
    description = 'Gestão — Almoxarifado: estoque físico, entradas, saídas, reservas e localização.',
    active = true
WHERE scope_key = 'GESTAO-ALMOXARIFADO';

INSERT INTO public.elo_scopes (scope_type, scope_key, description, active)
SELECT 'DOMAIN', 'GESTAO-ALMOXARIFADO', 'Gestão — Almoxarifado: estoque físico, entradas, saídas, reservas e localização.', true
WHERE NOT EXISTS (
  SELECT 1 FROM public.elo_scopes WHERE scope_key = 'GESTAO-ALMOXARIFADO'
);

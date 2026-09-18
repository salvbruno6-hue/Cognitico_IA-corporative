-- Canonical operational area scopes used by the ELO Web portal.
-- Scopes are separate from capabilities: the scope identifies the governed area,
-- while the capability identifies the permitted operation within that area.

UPDATE public.elo_scopes
SET description = 'PCP — Lista-Mãe: concepção, composição, quantidades e valores unitários.',
    active = true
WHERE scope_key = 'PCP-LISTA-MAE';

INSERT INTO public.elo_scopes (scope_key, description, active)
SELECT 'PCP-LISTA-MAE', 'PCP — Lista-Mãe: concepção, composição, quantidades e valores unitários.', true
WHERE NOT EXISTS (
  SELECT 1 FROM public.elo_scopes WHERE scope_key = 'PCP-LISTA-MAE'
);

UPDATE public.elo_scopes
SET description = 'Gestão — Almoxarifado: estoque físico, entradas, saídas, reservas e localização.',
    active = true
WHERE scope_key = 'GESTAO-ALMOXARIFADO';

INSERT INTO public.elo_scopes (scope_key, description, active)
SELECT 'GESTAO-ALMOXARIFADO', 'Gestão — Almoxarifado: estoque físico, entradas, saídas, reservas e localização.', true
WHERE NOT EXISTS (
  SELECT 1 FROM public.elo_scopes WHERE scope_key = 'GESTAO-ALMOXARIFADO'
);

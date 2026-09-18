-- Canonical operational area scopes used by the ELO Web portal.
-- Scopes are separate from capabilities: the scope identifies the governed area,
-- while the capability identifies the permitted operation within that area.

INSERT INTO public.elo_scopes (scope_key, description, active)
VALUES
  ('PCP-LISTA-MAE', 'PCP — Lista-Mãe: concepção, composição, quantidades e valores unitários.', true),
  ('GESTAO-ALMOXARIFADO', 'Gestão — Almoxarifado: estoque físico, entradas, saídas, reservas e localização.', true)
ON CONFLICT (scope_key) DO UPDATE
SET description = EXCLUDED.description,
    active = EXCLUDED.active;

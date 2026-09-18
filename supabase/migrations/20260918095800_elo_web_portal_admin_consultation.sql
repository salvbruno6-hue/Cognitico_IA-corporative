-- Grant portal consultation to the existing ELO_ADMIN role only.
-- No write capability is granted.
INSERT INTO public.elo_role_capabilities (role_id, capability_id)
SELECT r.role_id, c.capability_id
FROM public.elo_roles r
CROSS JOIN public.elo_capabilities c
WHERE r.code='ELO_ADMIN' AND r.active=true AND c.code='PORTAL_READ' AND c.active=true
  AND NOT EXISTS (
    SELECT 1 FROM public.elo_role_capabilities rc
    WHERE rc.role_id=r.role_id AND rc.capability_id=c.capability_id
  );

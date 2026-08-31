export const ELO_BASE_PATH = '/Cognitico_IA-corporative/';
export const ELO_AUTH_CALLBACK = `${ELO_BASE_PATH}auth/callback`;

export function eloPath(path = ''): string {
  const normalized = path.replace(/^\/+/, '');
  return `${ELO_BASE_PATH}${normalized}`;
}

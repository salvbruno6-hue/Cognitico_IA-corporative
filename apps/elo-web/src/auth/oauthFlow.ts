/** ELO Web OAuth lifecycle adapter. Supabase remains the session authority. */
type Auth = {
  getSession(): Promise<{ data: { session: unknown }; error: { message: string } | null }>;
  exchangeCodeForSession(code: string): Promise<{ data: { session: unknown }; error: { message: string } | null }>;
  signInWithOAuth(options: { provider: "google"; options: { redirectTo: string } }): Promise<{ error: { message: string } | null }>;
};
export function createOAuthFlow(auth: Auth) {
  let starting: Promise<void> | undefined;
  let callback: Promise<void> | undefined;
  return {
    start(origin: string) {
      if (starting) return starting;
      starting = (async () => {
        const { data, error } = await auth.getSession();
        if (error) throw new Error(error.message);
        if (data.session) return;
        const result = await auth.signInWithOAuth({ provider: "google", options: { redirectTo: `${origin}/auth/callback` } });
        if (result.error) throw new Error(result.error.message);
      })().catch(error => { starting = undefined; throw error; });
      return starting;
    },
    complete(href: string, clean: () => void) {
      if (callback) return callback;
      const params = new URL(href).searchParams;
      const code = params.get("code");
      const oauthError = params.get("error_description") ?? params.get("error");
      // Publish the promise before cleanup/remount; all subscribers await the same exchange.
      callback = Promise.resolve().then(async () => {
        if (oauthError) throw new Error(oauthError);
        const current = await auth.getSession();
        if (current.error) throw new Error(current.error.message);
        if (current.data.session) return;
        if (!code) throw new Error("O retorno do Google não trouxe um código de autenticação válido.");
        const exchanged = await auth.exchangeCodeForSession(code);
        if (exchanged.error) throw new Error(exchanged.error.message);
        const persisted = await auth.getSession();
        if (persisted.error) throw new Error(persisted.error.message);
        if (!persisted.data.session) throw new Error("Não foi possível confirmar a sessão Supabase.");
      });
      clean();
      return callback;
    },
  };
}

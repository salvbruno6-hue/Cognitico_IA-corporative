import { Navigate, Route, Routes } from 'react-router-dom';
import { ELOAuthCallback } from './auth/ELOAuthCallback';
import { ELOGoogleLogin } from './auth/ELOGoogleLogin';

function ELOCore() {
  return (
    <main className="elo-core" data-elo-core="authenticated">
      <div className="elo-core__status"><span /> CONECTADO AO ELO</div>
      <h1>Núcleo ELO</h1>
      <p>Sessão autenticada. A camada de inteligência corporativa está disponível.</p>
      <div className="elo-core__grid">
        <article><strong>MEMÓRIA</strong><span>Conhecimento</span></article>
        <article><strong>PROCESSAMENTO</strong><span>Arbitragem</span></article>
        <article><strong>DECISÃO</strong><span>Governança</span></article>
      </div>
    </main>
  );
}

function Login() {
  return <ELOGoogleLogin><ELOCore /></ELOGoogleLogin>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/auth/callback" element={<ELOAuthCallback />} />
      <Route path="/app/*" element={<Login />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

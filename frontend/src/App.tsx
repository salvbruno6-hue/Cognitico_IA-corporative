import { useState } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { ELOAuthCallback } from './auth/ELOAuthCallback';
import { ELOGoogleLogin } from './auth/ELOGoogleLogin';

type CoreArea = 'memoria' | 'processamento' | 'decisao' | null;

const areaContent = {
  memoria: {
    title: 'Memória',
    text: 'Camada de conhecimento do ELO. Aqui ficarão consultas, registros e referências consolidadas.',
  },
  processamento: {
    title: 'Processamento',
    text: 'Camada de arbitragem do ELO. Aqui ficarão análises, validações e processamento das informações.',
  },
  decisao: {
    title: 'Decisão',
    text: 'Camada de governança do ELO. Aqui ficarão decisões arbitradas, diretrizes e controles.',
  },
} as const;

function ELOCore() {
  const [activeArea, setActiveArea] = useState<CoreArea>(null);

  return (
    <main className="elo-core" data-elo-core="authenticated">
      <div className="elo-core__status"><span /> CONECTADO AO ELO</div>
      <h1>Núcleo ELO</h1>
      <p>Sessão autenticada. A camada de inteligência corporativa está disponível.</p>

      <div className="elo-core__grid" aria-label="Áreas do ELO">
        <button type="button" className="elo-core__card" onClick={() => setActiveArea('memoria')}>
          <strong>MEMÓRIA</strong>
          <span>Conhecimento</span>
          <small>Consultar →</small>
        </button>
        <button type="button" className="elo-core__card" onClick={() => setActiveArea('processamento')}>
          <strong>PROCESSAMENTO</strong>
          <span>Arbitragem</span>
          <small>Consultar →</small>
        </button>
        <button type="button" className="elo-core__card" onClick={() => setActiveArea('decisao')}>
          <strong>DECISÃO</strong>
          <span>Governança</span>
          <small>Consultar →</small>
        </button>
      </div>

      {activeArea && (
        <section className="elo-core__panel" aria-live="polite">
          <div>
            <strong>{areaContent[activeArea].title}</strong>
            <p>{areaContent[activeArea].text}</p>
          </div>
          <button type="button" onClick={() => setActiveArea(null)}>Fechar</button>
        </section>
      )}
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

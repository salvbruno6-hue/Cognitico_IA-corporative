import React, { useMemo, useState } from 'react';

type Item = {
  id: string;
  descricao: string;
  modelo?: string;
  unidade: string;
  quantidade: number;
  origem: 'lista-mae' | 'modelo' | 'excedente' | 'interligacao' | 'especialista';
  status: 'identificado' | 'validado' | 'pendente' | 'aprovacao';
};

type Audit = { regra: string; resultado: 'OK' | 'ATENÇÃO' | 'BLOQUEIO'; detalhe: string };

const seed: Item[] = [
  { id: 'MLT.M01', descricao: 'Módulo Amplo 20 pés', modelo: 'MLT.M01', unidade: 'un', quantidade: 5, origem: 'lista-mae', status: 'validado' },
  { id: 'EXC-001', descricao: 'Janela adicional', unidade: 'un', quantidade: 3, origem: 'excedente', status: 'identificado' },
  { id: 'EXC-002', descricao: 'Divisória adicional', unidade: 'm²', quantidade: 1, origem: 'excedente', status: 'identificado' },
  { id: 'EXC-003', descricao: 'Tomada adicional', unidade: 'un', quantidade: 1, origem: 'excedente', status: 'identificado' },
  { id: 'INT-001', descricao: 'Interligação elétrica entre módulos', unidade: 'serv', quantidade: 1, origem: 'interligacao', status: 'pendente' },
];

const audits: Audit[] = [
  { regra: 'Taxonomia MLT', resultado: 'OK', detalhe: 'Modelo reconhecido e associado à família.' },
  { regra: 'Dimensões', resultado: 'OK', detalhe: 'Padrão atual: altura 3010 mm; área interna conforme cadastro vigente.' },
  { regra: 'Excedentes', resultado: 'ATENÇÃO', detalhe: 'Itens fora da composição padrão foram segregados.' },
  { regra: 'Interligações', resultado: 'ATENÇÃO', detalhe: 'Especialista deve validar composição e dependências.' },
  { regra: 'Valor de tabela', resultado: 'OK', detalhe: 'Preço do modelo deve vir da Lista-Mãe; não estimar quando cadastrado.' },
];

export const ELOOrcamentoView: React.FC = () => {
  const [items, setItems] = useState(seed);
  const [command, setCommand] = useState('');
  const [message, setMessage] = useState('Aguardando instrução do especialista.');

  const pending = useMemo(() => items.filter((item) => item.status === 'pendente').length, [items]);
  const approved = useMemo(() => items.filter((item) => item.status === 'validado').length, [items]);

  const audit = () => {
    setMessage(`Auditoria concluída: ${approved} itens validados, ${pending} itens aguardando especialista.`);
  };

  const requestSpecialist = () => {
    setItems((current) => current.map((item) => item.status === 'pendente' ? { ...item, status: 'aprovacao' } : item));
    setMessage('ELO solicitou ao especialista a validação das interligações e dos excedentes.');
  };

  const processCommand = () => {
    const normalized = command.trim().toLowerCase();
    if (!normalized) return;
    if (normalized.includes('orçar') || normalized.includes('orcamento')) {
      setMessage('Modo orçamento ativado: Lista-Mãe → taxonomia → modelo → excedentes → interligações → auditoria.');
    } else if (normalized.includes('comparar')) {
      setMessage('Comparação preparada: separar preço fechado de tabela, excedentes e composições variáveis.');
    } else {
      setMessage('Solicitação registrada para análise sem alterar a estrutura canônica.');
    }
    setCommand('');
  };

  return (
    <main className="elo-budget" aria-label="ELO Orçamento e Auditoria">
      <header className="elo-budget__header">
        <div>
          <span className="eyebrow">ELO • FORGE • ORÇAMENTO</span>
          <h1>Orçamento Cognitivo</h1>
          <p>Auditoria de relações, reconhecimento de modelos e preparação da decisão do especialista.</p>
        </div>
        <div className="status-pill">● Execução supervisionada</div>
      </header>

      <section className="metrics">
        <article><strong>{items.length}</strong><span>itens rastreados</span></article>
        <article><strong>{approved}</strong><span>validados</span></article>
        <article><strong>{items.filter(i => i.origem === 'excedente').length}</strong><span>excedentes</span></article>
        <article><strong>{pending}</strong><span>pendências</span></article>
      </section>

      <section className="flow" aria-label="Fluxo de orçamento">
        {['Entrada', 'Lista-Mãe', 'Taxonomia', 'Modelo', 'Excedentes', 'Relações', 'Especialista', 'Decisão'].map((step, index) => (
          <React.Fragment key={step}>
            <div className={`flow-step ${index < 4 ? 'is-active' : ''}`}><b>{String(index + 1).padStart(2, '0')}</b>{step}</div>
            {index < 7 && <span className="flow-arrow">→</span>}
          </React.Fragment>
        ))}
      </section>

      <section className="workspace">
        <div className="panel">
          <div className="panel-title"><h2>Estrutura do orçamento</h2><button onClick={audit}>Auditar</button></div>
          <div className="table-wrap">
            <table><thead><tr><th>Item</th><th>Modelo</th><th>Qtd.</th><th>Origem</th><th>Status</th></tr></thead>
              <tbody>{items.map(item => <tr key={item.id}><td><b>{item.id}</b><br />{item.descricao}</td><td>{item.modelo ?? '—'}</td><td>{item.quantidade} {item.unidade}</td><td>{item.origem}</td><td><span className={`badge ${item.status}`}>{item.status}</span></td></tr>)}</tbody>
            </table>
          </div>
        </div>

        <aside className="panel audit-panel">
          <div className="panel-title"><h2>Auditoria de relações</h2><span>CORE</span></div>
          {audits.map(row => <div className="audit-row" key={row.regra}><div><b>{row.regra}</b><small>{row.detalhe}</small></div><strong className={row.resultado.toLowerCase()}>{row.resultado}</strong></div>)}
          <button className="primary" onClick={requestSpecialist}>Solicitar validação ao especialista</button>
        </aside>
      </section>

      <section className="specialist">
        <div><span className="eyebrow">CANAL ESPECIALISTA</span><h2>O ELO encontrou uma decisão?</h2><p>{message}</p></div>
        <div className="command"><input value={command} onChange={e => setCommand(e.target.value)} onKeyDown={e => e.key === 'Enter' && processCommand()} placeholder="Ex.: orçar M01, comparar valores, analisar excedentes..." /><button onClick={processCommand}>Executar</button></div>
      </section>

      <style>{`
        .elo-budget{min-height:100vh;padding:32px;background:#0b1020;color:#e8ecf5;font-family:Inter,system-ui,sans-serif}.elo-budget__header,.workspace,.specialist,.metrics{max-width:1240px;margin:auto}.elo-budget__header{display:flex;justify-content:space-between;gap:24px;align-items:flex-start}.eyebrow{font-size:11px;letter-spacing:.14em;color:#7dd3fc;font-weight:800}.elo-budget h1{font-size:34px;margin:8px 0}.elo-budget p{color:#9aa6bd}.status-pill{padding:10px 14px;border:1px solid #24405d;border-radius:999px;color:#8ee0b2}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:24px}.metrics article,.panel,.specialist{background:#11182a;border:1px solid #202c43;border-radius:16px}.metrics article{padding:18px}.metrics strong{display:block;font-size:28px}.metrics span{color:#8c99b2;font-size:13px}.flow{max-width:1240px;margin:20px auto;display:flex;align-items:center;justify-content:space-between;gap:6px;overflow:auto}.flow-step{padding:9px 11px;border:1px solid #293750;border-radius:10px;color:#74819a;white-space:nowrap}.flow-step b{margin-right:7px}.flow-step.is-active{border-color:#25617e;color:#b7ecff;background:#0d2433}.flow-arrow{color:#52627d}.workspace{display:grid;grid-template-columns:1.7fr 1fr;gap:16px}.panel{padding:18px}.panel-title{display:flex;justify-content:space-between;align-items:center}.panel-title h2,.specialist h2{margin:0 0 8px}.panel button,.primary,.command button{border:0;border-radius:9px;padding:9px 13px;background:#1c789d;color:white;font-weight:700}.table-wrap{overflow:auto;margin-top:14px}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:12px;border-bottom:1px solid #202c43;font-size:13px}th{color:#7f8ca5}.badge{padding:5px 8px;border-radius:999px;font-size:11px}.validado{background:#153c2c;color:#8ee0b2}.identificado{background:#29344a;color:#b5c3dc}.pendente,.aprovacao{background:#4a3515;color:#f3c96b}.audit-row{display:flex;justify-content:space-between;gap:12px;padding:13px 0;border-bottom:1px solid #202c43}.audit-row small{display:block;color:#8995aa;margin-top:4px}.audit-row strong{font-size:11px}.ok{color:#8ee0b2}.atenção{color:#f3c96b}.bloqueio{color:#ff8c8c}.primary{width:100%;margin-top:16px}.specialist{margin-top:16px;padding:20px;display:flex;justify-content:space-between;gap:24px;align-items:center}.command{display:flex;min-width:48%}.command input{flex:1;background:#0b1020;border:1px solid #2a3851;color:white;padding:12px;border-radius:9px 0 0 9px}.command button{border-radius:0 9px 9px 0}@media(max-width:900px){.metrics{grid-template-columns:repeat(2,1fr)}.workspace,.specialist{grid-template-columns:1fr;display:grid}.elo-budget__header{display:block}.flow{justify-content:flex-start}}
      `}</style>
    </main>
  );
};

export default ELOOrcamentoView;

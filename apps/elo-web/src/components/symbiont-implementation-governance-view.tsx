"use client";

type ImplementationView = {
  implementation_id: string;
  phase: "START" | "END";
  candidate_id: string;
  owner: string;
  functional_branch: string;
  capability: string;
  specialization?: string | null;
  ownership: string;
  source_ref: string;
  source_commit: string;
  evidence_refs: string[];
  environment: string;
  loop_stage: string;
  loop_result?: string | null;
  evolution_level: number;
  evolution_levels_total: number;
  evolution_gate_status: string;
  governance_status: string;
  runtime_status: string;
  tree_path: string[];
};

type Props = {
  startView?: ImplementationView | null;
  endView?: ImplementationView | null;
};

const phaseLabel: Record<ImplementationView["phase"], string> = {
  START: "Início do loop",
  END: "Fim do loop",
};

function Tree({ view }: { view: ImplementationView }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-950 p-4 font-mono text-xs text-white">
      {view.tree_path.map((node, index) => (
        <div key={`${node}-${index}`} className="leading-6" style={{ paddingLeft: index * 14 }}>
          <span className="text-white/35">{index === view.tree_path.length - 1 ? "└── " : "├── "}</span>
          <span className={index === view.tree_path.length - 1 ? "font-semibold text-white" : "text-white/70"}>{node}</span>
        </div>
      ))}
      <div className="mt-2 border-t border-white/10 pt-2 text-white">
        ◄ IMPLEMENTAÇÃO {view.implementation_id}
      </div>
    </div>
  );
}

function ViewCard({ title, view }: { title: string; view: ImplementationView }) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="text-[10px] font-bold uppercase tracking-[.18em] text-slate-400">{title}</div>
          <h3 className="mt-1 font-semibold">{phaseLabel[view.phase]}</h3>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold">
          Nível {view.evolution_level}/{view.evolution_levels_total}
        </span>
      </div>
      <div className="mt-4 grid gap-3 text-xs sm:grid-cols-2">
        <div><span className="text-slate-400">Estado</span><div className="mt-1 font-semibold">{view.loop_stage}</div></div>
        <div><span className="text-slate-400">Resultado</span><div className="mt-1 font-semibold">{view.loop_result ?? "—"}</div></div>
        <div><span className="text-slate-400">Owner</span><div className="mt-1">{view.owner}</div></div>
        <div><span className="text-slate-400">Ownership</span><div className="mt-1">{view.ownership}</div></div>
        <div><span className="text-slate-400">Evolution Gate</span><div className="mt-1">{view.evolution_gate_status}</div></div>
        <div><span className="text-slate-400">Governança</span><div className="mt-1">{view.governance_status}</div></div>
        <div><span className="text-slate-400">Runtime</span><div className="mt-1">{view.runtime_status}</div></div>
        <div><span className="text-slate-400">Evidências</span><div className="mt-1">{view.evidence_refs.length}</div></div>
      </div>
      <div className="mt-4"><Tree view={view} /></div>
    </article>
  );
}

export function SymbiontImplementationGovernanceView({ startView, endView }: Props) {
  if (!startView && !endView) {
    return (
      <section className="rounded-[2rem] border border-slate-200 bg-white p-6">
        <div className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-400">EVOLUÇÃO · SYMBIONT</div>
        <h2 className="mt-2 text-xl font-semibold">View de implantação</h2>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          Nenhum loop de implantação está disponível para leitura. A ausência de dados não é convertida em estado positivo.
        </p>
      </section>
    );
  }

  return (
    <section className="space-y-4">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6">
        <div className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-400">EVOLUÇÃO · SYMBIONT</div>
        <h2 className="mt-2 text-xl font-semibold">Implantação governada</h2>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          Read model: início → loop → fim. Esta view não autoriza mutação canônica, promoção ou deploy.
        </p>
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        {startView && <ViewCard title="START VIEW" view={startView} />}
        {endView && <ViewCard title="END VIEW" view={endView} />}
      </div>
    </section>
  );
}

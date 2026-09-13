"use client";

type Props = {
  onClose?: () => void;
};

const traceabilityColumns = [
  "Nº",
  "Tópico / Item",
  "REFERÊNCIA TR / DOCUMENTO",
  "Requisito / Descrição da SO",
  "Solução Técnica Proposta",
  "Quantitativo",
  "Unid.",
  "Composição / Escopo",
  "Premissa / Critério",
  "Referência do Orçamento",
  "Valor",
  "Inclusão no Orçamento",
  "Atendimento",
  "Observação / Pendência",
];

export function EloPtsPosTable({ onClose }: Props) {
  return (
    <section className="rounded-[2rem] border border-slate-200 bg-white shadow-sm">
      <div className="flex flex-col gap-4 border-b border-slate-200 p-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-400">PTS · Pós-Orçamento</div>
          <h2 className="mt-1 text-2xl font-semibold tracking-tight">Matriz de Rastreabilidade Técnica e Orçamentária</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Estrutura canônica da PTS Técnica Pós-Orçamento. A tabela exibe a matriz obrigatória e preserva a separação entre referência da exigência e referência do orçamento.
          </p>
        </div>
        {onClose && (
          <button type="button" onClick={onClose} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50">
            Fechar PTS
          </button>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-[2100px] border-collapse text-left text-xs">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50 text-[10px] font-bold uppercase tracking-[.12em] text-slate-500">
              {traceabilityColumns.map((column) => (
                <th key={column} className="whitespace-nowrap px-4 py-3 align-top">{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-slate-100">
              <td colSpan={traceabilityColumns.length} className="px-4 py-12 text-center text-slate-400">
                PTS-POS-001 · DRAFT · aguardando dados da solicitação/orçamento para preenchimento dos itens.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="border-t border-slate-200 bg-slate-50/60 p-4 text-xs text-slate-500">
        Fluxo governado: análise → recomendação → arbitragem → decisão. Lacunas não devem ser preenchidas por inferência silenciosa.
      </div>
    </section>
  );
}

export type SectorKey =
  | "planejamento"
  | "comercial"
  | "financeiro"
  | "rh"
  | "operacoes"
  | "pcp"
  | "ti";

export type Sector = {
  key: SectorKey;
  label: string;
  subtitle: string;
  accent: string;
  metrics: { label: string; value: string; delta: string; source: "reference" | "cognitive" }[];
  chartTitle: string;
  chartValues: number[];
  quickActions: string[];
};

const referenceMetric = (label: string) => ({ label, value: "—", delta: "Cognitivo", source: "reference" as const });

export const sectors: Sector[] = [
  { key: "planejamento", label: "Planejamento", subtitle: "Inteligência para decisões e propostas", accent: "#2563eb", metrics: [referenceMetric("Solicitações abertas"), referenceMetric("Orçamentos"), referenceMetric("Licitações"), referenceMetric("Em análise")], chartTitle: "Carteira de solicitações", chartValues: [], quickActions: ["Nova solicitação", "Analisar orçamento", "Consultar ELO", "Abrir relatório"] },
  { key: "comercial", label: "Comercial", subtitle: "Mais oportunidades, mais resultados", accent: "#b45309", metrics: [referenceMetric("Leads ativos"), referenceMetric("Oportunidades"), referenceMetric("Propostas"), referenceMetric("Conversão")], chartTitle: "Vendas por período", chartValues: [], quickActions: ["Qualificar lead", "Gerar proposta", "Analisar conversão", "Identificar risco"] },
  { key: "financeiro", label: "Financeiro", subtitle: "Gestão inteligente de recursos", accent: "#047857", metrics: [referenceMetric("Saldo atual"), referenceMetric("Contas a pagar"), referenceMetric("Contas a receber"), referenceMetric("Orçamento")], chartTitle: "Fluxo de caixa", chartValues: [], quickActions: ["Gerar relatório", "Analisar despesas", "Prever fluxo", "Ver inadimplência"] },
  { key: "rh", label: "Recursos Humanos", subtitle: "Pessoas que fazem o futuro", accent: "#6d28d9", metrics: [referenceMetric("Colaboradores"), referenceMetric("Novas contratações"), referenceMetric("Turnover"), referenceMetric("Satisfação")], chartTitle: "Distribuição por área", chartValues: [], quickActions: ["Abrir vaga", "Analisar clima", "Plano de desenvolvimento", "Relatório de desempenho"] },
  { key: "operacoes", label: "Operações", subtitle: "Processos eficientes, resultados consistentes", accent: "#c2410c", metrics: [referenceMetric("Processos ativos"), referenceMetric("Tarefas em andamento"), referenceMetric("SLA no prazo"), referenceMetric("Incidentes")], chartTitle: "Produtividade semanal", chartValues: [], quickActions: ["Iniciar processo", "Verificar gargalos", "Gerar relatório", "Acompanhar fornecedor"] },
  { key: "pcp", label: "PCP", subtitle: "Capacidade, produção e gargalos", accent: "#0f766e", metrics: [referenceMetric("Ordens abertas"), referenceMetric("Capacidade"), referenceMetric("Gargalos"), referenceMetric("Estoque crítico")], chartTitle: "Carga de produção", chartValues: [], quickActions: ["Programar produção", "Ver Gantt", "Analisar estoque", "Detectar gargalo"] },
  { key: "ti", label: "Tecnologia da Informação", subtitle: "Infraestrutura segura, inovação contínua", accent: "#1d4ed8", metrics: [referenceMetric("Sistemas ativos"), referenceMetric("Chamados abertos"), referenceMetric("Disponibilidade"), referenceMetric("Riscos de segurança")], chartTitle: "Status dos sistemas", chartValues: [], quickActions: ["Abrir chamado", "Ver status", "Analisar vulnerabilidades", "Gerar relatório"] },
];

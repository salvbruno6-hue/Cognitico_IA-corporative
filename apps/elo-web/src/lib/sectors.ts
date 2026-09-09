export type SectorKey =
  | "planejamento"
  | "comercial"
  | "financeiro"
  | "rh"
  | "operacoes"
  | "pcp"
  | "producao"
  | "almoxarifado"
  | "compras"
  | "qualidade"
  | "expedicao"
  | "ti";

export type Sector = {
  key: SectorKey;
  label: string;
  subtitle: string;
  accent: string;
  metrics: { label: string; value: string; delta: string }[];
  chartTitle: string;
  chartValues: number[];
  quickActions: string[];
};

export const sectors: Sector[] = [
  {
    key: "planejamento",
    label: "Planejamento",
    subtitle: "Inteligência para decisões e propostas",
    accent: "#2563eb",
    metrics: [
      { label: "Solicitações abertas", value: "38", delta: "+8%" },
      { label: "Orçamentos", value: "17", delta: "+12%" },
      { label: "Licitações", value: "9", delta: "+3%" },
      { label: "Em análise", value: "6", delta: "-14%" },
    ],
    chartTitle: "Carteira de solicitações",
    chartValues: [42, 55, 49, 68, 61, 76, 82],
    quickActions: ["Nova solicitação", "Analisar orçamento", "Consultar ELO", "Abrir relatório"],
  },
  {
    key: "comercial",
    label: "Comercial",
    subtitle: "Mais oportunidades, mais resultados",
    accent: "#b45309",
    metrics: [
      { label: "Leads ativos", value: "1.248", delta: "+12%" },
      { label: "Oportunidades", value: "320", delta: "+8%" },
      { label: "Propostas", value: "87", delta: "+15%" },
      { label: "Conversão", value: "28%", delta: "+6%" },
    ],
    chartTitle: "Vendas por período",
    chartValues: [28, 35, 46, 54, 63, 78, 91],
    quickActions: ["Qualificar lead", "Gerar proposta", "Analisar conversão", "Identificar risco"],
  },
  {
    key: "financeiro",
    label: "Financeiro",
    subtitle: "Gestão inteligente de recursos",
    accent: "#047857",
    metrics: [
      { label: "Saldo atual", value: "R$ 2,48 mi", delta: "+12%" },
      { label: "Contas a pagar", value: "R$ 320 mil", delta: "-5%" },
      { label: "Contas a receber", value: "R$ 1,12 mi", delta: "+18%" },
      { label: "Orçamento", value: "62%", delta: "+4%" },
    ],
    chartTitle: "Fluxo de caixa",
    chartValues: [58, 66, 62, 74, 81, 76, 94],
    quickActions: ["Gerar relatório", "Analisar despesas", "Prever fluxo", "Ver inadimplência"],
  },
  {
    key: "rh",
    label: "Recursos Humanos",
    subtitle: "Pessoas que fazem o futuro",
    accent: "#6d28d9",
    metrics: [
      { label: "Colaboradores", value: "248", delta: "+5%" },
      { label: "Novas contratações", value: "12", delta: "+20%" },
      { label: "Turnover", value: "3,2%", delta: "-18%" },
      { label: "Satisfação", value: "8,7", delta: "+12%" },
    ],
    chartTitle: "Distribuição por área",
    chartValues: [28, 22, 18, 14, 12, 6],
    quickActions: ["Abrir vaga", "Analisar clima", "Plano de desenvolvimento", "Relatório de desempenho"],
  },
  {
    key: "operacoes",
    label: "Operações",
    subtitle: "Processos eficientes, resultados consistentes",
    accent: "#c2410c",
    metrics: [
      { label: "Processos ativos", value: "32", delta: "+10%" },
      { label: "Tarefas em andamento", value: "48", delta: "-12%" },
      { label: "SLA no prazo", value: "92%", delta: "+5%" },
      { label: "Incidentes", value: "3", delta: "-40%" },
    ],
    chartTitle: "Produtividade semanal",
    chartValues: [54, 61, 58, 69, 72, 76, 89],
    quickActions: ["Iniciar processo", "Verificar gargalos", "Gerar relatório", "Acompanhar fornecedor"],
  },
  {
    key: "pcp",
    label: "PCP",
    subtitle: "Capacidade, produção e gargalos",
    accent: "#0f766e",
    metrics: [
      { label: "Ordens abertas", value: "26", delta: "+4%" },
      { label: "Capacidade", value: "84%", delta: "+7%" },
      { label: "Gargalos", value: "4", delta: "-20%" },
      { label: "Estoque crítico", value: "8", delta: "-11%" },
    ],
    chartTitle: "Carga de produção",
    chartValues: [45, 52, 71, 68, 83, 79, 88],
    quickActions: ["Programar produção", "Ver Gantt", "Analisar estoque", "Detectar gargalo"],
  },
  {
    key: "producao",
    label: "Produção",
    subtitle: "Execução industrial, equipes internas e externas",
    accent: "#9a3412",
    metrics: [
      { label: "Ordens em execução", value: "—", delta: "ELO" },
      { label: "Equipe interna", value: "—", delta: "ELO" },
      { label: "Serviços externos", value: "—", delta: "ELO" },
      { label: "Etapas críticas", value: "—", delta: "ELO" },
    ],
    chartTitle: "Fluxo de produção",
    chartValues: [40, 52, 64, 58, 72, 68, 80],
    quickActions: ["Abrir ordens", "Ver etapas", "Serviços externos", "Consultar PCP"],
  },
  {
    key: "almoxarifado",
    label: "Almoxarifado",
    subtitle: "Estoque, reserva, picking e materiais",
    accent: "#166534",
    metrics: [
      { label: "Itens disponíveis", value: "—", delta: "ELO" },
      { label: "Reservas", value: "—", delta: "ELO" },
      { label: "Rupturas", value: "—", delta: "ELO" },
      { label: "Picking", value: "—", delta: "ELO" },
    ],
    chartTitle: "Disponibilidade de materiais",
    chartValues: [68, 61, 73, 70, 77, 74, 82],
    quickActions: ["Consultar estoque", "Reservar material", "Separar pedido", "Sinalizar ruptura"],
  },
  {
    key: "compras",
    label: "Compras",
    subtitle: "Suprimentos, fornecedores e lead time",
    accent: "#854d0e",
    metrics: [
      { label: "Pedidos abertos", value: "—", delta: "ELO" },
      { label: "Em aprovação", value: "—", delta: "ELO" },
      { label: "Lead time crítico", value: "—", delta: "ELO" },
      { label: "Impactos em AF/Projeto", value: "—", delta: "ELO" },
    ],
    chartTitle: "Pedidos e lead time",
    chartValues: [45, 54, 49, 63, 59, 71, 68],
    quickActions: ["Novo pedido", "Ver aprovações", "Analisar lead time", "Impactos no PCP"],
  },
  {
    key: "qualidade",
    label: "Qualidade",
    subtitle: "Inspeção, não conformidades, liberação e reparo",
    accent: "#7c2d12",
    metrics: [
      { label: "Inspeções", value: "—", delta: "ELO" },
      { label: "Não conformidades", value: "—", delta: "ELO" },
      { label: "Em reparo", value: "—", delta: "ELO" },
      { label: "Liberados", value: "—", delta: "ELO" },
    ],
    chartTitle: "Qualidade e liberação",
    chartValues: [72, 68, 74, 66, 79, 77, 84],
    quickActions: ["Abrir inspeção", "Ver não conformidades", "Liberar item", "Encaminhar reparo"],
  },
  {
    key: "expedicao",
    label: "Expedição",
    subtitle: "Conferência, saída, entrega, quarentena e retorno",
    accent: "#0369a1",
    metrics: [
      { label: "Expedições", value: "—", delta: "ELO" },
      { label: "Em conferência", value: "—", delta: "ELO" },
      { label: "Em quarentena", value: "—", delta: "ELO" },
      { label: "Retornos", value: "—", delta: "ELO" },
    ],
    chartTitle: "Fluxo logístico",
    chartValues: [52, 60, 58, 69, 65, 78, 74],
    quickActions: ["Conferir saída", "Acompanhar entrega", "Ver quarentena", "Processar retorno"],
  },
  {
    key: "ti",
    label: "Tecnologia da Informação",
    subtitle: "Infraestrutura segura, inovação contínua",
    accent: "#1d4ed8",
    metrics: [
      { label: "Sistemas ativos", value: "24", delta: "+4%" },
      { label: "Chamados abertos", value: "8", delta: "-27%" },
      { label: "Disponibilidade", value: "99,8%", delta: "+0,2%" },
      { label: "Riscos de segurança", value: "2", delta: "-50%" },
    ],
    chartTitle: "Status dos sistemas",
    chartValues: [83, 8, 6, 3],
    quickActions: ["Abrir chamado", "Ver status", "Analisar vulnerabilidades", "Gerar relatório"],
  },
];

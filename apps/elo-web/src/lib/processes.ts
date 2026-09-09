export type ProcessId = "planning-demand" | "planning-modular";

export type ProcessNode = {
  id: string;
  label: string;
  kind: "entry" | "stage" | "gate" | "decision" | "output";
  status: "REFERENCE" | "A_VALIDAR";
};

export type ProcessRelation = {
  from: string;
  to: string;
  relation: "contains" | "depends_on" | "provides" | "consumes" | "governs";
  label?: string;
};

export type ProcessDefinition = {
  id: ProcessId;
  title: string;
  sector: "Planejamento" | "PCP";
  source: "ELO-PROC-MULTITEINER-001";
  authority: "reference";
  status: "draft";
  summary: string;
  nodes: ProcessNode[];
  relations: ProcessRelation[];
  connectedSectors: string[];
};

export const processes: ProcessDefinition[] = [
  {
    id: "planning-demand",
    title: "Fluxo de Demanda",
    sector: "Planejamento",
    source: "ELO-PROC-MULTITEINER-001",
    authority: "reference",
    status: "draft",
    summary: "Da demanda formalizada até a liberação do planejamento para execução.",
    nodes: [
      { id: "af", label: "AF recebida", kind: "entry", status: "REFERENCE" },
      { id: "scope", label: "Analisar escopo", kind: "stage", status: "REFERENCE" },
      { id: "config", label: "Validar configuração", kind: "stage", status: "REFERENCE" },
      { id: "pattern", label: "Padrão ou personalizado?", kind: "gate", status: "REFERENCE" },
      { id: "variation", label: "Excedentes / variações", kind: "stage", status: "REFERENCE" },
      { id: "materials", label: "Verificar materiais", kind: "stage", status: "REFERENCE" },
      { id: "capacity", label: "Verificar capacidade", kind: "stage", status: "REFERENCE" },
      { id: "deadline", label: "Verificar prazo", kind: "stage", status: "REFERENCE" },
      { id: "dependencies", label: "Verificar dependências", kind: "stage", status: "REFERENCE" },
      { id: "priority", label: "Definir sequência / prioridade", kind: "stage", status: "REFERENCE" },
      { id: "release", label: "Liberar planejamento", kind: "output", status: "REFERENCE" },
    ],
    relations: [
      { from: "af", to: "scope", relation: "provides" },
      { from: "scope", to: "config", relation: "depends_on" },
      { from: "config", to: "pattern", relation: "depends_on" },
      { from: "pattern", to: "variation", relation: "contains" },
      { from: "variation", to: "materials", relation: "depends_on" },
      { from: "materials", to: "capacity", relation: "depends_on" },
      { from: "capacity", to: "deadline", relation: "depends_on" },
      { from: "deadline", to: "dependencies", relation: "depends_on" },
      { from: "dependencies", to: "priority", relation: "depends_on" },
      { from: "priority", to: "release", relation: "provides" },
    ],
    connectedSectors: ["Comercial / Locação", "Engenharia", "Orçamento / Customização", "Almoxarifado", "Compras", "Produção", "Qualidade", "Expedição"],
  },
  {
    id: "planning-modular",
    title: "Fluxo Modular",
    sector: "PCP",
    source: "ELO-PROC-MULTITEINER-001",
    authority: "reference",
    status: "draft",
    summary: "Linha modular puxada por modelo/configuração, materiais, capacidade e sequência.",
    nodes: [
      { id: "planning", label: "Planejamento", kind: "entry", status: "REFERENCE" },
      { id: "materials", label: "Materiais / estoque", kind: "stage", status: "REFERENCE" },
      { id: "availability", label: "Material disponível?", kind: "gate", status: "REFERENCE" },
      { id: "picking", label: "Picking / abastecimento", kind: "stage", status: "REFERENCE" },
      { id: "purchase", label: "Compras", kind: "stage", status: "REFERENCE" },
      { id: "production", label: "Produção modular", kind: "stage", status: "REFERENCE" },
      { id: "quality", label: "Qualidade", kind: "gate", status: "REFERENCE" },
      { id: "shipping", label: "Expedição", kind: "output", status: "REFERENCE" },
      { id: "return", label: "Retorno / novo ciclo", kind: "decision", status: "REFERENCE" },
    ],
    relations: [
      { from: "planning", to: "materials", relation: "depends_on" },
      { from: "materials", to: "availability", relation: "governs" },
      { from: "availability", to: "picking", relation: "provides", label: "SIM" },
      { from: "availability", to: "purchase", relation: "provides", label: "NÃO" },
      { from: "picking", to: "production", relation: "provides" },
      { from: "purchase", to: "production", relation: "provides" },
      { from: "production", to: "quality", relation: "depends_on" },
      { from: "quality", to: "shipping", relation: "provides", label: "APROVADO" },
      { from: "shipping", to: "return", relation: "contains" },
      { from: "return", to: "planning", relation: "depends_on", label: "NOVO CICLO" },
    ],
    connectedSectors: ["Planejamento", "Almoxarifado", "Compras", "Produção", "Qualidade", "Expedição", "Operações / Campo", "Reparos"],
  },
];

export function getProcess(processId: ProcessId) {
  return processes.find((process) => process.id === processId) ?? processes[0];
}

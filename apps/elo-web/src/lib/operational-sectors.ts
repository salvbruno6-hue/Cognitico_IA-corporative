export type OperationalSectorId =
  | "producao"
  | "almoxarifado"
  | "compras"
  | "qualidade"
  | "expedicao";

export type OperationalTeam = "interna" | "externa";

export type OperationalSector = {
  id: OperationalSectorId;
  label: string;
  purpose: string;
  teams?: OperationalTeam[];
  inputs: string[];
  outputs: string[];
  connectedSectors: string[];
};

export const operationalSectors: OperationalSector[] = [
  {
    id: "producao",
    label: "Produção",
    purpose: "Executar a transformação dos módulos conforme planejamento, configuração, materiais, capacidade e sequência.",
    teams: ["interna", "externa"],
    inputs: ["planejamento", "materiais", "configuração", "ordem de produção"],
    outputs: ["módulo em produção", "status da etapa", "tempo", "retrabalho", "liberação para qualidade"],
    connectedSectors: ["PCP", "Almoxarifado", "Compras", "Qualidade", "Expedição", "Reparos"],
  },
  {
    id: "almoxarifado",
    label: "Almoxarifado",
    purpose: "Controlar recebimento, estoque, reservas, picking e abastecimento dos processos.",
    inputs: ["lista de materiais", "necessidade PCP", "recebimentos", "devoluções"],
    outputs: ["disponibilidade", "reserva", "ruptura", "picking", "requisição de compra"],
    connectedSectors: ["PCP", "Produção", "Compras", "Reparos"],
  },
  {
    id: "compras",
    label: "Compras",
    purpose: "Converter necessidades de materiais em pedidos acompanhados por prazo, fornecedor e recebimento.",
    inputs: ["necessidade de material", "ruptura", "requisição"],
    outputs: ["pedido", "previsão de chegada", "material recebido", "risco de atraso"],
    connectedSectors: ["PCP", "Almoxarifado", "Produção", "Reparos"],
  },
  {
    id: "qualidade",
    label: "Qualidade",
    purpose: "Inspecionar módulos, registrar conformidade e direcionar aprovação, reparo ou retrabalho.",
    inputs: ["módulo produzido", "módulo reparado", "critérios de inspeção", "testes"],
    outputs: ["aprovado", "falha", "não conformidade", "liberação", "retorno para reparo/retrabalho"],
    connectedSectors: ["Produção", "Reparos", "PCP", "Expedição"],
  },
  {
    id: "expedicao",
    label: "Expedição",
    purpose: "Preparar, conferir e liberar módulos para saída controlada ao cliente, campo ou operação.",
    inputs: ["módulo liberado", "checklist", "NF", "destino"],
    outputs: ["conferência", "carregamento", "saída", "destino", "rastreabilidade da entrega"],
    connectedSectors: ["PCP", "Qualidade", "Operações / Campo", "Comercial / Locação"],
  },
];

export function getOperationalSector(id: OperationalSectorId) {
  return operationalSectors.find((sector) => sector.id === id) ?? operationalSectors[0];
}

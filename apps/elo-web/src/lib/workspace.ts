/** ELO Web experience mapping. This describes UI sections; it grants no access. */
export type WorkspaceArea = {
  key: string; label: string; description: string;
  sections: { label: string; sources: string[]; gap: string }[];
};
const readGap = "A fonte existe, mas sua consulta operacional ainda precisa ser integrada com as permissões correspondentes.";
export const workspaceAreas: WorkspaceArea[] = [
  { key: "orquestrador", label: "Orquestrador", description: "Pendências, orientações e decisões apoiadas nas fontes do ELO.", sections: [
    { label: "Agentes por setor", sources: ["elo_aprendizado_especializacoes"], gap: "Especializações cadastradas não comprovam agentes conectados ou em execução." },
    { label: "Simulações e gargalos", sources: ["elo_sim_cenarios", "elo_sim_diagnosticos"], gap: "Os cenários precisam de um contrato de execução integrado ao workspace; nenhuma simulação é executada por estes painéis." },
  ] },
  { key: "dashboard", label: "Dashboard Comercial", description: "Demanda, capacidade comercial, estoque, prazos e cobertura.", sections: [
    { label: "KPIs e metas", sources: ["mt_definicoes_kpi", "mt_snapshots_kpi"], gap: "Indicadores dependem de definições, medições e períodos comparáveis. Nenhuma meta foi presumida." },
    { label: "Demanda e sazonalidade", sources: ["mt_demanda_historico", "mt_previsoes_demanda"], gap: readGap },
    { label: "Cobertura de demanda", sources: ["mt_balanco_demanda"], gap: readGap },
  ] },
  { key: "comercial", label: "Comercial", description: "Solicitações, demanda sazonal e movimentação de clientes.", sections: [
    { label: "Solicitações e orçamentos", sources: ["elo_orcamentos"], gap: "Orçamento não equivale ao cadastro completo da solicitação. O número SO é informado pelo analista de orçamento; não é gerado automaticamente aqui." },
    { label: "Pedidos e clientes", sources: ["mt_pedidos_venda", "mt_pedidos_venda_itens", "mt_clientes"], gap: readGap },
    { label: "Demanda sazonal", sources: ["mt_demanda_historico", "mt_previsoes_demanda"], gap: "Meses sem registro não são preenchidos com zero. Histórico real e previsão devem permanecer distintos." },
    { label: "Fornecimento e devoluções", sources: ["mt_contratos_locacao", "mt_devolucoes"], gap: readGap },
  ] },
  { key: "almoxarifado", label: "Almoxarifado", description: "Estoque físico, reservas, movimentações e necessidades de material.", sections: [
    { label: "Estoque de materiais", sources: ["mt_lotes_estoque", "mt_movimentacoes_estoque"], gap: readGap },
    { label: "Estoque de módulos", sources: ["mt_unidades_modulares", "mt_eventos_el"], gap: readGap },
    { label: "Pedidos de material", sources: ["mt_necessidades_materiais"], gap: "Necessidade calculada não equivale a pedido aprovado. Falta reconciliar o fluxo de solicitação e entrega." },
  ] },
  { key: "compras", label: "Compras", description: "Pedidos, fornecedores, cotações e prazos de entrega.", sections: [
    { label: "Ordens e itens de compra", sources: ["mt_ordens_compra", "mt_ordens_compra_itens"], gap: readGap },
    { label: "Fornecedores e cotações", sources: ["fornecedores", "fornecedor_itens_cotacao"], gap: readGap },
    { label: "Lead time e vínculos", sources: ["mt_ordens_compra", "mt_necessidades_materiais"], gap: "Lead time exige datas e vínculo comprovado. Sem esses dados, o prazo médio permanece indisponível." },
  ] },
  { key: "producao", label: "Produção", description: "Ordens, oficinas, etapas, reparos e serviços externos.", sections: [
    { label: "Ordens e etapas", sources: ["mt_ordens_producao", "mt_operacoes_ordem_producao", "fluxo_produtivo_modular_etapas"], gap: "A sequência real deve vir do fluxo produtivo cadastrado. O anexo não define a etapa de cada ordem." },
    { label: "Reparos", sources: ["mt_ordens_reparo", "mt_eventos_reparo"], gap: readGap },
    { label: "Serviços externos", sources: ["mt_ordens_montagem_externa", "mt_eventos_montagem_externa"], gap: "Montagem externa é uma fonte existente; não representa automaticamente todo serviço terceirizado do anexo." },
  ] },
  { key: "pcp", label: "Planejamento/PCP", description: "Análise, orçamento, planos, capacidade e programação em uma única área.", sections: [
    { label: "Projetos e orçamentos", sources: ["elo_orcamentos", "mt_documentos_engenharia"], gap: readGap },
    { label: "Planos e ordens de fabricação", sources: ["mt_planos_pcp", "mt_linhas_plano_pcp", "mt_ordens_producao"], gap: readGap },
    { label: "Kanban de produção", sources: ["fluxo_produtivo_modular_etapas", "mt_operacoes_ordem_producao"], gap: "O quadro precisa de vínculo entre operação e etapa. Mover cartões exige uma operação autorizada; nenhuma etapa será inventada." },
    { label: "Capacidade e recursos", sources: ["mt_regras_capacidade", "mt_capacidade_diaria"], gap: readGap },
  ] },
  { key: "expedicao", label: "Expedição", description: "Saídas, quarentena, condições de retorno e disponibilidade dos ativos.", sections: [
    { label: "Expedições", sources: ["mt_expedicoes", "mt_expedicao_itens"], gap: readGap },
    { label: "Retorno e quarentena", sources: ["mt_devolucoes", "mt_devolucao_itens", "mt_inspecoes"], gap: "Disponibilidade e liberação dependem de inspeção e eventos reais; retorno não libera o ativo automaticamente." },
  ] },
  { key: "catalogo", label: "Catálogo", description: "Taxonomia, Lista-Mãe, modelos, dimensões, fichas e composições.", sections: [
    { label: "BOM versionada", sources: ["mt_versoes_bom", "mt_bom_itens"], gap: "Kits e estrutura modular estão disponíveis para consulta. Não substituem a BOM versionada." },
    { label: "Diretório de documentos", sources: ["mt_documentos_engenharia"], gap: "A navegação por arquivos depende de vínculos e acesso ao repositório de documentos; não há diretório conectado aqui." },
  ] },
  { key: "chat", label: "Chat", description: "Diálogo com o ELO para esclarecer e registrar os dados pendentes de Planejamento/PCP.", sections: [
    { label: "Comunicação da equipe", sources: [], gap: "Não foi encontrado um contrato canônico de mensagens entre colaboradores. O diálogo com o ELO não envia mensagens à equipe." },
  ] },
  { key: "notificacoes", label: "Notificações", description: "Pendências e pontos de atenção devolvidos pelo ELO.", sections: [
    { label: "Leitura e acompanhamento", sources: ["v_elo_pcp_dados_pendentes"], gap: "A consulta de pendências está conectada. Marcar alertas como vistos exige um contrato de acompanhamento ainda não identificado." },
  ] },
  { key: "configuracoes", label: "Configurações", description: "Preferências do workspace e informações do seu acesso.", sections: [
    { label: "Usuários, setores e permissões", sources: ["elo_identity_registry", "elo_identity_roles", "elo_identity_scopes"], gap: "O workspace consulta o próprio acesso. Administração de outros usuários continua sujeita às funções e permissões canônicas." },
    { label: "Integrações e backup", sources: [], gap: "Supabase e GitHub permanecem as fontes existentes. Importação, exportação global e sincronização com planilhas não têm operação integrada neste workspace." },
  ] },
];

export function isEvidenceBacked(result: { sources?: unknown[]; provenance?: { evidence_refs?: unknown[] } }): boolean {
  return (result.sources?.length ?? 0) > 0 || (result.provenance?.evidence_refs?.length ?? 0) > 0;
}

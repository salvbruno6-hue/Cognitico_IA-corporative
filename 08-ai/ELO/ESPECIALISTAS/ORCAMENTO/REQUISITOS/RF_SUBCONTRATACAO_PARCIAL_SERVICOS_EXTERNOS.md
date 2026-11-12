# RF — Gate documental para subcontratação parcial no orçamento

**Identificador:** RF-ORC-SUB-001 a RF-ORC-SUB-010  
**Owner:** ELO/Governance | **Executor:** FORGE-BUDGETING-001  
**Classificação:** requisito operacional candidato, condicionado ao Evolution Gate; não cria nova autoridade  
**Origem:** decisão do owner, UEMG Passos, SEI 2350.01.0008746/2026-52; licitação declinada por insuficiência de prazo (relato do owner, 12/11/2026).  
**Registro cognitivo:** Supabase `tb_elo_eventos_governanca.id=7` (experiência consultiva, não regra automaticamente validada).

## Escopo e princípios

Ao analisar uma SO/LIC com instalação externa, obra civil, infraestrutura seca, escavação, recomposição, fundação ou serviços especializados, o Orçamentista deve **avaliar** a possibilidade de subcontratação parcial. Avaliar não é autorizar. A autorização e os limites dependem do edital, TR, minuta/contrato, anexos e esclarecimentos aplicáveis à contratação concreta. A responsabilidade da contratada principal deve ser examinada no instrumento vigente. Não inferir permissão de silêncio documental, prática de mercado ou experiência anterior.

## Requisitos funcionais

| ID | Comportamento obrigatório | Evidência/saída |
|---|---|---|
| RF-ORC-SUB-001 | Detectar serviços potencialmente executáveis por terceiro na leitura inicial da SO/LIC, sem incluí-los automaticamente como terceirizados. | Matriz de escopo por parcela e responsável proposto. |
| RF-ORC-SUB-002 | Consultar e citar cláusulas vigentes do edital, TR, contrato/minuta, anexos, retificações e esclarecimentos sobre subcontratação parcial, vedação, limites e autorização prévia. | Documento, versão, cláusula, trecho, fonte e data. |
| RF-ORC-SUB-003 | Classificar cada parcela como PERMITIDA_COM_EVIDENCIA, VEDADA_COM_EVIDENCIA, CONDICIONADA ou NAO_COMPROVADA. Silêncio/ausência = NAO_COMPROVADA, não PERMITIDA. | Classificação auditável por parcela. |
| RF-ORC-SUB-004 | Bloquear a decisão de terceirizar e a consolidação do cenário terceirizado como executável quando houver vedação ou ausência de evidência; abrir GAP e emitir questionamento ao órgão/gestão quando cabível. | Gate jurídico-documental: APTO, CONDICIONAL ou BLOQUEADO. |
| RF-ORC-SUB-005 | Verificar exigências de anuência, percentual/parcelas autorizadas, habilitação, responsabilidade técnica, ART, fiscalização e responsabilidade da contratada principal, conforme documentos vigentes. | Checklist de conformidade e dependências. |
| RF-ORC-SUB-006 | Se documentalmente admissível, estruturar cotação separada do escopo do terceiro, distinguindo fornecimento, execução, interfaces, materiais, equipamentos, mobilização, resíduos, recomposição e exclusões. | Memorial, mapa de responsabilidades e planilha sem duplicidade. |
| RF-ORC-SUB-007 | Avaliar prazo crítico: cotação, contratação, aprovação, mobilização, execução, interfaces, inspeção, recomposição e folgas frente à data contratual. | Cronograma de viabilidade e risco; sem prazo confirmado = GAP. |
| RF-ORC-SUB-008 | Confrontar cenário próprio e cenário terceirizado apenas quando admissíveis; preservar custos mínimos reais de equipamentos, transporte e mobilização e não duplicar serviços entre equipes. | Cenários e memória de cálculo rastreáveis. |
| RF-ORC-SUB-009 | Aplicar o gate na PTS Técnica, antes da aprovação da estratégia de orçamento, e revalidá-lo na PTS Pós-Orçamento e antes da proposta/compromisso comercial. | Indicadores canônicos Conhecimento/Flexibilidade/Risco/Decisão, com evidência e pendências. |
| RF-ORC-SUB-010 | Registrar resultado, motivos de declínio, GAPs e lições como CASE/PRECEDENT/LEARNING_CANDIDATE, sem promover automaticamente ao Core. | Despacho ao learning governance, aprovação humana e Evolution Gate quando aplicáveis. |

## Matriz de decisão

| Situação documental | Decisão |
|---|---|
| Permissão explícita para a parcela e requisitos satisfeitos | APTO para cotação/planejamento terceirizado, sujeito às demais verificações. |
| Permissão condicionada a anuência, limites ou documentos pendentes | CONDICIONAL: cotação exploratória identificada; **não** tratar execução como autorizada até cumprir condições. |
| Vedação explícita da parcela | BLOQUEADO: não estruturar contratação de terceiro como opção executável. |
| Cláusula ausente, ambígua, contraditória ou documento indisponível | NAO_COMPROVADA/BLOQUEADO: GAP, investigação e pedido de esclarecimento; nunca presumir autorização. |
| Permissão documental, mas prazo inviável | INVIAVEL_PRAZO: reavaliar solução própria, negociar prazo se possível ou recomendar declínio fundamentado. |

## Escopo ilustrativo da experiência UEMG (não padrão universal)

Infraestrutura seca de elétrica/dados: valas, eletrodutos subterrâneos, caixas, fio-guia, corte e demolição, reaterro, compactação, gramado/concreto/pedra mineira, equipamentos, carga/transporte/destinação de resíduos. SPDA: **somente** serviços civis perimetrais quando especificados; não presumir tubulação para condutor de aterramento. Cabos, lançamento, conexões e componentes específicos de SPDA permanecem com equipe instaladora conforme escopo do caso. Fundação/radier deve ter definição contratual própria. Não copiar metragens ou preços deste caso para novas SOs.

**GAP do caso histórico:** não foi comprovada neste aprendizado a cláusula que autorizaria subcontratar no pregão UEMG; não afirmar que era permitida. O motivo do declínio informado foi insuficiência de prazo.

## Testes de aceitação

1. Edital proíbe subcontratação: sistema marca VEDADA_COM_EVIDENCIA, BLOQUEADO, não aprova cenário terceirizado.
2. Edital permite somente parcela definida: demais parcelas não herdam autorização.
3. Documento omisso: NAO_COMPROVADA, GAP, sem aprovação automática.
4. Permissão depende de anuência: CONDICIONAL até comprovação.
5. Permissão comprovada e prazo insuficiente: INVIAVEL_PRAZO, recomendação fundamentada, sem compromisso inexequível.
6. Infraestrutura seca com instaladora própria: separar tubos/guia/caixas dos cabos e conexões; verificar interface antes do reaterro.
7. PTS Técnica e Pós registram fonte documental, classificação, responsável, custos, prazo e status; não criam indicadores paralelos.
8. Caso histórico isolado permanece experiência Forge; promoção requer generalização, evidência, aprovação humana e Evolution Gate.

## Integração arquitetural

A Skill de Orçamento orquestra este checklist; o especialista executa a análise. A autoridade permanece na documentação da SO e contratos canônicos existentes. O contrato de aprendizado contínuo e `src/elo/core/learning_governance.py` governam a classificação e eventual promoção. Esta RF não implementa por si só enforcement em código nem altera permissões legais/contratuais.

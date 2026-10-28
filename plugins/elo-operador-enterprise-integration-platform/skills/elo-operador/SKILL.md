---
name: elo-operador
description: Consulta governada e auditável da Enterprise Integration Platform do ELO. Use para verificar estado, dados canônicos permitidos, pendências PCP, indicadores, Decision Outcome Loop, calibração e precedentes.
---

# ELO Operador

Use as ferramentas expostas pelo servidor MCP `elo_mcp` para consultar o ELO por meio da fronteira autenticada e auditável. Para consultar o status, chame `elo_status` com argumentos vazios (`{}`). `elo_mcp` identifica o servidor, não uma ferramenta.

Se `elo_status` ou as demais ferramentas não estiverem disponíveis na conversa, informe que a conexão não está carregada ou autenticada e solicite a conexão do plugin. Não simule resultados nem apresente o estado do repositório como status operacional do ELO.

## Limite de autoridade

- O ELO continua sendo o orquestrador cognitivo e a autoridade de admissão, decisão e evolução.
- Esta integração é de leitura. Não proponha escrita de dados, alterações de schema, promoção de conhecimento, mudança de regra ou liberação de gate.
- Trate o resultado como evidência consultada, não como fato independente: preserve fonte, contexto, lacunas, incerteza e próximos passos.
- Quando dados estiverem ausentes, declare o GAP; nunca estime ou preencha por inferência.

## Fluxo operacional

1. Estabeleça o objetivo, o contexto e o escopo autorizado.
2. Chame `elo_status` antes da primeira leitura quando for necessário confirmar identidade, papéis e limite de acesso.
3. Escolha a tool mais específica disponível; use `elo_read` somente para tabelas explicitamente permitidas.
4. Para PCP, siga as perguntas devolvidas por `elo_pcp_dados_pendentes`, `elo_pcp_demanda_crossing_status` e `elo_pcp_decisao_externa_status` antes de calcular ou recomendar.
5. Não chame um indicador de KPI formal sem confirmação de `elo_pcp_indicadores_status`.
6. Diferencie evidência, hipótese, recomendação e decisão humana no retorno.

## Resposta

Apresente, de forma objetiva: objetivo, evidências consultadas, lacunas/limites, análise e próxima ação autorizada. Não exponha dados não necessários nem credenciais.

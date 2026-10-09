# E2E PCP/KPI/MCP audit and implementation preparation

## Escopo

Audita e reconcilia a cadeia PCP → indicadores → KPI → API → MCP sem criar autoridade paralela ou promover dados ausentes.

## Incluído

- documentação MCP alinhada ao runtime atual;
- mapa canônico MCP atualizado;
- auditoria E2E e matriz de estado;
- contrato de implementação;
- prompt Codex;
- critérios de teste/rastreabilidade;
- aviso explícito de não merge.

## Achados

- tools PCP já existiam no ELO-MCP, mas a documentação estava desatualizada;
- read-models de capacidade e indicadores externos existem, mas ainda não estavam governados no catálogo cognitivo consultado;
- `mt_definicoes_kpi` e `mt_snapshots_kpi` existem, porém estavam vazias;
- `/cognitive` e `CognitiveResponse/Provenance` já suportam a boundary necessária;
- falta integração de capacidade/indicadores no Forge cross-domain, Humanizer e MCP específico.

## Ainda pendente antes de merge

- nova migration via Supabase CLI;
- governança das views de capacidade/indicadores;
- código Forge/Humanizer/MCP;
- testes e validação E2E;
- autorização explícita de merge.

**Este PR deve permanecer draft até a implementação e os testes serem concluídos.**

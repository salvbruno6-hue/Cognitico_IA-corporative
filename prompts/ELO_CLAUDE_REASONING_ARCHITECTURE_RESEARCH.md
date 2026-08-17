# Prompt — ELO Claude Reasoning Architecture Research

Analise a arquitetura publicamente observável da família Claude e de sistemas agentic associados, sem tentar obter ou reproduzir chain-of-thought privado, pesos, prompts proprietários ou mecanismos internos não divulgados.

Objetivo: extrair princípios que possam aumentar a capacidade cognitiva, agilidade e autonomia do ELO.

## Investigue

1. Extended/adaptive thinking e alocação dinâmica de esforço.
2. Checkpoints explícitos durante cadeias de uso de ferramentas.
3. Relação entre planejamento e execução.
4. Loop read → plan → act → observe.
5. Uso de ferramentas e subagentes.
6. Conhecimento persistente fora do modelo.
7. Testes, validação e autocorreção.
8. Context compaction e reconstrução de contexto.
9. Sandboxing e contenção de agentes.
10. Escalonamento de tarefas e paralelização.

## Para cada padrão

Informe:

- evidência primária;
- o que é fato;
- o que é inferência;
- mecanismo arquitetural observável;
- equivalente existente no ELO;
- lacuna do ELO;
- possibilidade de reprodução independente do modelo Claude;
- benefício esperado;
- custo/latência;
- risco;
- experimento mínimo;
- decisão REUSE / EXTEND / EXPERIMENT / PROMOTE / REJECT / ROADMAP.

## Pergunta central

Não pergunte apenas "como Claude pensa?".

Pergunte:

> "Que mecanismos de operação fazem um agente como Claude transformar uma intenção em uma sequência longa de decisões, ferramentas, observações, correções e resultado verificável, e quais desses mecanismos o ELO pode implementar de forma model-agnostic?"

## Regra de segurança epistemológica

Nunca afirme conhecer o chain-of-thought privado ou os mecanismos internos não divulgados do modelo. Diferencie:

OBSERVADO → DOCUMENTADO → INFERIDO → HIPOTÉTICO.

## Resultado esperado

Produza um desenho de arquitetura para o ELO contendo:

- Cognitive Controller;
- Effort Router;
- Cognitive Checkpoint;
- Tool Gateway;
- Specialist Router;
- Evidence Gate;
- Verification Loop;
- Context Compaction;
- Structured Memory;
- Sandbox/Containment;
- Replanning Loop.

Mostre como cada componente conversa com o Cognitive Core, AI Gateway, Memory, Knowledge, Agents, Provenance e Governance já existentes no Cognitico.

Finalize com as cinco capacidades que deveriam ser experimentadas primeiro e com um plano de implementação incremental que não crie um segundo Cognitive Core.

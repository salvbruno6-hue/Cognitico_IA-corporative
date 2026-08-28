# ELO APRENDER — Roteamento Canônico de Aprendizados de Orçamento

## Autoridade operacional

O comportamento completo do gatilho é definido por `ELO_APRENDER_CANONICO_MASTER_PROMPT.md`.

Este arquivo controla o roteamento físico; o Prompt Mestre controla busca, varredura, separação, persistência, governança e retorno.

## Regra obrigatória

Quando `ELO APRENDER` processar uma Solicitação de Orçamento (SO) do domínio do Especialista de Orçamento, o artefato cognitivo deve ser criado ou consolidado exclusivamente em:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/`

## Separação Git × Supabase

- **Git:** conhecimento cognitivo/instrucional, conceitos, decisões, critérios, precedentes, regras, diretrizes e governança.
- **Supabase:** somente memória quantitativa estruturada de cálculos e suas evidências.

A mesma execução de `ELO APRENDER` deve produzir as duas camadas quando houver conteúdo aplicável.

## Busca cognitiva obrigatória

Antes de criar ou alterar aprendizado, o gatilho deve identificar a SO/documentos, localizar o artefato canônico, pesquisar fontes legadas como proveniência, consultar conceitos existentes e seus estados, consultar memória de cálculo existente, agrupar semanticamente e deduplicar, e agregar nova evidência quando o conceito já existir.

## Varredura de cálculos obrigatória

Para toda SO de orçamento, executar `VARRER_CÁLCULOS` antes da consolidação final. Percorrer SO, TR, PTS Técnica, Orçamento, PTS Pós-Orçamento, planilhas, composições e anexos disponíveis.

Investigar cálculos explícitos e implícitos de quantitativos, excedentes, cobertura/telhado, estrutura, hidráulica/esgoto, elétrica, climatização, manutenção, mão de obra, produtividade, logística, acoplamento, ART/RRT, áreas, equipamentos, composição de preços, equivalências e percentuais.

Não guardar apenas o número: reconstruir `entrada → fonte → premissa → fórmula → subcálculo → resultado → validação → origem`.

## Proibição de destinos paralelos

O gatilho não deve criar novos aprendizados de orçamento em `memory/solicitations/<SO>/LEARNING.md`, `memory/solicitations_learning/`, `04-knowledge-handbook/` ou qualquer outro diretório paralelo.

Arquivos históricos nesses locais são fontes legadas para migração/consolidação, preservando proveniência.

## Governança e integridade

Se o conceito já estiver `VALIDATED_LEARNING`, reutilizar sem duplicar e agregar somente ocorrência/evidência. Nunca promover `PRECEDENT` a `RULE` automaticamente.

O ID de cálculo é gerado/controlado pelo Supabase. O modelo não fabrica IDs.

Se a persistência aplicável falhar, a experiência permanece pendente e não pode ser marcada como consolidada.

## Laboratório

O Laboratório Virtual é separado e somente é executado quando chamado explicitamente pelo usuário.

## Critério de conclusão

A experiência só pode ser considerada consolidada quando o commit Git aplicável e, havendo cálculos, a persistência/confirmação no Supabase estiverem confirmadas.
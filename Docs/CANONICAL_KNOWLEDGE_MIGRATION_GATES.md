# ELO — Gates da Consolidação do Conhecimento

## Gate 1 — Inventário
Todos os arquivos e diretórios candidatos estão identificados.

## Gate 2 — Identidade
Todo artefato candidato possui `artifact_id`/`concept_id` estáveis.

## Gate 3 — Classificação
Nenhuma decisão de fusão permanece como `AR`; conflitos são explicitamente registrados.

## Gate 4 — Dependências
Consumidores, referências de entrada/saída e aliases estão mapeados.

## Gate 5 — Consolidação lógica
Equivalentes e complementares possuem um único proprietário sem perda de conteúdo.

## Gate 6 — Compatibilidade
Resolução por identidade e por alias histórico retorna o mesmo conceito esperado.

## Gate 7 — Verificação
Testes de resolução, proveniência, integridade, links e regressão aplicáveis passam.

## Gate 8 — Depreciação
Caminhos antigos são marcados `DEPRECATED`/`SUPERSEDED` somente após o Gate 7.

## Gate 9 — Remoção
Remoção física somente quando não houver conteúdo exclusivo, consumidores ativos ou dependência histórica necessária.

## Gate 10 — Pós-migração
Índices, documentação, agentes e registros apontam para a autoridade canônica; a CI permanece capaz de detectar retorno de duplicidade.

## Regra de bloqueio
Qualquer falha de gate interrompe a migração. Não existe merge automático por simples conclusão documental; o merge depende dos gates efetivamente disponíveis no repositório.

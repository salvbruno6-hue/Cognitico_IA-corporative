# ELO Context Resolution

## Objetivo

Resolver intenção, entidade e escopo antes de qualquer consulta especializada. O usuário informa a pergunta; o ELO determina quais fontes autorizadas são relevantes.

## Fluxo canônico

Pergunta → Intent/Entity Resolution → Context Resolution → fontes autorizadas → Context Pack → análise do ELO → pergunta especializada ao GPT → crítica do ELO → resposta sistêmica.

## Regras

1. Não exigir caminhos de pastas/projetos ao usuário.
2. Não consultar o GPT antes de procurar contexto interno autorizado.
3. Não confundir ausência em uma fonte com ausência de conhecimento.
4. Respeitar escopo de entidade, unidade, período e autoridade da fonte.
5. Separar fatos, inferências, hipóteses e lacunas.
6. Dados externos permanecem sujeitos a proveniência, memória temporal e admissão governada.
7. O GPT recebe um Context Pack e uma questão especializada; não recebe autoridade para decidir ou alterar a Soul/Core.
8. Conflitos de fonte devem ser explicitados e encaminhados ao Evolution Gate quando afetarem estruturas canônicas.

## Escopo empresarial

Para consultas sobre uma unidade, como Multiteiner em Duque de Caxias, o resolvedor deve priorizar evidências explicitamente associadas à entidade e ao local antes de consolidar informações corporativas gerais.

## Critério de maturidade

Quando o ELO já possuir contexto suficiente, o GPT atua como especialista de validação/ampliação. Quando o contexto for insuficiente, o GPT pode apoiar descoberta/contextualização conforme o Maturity Engine.

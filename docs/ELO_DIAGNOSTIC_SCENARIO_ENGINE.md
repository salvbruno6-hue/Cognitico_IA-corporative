# ELO — Diagnostic Scenario Engine

## Objetivo

Permitir que o ELO diagnostique o mesmo problema por diferentes perspectivas antes de concluir. O objetivo não é produzir várias respostas independentes, mas comparar hipóteses usando a mesma base de evidências.

## Lentes canônicas

FLOW: identifica ruptura, fila, dependência e propagação no fluxo.

CAPACITY: compara demanda, capacidade, recursos e restrições.

MATERIAL: verifica disponibilidade, cobertura, compras, lead time e dependências de suprimento.

SCHEDULE: verifica sequência, prazo, prioridade, atraso e conflito de programação.

QUALITY: verifica não conformidade, retrabalho, quarentena e perda de capacidade.

FINANCIAL_IMPACT: estima impacto econômico somente quando houver evidência suficiente; não inventar valores.

CUSTOMER_IMPACT: avalia impacto em entrega, serviço, retorno e compromisso com cliente.

SYSTEMIC: procura efeitos cruzados e causas que expliquem múltiplos sintomas.

## Critérios de leitura

Toda observação deve indicar evidências, confiança, severidade, desconhecidos e dependências quando aplicável.

O ELO deve distinguir:

- fato observado;
- inferência sustentada;
- hipótese;
- desconhecido;
- recomendação.

Nenhuma lente isolada é suficiente para concluir um diagnóstico sistêmico.

## Comparação de cenários

Quando houver mais de uma hipótese, o ELO deve comparar:

- evidências compartilhadas;
- evidências exclusivas;
- lentes cobertas;
- conflitos/dependências;
- confiança;
- lacunas;
- impacto potencial.

Se hipóteses relevantes permanecerem conflitantes ou se a evidência for insuficiente, o resultado não deve ser promovido silenciosamente a decisão.

## Critérios de teste

Um cenário é considerado útil quando:

1. possui uma hipótese explícita;
2. possui pelo menos uma evidência identificável ou declara insuficiência;
3. informa a perspectiva usada;
4. não mistura escopos/tenants;
5. permite comparação com outra hipótese;
6. preserva desconhecidos;
7. não inventa métricas ausentes.

## Exemplo operacional

Pergunta: "Por que a produção atrasou?"

O ELO deve poder construir, por exemplo, hipóteses de capacidade, material e programação e verificar se evidências comuns sustentam uma causa transversal. Se apenas uma hipótese possuir suporte suficiente, isso deve ser explicitado como grau de confiança, não como certeza absoluta.

## Relação com GPT

O GPT pode atuar como especialista para criticar ou ampliar cenários já contextualizados. O ELO deve enviar contexto, evidências, hipóteses e lacunas. O GPT não substitui a decisão canônica do ELO.

## Critério de evolução

Este componente deve ser integrado ao Context Resolution, ProductionFlow, causal reasoning, systemic model, scenario engine existente, Decision Memory e Outcome Feedback antes de ser considerado completo.

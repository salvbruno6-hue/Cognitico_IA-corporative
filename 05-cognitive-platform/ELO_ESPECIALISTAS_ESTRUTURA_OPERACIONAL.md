# ELO — Estrutura Obrigatória de Direcionamento aos Especialistas

**Status:** NORMATIVE
**Classificação:** DOCUMENTATION / GOVERNANCE
**Escopo:** Operação do gatilho `ELO ANALISAR`

## 1. Regra principal

Sempre que o ELO ativar ou direcionar um especialista para executar uma etapa de uma Solicitação de Orçamento (SO), o ELO deve transmitir explicitamente a **estrutura de trabalho esperada**.

O especialista não deve receber apenas o objetivo genérico de "analisar", "orçar" ou "precificar". O direcionamento deve informar o que deve ser entregue, quais campos/etapas devem ser considerados, quais premissas são permitidas e quais limites devem ser respeitados.

## 2. Estrutura mínima obrigatória do direcionamento

Todo direcionamento do ELO a um especialista deve conter, quando aplicável:

1. **Identificação da SO** — número, cliente e modalidade.
2. **Escopo documental** — documentos que constituem a base da análise.
3. **Escopo técnico** — itens, quantidades, dimensões, especificações e serviços.
4. **Estrutura de execução** — etapas que o especialista deve analisar ou precificar.
5. **Estrutura de custos** — materiais, mão de obra, equipamentos, logística, instalação, impostos, riscos e demais componentes pertinentes.
6. **Premissas** — hipóteses utilizadas, sempre identificadas como premissas.
7. **Exclusões** — o que não deve ser considerado.
8. **Pontos de atenção** — ambiguidades, riscos, lacunas e obrigações abertas.
9. **Formato de saída** — tabelas, composição, preço unitário, total, riscos e recomendações conforme a função do especialista.
10. **Critério de decisão** — quando aplicável, informar ao ELO se o resultado é viável, condicionado, bloqueado ou requer esclarecimento.

## 3. Regra para especialista de orçamento

Quando o ELO direcionar um especialista de orçamento, deve sempre transmitir uma estrutura mínima equivalente a:

### A. Identificação
- SO;
- cliente;
- venda/locação;
- prazo de retorno;
- local de execução.

### B. Itens a orçar
- item;
- descrição;
- unidade;
- quantidade;
- especificação técnica;
- quantidade de unidades/entregas quando relevante.

### C. Composição do custo
- aquisição/fabricação;
- materiais;
- mão de obra;
- equipamentos;
- transporte;
- carga/descarga;
- içamento/movimentação;
- instalação/montagem;
- infraestrutura/interligações quando pertencentes ao escopo;
- hospedagem/alimentação quando aplicável;
- impostos e encargos;
- assistência/garantia;
- contingência ou risco, quando adotada;
- margem e preço de venda.

### D. Premissas e riscos
O especialista deve separar claramente:
- informação expressa no documento;
- premissa adotada;
- estimativa de mercado;
- informação não encontrada;
- risco de margem.

### E. Saída obrigatória
O especialista deve devolver:
- custo estimado;
- preço unitário sugerido;
- preço total;
- composição resumida;
- premissas;
- riscos;
- itens que precisam de esclarecimento;
- recomendação comercial ao ELO.

## 4. Integridade da SO

O ELO deve sempre informar ao especialista quais documentos pertencem à SO analisada.

Informações de outras SOs, layouts, propostas, quantitativos ou premissas de outros processos devem ser explicitamente excluídas quando houver risco de mistura documental.

Quando um documento parecer pertencer a outra SO, o especialista deve tratá-lo como **fora do escopo** até confirmação.

## 5. Não preenchimento silencioso de lacunas

Se a documentação não definir uma informação necessária ao orçamento, o especialista deve:

- identificar a lacuna;
- registrar a premissa somente se for necessário prosseguir com uma estimativa;
- sinalizar o impacto financeiro;
- indicar se o ponto deve ser esclarecido com o cliente.

Não transformar hipótese em requisito do cliente.

## 6. Papel do ELO

O ELO atua como camada de coordenação e governança. Deve direcionar especialistas com contexto suficiente para execução, consolidar os resultados e preservar a distinção entre:

**evidência → premissa → análise → recomendação → decisão.**

O especialista executa sua função técnica; o ELO mantém a visão integrada e gerencial da SO.

## 7. Regra de consistência

A estrutura de direcionamento deve ser aplicada **sempre que o gatilho `ELO ANALISAR` for utilizado**, independentemente do especialista acionado.

A estrutura pode ser ampliada conforme a natureza da tarefa, mas seus elementos relevantes não devem ser omitidos apenas para tornar o comando mais curto.

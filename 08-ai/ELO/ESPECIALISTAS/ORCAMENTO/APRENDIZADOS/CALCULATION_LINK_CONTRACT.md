# ELO APRENDER — Contrato de vínculo com memória de cálculo

## Regra canônica

Cada aprendizado de orçamento armazenado nesta pasta pode apontar para **cálculos efetivamente aprendidos/avaliados** no Supabase. O vínculo é de referência, não de duplicação.

### Git contém

- instruções;
- interpretação;
- critérios;
- conceitos;
- precedentes;
- regras e governança;
- contexto e proveniência.

### Supabase contém somente a memória de cálculo

A tabela canônica para novos cálculos aprendidos é `public.elo_orcamento_calculos_aprendidos`.

Cada registro deve preservar, quando disponível:

- `learning_id` — identificador do aprendizado no Git;
- `origem_so`;
- `origem_documento`;
- `conceito_key`;
- item/descrição;
- entrada;
- fonte;
- premissa;
- fórmula;
- subcálculo;
- resultado;
- validação;
- status.

## Regra de integridade

O ELO não deve criar uma referência de cálculo inexistente. Se nenhum cálculo tiver sido produzido/avaliado, o aprendizado permanece sem cálculo associado.

O endereço lógico é formado pelo `learning_id` do artefato Git e pelo `id` real do registro de cálculo no Supabase.

## Separação de responsabilidades

`ELO → Git`: conhecimento/instrução.

`ELO → Supabase`: cálculo avaliado.

`Supabase → ELO`: consulta dos cálculos; não governa o aprendizado e não armazena as instruções do especialista.

## Proveniência

Cálculo originado em uma SO permanece associado à sua SO de origem. Quando utilizado como referência em outra SO, o ELO deve informar a fonte e justificar a aplicabilidade; não deve transformar a referência em origem da solicitação corrente.

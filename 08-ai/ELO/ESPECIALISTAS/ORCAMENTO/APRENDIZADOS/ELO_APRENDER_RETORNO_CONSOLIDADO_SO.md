# ELO APRENDER — Retorno Consolidado de Solicitação de Orçamento

## Finalidade

Quando o usuário solicitar informações sobre uma SO de orçamento, o ELO deve reconstruir a experiência completa da solicitação e retornar, no mesmo resultado, o conhecimento cognitivo/instrucional e a memória quantitativa de cálculo.

A memória de cálculo não substitui SO, PTS Técnica, Orçamento ou PTS Pós-Orçamento. Ela é a camada quantitativa do raciocínio utilizado para formar, validar, alterar ou justificar o orçamento.

## Regra canônica

`CONSULTA SO → SO + TR + PTS TÉCNICA + ORÇAMENTO + PTS PÓS + GIT + SUPABASE → RECONSTRUÇÃO DA EXPERIÊNCIA → RETORNO CONSOLIDADO`

O retorno deve responder não apenas "quais cálculos existem", mas também:

- quem é a SO;
- qual é seu objeto e escopo;
- quantos módulos/contêineres e quais modelos estão envolvidos, quando houver evidência;
- como a PTS Técnica estruturou a solução;
- como o orçamento tratou modelo-base, excedentes, serviços, manutenção e composições;
- quais problemas/incongruências foram encontrados;
- quais decisões resolveram esses problemas;
- o que mudou na PTS Pós-Orçamento;
- quais conhecimentos foram aprendidos e registrados no Git;
- quais memórias quantitativas estão no Supabase;
- como cada cálculo foi produzido e validado;
- o que pode ser reutilizado em outra SO e por que.

## Camadas obrigatórias

### 1. Identificação da SO

Apresentar somente dados encontrados nas fontes:

- SO;
- cliente;
- objeto;
- local;
- modalidade/prazo, quando disponível;
- quantidade de módulos/contêineres;
- modelos/tipos;
- demais características relevantes.

Se não localizado, registrar `NÃO LOCALIZADO`.

### 2. Reconstrução técnica

Consultar e correlacionar, quando existentes:

`SO → TR → PTS Técnica → Orçamento → PTS Pós-Orçamento`

Explicar a evolução da solução e as decisões que afetaram o orçamento.

### 3. Conhecimento cognitivo — Git

Retornar:

- aprendizado;
- conceito;
- regra/instrução;
- precedente;
- decisão;
- critério;
- governança;
- aplicabilidade.

O Git é a fonte da camada instrucional/cognitiva.

### 4. Memória de cálculo — Supabase

Consultar a memória quantitativa e apresentar **todas as tabelas de cálculos aplicáveis encontradas**, sem resumir somente o resultado.

Formato obrigatório:

| ID | ID Memória | Categoria | Item | Fonte | Entrada/Base | Unidade | Parâmetro/Premissa | Fórmula | Subcálculo | Resultado | Unidade Resultado | Validação | Origem |
|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|

Cada linha deve preservar:

`FONTE → DADO ENCONTRADO → PARÂMETRO/PREMISSA → ID → ID MEMÓRIA → FÓRMULA → SUBCÁLCULO → QUANTITATIVO → COMPOSIÇÃO → CUSTO → VALIDAÇÃO → ORIGEM`

Quando houver composição financeira, apresentar também:

| ID Item | ID Memória | Descrição | Unidade | Quantidade | Valor Unitário | Valor Total |
|---|---|---|---|---:|---:|---:|

### 5. Relação conhecimento × cálculo

Para cada decisão relevante, explicar a relação:

`DECISÃO/CONHECIMENTO → MEMÓRIA DE CÁLCULO → RESULTADO → IMPACTO NO ORÇAMENTO`

Exemplo:

`Regra de cobertura 30% → quantidade base × 1,30 → quantitativo resultante → composição de manutenção`

A regra/instrução permanece no Git; o cálculo efetivamente realizado permanece no Supabase.

## Referências de outras SOs

Uma memória de outra SO é sempre **referência consultiva**, nunca origem da SO atual.

O retorno deve informar:

- SO de origem;
- documento/item de origem;
- valor/quantitativo;
- características técnicas;
- data, quando disponível;
- fonte;
- motivo pelo qual pode ser aplicável;
- diferenças de contexto;
- validação necessária.

O ELO deve explicar por que sugere a aplicação. Exemplo: valor temporalmente adequado e características técnicas equivalentes ou próximas (tipo de telha, cor, espessura, dimensão, unidade, etc.), sempre distinguindo fato encontrado de recomendação do ELO.

## Estados da memória de cálculo

Cada memória deve ser apresentada com seu estado:

- `PERSISTIDA`;
- `RECUPERADA`;
- `AGREGADA`;
- `PENDENTE_VALIDACAO`;
- `PENDENTE_PERSISTENCIA`;
- `NAO_RECONSTRUIVEL`.

E com classificação:

- `CALCULATION_CONFIRMED`;
- `CALCULATION_PARTIAL`;
- `CALCULATION_REFERENCE`;
- `CALCULATION_NOT_RECONSTRUCTABLE`;
- `NO_CALCULATION_FOUND`.

Nunca inventar cálculo para preencher lacunas.

## Consulta posterior

Quando o usuário disser, por exemplo, `ELO — informações SO 155.26`, `ELO — o que sabemos sobre SO X` ou pedir dados de orçamento, executar consulta conjunta:

1. localizar fontes/documentos da SO;
2. reconstruir SO/PTS Técnica/Orçamento/PTS Pós;
3. consultar conhecimento cognitivo no Git;
4. consultar memória de cálculo no Supabase;
5. correlacionar decisões e cálculos;
6. retornar a experiência completa em formato estruturado.

A resposta não deve apresentar somente a memória de cálculo nem somente o aprendizado textual.

## Laboratório Virtual

Esta regra não altera o acionamento do Laboratório.

O Laboratório Virtual é subfluxo separado e somente executa quando explicitamente chamado.

`ELO APRENDER` → aprende e persiste.

`LABORATÓRIO` → testa quando chamado.

## Regra de integridade

Se uma fonte ou camada não estiver acessível, registrar explicitamente a ausência. Não simular leitura, não criar dados e não afirmar persistência inexistente.

O objetivo do retorno é permitir que o usuário compreenda **quem é a SO, como a solução foi tratada, como o orçamento foi resolvido e qual raciocínio quantitativo produziu seus números**, mantendo Git e Supabase como destinos distintos.
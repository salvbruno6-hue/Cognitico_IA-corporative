# PTS Pós-Orçamento — Estrutura Canônica Evolutiva do ELO

**Versão estrutural:** 3.0  
**Status:** Implementada e evolutiva  
**Owner:** ELO / PTS  
**Fonte de estrutura:** este documento + schema + template canônicos desta pasta

## 1. Finalidade

A PTS Pós-Orçamento comprova a aderência entre a Solicitação/Termo de Referência, os demais documentos da solicitação e a composição orçamentária efetivamente desenvolvida.

Ela deve permitir reconstruir o raciocínio técnico e econômico:

**REQUISITO → INTERPRETAÇÃO → SOLUÇÃO → QUANTITATIVO → COMPOSIÇÃO → ORÇAMENTO → PREMISSA → JUSTIFICATIVA → RISCO/PENDÊNCIA → VALIDAÇÃO**

A PTS é simultaneamente:

- documento de comprovação técnica;
- instrumento de rastreabilidade orçamentária;
- registro das memórias de cálculo;
- conferência quantitativa e financeira;
- auditoria reversa;
- mecanismo de identificação de divergências, riscos e pendências;
- base para análise de competitividade;
- fonte estruturada para aprendizado governado.

Não preencher lacunas por suposição silenciosa.

## 2. Estrutura canônica de saída

A PTS Pós-Orçamento utiliza **17 seções obrigatórias**, nesta ordem:

1. IDENTIFICAÇÃO E OBJETIVO
2. DOCUMENTOS UTILIZADOS
3. MATRIZ PRINCIPAL — TR × ORÇAMENTO
4. CONFERÊNCIA DE QUANTITATIVOS
5. CONFERÊNCIA DE VALORES
6. AUDITORIA REVERSA — PRINCIPAIS CUSTOS
7. ITENS ORÇADOS POR PREMISSA
8. LOGÍSTICA
9. MÃO DE OBRA
10. EXCLUSÕES E RESPONSABILIDADES
11. MATRIZ DE DIVERGÊNCIAS
12. MATRIZ DE RISCOS
13. PENDÊNCIAS
14. ITENS NÃO ORÇADOS / NÃO CONFIRMADOS
15. CHECKLIST DE COMPLETUDE
16. CONCLUSÃO E VALIDAÇÃO
17. REGRA DE RASTREABILIDADE

Esta estrutura é **canônica, mas não congelada**. Ela pode evoluir quando houver necessidade comprovada. Toda alteração estrutural deve ser feita no owner canônico desta pasta, com atualização coordenada de diretriz, schema, template, modelo de dados, testes e documentação.

Não é permitido criar uma segunda estrutura paralela de PTS para acomodar uma evolução.

## 3. Camada de dados da PTS

Cada SO possui seus próprios dados. O template não contém regras específicas de uma obra.

A variação deve ocorrer no JSON da SO, preservando o mesmo template estrutural.

As chaves principais são:

- `so`;
- `cliente`;
- `objeto`;
- `revisao`;
- `documentos`;
- `matriz_principal`;
- `blocos_quantitativos`;
- `conferencia_valores`;
- `auditoria_reversa`;
- `itens_premissa`;
- `logistica`;
- `mao_de_obra`;
- `exclusoes`;
- `divergencias`;
- `riscos`;
- `pendencias`;
- `itens_nao_orcados`;
- `checklist`;
- `conclusao`.

## 4. Matriz principal — TR × orçamento

A matriz principal deve preservar separadamente a origem do requisito e sua correspondência no orçamento.

| Nº | Tópico | Ref. TR | Requisito | Q. Prevista | Q. Orçada | Ref. Orçamento | Valor | Status | Divergência |
|---:|---|---|---|---:|---:|---|---:|---|---|

A matriz deve permitir identificar:

- requisito sem correspondente no orçamento;
- requisito parcialmente atendido;
- solução equivalente;
- quantidade diferente;
- item orçado sem requisito identificável;
- divergência entre requisito e composição.

## 5. Conferência de quantitativos

A conferência deve confrontar, quando aplicável:

**quantidade prevista → quantidade calculada → quantidade adotada → quantidade orçada**

Para cada diferença deve existir explicação ou registro de pendência.

Os blocos quantitativos podem registrar:

- área;
- perímetro;
- comprimento;
- quantidade de peças;
- número de módulos;
- produtividade;
- profissionais;
- dias;
- ciclos;
- perdas;
- consumo;
- logística;
- demais bases de dimensionamento.

## 6. Conferência de valores

A conferência deve demonstrar os principais componentes financeiros do orçamento.

| Componente | Valor |
|---|---:|
| Subtotal geral | |
| Taxa administrativa | |
| BDI | |
| Total geral | |

Quando houver inconsistência matemática entre os componentes, registrar a divergência em vez de corrigir silenciosamente o orçamento de origem.

## 7. Auditoria reversa — principais custos

A auditoria reversa parte dos maiores custos do orçamento e retorna à sua origem.

| Item | Referência | Valor | Base | Justificativa |
|---|---|---:|---|---|

A cadeia mínima é:

**VALOR → ITEM → COMPOSIÇÃO → FONTE → PREMISSA → MEMÓRIA → EVIDÊNCIA**

## 8. Itens orçados por premissa

Devem ser identificados os itens cuja formação depende de premissa, verba global, estimativa, condição comercial ou interpretação que não esteja integralmente demonstrada na TR.

| Item | Origem | Premissa | Impacto | Tratamento |
|---|---|---|---|---|

A premissa deve indicar claramente se foi:

- comprovada;
- adotada;
- estimada;
- pendente;
- condicionada à confirmação.

## 9. Logística

A logística deve ser apresentada separadamente da composição técnica quando houver impacto próprio.

| Componente | Cálculo | Valor | Critério |
|---|---|---:|---|

Podem ser registrados, conforme evidência:

- alimentação;
- deslocamento;
- hospedagem;
- veículo;
- transporte;
- frete;
- mobilização;
- desmobilização;
- visitas;
- demais custos logísticos.

## 10. Mão de obra

A mão de obra deve preservar a separação entre frentes quando aplicável.

| Frente | Função | Dias | Colaboradores | V. Unitário | Parcial |
|---|---|---:|---:|---:|---:|

Os totais devem ser apresentados por bloco quando os dados estiverem disponíveis.

## 11. Exclusões e responsabilidades

| Item | Responsável | Orçado | Status |
|---|---|---|---|

Devem ser explicitadas responsabilidades, exclusões e itens que dependem de terceiros ou confirmação.

Não presumir responsabilidade contratual sem evidência documental.

## 12. Matriz de divergências

| Nº | Item | Tipo | Previsto | Orçado | Motivo | Impacto | Ação |
|---:|---|---|---|---|---|---|---|

Tipos podem incluir:

- quantitativo;
- valor;
- composição;
- unidade;
- requisito;
- escopo;
- premissa;
- responsabilidade;
- fornecedor;
- versão;
- ausência;
- duplicidade.

## 13. Matriz de riscos

| Risco | Tipo | Impacto | Condição | Tratamento |
|---|---|---|---|---|

O risco deve estar vinculado a uma evidência, premissa ou lacuna identificável.

## 14. Pendências

| Pendência | Origem | Impacto | Ação | Status |
|---|---|---|---|---|

Pendência não deve ser ocultada para produzir aparência de completude.

## 15. Itens não orçados / não confirmados

Registrar itens identificados na análise que:

- não possuem correspondência no orçamento;
- possuem correspondência insuficiente;
- dependem de confirmação;
- estão contidos em verba global sem detalhamento suficiente;
- possuem origem ou composição ainda não comprovada.

## 16. Checklist de completude

O checklist mínimo possui 14 verificações:

1. Todos os requisitos principais possuem correspondência?
2. Itens relevantes possuem origem/justificativa?
3. Quantitativos confrontados?
4. Áreas molhadas reavaliadas?
5. Valores conferidos?
6. Maiores custos justificados?
7. Premissas registradas?
8. Exclusões registradas?
9. Pendências registradas?
10. Riscos registrados?
11. Responsabilidades verificadas?
12. Logística conferida?
13. Licenças/ART/RRT completamente confirmadas?
14. BDI/taxa/total conferidos?

O checklist não substitui a análise. Ele registra a cobertura da auditoria.

## 17. Conclusão e validação

A conclusão deve separar:

- atendimento técnico;
- atendimento orçamentário;
- divergências;
- riscos;
- pendências;
- limitações de evidência;
- validações ainda necessárias.

Não declarar atendimento integral quando houver pendência material, divergência não resolvida ou requisito sem evidência suficiente.

## 18. Regra de rastreabilidade

A PTS deve preservar a rastreabilidade:

**TR/SO → requisito → interpretação → solução → quantitativo → composição → orçamento → premissa → justificativa → risco/pêndencia → validação**

Toda informação utilizada deve possuir origem identificável.

### Fronteira documental

O fluxo é:

**ACERVO CONSULTIVO → ELO → SO ATUAL → ORÇAMENTO ATUAL → PTS**

O acervo histórico pode ser consultado pelo ELO para desenvolver o orçamento corrente, mas não é fonte direta da PTS.

Somente a aplicação efetivamente adotada na SO atual, com sua evidência e contexto, pode aparecer no documento corrente.

### Evolução da estrutura

A PTS **não deve ser congelada** após ser considerada correta.

Ela deve permanecer:

**CANÔNICA → VERSIONADA → TESTADA → EVOLUTIVA**

Quando uma necessidade real demonstrar que a estrutura precisa mudar:

1. identificar a necessidade;
2. comparar com a estrutura existente;
3. reutilizar antes de criar;
4. definir a alteração no owner canônico;
5. atualizar schema e template em conjunto;
6. atualizar o modelo JSON;
7. atualizar testes;
8. validar uma SO real;
9. registrar a mudança;
10. promover pela governança do ELO.

Assim, uma PTS correta hoje não impede uma PTS melhor amanhã e, ao mesmo tempo, nenhuma SO pode criar sua própria variante estrutural.

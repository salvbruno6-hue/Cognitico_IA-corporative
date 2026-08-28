# ELO APRENDER — Subfluxo VARRER CÁLCULOS

## Finalidade

`VARRER_CÁLCULOS` é um subfluxo especializado do gatilho `ELO APRENDER`. Sua única finalidade é localizar, extrair, reconstruir e registrar memórias de cálculo relevantes para os aprendizados de orçamento.

Ele NÃO substitui o fluxo cognitivo que estrutura conhecimento e instruções no Git.

## Acionamento

Sempre que `ELO APRENDER` processar uma Solicitação de Orçamento, o subfluxo deve ser acionado antes da consolidação da experiência.

## Escopo da varredura

Percorrer SO, PTS Técnica, Orçamento, PTS Pós-Orçamento e documentos/anexos disponíveis, procurando cálculos efetivamente usados, avaliados ou aprendidos.

Exemplos: excedentes; telhados/coberturas; esgoto subterrâneo; elétrica aérea; reforços estruturais; quantitativos derivados; áreas; comprimentos; volumes; pesos; dimensionamentos; conversões; rateios; composições; produtividade; equivalências técnicas com impacto econômico e demais memórias de cálculo encontradas.

## Tratamento

Para cada achado:

1. preservar SO/documento/item de origem;
2. determinar se é realmente cálculo;
3. extrair entradas e unidades;
4. identificar fonte;
5. identificar premissas;
6. reconstruir fórmula;
7. reconstruir subcálculos;
8. obter resultado e unidade;
9. registrar evidência/validação disponível;
10. verificar duplicidade por conceito e cálculo;
11. registrar somente a memória de cálculo no Supabase;
12. obter e preservar `calculation_id` real;
13. disponibilizar a referência ao fluxo cognitivo do aprendizado no Git.

## Separação de responsabilidades

Git: conhecimento, instruções, interpretação, conceitos, precedentes, regras e governança.

Supabase: somente memória estruturada de cálculos aprendidos/avaliados.

O subfluxo não promove conhecimento, não cria regra e não substitui a decisão do ELO.

## Integridade

Não inventar cálculo, fonte, premissa, fórmula, resultado ou identificador.

Se um cálculo for identificado e não puder ser registrado/confirmado, registrar `CALCULATION_NOT_REGISTERED` e impedir que a experiência seja considerada plenamente consolidada até a retomada.

Se o mesmo cálculo aparecer em múltiplos documentos da mesma SO, consolidar em um único registro e manter as evidências de ocorrência.

## Referência entre SOs

Cálculos originados em outras SOs são consultivos. Ao serem utilizados em uma nova SO, o ELO deve informar a fonte, as características comparadas, a equivalência, o motivo de aplicabilidade e a necessidade de validação. O cálculo nunca muda de origem.

## Completude

O fluxo de conhecimento no Git continua obrigatório. O `VARRER_CÁLCULOS` é paralelo/complementar e deve concluir sua etapa antes da consolidação final do aprendizado de orçamento.
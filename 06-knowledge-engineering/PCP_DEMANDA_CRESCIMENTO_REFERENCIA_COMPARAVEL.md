# Direção de trabalho — demanda de crescimento

## Objetivo

Construir a referência histórica comparável antes de calcular qualquer necessidade de mão de obra por função.

A ordem correta da implantação é:

**Demanda Comercial → referência histórica comparável → fator de crescimento/redução → carga projetada → composição operacional → produtividade → demanda por função → RH**

Nesta etapa, o trabalho termina na reconstrução e validação da referência comparável. Não devem ser produzidos números de eletricistas, montadores, ajudantes ou outras funções sem evidência histórica e composição prevista.

## 1. Separar as bases de demanda

Para setembro/2025 a fevereiro/2026, o PCP deve reconstruir as bases de demanda separadamente, preservando natureza da demanda, modelo/taxonomia, quantidade, período, evento/chave de comparabilidade e demais dimensões necessárias para reproduzir a mesma estrutura da previsão futura.

Exemplo estrutural:

| Natureza | Produto | Quantidade | Referência |
|---|---|---:|---|
| Sazonalidade | Módulos | 375 | set/2025–fev/2026 |
| Sazonalidade/Eventos | Contêineres | 75 | set/2025–fev/2026 |
| SPOT | Produtos | 150 | set/2025–fev/2026 |
| Grande porte | Módulos | ~400 | operação específica |

Os valores acima são exemplos de estrutura, não dados operacionais validados.

Essas linhas não devem ser somadas automaticamente. Primeiro é necessário determinar quais representam a mesma dimensão de demanda e quais são dimensões distintas.

## 2. Construir a referência comparável

A primeira pergunta do PCP é:

> **O que exatamente queremos prever para setembro/2026 a fevereiro/2027?**

A previsão futura deve definir a estrutura da comparação. Se o Comercial informar AF/CA de determinado tipo, quantidade de módulos, quantidade de contêineres, eventos, sazonalidade e demanda SPOT, o histórico de setembro/2025 a fevereiro/2026 deve ser reconstruído com a mesma estrutura de classificação.

### Exemplo

**Histórico — set/2025 → fev/2026**

| Natureza | Produto | Quantidade |
|---|---|---:|
| Eventos | Módulos | 120 |
| Eventos | Contêineres | 30 |
| Sazonalidade | Módulos | 255 |
| Sazonalidade | Contêineres | 45 |
| SPOT | Produtos | 150 |

**Previsão — set/2026 → fev/2027**

| Natureza | Produto | Quantidade |
|---|---|---:|
| Eventos | Módulos | X |
| Eventos | Contêineres | X |
| Sazonalidade | Módulos | X |
| Sazonalidade | Contêineres | X |
| SPOT | Produtos | X |

A comparação passa a ocorrer entre dimensões equivalentes: evento × evento; sazonalidade × sazonalidade; SPOT × SPOT; produto/modelo equivalente × produto/modelo equivalente.

Quando não existir histórico válido para uma dimensão futura, isso deve ser identificado como GAP de comparabilidade, e não preenchido por inferência.

## 3. Modelo/Taxonomia é a referência do produto

O tipo de produto informado pelo Comercial corresponde ao Modelo/Taxonomia existente no domínio de produtos.

A reconstrução histórica deve preservar o modelo/taxonomia como dimensão de comparação quando essa granularidade fizer parte da previsão.

A lista-mãe não precisa entrar no cálculo de crescimento. A estrutura/chassi também não constitui requisito desta etapa.

## 4. O fator pode ser diferente por natureza

Depois que a referência comparável estiver corretamente reconstruída, o fator de crescimento/redução poderá ser calculado por dimensão comparável, e não necessariamente como um único percentual para toda a demanda.

Exemplo meramente hipotético:

| Natureza | Histórico | Previsão | Fator | Variação |
|---|---:|---:|---:|---:|
| Evento | 120 | 150 | 1,250 | +25,00% |
| Sazonalidade | 255 | 150 | 0,588 | -41,18% |
| SPOT | 150 | 200 | 1,333 | +33,33% |

**Fator = Demanda futura comparável / Demanda histórica comparável**

**Variação = (Fator - 1) × 100**

Esses valores são apenas ilustrativos.

Uma consequência importante é que o volume total pode cair enquanto determinada composição operacional cresce. Por isso, não se deve aplicar indiscriminadamente um único percentual às funções.

## 5. Não calcular ainda a necessidade por função

A etapa seguinte, depois do fator, será a composição operacional. Mas não é o próximo cálculo desta implantação.

Antes precisamos obter dados históricos reais que permitam responder:

> Para cada natureza e modelo/produto, quais funções participaram da execução e em que proporção?

| Produto/Modelo | Eletricista | Hidráulica | Montador | Ajudante | Serralheiro | Soldador |
|---|---:|---:|---:|---:|---:|---:|
| Módulo | ? | ? | ? | ? | ? | ? |
| Contêiner | ? | ? | ? | ? | ? | ? |

Os '?' representam dados ainda não determinados. Não devem ser convertidos em percentuais ou quantidades sem evidência.

## 6. Produtividade somente depois da composição

Somente depois de reconstruída a composição operacional será possível calcular produtividade histórica por função.

Exemplo estrutural: se, em determinado período comparável, foram realizados 200 módulos e participaram 10 montadores, a produtividade histórica preliminar seria 20 módulos por montador no período.

Esse número não deve ser imediatamente tratado como produtividade padrão. A validação deve considerar, quando disponível, produto/modelo, complexidade, período, horas trabalhadas, composição da equipe, natureza da demanda, volume realizado e escopo efetivamente executado.

## 7. Só então chega-se à demanda por função

**Histórico comparável → previsão futura equivalente → fator de crescimento/redução → carga projetada → composição operacional → produtividade validada → demanda projetada por função → RH**

Nesta etapa atual, o fluxo deve parar antes da demanda por função.

## 8. Informação final para RH

Quando todas as etapas estiverem comprovadas, o PCP deverá entregar ao RH uma visão rastreável por função:

| Função | Demanda projetada PCP | RH possui/contratou | Diferença | Qualificação |
|---|---:|---:|---:|---|
| Eletricista | X | Y | Z | Eletricista |
| Bombeiro hidráulico | X | Y | Z | Bombeiro hidráulico |
| Montador | X | Y | Z | Montador |
| Ajudante | X | Y | Z | Ajudante |
| Serralheiro | X | Y | Z | Serralheiro |
| Soldador | X | Y | Z | Soldador |

O resultado não será simplesmente 'Precisamos de 30 pessoas'. Será uma demanda por função, período, qualificação e origem da carga.

## 9. Rastreabilidade

Cada número apresentado ao RH deverá ser rastreável até a demanda Comercial que o originou.

**AF/CA → Modelo/Taxonomia → Produto → Natureza da demanda → Histórico equivalente → Fator → Carga projetada → Composição operacional → Produtividade → Demanda por função → RH → Contratos + qualificação → Demanda × fornecimento**

A rastreabilidade é requisito da cadeia e não uma informação opcional.

## 10. Regra de governança

O sistema deve distinguir dado histórico, previsão Comercial, referência comparável, fator calculado, carga projetada, composição operacional, produtividade, demanda humana e informação de RH.

Um dado ausente gera GAP. Não deve gerar estimativa inventada, percentual presumido, produtividade hipotética tratada como fato ou quantidade de pessoas por função sem evidência.

## 11. Escopo desta etapa

### Fazer agora

1. Identificar exatamente a estrutura da previsão Comercial para setembro/2026–fevereiro/2027.
2. Reconstituir setembro/2025–fevereiro/2026 com a mesma estrutura.
3. Separar evento, sazonalidade, SPOT e demais naturezas quando aplicáveis.
4. Preservar Modelo/Taxonomia como dimensão de produto.
5. Identificar dimensões realmente comparáveis.
6. Registrar GAPs de histórico/comparabilidade.
7. Validar a base histórica antes de calcular fatores.

### Não fazer agora

- calcular necessidade de eletricistas;
- calcular necessidade de montadores;
- calcular necessidade de ajudantes;
- calcular contratação;
- aplicar um único fator às funções;
- inferir composição a partir da lista-mãe;
- utilizar chassi como requisito;
- criar disponibilidade de RH;
- criar tabela de produtividade sem evidência.

## 12. Critério de avanço

A implantação só deve avançar para o cálculo de composição funcional quando houver uma resposta validada para:

> **Qual é exatamente a unidade de demanda que estamos prevendo para setembro/2026–fevereiro/2027 e qual é sua referência histórica equivalente em setembro/2025–fevereiro/2026?**

Somente depois dessa resposta o fator de crescimento passa a ter significado operacional.

---

**Direção de implantação atual:**

> **Primeiro construir a referência histórica comparável. Não calcular ainda a necessidade por função.**
## 13. Aplicação do fator à demanda humana histórica

A regra operacional foi refinada:

> **O fator é calculado sobre a quantidade de produtos comparáveis e, somente depois, aplicado à demanda humana histórica correspondente por função.**

Não aplicar o fator diretamente sobre o quadro atual de RH.

A cadeia passa a ser:

`Produto comparável histórico → produto comparável futuro → fator → demanda humana histórica por função → demanda humana projetada por função → RH`

Exemplo:

`450 produtos → 350 produtos → 350/450 = 0,7778`

Se a demanda humana histórica validada de montadores for 12, a projeção ilustrativa seria:

`12 × 0,7778 = 9,33`

Esse cálculo é ilustrativo até que os dados históricos reais por função estejam disponíveis.

## 14. Controle de composição

O fator global somente pode ser aplicado diretamente às funções quando a composição operacional for comparável.

Se o histórico tiver 375 módulos + 75 contêineres e a previsão tiver uma composição muito diferente, o fator global pode ocultar diferenças de carga por função.

Nesse caso, o PCP deve trabalhar no nível de produto/modelo e natureza:

`Carga futura por produto × composição funcional validada → demanda por função`

Não fazer rateio de mão de obra entre modelos quando uma ordem externa possuir múltiplos modelos sem uma regra operacional validada. Essa situação é registrada como GAP.

## 15. Views operacionais

As views governadas são:

- `v_elo_pcp_referencia_demanda_comparavel` — quantidade histórica, quantidade futura, fator e estado de comparabilidade;
- `v_elo_pcp_demanda_humana_historica_externa` — demanda humana histórica externa por modelo e função, usando somente ordens vinculadas a um único modelo;
- `v_elo_pcp_gap_composicao_humana_externa` — pedidos/ordens com múltiplos modelos que não podem receber rateio automático;
- `v_elo_pcp_demanda_humana_projetada_externa` — aplica o fator à demanda humana histórica da mesma combinação de modelo/natureza/chave e expõe o estado do cálculo.

A projeção não consulta o quadro de RH e não produz contratação.

## 16. Gatilho do loop ELO

Quando os dois horizontes possuírem dados em `mt_demanda_historico` e `mt_previsoes_demanda`, os triggers:

- `trg_elo_pcp_demanda_historico_crossing`;
- `trg_elo_pcp_previsoes_crossing`

acionam `elo_pcp_disparar_crossing_demanda()`.

O trigger não calcula silenciosamente. Ele cria uma execução `PENDING_INPUT` em `elo_automation_runs` para a automação `elo_pcp_demanda_crossing`.

A pergunta registrada para o ELO é:

> **Os dados históricos e a previsão foram inseridos. Posso cruzar os produtos comparáveis, calcular os fatores de crescimento/redução e aplicar esses fatores à demanda humana histórica por função?**

O ELO deve solicitar essa confirmação antes do cruzamento. A confirmação não autoriza contratação automática; ela apenas libera a etapa analítica de cruzamento.

## 17. Loop de execução

`Dados inseridos → trigger → PENDING_INPUT → ELO lê o estado → ELO pergunta → confirmação → cruzamento → fator → aplicação à demanda humana histórica → resultado por função → RH`

Se houver GAP de comparabilidade, modelo sem histórico, previsão sem histórico ou composição não rastreável, o loop deve parar naquele ponto e solicitar o dado faltante.


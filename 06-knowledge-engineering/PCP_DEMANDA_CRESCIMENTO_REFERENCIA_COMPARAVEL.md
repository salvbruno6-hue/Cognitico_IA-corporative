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
## 13. Capacidade posterior já especificada — não liberada no gate atual

As seções 13 em diante descrevem a capacidade que será executada depois que os gates anteriores forem satisfeitos. Elas não antecipam a execução atual. A implantação de views, triggers ou ferramentas pode existir previamente, mas o estado operacional continua bloqueado enquanto o gate histórico/comparabilidade não estiver validado.

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



## 18. Reconciliação Git × Supabase e gates técnicos

A implantação deste processo possui duas autoridades complementares:

- **GitHub** é a autoridade canônica do código, das migrações e da documentação versionada.
- **Supabase** é a autoridade do estado operacional do banco, das views, funções, triggers e registros efetivamente existentes.

A presença de um objeto no schema do Supabase não prova, sozinha, que o arquivo de migração correspondente esteja reconciliado no histórico versionado. Da mesma forma, a presença de um arquivo no GitHub não prova que sua alteração tenha sido aplicada ao banco.

### 18.1 Regra para divergência

Quando GitHub e Supabase apresentarem estados diferentes:

1. registrar o GAP;
2. identificar se a divergência é de **schema**, **histórico de migração**, **código** ou **documentação**;
3. comparar o estado efetivo antes de qualquer nova aplicação;
4. reconciliar por uma alteração versionada e rastreável;
5. validar novamente o schema e o histórico;
6. não inserir manualmente registros em `supabase_migrations.schema_migrations`;
7. não reaplicar cegamente uma migração apenas para fazer o histórico parecer alinhado.

### 18.2 Reconciliação das migrações deste processo

As quatro alterações PCP já estão presentes no banco sob as versões efetivamente registradas no histórico de migrações:

| Versão aplicada | Alteração canônica |
|---|---|
| 20261003033848 | criação de `v_elo_pcp_referencia_demanda_comparavel` |
| 20261003033912 | refinamento dos horizontes da referência comparável |
| 20261003033929 | documentação dos campos de comparabilidade |
| 20261003041027 | fator → demanda humana → loop ELO |
| 20261003121245 | cockpit decisório e gatilhos do PCP externo |
| 20261003121322 | correção do resumo decisório para observabilidade sem dados |

O repositório deve usar essas mesmas versões como prefixo dos arquivos de migração, preservando o conteúdo já aplicado. Essa é uma reconciliação de identificação/versionamento; não deve gerar uma segunda aplicação do mesmo DDL.

### 18.3 Gate técnico antes do cruzamento ponta a ponta

O processo só pode entrar no cruzamento analítico quando todos os gates abaixo estiverem satisfeitos:

`Git main atualizado` → `arquivos de migração versionados` → `histórico de migração reconciliado` → `schema Supabase validado` → `views/funções/triggers validados` → `ELO-MCP validado` → `histórico + previsão inseridos` → `PENDING_INPUT criado` → `confirmação do ELO` → `cruzamento comparável` → `fator` → `demanda humana histórica` → `demanda humana projetada` → `RH`

A implantação de código pode existir antes desses dados estarem disponíveis. Isso não significa que o processo esteja liberado para cálculo.

### 18.4 Estado bloqueado

Enquanto qualquer gate obrigatório estiver pendente, o estado operacional é:

**BLOQUEADO PARA EXECUÇÃO ANALÍTICA**

Nesse estado:

- não calcular fator;
- não projetar demanda humana;
- não consultar disponibilidade de RH como base de cálculo;
- não gerar contratação;
- não substituir dado ausente por inferência.

Quando o dado histórico e a previsão estiverem presentes, o trigger deve gerar `PENDING_INPUT`. O ELO deve fazer a pergunta registrada e aguardar a confirmação antes de executar o cruzamento.

### 18.5 Critério de fechamento técnico

Antes da execução ponta a ponta, validar conjuntamente:

1. GitHub `main` contém os arquivos canônicos;
2. os quatro prefixos de migração correspondem às quatro versões efetivamente aplicadas;
3. views, funções e triggers existem no schema esperado;
4. `elo_pcp_demanda_crossing` está habilitada e exige validação;
5. `elo_pcp_demanda_crossing_status` está disponível no ELO-MCP;
6. as fontes históricas e futuras ainda podem estar vazias — isso é GAP operacional, não erro técnico;
7. nenhum cálculo é executado antes da confirmação registrada pelo ELO.


## 19. Cockpit decisório e gatilho de leitura integrada do PCP externo

O processo passa a possuir uma camada de decisão integrada, sem criar uma nova autoridade de dados.

As views:

- `v_elo_pcp_decisao_externa_detalhe`
- `v_elo_pcp_decisao_externa_resumo`

consolidam, em uma mesma leitura, os seguintes elementos:

`demanda comercial → referência histórica → previsão → comparabilidade → fator → operação externa → demanda humana histórica → demanda humana projetada → gaps → informação faltante para decisão`

A camada é **analítica e descritiva**. Ela não transforma crescimento comercial em aumento automático de quadro de RH e não substitui validação operacional.

### 19.1 Fontes que funcionam como gatilho

A automação `elo_pcp_decisao_externa` registra uma nova leitura decisória quando houver inserção ou alteração em:

- `mt_pedidos_venda`;
- `mt_pedidos_venda_itens`;
- `mt_demanda_historico`;
- `mt_previsoes_demanda`;
- `mt_ordens_montagem_externa`;
- `mt_equipe_montagem_externa`.

A equipe externa representa a evidência operacional de demanda humana por função. O gatilho não interpreta `mt_pessoas` como capacidade disponível para contratação.

### 19.2 O que o resumo deve demonstrar

O resumo expõe:

- estado atual da análise;
- pedidos e unidades comerciais;
- quantidade histórica e prevista;
- quantidade de fatores calculados;
- fatores de crescimento e redução;
- ordens externas;
- horas planejadas de montagem externa;
- demanda humana histórica média;
- demanda humana projetada média;
- gaps de composição;
- informações que ainda precisam ser validadas.

### 19.3 Motivo analítico

Cada linha detalhada possui um `motivo_analitico`, por exemplo:

- `GAP_COMPOSICAO_OPERACIONAL`;
- `SEM_HISTORICO_HUMANO`;
- `DADO_COMERCIAL_NAO_COMPARAVEL`;
- `HISTORICO_ZERO_SEM_FATOR`;
- `AUMENTO_DEMANDA_COMPARAVEL`;
- `REDUCAO_DEMANDA_COMPARAVEL`;
- `DEMANDA_ESTAVEL`.

Esses motivos explicam o estado observado. Eles não são recomendações de contratação.

### 19.4 Informações que aumentam a precisão da decisão

A leitura deve solicitar ou destacar, quando ausentes:

1. chave de comparabilidade validada;
2. previsão por modelo e natureza;
3. histórico real por modelo e natureza;
4. início, fim e horas planejadas das ordens externas;
5. composição funcional validada;
6. histórico humano por função;
7. confiabilidade da previsão;
8. origem comercial rastreável.

Para uma decisão futura de dimensionamento de RH, ainda será necessário acrescentar produtividade validada por função e, somente depois, confrontar a demanda projetada com a capacidade efetivamente autorizada pelo processo de RH.

### 19.5 Regra de execução

`inserção/alteração de dado → trigger → PENDING_INPUT → ELO consolida o cockpit → validação → cruzamento comparável → fator → impacto na demanda humana → análise por função → etapa RH`

O cockpit pode existir e atualizar-se antes de haver dados suficientes para cálculo. Nesse caso, seu papel é demonstrar o estado, os impactos observáveis e os dados faltantes, mantendo o processo bloqueado onde a evidência ainda não é suficiente.

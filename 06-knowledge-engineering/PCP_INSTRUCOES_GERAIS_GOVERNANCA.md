# PCP — Instruções Gerais e Governança de Conhecimento

## 1. Finalidade

Este documento é a **instrução geral e autoridade documental do domínio PCP**.

Nenhuma instrução específica de PCP deve ser interpretada isoladamente. Documentos especializados existem para detalhar uma etapa, fonte, regra ou integração prevista neste documento mestre.

A relação documental é:

**Instrução Geral PCP → Diretriz/Processo → Instrução Especializada → Procedimento Operacional → Execução no ELO/Supabase**

Um documento especializado não pode criar uma regra que contradiga a instrução geral. Quando uma regra nova for necessária, primeiro deve ser incorporada à governança do PCP e somente depois detalhada em documento específico.

## 2. Princípio de autoridade

### GitHub
É a autoridade canônica de instruções, regras de negócio, conhecimento operacional versionado, migrações, views, funções, triggers, contratos de integração e histórico das alterações.

### Supabase
É a autoridade do estado operacional efetivamente armazenado: dados, schema, views implantadas, funções, triggers e registros de execução.

### ELO
É a camada de interpretação, validação e orquestração.

O ELO não cria autoridade paralela. Ele deve seguir as regras documentadas e os estados efetivamente disponíveis.

## 3. Hierarquia documental

### Nível 1 — Instrução Geral PCP
Define princípios, sequência geral, autoridades, gates, regras de evidência e governança.

Este arquivo é o nível 1.

### Nível 2 — Diretrizes e processos
Detalham grandes processos do PCP, como demanda, planejamento, cobertura, produção, capacidade, operação externa e integração com RH.

### Nível 3 — Instruções especializadas
Detalham uma regra específica sem criar nova autoridade.

Exemplos: vínculo entre reparo e unidade modular, integração ELO para reparos, comparabilidade da demanda e composição funcional.

### Nível 4 — Procedimentos operacionais
Descrevem como executar uma operação concreta, incluindo carga, validação, reconciliação e testes.

## 4. Regra de não isolamento

Todo documento especializado deve possuir:

1. referência explícita a este documento mestre;
2. finalidade dentro do processo PCP;
3. entradas necessárias;
4. regra que está detalhando;
5. dependências;
6. saída produzida;
7. GAPs possíveis;
8. gate de validação;
9. autoridade dos dados;
10. documento ou processo pai.

Se não possuir esses elementos, não deve ser tratado como instrução oficial do PCP.

## 5. Regra de evidência

**Dado ausente gera GAP. Nunca gera inferência.**

O PCP deve distinguir dado recebido, dado validado, cálculo, hipótese, GAP e decisão autorizada.

Uma fonte operacional não se torna autoridade apenas porque foi recebida.

## 6. Cadeia geral do PCP externo

**Demanda Comercial → Histórico Comparável → Previsão → Fator → Cobertura Física → Produção Programada → Necessidade Adicional de Fabricação → Carga Operacional → Capacidade/Gargalos → Composição Funcional → Produtividade → Demanda Humana → RH**

A cadeia pode parar em qualquer gate quando faltar evidência.

## 7. Demanda

A demanda deve preservar período, natureza, produto/modelo, taxonomia, quantidade, chave de comparabilidade, origem e confiabilidade.

O fator de crescimento/redução é calculado sobre dimensões comparáveis.

O fator não deve ser aplicado diretamente ao quadro de RH, ao estoque físico ou à quantidade de reparos.

## 8. Cobertura física

Antes de concluir que o crescimento da demanda exige fabricação adicional, o PCP deve verificar:

1. estoque disponível;
2. reparos recuperáveis;
3. produção já programada.

A regra analítica é:

**Necessidade adicional de fabricação = max(demanda prevista - estoque disponível - reparos recuperáveis - produção programada, 0)**

A cobertura física deve ser consolidada no nível de modelo para evitar dupla contagem entre diferentes naturezas de demanda.

## 9. Reparos

Reparos são uma fonte potencial de cobertura, não uma nova demanda.

Um reparo só pode ser considerado recuperável quando houver evidência suficiente de identidade da unidade, modelo válido, status compatível, data necessária ao horizonte, ausência de condição impeditiva e ausência de dupla contagem.

A documentação especializada deste processo é:

'06-knowledge-engineering/PCP_VINCULO_REPARO_UNIDADE_MODULAR.md'

A instrução de integração do ELO é:

'06-knowledge-engineering/PCP_ELO_INTEGRACAO_REPAROS.md'

Esses documentos são subordinados a esta instrução geral.

## 10. Integração com o Projeto Integrador

O PCP deve refletir os impactos da decisão no fluxo operacional.

O Projeto Integrador identifica a necessidade de gestão visual, controle de lead time, OEE, cronometragem dos processos, gestão de gargalos, integração entre setores, redução de reprogramações e maior confiabilidade dos dados.

Esses elementos são contexto para a reflexão operacional. Não substituem as regras de comparabilidade da demanda nem autorizam inferências.

O fluxo produtivo de referência documentado no Projeto Integrador é:

**Comercial → Engenharia → PCP → Compras → Almoxarifado → Estrutura Metálica → Pintura → Montagem → Componentes Complementares → Expedição**

## 11. ELO

O ELO deve:

1. ler o estado atual;
2. identificar a regra aplicável;
3. verificar evidências;
4. identificar GAPs;
5. solicitar validação quando o gate exigir;
6. executar somente operações autorizadas;
7. registrar o resultado;
8. preservar rastreabilidade.

O ELO não deve criar dados fictícios, escolher uma fonte concorrente, transformar GAP em estimativa, aplicar automaticamente crescimento ao RH, reconhecer reparo como cobertura sem vínculo validado ou criar regra especializada fora da hierarquia documental.

## 12. Git × Supabase

A existência de um objeto no Supabase não prova que ele esteja versionado corretamente no Git.

A existência de uma regra no Git não prova que ela esteja implantada no Supabase.

Quando houver divergência:

**registrar GAP → identificar natureza da divergência → comparar estados → reconciliar por alteração versionada → validar novamente**

Não editar manualmente o histórico de migrações para esconder divergências.

## 13. Gate documental

Uma instrução especializada somente pode ser considerada oficial quando:

- possui documento pai;
- está vinculada ao processo correspondente;
- não contradiz a instrução geral;
- possui entradas e saídas definidas;
- possui critérios de evidência;
- possui tratamento de GAP;
- possui gate de validação;
- está versionada no Git;
- sua implementação, quando houver, está alinhada ao Supabase.

## 14. Gate de execução

A existência da documentação não significa que o cálculo esteja liberado.

A execução deve seguir:

**Documento → regra → fonte → dado → validação → cálculo → resultado → validação → decisão**

Quando faltar qualquer evidência obrigatória, o processo fica bloqueado no respectivo gate.

## 15. Regra para criação de novas instruções

Antes de criar uma nova instrução PCP:

1. procurar instrução existente;
2. identificar o documento pai;
3. verificar se a regra já existe;
4. consolidar duplicidades;
5. decidir se é extensão ou nova instrução;
6. registrar dependências;
7. criar o documento especializado somente se necessário;
8. versionar no Git;
9. validar a relação com o ELO e Supabase.

**Não criar instruções isoladas.**

## 16. Mapa atual

### Documento mestre

'PCP_INSTRUCOES_GERAIS_GOVERNANCA.md'

### Processo de demanda

'PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md'

### Especialização de reparos

'PCP_VINCULO_REPARO_UNIDADE_MODULAR.md'

### Integração ELO de reparos

'PCP_ELO_INTEGRACAO_REPAROS.md'

O processo de demanda e os documentos de reparo devem ser lidos como partes de uma mesma cadeia, subordinados a esta instrução geral.

## 17. Regra de atualização

Alterações em uma instrução especializada que alterem princípio, autoridade, sequência ou gate do PCP devem primeiro atualizar esta instrução geral.

Alterações que apenas detalhem uma execução podem permanecer no documento especializado, desde que não contradigam o nível superior.

## 18. Estado de governança

O objetivo é impedir que o conhecimento do PCP se transforme em um conjunto de arquivos independentes.

A unidade de conhecimento é:

**Governança PCP → Processo → Instrução → Procedimento → Evidência → ELO → Supabase → Resultado**

Essa estrutura deve ser preservada em todas as próximas implantações.

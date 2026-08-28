# ELO APRENDER — Roteamento Canônico de Aprendizados de Orçamento

## Autoridade operacional

O comportamento completo do gatilho é definido por `ELO_APRENDER_CANONICO_MASTER_PROMPT.md`.

Este arquivo controla o roteamento físico; o Prompt Mestre controla busca, varredura, separação, persistência, governança e retorno.

## Regra obrigatória

Quando `ELO APRENDER` processar uma Solicitação de Orçamento (SO) do domínio do Especialista de Orçamento, o artefato cognitivo deve ser criado ou consolidado exclusivamente em:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/`

## Separação Git × Supabase

- **Git:** conhecimento cognitivo/instrucional, conceitos, decisões, critérios, precedentes, regras, diretrizes e governança.
- **Supabase:** somente memória quantitativa estruturada de cálculos e suas evidências.

A mesma execução de `ELO APRENDER` deve produzir as duas camadas quando houver conteúdo aplicável.

## Busca cognitiva obrigatória

Antes de criar ou alterar aprendizado, o gatilho deve identificar a SO/documentos, localizar o artefato canônico, pesquisar fontes legadas como proveniência, consultar conceitos existentes e seus estados, consultar memória de cálculo existente, agrupar semanticamente e deduplicar, e agregar nova evidência quando o conceito já existir.

A **Análise de Solicitações é a fonte primária de investigação**. Conhecimento previamente persistido, incluindo `memory/evolution`, serve como histórico, evidência ou apoio auxiliar e não substitui a consulta à fonte original. Uma SO já aprendida pode e deve ser reinvestigada para identificar informação material ainda não absorvida.

## Varredura de cálculos obrigatória

Para toda SO de orçamento, executar `VARRER_CÁLCULOS` antes da consolidação final. Percorrer SO, TR, PTS Técnica, Orçamento, PTS Pós-Orçamento, planilhas, composições e anexos disponíveis.

Investigar cálculos explícitos e implícitos de quantitativos, excedentes, cobertura/telhado, estrutura, hidráulica/esgoto, elétrica, climatização, manutenção, mão de obra, produtividade, logística, acoplamento, ART/RRT, áreas, equipamentos, composição de preços, equivalências e percentuais.

Não guardar apenas o número: reconstruir `entrada → fonte → premissa → fórmula → subcálculo → resultado → validação → origem`.

## Conhecimento cognitivo reutilizável de orçamento

Quando uma experiência de orçamento revelar uma metodologia generalizável, o ELO deve classificá-la como **CONHECIMENTO COGNITIVO** no Git, sem confundi-la com uma memória de cálculo específica no Supabase.

Metodologias reutilizáveis reconhecidas pelo ELO:

1. **Regra de três composta:** redimensionar precedentes considerando simultaneamente quantidade, período, frequência, produtividade, equipe e logística.
2. **Custo fixo × variável:** separar custos que não variam com o quantitativo daqueles proporcionais ao serviço.
3. **Produtividade inversa:** converter produtividade em necessidade de dias/equipe.
4. **Frequência × período:** dimensionar ciclos e atendimentos recorrentes conforme periodicidade e duração contratual.
5. **Quantidade × consumo unitário:** dimensionar materiais e componentes por unidade de referência.
6. **Equipe × produtividade:** verificar se a composição da equipe é compatível com a produtividade necessária.
7. **Atendimento médio:** estimar demanda de serviços corretivos usando histórico/precedentes quando não houver quantitativo explícito.
8. **Padrão × excedente:** preservar a composição padrão e dimensionar separadamente acréscimos e adaptações.
9. **Precedente × equivalência:** reutilizar uma referência somente após validar contexto, composição, unidade, material e condições de execução.
10. **Piso operacional:** impedir que o resultado matemático gere uma quantidade operacionalmente inviável.
11. **Arredondamento técnico:** converter frações em quantidades executáveis conforme a natureza do serviço.
12. **Cenários:** comparar cenários mínimo, provável e conservador quando houver incerteza relevante.
13. **Sensibilidade:** identificar as variáveis que mais impactam o valor final.
14. **Custo por unidade equivalente:** comparar SOs de escalas diferentes por módulo, equipamento, metro, mês ou outra unidade adequada.
15. **Rateio por unidade:** distribuir custos consolidados entre unidades quando tecnicamente justificável.
16. **Conversão de periodicidade:** transformar frequências semanais, mensais, trimestrais ou outras em ciclos de execução.
17. **Validação cruzada:** confrontar o resultado com precedente, produtividade, TR, histórico e demais evidências disponíveis.
18. **Detecção de anomalia:** sinalizar resultados muito acima ou abaixo de precedentes equivalentes.
19. **Contingência condicionada:** considerar margem adicional somente quando houver justificativa técnica/comercial identificável.
20. **Regra de não proporcionalidade:** impedir a aplicação automática de proporcionalidade a custos que possuem comportamento fixo ou mínimo operacional.

### Regra específica para regra de três composta

A regra de três composta é um **método de dimensionamento por precedente**, não uma regra cega. O ELO deve:

`identificar precedente → identificar variáveis dimensionadoras → comparar equivalência → redimensionar → arredondar quando necessário → validar contra TR/SLA/histórico → aplicar.`

O resultado matemático não substitui a premissa operacional. Quando houver conflito entre proporcionalidade e exigência contratual, SLA, histórico ou mínimo operacional, o ELO deve registrar a divergência e justificar a escolha.

## Proibição de destinos paralelos

O gatilho não deve criar novos aprendizados de orçamento em `memory/solicitations/<SO>/LEARNING.md`, `memory/solicitations_learning/`, `04-knowledge-handbook/` ou qualquer outro diretório paralelo.

Arquivos históricos nesses locais são fontes legadas para migração/consolidação, preservando proveniência.

## Governança e integridade

Se o conceito já estiver `VALIDATED_LEARNING`, reutilizar sem duplicar e agregar somente ocorrência/evidência. Nunca promover `PRECEDENT` a `RULE` automaticamente.

O ID de cálculo é gerado/controlado pelo Supabase. O modelo não fabrica IDs.

Se a persistência aplicável falhar, a experiência permanece pendente e não pode ser marcada como consolidada.

## Laboratório

O Laboratório Virtual é separado e somente é executado quando chamado explicitamente pelo usuário.

## Critério de conclusão

A experiência só pode ser considerada consolidada quando o commit Git aplicável e, havendo cálculos, a persistência/confirmação no Supabase estiverem confirmadas.

## Compatibilidade — fluxo macro do ELO APRENDER

Esta seção é aditiva e não substitui nem altera o Prompt Mestre. O gatilho deve interpretar o fluxo da seguinte forma:

```text
ELO APRENDER
     │
     ▼
ANÁLISE DE SOLICITAÇÕES
     │
     ├── SO
     ├── TR
     ├── PTS Técnica
     ├── Orçamento
     ├── PTS Pós
     └── demais documentos/evidências
     │
     ▼
ELO COGNITIVO
     │
     ├── identifica decisões
     ├── identifica soluções
     ├── identifica experiências
     ├── identifica critérios
     ├── identifica precedentes
     └── VARRER CÁLCULOS
     │
     ├──────────────────┐
     ▼                  ▼
    GIT              SUPABASE
     │                  │
     ▼                  ▼
CONHECIMENTO         MEMÓRIA
COGNITIVO            DE CÁLCULO
     │                  │
     ▼                  ▼
08-ai/ELO/           tabelas de
ESPECIALISTAS/       cálculos
ORCAMENTO/
APRENDIZADOS/
```

### Regra de compatibilidade

A inclusão deste fluxo não cria novo gatilho, não altera o comando `ELO APRENDER`, não altera o Laboratório, não cria destino paralelo e não modifica o modelo de persistência.

Ele apenas explicita a sequência operacional já estabelecida:

`ELO APRENDER → ANÁLISE DE SOLICITAÇÕES → ELO COGNITIVO → VARRER CÁLCULOS → GIT + SUPABASE → CONFIRMAÇÃO`.

### Regra de separação das camadas

`GIT = conhecimento cognitivo/instrucional.`

`SUPABASE = memória quantitativa estruturada, cálculos e evidências.`

Quando não houver cálculo aplicável, não criar registro artificial no Supabase. Quando houver cálculo aplicável, executar a persistência prevista no fluxo existente.

### Regra de não regressão

O fluxo existente de `ELO APRENDER` permanece a autoridade de execução. Esta seção não deve ser interpretada como novo fluxo concorrente, novo gatilho ou nova origem de dados.

# ELO — Conhecimento Maturado para Execução de Orçamento

**Status:** contrato cognitivo canônico  
**Owner:** ELO Cognitivo  
**Função:** transformar aprendizado validado em conhecimento consultivo reutilizável durante novos orçamentos.

## 1. Princípio

O ELO não deve acumular repetição. Deve aprender o entendimento que explica decisões.

A unidade de aprendizado é:

**CONDIÇÃO → FUNÇÃO → DECISÃO → MOTIVO → SOLUÇÃO → APLICABILIDADE → LIMITAÇÃO**

O resultado numérico, preço, quantidade ou cálculo detalhado permanece em sua estrutura própria.

## 2. Crítica obrigatória

Quando o ELO encontrar casos aparentemente iguais com soluções diferentes:

**OBSERVAR → COMPARAR → IDENTIFICAR DIFERENÇA → FORMULAR PERGUNTA → INVESTIGAR EVIDÊNCIAS → ENTENDER → CONSOLIDAR.**

A pergunta é interna ao ELO. Ela serve para descobrir evidências de escolhas que não ficaram explícitas.

Se a resposta não puder ser comprovada, a lacuna permanece pendente.

## 3. Tipos

### Experiência condicional

Exemplo:

**VÃO ≥ 6 m → reforço estrutural compatível com a dimensão do vão.**

**VÃO CURTO + estrutura já reforçada → tubo 50×30 mm como acabamento, não como reforço estrutural.**

O ELO deve guardar a condição e a função, não transformar o material em regra universal.

### Associação construtiva

Exemplo:

**PAINEL PIR ↔ GUIA U**

Função entendida: componente de fixação dos painéis e acabamento associado ao reforço estrutural.

Em uma nova composição de painel PIR, a ausência da guia U deve gerar **ALERTA DE VERIFICAÇÃO**, quando a configuração atual indicar sua necessidade.

O alerta não autoriza inclusão automática.

### Cálculo aprendido

Representa:

**ENTRADAS → PREMISSAS → MÉTODO → RESULTADO → APLICAÇÃO**

Exemplo: tabela de cargas → configuração do QDF → dimensionamento → quantidade de materiais.

A memória matemática detalhada permanece em **elo_orcamento_calculos_aprendidos**. Este documento registra somente o entendimento, a aplicabilidade e o apontamento para a memória real.

### Alerta

**GATILHO → O QUE VERIFICAR → NÃO APLICAR AUTOMATICAMENTE**

### Exceção

Condição comprovada em que uma associação ou regra usual não deve ser aplicada.

### Pergunta de aprendizado

Pergunta criada pelo ELO para fechar uma lacuna de entendimento. Não é obrigatoriamente uma pergunta enviada ao usuário.

## 4. Não duplicação

Não criar conhecimento maturado para repetir:

- cálculo já persistido;
- quantidade já registrada;
- preço já existente;
- composição já existente;
- texto de PTS sem decisão ou entendimento novo.

Criar ou atualizar conhecimento quando houver novo **motivo, condição, função, associação, exceção, alerta, método ou critério de aplicação**.

## 5. Relação com banco

O Markdown é a camada explicativa. As relações estruturadas reutilizam as estruturas existentes.

### Orçamento

- elo_orcamento_memoria
- elo_orcamento_calculos_aprendidos
- elo_orcamento_calculo_evidencias
- elo_orcamento_calculo_varreduras
- elo_orcamento_associacoes
- elo_orcamento_decisoes

### Aprendizado

- elo_aprendizado_experiencias
- elo_aprendizado_conceitos
- elo_aprendizado_padroes_raciocinio
- elo_aprendizado_relacoes
- elo_aprendizado_fontes

### Produto / material / serviço

Quando houver relação comprovada, apontar para a identidade existente de:

- Lista-Mãe: lista_mae_id, cod_produt, cod_item;
- serviço/composição/EXC;
- cálculo aprendido;
- experiência/conceito de origem.

Não criar identidade paralela no Markdown.

## 6. Estados de relação

Uma associação pode ser:

- RELACAO_CONFIRMADA
- RELACAO_PARCIAL
- REFERENCIA_CONSULTIVA
- SEM_RELACAO
- PENDENTE_VALIDACAO

Antes de aplicar:

**CONHECIMENTO → RELAÇÃO → EVIDÊNCIA → EQUIVALÊNCIA → VALIDAÇÃO DA SO ATUAL → APLICAÇÃO**

## 7. Maturidade

Usar:

**CANDIDATO → EM_ANALISE → VALIDADO → CONSOLIDADO**

E, quando necessário:

**CONDICIONAL | ALERTA | REVISAR | SUPERADO**

VALIDADO ou CONSOLIDADO não significa aplicação automática.

## 8. Proveniência

Preservar:

- SO de origem;
- documento;
- item/tópico;
- evidência;
- pergunta gerada;
- resposta;
- condição;
- critério de aplicação;
- limitação;
- status.

Referência histórica continua sendo consultiva e não se torna origem da SO atual.

## 9. Uso no orçamento

O conhecimento maturado é consultado depois da compreensão do requisito atual e antes do fechamento da composição:

**TR/SO → requisito → interpretação → conhecimento → validação → Lista-Mãe/EXC/cálculo → composição → orçamento**

Pode:

- sugerir associação;
- gerar alerta;
- indicar pergunta;
- indicar cálculo;
- recuperar experiência;
- apontar condição ou exceção.

Não pode:

- alterar automaticamente a TR;
- inserir automaticamente produto;
- inserir automaticamente serviço;
- substituir cálculo;
- substituir decisão;
- contaminar a PTS atual com histórico interno.

## 10. Relação com PTS

Não existe:

**ACERVO → PTS**

Existe:

**ACERVO → ELO → análise da SO atual → solução atual → PTS**

Quando um aprendizado histórico for efetivamente utilizado, a PTS registra apenas a premissa/decisão da SO atual, não o acervo histórico.

## 11. Consolidação

Só consolidar quando:

1. observação identificada;
2. pergunta crítica formulada quando necessária;
3. evidência investigada;
4. resposta sustentada;
5. condição definida;
6. limitação registrada;
7. relações estruturadas apontadas;
8. duplicação descartada;
9. governança definida.

## 12. Extensão para outros setores

A mesma lógica pode ser reutilizada em outros setores e camadas sem criar uma arquitetura paralela:

**OBSERVAR → CRITICAR → PERGUNTAR → INVESTIGAR → ENTENDER → RELACIONAR → VALIDAR → MATURAR → APLICAR**


## 13. Recuperação automática de aprendizados candidatos

Aprendizado originado de uma SO não precisa ter o mesmo número, nome ou cliente da SO atual para ser consultado.

O ELO ANALISAR deve recuperar automaticamente aprendizados candidatos quando houver correspondência relevante de conteúdo, estrutura, requisito, função, produto, processo, código técnico, configuração ou padrão de decisão.

A recuperação é consultiva e ocorre antes do fechamento da solução atual:

SO/TR atual → compreensão do requisito → recuperação de aprendizados candidatos relacionados → comparação de condições → validação da evidência atual → decisão da SO atual.

O aprendizado candidato deve aparecer como sugestão, alerta, precedente ou pergunta de verificação. Ele não deve ser aplicado automaticamente, nem transformar sua origem histórica em requisito da SO atual.

O número/nome da SO de origem permanece como proveniência e não como gatilho exclusivo de recuperação.

A promoção para conhecimento canônico continua dependente de evidência, validação e governança.

# TRABALHO ORIENTADO — FABRICAÇÃO CUSTOMIZADA

## Objetivo

Ensinar ao ELO como a fabricação customizada realmente funciona, antes de transformar conhecimento do especialista em regra operacional ou orientar a inserção de dados.

## Regra central

A fabricação customizada não é uma observação livre. Ela precisa ser rastreável desde o pedido/projeto até a execução.

`Pedido/AF → customização → roteiro personalizado → aprovação → operações → execução → inspeção`

## Etapa 1 — Identificar a origem

O especialista deve apresentar um caso real e responder:

- qual pedido/item;
- qual modelo base;
- qual característica tornou o módulo customizado;
- onde a necessidade foi registrada;
- quem solicitou;
- quem aprovou.

### Evidência esperada

Pedido/item, projeto, documento técnico, aprovação ou outra fonte operacional explicitamente reconhecida.

## Etapa 2 — Ensinar a diferença para o padrão

O especialista deve comparar:

| Aspecto | Padrão | Customizado |
|---|---|---|
| Modelo base | conforme cadastro | conforme cadastro |
| Roteiro | padrão | versão personalizada |
| Operações | roteiro padrão | operações mantidas/adicionadas/removidas/alteradas |
| Aprovação | regra padrão | aprovação da customização |
| Materiais | estrutura aplicável | estrutura com alterações justificadas |
| Capacidade | referência padrão | deve ser reavaliada quando a mudança exigir |
| Execução | eventos reais | eventos reais da configuração customizada |

A tabela é uma estrutura de comparação para investigação; os valores concretos devem ser ensinados pelo especialista.

## Etapa 3 — Ensinar o roteiro personalizado

Tabelas:

- `mt_versoes_roteiro_personalizado`
- `mt_operacoes_roteiro_personalizado`

O ELO deve descobrir:

- como nasce uma versão;
- quando uma versão é rascunho;
- quem aprova;
- como é identificada;
- como as operações são sequenciadas;
- como centro de trabalho é definido;
- como minutos padrão e setup são informados.

## Etapa 4 — Ensinar a passagem para a produção

O ELO deve confrontar:

`roteiro personalizado` → `OP` → `operações da OP`

Na estrutura atual, `mt_operacoes_ordem_producao.operacao_roteiro_id` referencia uma operação de roteiro. A forma específica de vincular uma operação personalizada à ordem deve ser confirmada no desenho físico do banco antes de ser tratada como relação canônica.

## Etapa 5 — Ensinar o realizado

O especialista deve apontar qual registro comprova:

- início;
- fim;
- quantidade concluída;
- parada;
- retrabalho;
- inspeção;
- aprovação/reprovação.

O ELO não deve considerar a existência do roteiro como prova de execução.

## Etapa 6 — Ensinar alterações durante a fabricação

Perguntar:

- o que acontece se o cliente alterar o projeto depois da aprovação;
- se uma nova versão do roteiro é criada;
- o que acontece com operações já iniciadas;
- como materiais já separados são tratados;
- quem autoriza a mudança;
- como o histórico é preservado.

## Saída da sessão

O ELO deverá produzir:

1. **Mapa do processo customizado**
2. **Tabela → campo → significado**
3. **Fonte → evidência**
4. **Responsável por cada dado**
5. **Regra validada**
6. **Campos ainda não localizados**
7. **Relações físicas confirmadas**
8. **Relações conceituais pendentes**
9. **Perguntas para a próxima sessão**

## Proibição

Não promover automaticamente o conhecimento da sessão para aprendizado permanente.

O conhecimento deve passar pelo fluxo de evidência, confronto, validação e governança já definido para o ELO/Symbiont.

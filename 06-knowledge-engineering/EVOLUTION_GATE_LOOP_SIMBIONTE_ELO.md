# Evolution Gate — Loop Simbionte ELO

**Status:** implementação inicial — candidata à validação  
**Issue:** #701  
**Escopo:** decisão governada de promoção de aprendizado

## Finalidade

O Evolution Gate transforma evidência de aprendizado em uma **decisão governada**. Ele não grava diretamente no Supabase, não altera a regra canônica e não substitui o Cognitive MERGE.

### Sequência

`EVIDÊNCIA → TESTE → REGRESSÃO → REPRODUTIBILIDADE → CONTRADIÇÃO/DUPLICIDADE → CONFIANÇA → APLICABILIDADE → DECISÃO`

## Decisões

| Decisão | Significado |
|---|---|
| `PROMOVER` | critérios atendidos; pode seguir para promoção governada |
| `RETER` | há evidência, mas teste/regressão/confiança ainda não sustentam promoção |
| `REJEITAR` | há contradição explícita com conhecimento existente |
| `SOLICITAR_MAIS_EVIDENCIA` | faltam evidência, reprodutibilidade ou delimitação de aplicabilidade |
| `REPLAN` | entrada inválida ou possível duplicidade exige reorganização/consolidação |

## Critérios

Valores iniciais:

- mínimo de **2 evidências independentes**;
- teste `PASS`;
- regressão aprovada;
- resultado reproduzível;
- confiança >= **0,70**;
- ausência de contradição;
- ausência de duplicidade não resolvida;
- aplicabilidade definida.

Os limites de evidência e confiança são configuráveis.

## Proveniência

A evidência estruturada preserva:

- identificador;
- fonte;
- tipo;
- proveniência;
- chave de independência opcional.

Strings legadas continuam aceitas para compatibilidade, mas não fornecem proveniência rica.

## Não promoção automática

`PROMOVER` significa apenas que os critérios do Gate foram atendidos.

Não significa que o conhecimento canônico foi alterado.

A sequência posterior permanece:

`GATE → COGNITIVE MERGE → GOVERNANÇA → COMMIT/ATUALIZAÇÃO AUTORIZADA`

## Persistência

`GateOutput.to_evolution_event()` produz um payload lógico para o papel de `elo_evolution_events`, sem executar INSERT.

O orquestrador autorizado deve persistir, quando aplicável:

- experiência de origem;
- padrão de origem;
- evidências;
- motivo;
- confiança;
- nível de origem/destino.

## Estado

A implementação é candidata à validação. A integração com o ciclo completo, persistência real e promoção efetiva continuam fora deste primeiro incremento.

# Cognitive Runtime Loop (CRL)

Orquestrador do ciclo cognitivo canônico do ELO.

## Princípio

O CRL não implementa estágios cognitivos. Ele despacha para os
loops governados já existentes em `src/elo/`.

O CRL governa **a progressão do ciclo cognitivo** (por exemplo, observar,
contextualizar, analisar, decidir, executar, monitorar e aprender). Ele não
substitui o `GovernedOrchestrator`.

O `GovernedOrchestrator` coordena **a composição entre autoridades canônicas**
necessárias a um estágio: capabilities, evidência, Forge, routing,
autorização recebida e ExecutionBoundary.

A apresentação ao usuário é uma terceira responsabilidade: a
`GovernedOrchestratorReadSurface` pode projetar uma visão sistêmica para
ADM/desenvolvedor ou uma visão operacional para interfaces corporativas, sem
assumir a autoridade do CRL, do Forge, do `elo-authz`, do DecisionLifecycle,
do learning ou do Evolution Gate.

Fluxo-alvo de integração:

`CognitiveCore -> CRL -> GovernedOrchestrator -> autoridades canônicas -> CRL/outcome -> read surface`

Esse fluxo expressa coordenação, não transferência de ownership.

## Uso

```python
from src.elo.cognitive.runtime.crl import (
    CognitiveRuntimeLoop,
    CRLContext,
    Stage,
)

crl = CognitiveRuntimeLoop()
crl.register(Stage.OBSERVE, observe_handler)
crl.register(Stage.ANALYZE, analyze_handler)

ctx = CRLContext(request_id="req-001")
ctx = crl.run(ctx)
```
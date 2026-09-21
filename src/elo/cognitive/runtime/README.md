# Cognitive Runtime Loop (CRL)

Orquestrador do ciclo cognitivo canônico do ELO.

## Princípio

O CRL não implementa estágios cognitivos. Ele despacha para os
loops governados já existentes em `src/elo/`.

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
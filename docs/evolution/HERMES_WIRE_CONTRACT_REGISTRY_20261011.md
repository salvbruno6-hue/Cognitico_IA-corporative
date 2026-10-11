# Hermes Wire Contract Registry → ELO — reconciliação 2026-10-11

## Descoberta
A superfície Hermes de refinamento de wire contracts continua relevante como evidência de compatibilidade de interface. A PR histórica #916 está 37 commits atrás da main e não deve ser integrada diretamente.

## Owner reutilizado
A introdução reutiliza exclusivamente `src/elo/interface/contracts.py` e os modelos `CognitiveRequest`, `CognitiveResponse` e `ErrorContract`. Não cria segundo router, API, transport, registry de autoridade, autorização, memória, learning ou Evolution Gate.

## Introdução candidata
`HERMES-WIRE-CONTRACT-REGISTRY` é um refinamento observacional: produz descritores determinísticos com versão, transporte HTTP/JSON, owner canônico e SHA-256 do schema Pydantic existente. `execution_permitted=false` é invariável.

## Exclusões explícitas
Não importa JSON-RPC/OpenRPC, não cria endpoint, não executa Hermes, não executa operação de negócio, não altera conhecimento canônico e não promove learning.

## Validação controlada
Os testes exigem os três contratos canônicos, nomes únicos, versão explícita, transporte existente, owner canônico, digest determinístico e hexadecimal e ausência de autoridade de execução/JSON-RPC.

## Gate
A introdução só pode ser considerada validada após CI e Evolution Gate do HEAD reconciliado. Aprovação técnica não constitui prova de produção nem autorização cognitiva para promover experiência ao Core.

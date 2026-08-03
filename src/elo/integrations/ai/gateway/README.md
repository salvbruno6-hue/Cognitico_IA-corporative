# AI Gateway

## Objetivo

Definir o ponto único de entrada para interações com provedores de inteligência artificial na EIP.

## Função

O AI Gateway recebe solicitações da camada cognitiva ou de serviços autorizados, aplica políticas, valida contexto, encaminha a chamada ao provider apropriado e devolve a resposta validada com provenance registrada.

## Responsabilidades

- receber solicitações padronizadas
- selecionar o provider adequado
- aplicar políticas de custo, autonomia, segurança e escopo
- normalizar requests e responses
- registrar provenance e auditoria
- encaminhar erros e limitações de forma controlada

## Princípios

- nenhum domínio chama provider diretamente
- gateway é o ponto de controle da interoperabilidade com IA
- provider é intercambiável sem alteração do núcleo
- toda chamada externa deve ser observável e governada
- respostas devem voltar em formato canônico para o ELO

## Estrutura prevista

```text
gateway/
├── README.md
├── request_normalizer.py
├── response_normalizer.py
├── router.py
├── policy_executor.py
└── error_handler.py
```

## Fluxo

```text
ELO / Cognitive Layer
      ↓
AI Gateway
      ↓
Policies + Security
      ↓
Provider Adapter
      ↓
External AI
      ↓
Validation + Provenance
      ↓
Canonical Response
```

## Regras

- gateway não deve armazenar segredos
- gateway não deve ser acoplado a um fornecedor único
- o formato canônico deve permanecer estável
- chamadas de alto risco podem exigir aprovação humana

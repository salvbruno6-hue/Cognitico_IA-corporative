# AI Validation

## Objetivo

Definir a camada responsável por validar a qualidade, consistência, segurança e aderência governada das respostas recebidas de provedores de IA.

## Função

A validação determina se a resposta pode ser consumida pela EIP, se precisa de refinamento ou se deve ser rejeitada.

## Critérios possíveis

- aderência ao pedido
- consistência com o contexto
- presença de evidências ou referências
- conformidade com políticas
- ausência de conteúdo sensível indevido
- compatibilidade com a finalidade solicitada
- qualidade mínima da resposta

## Saídas

- validada
- validada com ressalvas
- rejeitada
- redirecionada para outro provider
- enviada para revisão humana

## Princípios

- validação deve ser independente do provider
- validação deve respeitar governança e segurança
- validação não deve gerar conhecimento novo sem base
- validação deve ser explicável
- validação deve registrar motivo de aprovação ou rejeição

## Estrutura prevista

```text
validation/
├── README.md
├── rules.py
├── evaluator.py
├── scorer.py
└── result.py
```

## Regras

- toda resposta cognitiva relevante deve ser validada antes de entrar no fluxo principal
- respostas críticas podem exigir validação reforçada ou humana
- o resultado da validação deve ser preservado em provenance

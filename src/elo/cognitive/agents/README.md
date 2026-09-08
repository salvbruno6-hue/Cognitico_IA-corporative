# Agents

## Objetivo

Definir a camada de orquestração de agentes da EIP, permitindo que capacidades especializadas atuem sobre contexto, conhecimento, raciocínio e decisão sob políticas de governança.

## Função

O layer de agentes coordena agentes internos ou externos, cada um com escopo, finalidade, limites e responsabilidades explícitas.

## Responsabilidades

- orquestrar agentes especializados
- delegar tarefas por domínio ou finalidade
- consolidar resultados de múltiplos agentes
- manter rastreabilidade de origem e contribuições
- aplicar políticas de segurança, autorização e autonomia
- encaminhar exceções para aprovação humana quando necessário

## Tipos de agentes

- agente de consulta
- agente de análise
- agente de recuperação de conhecimento
- agente de recomendação
- agente de validação
- agente de execução governada
- agente de integração com IA externa

## Hermes como runtime externo

O Hermes pode atuar como **runtime de execução/orquestração externo do ELO Cognitive**, acionado por um contrato governado através da natureza Simbionte.

A regra é:

```text
ELO Cognitive → autorização/contexto/missão
        ↓
     Simbionte
        ↓
      Hermes
        ↓
 execução + evidência
        ↓
     Simbionte
        ↓
 Governed Learning / Evolution Gate
```

Hermes não é um novo Cognitive Core e não possui autoridade sobre Soul, Core, conhecimento canônico, routing canônico, autorização, tenant boundary ou Evolution Gate.

O contrato ELO-owned está em `hermes_contract.py` e a especificação arquitetural em `docs/architecture/ELO_HERMES_SYMBIONT_CONTRACT.md`.

## Princípios

- agentes não devem operar sem escopo e política definidos
- agentes devem registrar entradas, saídas e justificativas
- agentes externos devem ser tratados como não confiáveis até validação
- múltiplos agentes podem cooperar, mas a decisão final permanece rastreável
- agentes não substituem o domínio nem a governança
- Hermes executa; ELO governa
- resultados externos retornam como evidência, nunca como conhecimento canônico automático

## Relação com a EIP

A camada de agentes amplia a plataforma para interações sofisticadas e multi-IA, mas sempre dentro do núcleo de contexto, conhecimento, raciocínio, decisão e aprendizado.

## Evolução futura

A implementação pode incluir:

- roteamento por intenção e domínio
- coordenação multiagente
- políticas de autonomia por tarefa
- integração com workflows
- avaliação de qualidade e desempenho por agente
- bridge governada com Hermes
- retorno de evidências para a Simbionte

# ELO Application

Camada de aplicação do ELO.

## Responsabilidade

Orquestrar casos de uso, comandos, consultas, DTOs e handlers.

## Subcamadas

- commands
- queries
- handlers
- dto
- use_cases

## Regra

Esta camada coordena o domínio, mas não deve conter lógica de persistência ou dependências de infraestrutura direta.

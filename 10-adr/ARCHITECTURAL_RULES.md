# Architectural Rules

## Purpose

Definir as regras normativas da arquitetura do ELO.

## Rules

- separar conhecimento, domínio, aplicação e infraestrutura
- manter baixo acoplamento entre módulos
- priorizar documentação como fonte de verdade
- introduzir integrações externas apenas por adaptadores
- tratar IA como componente integrado, não como núcleo acoplado

## Enforcement

Qualquer nova implementação deve ser validada contra estas regras antes de ser incorporada ao core.

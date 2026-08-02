# ELO Core

## Objetivo

Definir o núcleo técnico da plataforma ELO, responsável por orquestrar configuração, segurança, eventos e fundamentos operacionais do sistema.

## Escopo

- kernel do sistema
- configuração central
- segurança base
- eventos fundamentais
- mecanismos essenciais de inicialização

## Relação com a EIP

O core é a base executável da EIP. Ele deve permanecer estável, enxuto e independente de domínios específicos, mantendo apenas os fundamentos compartilhados pela plataforma.

## Regras

- o core não deve conter regras de negócio específicas de domínio
- o core deve ser reutilizável por qualquer cenário industrial suportado pela EIP
- integrações com IAs externas devem ser tratadas por camadas de adaptação, nunca diretamente pelo core

# Mapa de Domínios do ELO

## Objetivo

Definir os domínios funcionais e cognitivos que organizam a arquitetura do ELO e estabelecer suas principais responsabilidades e relações.

## Princípio

O ELO é orientado a decisões e recursos estratégicos, não à estrutura departamental. Os domínios existem para responder perguntas de negócio e conectar conhecimento, planejamento e execução.

## Domínios

1. Inteligência de Demanda — previsão, cenários, riscos e recomendações de demanda.
2. Engenharia e Produtos — modelos, produtos, BOM, revisões, componentes e conhecimento de engenharia.
3. Planejamento Estratégico — cenários de médio e longo prazo, investimentos, capacidade e riscos.
4. Planejamento Operacional (PCP) — plano mestre, sequenciamento, carga, capacidade e execução planejada.
5. Suprimentos — necessidades de materiais, compras, fornecedores, cobertura e risco de ruptura.
6. Produção — ordens, recursos, instalações, tempos, produtividade, gargalos e execução industrial.
7. Logística — movimentação, disponibilidade, abastecimento e fluxo de materiais e produtos.
8. Operação Externa — execução fora da fábrica, equipes, equipamentos, veículos e capacidade operacional.
9. Manutenção — ocorrências, falhas, reincidências, componentes, fornecedores e retroalimentação da engenharia.
10. Inteligência Operacional — consolidação de sinais operacionais, riscos, desvios, alertas e recomendações.
11. Conhecimento — documentos, fatos, conceitos, evidências, contexto e memória organizacional.
12. Analytics — indicadores, métricas, análises históricas, diagnósticas, preditivas e prescritivas.
13. IA — agentes, RAG, modelos, inferência, recomendação e assistência cognitiva governada.
14. Governança — políticas, segurança, qualidade, auditoria, rastreabilidade e ciclo de vida.

## Fluxo macro

```text
Inteligência de Demanda
        ↓
Engenharia e Produtos
        ↓
Planejamento Estratégico
        ↓
PCP → Suprimentos → Produção → Logística → Operação Externa
        ↑                                  ↓
        └──── Manutenção / Inteligência Operacional ────┘

Conhecimento + Analytics + IA + Governança
atuam transversalmente sobre todos os domínios.
```

## Domínios transversais

Conhecimento, Analytics, IA e Governança são capacidades transversais. Eles não substituem os domínios operacionais e não devem concentrar regras que pertencem ao negócio.

## Regras de fronteira

- cada conceito deve possuir domínio responsável claramente definido
- integrações entre domínios devem usar contratos explícitos
- dados não devem ser duplicados sem justificativa arquitetural
- regras de negócio devem permanecer próximas ao domínio que possui a decisão
- IA deve consumir contexto governado e rastreável
- sistemas especialistas permanecem responsáveis por suas funções administrativas ou transacionais quando não fizer sentido internalizá-las no ELO

## Perguntas como mecanismo de validação

Um domínio é considerado arquiteturalmente útil quando permite responder perguntas relevantes de decisão. O catálogo de perguntas do ELO deve ser usado para validar dados, capacidades, modelos, integrações e conhecimento.

## Rastreabilidade

Este mapa deve permanecer alinhado a `03_Modelo_Conceitual.md`, `04_Entidades.md`, `05_Relacionamentos.md`, `06_Regras_Negocio.md`, `DOMAIN_ARCHITECTURE_FRAMEWORK.md` e `01_Inteligencia_de_Demanda.md`.

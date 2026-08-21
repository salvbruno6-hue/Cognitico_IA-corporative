# ELO — Roadmap de Implementação do Motor de Orçamento

## Fase 01 — Fundação

- [ ] catálogo SQL;
- [ ] Lista-Mãe versionada;
- [ ] famílias MLT;
- [ ] modelos MLT;
- [ ] dimensões;
- [ ] unidades;
- [ ] componentes.

**Gate:** dados canônicos sem duplicidade semântica.

## Fase 02 — Relações

- [ ] relações modelo-componente;
- [ ] relações componente-composição;
- [ ] relações elétricas;
- [ ] relações hidráulicas;
- [ ] relações de mão de obra;
- [ ] relações logísticas;
- [ ] relações normativas.

**Gate:** toda relação automática precisa possuir origem e justificativa.

## Fase 03 — Matching

- [ ] identificar intenção de orçamento;
- [ ] identificar família;
- [ ] identificar modelo candidato;
- [ ] comparar dimensões;
- [ ] comparar configuração;
- [ ] identificar excedentes;
- [ ] calcular confiança.

**Gate:** nenhuma classificação ambígua pode ser tratada como certeza.

## Fase 04 — Composição

- [ ] carregar itens-base;
- [ ] carregar preços da Lista-Mãe;
- [ ] adicionar excedentes;
- [ ] adicionar mão de obra;
- [ ] acionar composições;
- [ ] auditar relações;
- [ ] produzir memória de cálculo.

**Gate:** orçamento rastreável item a item.

## Fase 05 — Especialista

- [ ] gerar pergunta objetiva;
- [ ] enviar contexto consolidado;
- [ ] receber decisão;
- [ ] registrar decisão;
- [ ] atualizar orçamento;
- [ ] manter evidência.

**Gate:** especialista não recebe uma demanda sem contexto suficiente.

## Fase 06 — Aprendizagem

- [ ] registrar experiência;
- [ ] classificar recorrência;
- [ ] medir benefício;
- [ ] separar experiência temporal de regra canônica;
- [ ] submeter candidato ao Evolution Gate.

**Gate:** nenhuma experiência altera estrutura canônica sem governança.

## Fase 07 — Automação Git

O ciclo de desenvolvimento deve permitir:

```text
Issue
 ↓
classificação ELO
 ↓
auditoria automática
 ↓
implementação
 ↓
testes
 ↓
Evolution Gate
 ↓
PR
 ↓
validação
 ↓
aprovação
 ↓
merge
```

Issues paradas devem ser classificadas por estado:

- aguardando informação;
- aguardando especialista;
- pronta para implementação;
- pronta para validação;
- pronta para merge;
- bloqueada.

O ELO pode recomendar avanço, mas ações que alterem a arquitetura canônica devem continuar sujeitas aos gates e às autorizações estabelecidas.

## Critério de pronto

Uma solicitação de orçamento é considerada coberta quando o ELO consegue:

1. interpretar a solicitação;
2. encontrar modelo/família;
3. comparar dimensões;
4. reconhecer componentes padrão;
5. detectar excedentes;
6. identificar relações;
7. carregar preços canônicos;
8. adicionar mão de obra/composições aplicáveis;
9. explicar lacunas;
10. solicitar decisão do especialista quando necessário;
11. registrar a decisão;
12. produzir evidência para evolução futura.
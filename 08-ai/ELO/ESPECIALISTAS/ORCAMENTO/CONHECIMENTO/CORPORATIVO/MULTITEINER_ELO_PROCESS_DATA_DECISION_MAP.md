---
id: ELO-KNOW-MULTITEINER-002
name: Multiteiner Process Data Decision Map
type: canonical-reference
layer: knowledge-engineering
status: draft
---

# MULTITEINER — MAPA DE PROCESSO, DADOS E DECISÕES DO ELO

## Objetivo

Conectar o fluxo operacional ao planejamento PCP e à camada de inteligência do ELO.

## Matriz de integração

| Processo | Informação gerada | Consumidores | Decisão suportada |
|---|---|---|---|
| Comercial | demanda, AF, modalidade, prazo | PCP, Orçamento | priorização e enquadramento |
| Orçamento | customização, materiais, recorrência, custo | PCP, Engenharia | capacidade e necessidade |
| PCP | sequência, prioridade, janela | Produção, Almox., Compras, Expedição | plano operacional |
| Almoxarifado | estoque, reserva, ruptura, picking | PCP, Produção, Reparos | abastecer ou comprar |
| Compras | pedido, previsão de chegada | PCP, Almoxarifado | replanejar materiais |
| Produção | etapa, tempo, status, retrabalho | PCP, Qualidade | sequenciar e corrigir |
| Qualidade | aprovado/falha, não conformidade | PCP, Reparos | liberar ou reparar |
| Expedição | saída, conferência, destino | Comercial, PCP | disponibilidade/entrega |
| Locação | utilização, ocorrência, retorno | PCP, Reparos | recuperação |
| Quarentena | condição inicial | Reparos, PCP | impedir falsa disponibilidade |
| Avarias | tipo, severidade, componente | Reparos, Orçamento, PCP | priorizar intervenção |
| Reparos | oficina, tempo, equipe, material | PCP, RH, Almox. | capacidade e custo |
| Teste reparo | aprovado/falha | PCP, Qualidade | liberar ou retrabalhar |
| Estoque segurança | disponibilidade real | PCP, Comercial | atender nova demanda |

## Cadeia decisória ELO

```text
DADO
 ↓
EVENTO DE PROCESSO
 ↓
INDICADOR
 ↓
SINAL
 ↓
DIAGNÓSTICO
 ↓
RESTRIÇÃO / CAUSA
 ↓
ALTERNATIVAS
 ↓
PLANO TÁTICO
 ↓
EXECUÇÃO
 ↓
RESULTADO
 ↓
APRENDIZADO / HISTÓRICO
```

## Gates obrigatórios do fluxo

1. AF completa?
2. Padrão ou customizado?
3. Materiais disponíveis?
4. Planejamento liberado?
5. Etapa produtiva liberada?
6. Qualidade aprovou?
7. Excedente/packing/conferência concluídos?
8. Módulo entregue ou locado?
9. No retorno: módulo está em condição de disponibilidade?
10. Avaria exige reparo?
11. Material de reparo disponível?
12. Teste de reparo aprovado?
13. Módulo liberado para estoque de segurança?
14. Disponibilidade real atende demanda?

## Estados críticos

`PLANEJADO → EM EXECUÇÃO → BLOQUEADO → AGUARDANDO MATERIAL → EM QUALIDADE → REPARO → LIBERADO → EXPEDIDO → EM LOCAÇÃO → RETORNADO → QUARENTENA → RECUPERAÇÃO → ESTOQUE SEGURANÇA → DISPONÍVEL`

## Regra de análise

O ELO deve diferenciar:

- fato registrado;
- indicador calculado;
- sinal detectado;
- diagnóstico analítico;
- hipótese;
- plano tático;
- decisão estratégica.

Não utilizar percentuais de produtividade, disponibilidade ou desempenho sem base nos dados efetivamente registrados.